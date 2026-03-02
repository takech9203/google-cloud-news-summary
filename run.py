#!/usr/bin/env python3
"""
Google Cloud News Summary Automation Script

This script runs the google-cloud-news-summary skill using the Claude Agent SDK with Amazon Bedrock.
It's designed to be executed by GitHub Actions on a daily schedule.

Usage:
    python run.py                           # Run with default prompt
    python run.py "Custom prompt here"      # Run with custom prompt
    python run.py --prompt "Custom prompt"  # Run with custom prompt (explicit flag)

Environment Variables:
    DEBUG=1         Enable debug mode (verbose logging)
    VERBOSE=1       Enable verbose mode (timing and details)
    AWS_REGION      AWS region for Bedrock (default: us-east-1)
"""

import argparse
import asyncio
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import boto3
from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions, query

from claude_agent_sdk.types import (
    AssistantMessage,
    ResultMessage,
    SystemMessage,
    UserMessage,
    TextBlock,
    ToolUseBlock,
)

# Default number of days to look back
DEFAULT_DAYS = 3

# Default prompt template for the skill
DEFAULT_PROMPT_TEMPLATE = (
    "Report Google Cloud news from the past {days} days. "
    "Fetch the RSS feed, filter updates, check for duplicates, "
    "and delegate report creation to subagents."
)

# Model configuration with fallback
PRIMARY_MODEL = "global.anthropic.claude-opus-4-6-v1"
FALLBACK_MODEL = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"

# Common tools for orchestrator and subagents
COMMON_TOOLS = [
    "Skill",
    "Read",
    "Write",
    "Edit",
    "MultiEdit",
    "Glob",
    "Grep",
    "Bash",
    "WebFetch",
]

# MCP tools for Google Developer Knowledge
MCP_TOOLS = [
    "mcp__google-developer-knowledge__search_documents",
    "mcp__google-developer-knowledge__get_document",
    "mcp__google-developer-knowledge__batch_get_documents",
    "mcp__cloud-cost__get_pricing",
    "mcp__cloud-cost__compare_pricing",
    "mcp__cloud-cost__list_services",
]


class Logger:
    """Logger with debug and verbose modes."""

    def __init__(self) -> None:
        self.debug = os.environ.get("DEBUG", "").lower() in ("1", "true", "yes")
        self.verbose = os.environ.get("VERBOSE", "").lower() in ("1", "true", "yes") or self.debug
        self.start_time = time.time()
        self.last_timestamp = self.start_time

    def elapsed(self) -> str:
        """Return elapsed time since start."""
        return f"{time.time() - self.start_time:.1f}s"

    def delta(self) -> str:
        """Return time since last timestamp and update it."""
        now = time.time()
        delta = now - self.last_timestamp
        self.last_timestamp = now
        return f"+{delta:.1f}s"

    def log(self, message: str, *, level: str = "INFO", force: bool = False) -> None:
        """Log a message with timestamp."""
        if force or self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}", flush=True)

    def log_debug(self, message: str) -> None:
        """Log debug message (only in debug mode)."""
        if self.debug:
            self.log(message, level="DEBUG")

    def log_verbose(self, message: str) -> None:
        """Log verbose message (in verbose or debug mode)."""
        if self.verbose:
            self.log(message, level="VERBOSE")

    def log_error(self, message: str) -> None:
        """Log error message (always shown)."""
        self.log(message, level="ERROR", force=True)

    def log_warn(self, message: str) -> None:
        """Log warning message (always shown)."""
        self.log(message, level="WARN", force=True)


# Global logger instance
logger = Logger()


def print_separator(char: str = "=", length: int = 60) -> None:
    """Print a separator line."""
    print(char * length)


def get_latest_reports(output_dir: Path, limit: int = 5) -> list[str]:
    """
    Get list of latest report files.

    Args:
        output_dir: Directory containing the reports
        limit: Maximum number of reports to return

    Returns:
        List of report filenames
    """
    reports = []

    try:
        if not output_dir.exists():
            return reports

        # Get all year directories
        year_dirs = [
            d for d in output_dir.iterdir()
            if d.is_dir() and d.name.isdigit()
        ]
        year_dirs.sort(reverse=True)

        # Get all markdown files from year directories
        for year_dir in year_dirs:
            for md_file in year_dir.glob("*.md"):
                reports.append({
                    "name": md_file.name,
                    "path": md_file,
                    "mtime": md_file.stat().st_mtime,
                })

        # Sort by modification time (newest first)
        reports.sort(key=lambda x: x["mtime"], reverse=True)

        return [r["name"] for r in reports[:limit]]

    except Exception as e:
        print(f"Warning: Could not read report directory: {e}", file=sys.stderr)
        return []


def generate_reports_index(reports_dir: Path) -> bool:
    """
    Generate index files (index.md and README.md) for reports directory.

    Args:
        reports_dir: Path to the reports directory

    Returns:
        True if index was updated, False otherwise
    """
    if not reports_dir.exists():
        print(f"Reports directory not found: {reports_dir}", file=sys.stderr)
        return False

    # Collect all reports grouped by year
    reports_by_year: dict[str, list[dict]] = {}

    year_dirs = [
        d for d in reports_dir.iterdir()
        if d.is_dir() and d.name.isdigit() and len(d.name) == 4
    ]

    for year_dir in year_dirs:
        year = year_dir.name
        reports_by_year[year] = []

        for md_file in year_dir.glob("*.md"):
            # Extract title from first H1 heading
            title = md_file.stem  # fallback to filename
            try:
                with open(md_file, encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            break
            except Exception:
                pass

            # Extract date from filename (YYYY-MM-DD-*.md)
            date_match = md_file.name[:10] if len(md_file.name) >= 10 else ""

            reports_by_year[year].append({
                "filename": md_file.name,
                "title": title,
                "date": date_match,
                "path": f"{year}/{md_file.name}",
            })

        # Sort by date (newest first)
        reports_by_year[year].sort(key=lambda x: x["date"], reverse=True)

    # Generate index content
    lines = [
        "# Google Cloud ニュースレポート一覧",
        "",
        "このページは、Google Cloud の最新ニュースとアップデートに関するレポートの一覧です。",
        "",
    ]

    # Sort years (newest first)
    for year in sorted(reports_by_year.keys(), reverse=True):
        reports = reports_by_year[year]
        if not reports:
            continue

        lines.append("")
        lines.append(f"## {year} 年")
        lines.append("")

        for report in reports:
            lines.append(f"- [{report['date']} - {report['title']}]({report['path']})")

    content = "\n".join(lines) + "\n"

    # Write to both index.md and README.md
    updated = False
    for filename in ["index.md", "README.md"]:
        filepath = reports_dir / filename
        existing_content = ""
        if filepath.exists():
            try:
                with open(filepath, encoding="utf-8") as f:
                    existing_content = f.read()
            except Exception:
                pass

        if existing_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Updated: {filepath}")
            updated = True

    return updated


def generate_infographic_index(infographic_dir: Path) -> bool:
    """
    Generate index.html for infographic directory.

    Args:
        infographic_dir: Path to the infographic directory

    Returns:
        True if index was updated, False otherwise
    """
    import re

    if not infographic_dir.exists():
        print(f"Infographic directory not found: {infographic_dir}", file=sys.stderr)
        return False

    # Collect all HTML files (excluding index.html)
    html_files = []
    for html_file in infographic_dir.glob("*.html"):
        if html_file.name == "index.html":
            continue

        # Extract title from HTML
        title = html_file.stem
        try:
            with open(html_file, encoding="utf-8") as f:
                content = f.read()
                match = re.search(r"<title>([^<]+)</title>", content)
                if match:
                    title = match.group(1)
        except Exception:
            pass

        # Extract date from filename (YYYYMMDD-*.html)
        date_raw = ""
        date_match = re.match(r"^(\d{8})-", html_file.name)
        if date_match:
            date_raw = date_match.group(1)

        html_files.append({
            "filename": html_file.name,
            "title": title,
            "date_raw": date_raw,
            "date_formatted": f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:8]}" if date_raw else "",
        })

    # Sort by date (newest first)
    html_files.sort(key=lambda x: x["date_raw"], reverse=True)

    # Generate index.html
    cards_html = ""
    for i, item in enumerate(html_files):
        border_color = "#F25C05"
        if i % 3 == 1:
            border_color = "#F2C53D"
        elif i % 3 == 2:
            border_color = "#F24405"

        cards_html += f'''        <div class="card" style="border-left-color: {border_color};">
          <a href="{item['filename']}">
            <div class="card-date">{item['date_formatted']}</div>
            <div class="card-title">{item['title']}</div>
            <div class="card-file">{item['filename']}</div>
          </a>
        </div>
'''

    if not cards_html:
        cards_html = '''        <div class="empty-state" style="grid-column: 1 / -1;">
          <p>📝 まだインフォグラフィックがありません</p>
          <p>Google Cloud ニュースレポートからインフォグラフィックを生成すると、ここに表示されます。</p>
        </div>
'''

    index_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Google Cloud News Infographic Gallery</title>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Kurenaido&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: linear-gradient(135deg, #fef3c7, #fde68a);
      font-family: 'Zen Kurenaido', sans-serif;
      color: #593C47;
      min-height: 100vh;
      padding: 32px 24px;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    h1 {{ font-size: 32px; margin-bottom: 8px; color: #F25C05; }}
    .subtitle {{ color: #666; margin-bottom: 32px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }}
    @media (max-width: 900px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    .card {{
      background: rgba(255,255,255,0.9);
      border-radius: 12px;
      border-left: 4px solid #F25C05;
      transition: transform 0.2s;
    }}
    .card:hover {{ transform: translateY(-4px); }}
    .card a {{
      display: block;
      padding: 20px;
      text-decoration: none;
      color: inherit;
    }}
    .card-date {{
      font-size: 12px;
      color: #F25C05;
      margin-bottom: 4px;
    }}
    .card-title {{
      font-size: 15px;
      font-weight: 600;
      margin-bottom: 8px;
    }}
    .card-file {{
      font-size: 11px;
      color: #888;
      font-family: monospace;
    }}
    footer {{
      margin-top: 40px;
      text-align: center;
      font-size: 12px;
      color: #888;
      border-top: 2px dashed #F2C53D;
      padding-top: 20px;
    }}
    .empty-state {{
      text-align: center;
      padding: 60px 20px;
      color: #666;
    }}
    .empty-state p {{ margin-bottom: 16px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>📊 Google Cloud News Infographic Gallery</h1>
    <p class="subtitle">Google Cloud ニュースレポートのインフォグラフィック一覧</p>
    <div class="grid">
{cards_html}    </div>
    <footer>
      <p>Generated by Google Cloud News Summary | {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </footer>
  </div>
</body>
</html>
'''

    index_path = infographic_dir / "index.html"
    existing_content = ""
    if index_path.exists():
        try:
            with open(index_path, encoding="utf-8") as f:
                existing_content = f.read()
        except Exception:
            pass

    # Compare without timestamp line to avoid unnecessary updates
    def strip_timestamp(content: str) -> str:
        return re.sub(r"Generated by Google Cloud News Summary \| \d{4}-\d{2}-\d{2} \d{2}:\d{2}", "", content)

    if strip_timestamp(existing_content) != strip_timestamp(index_content):
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
        print(f"  Updated: {index_path}")
        return True

    return False


def is_throttling_error(error: Exception) -> bool:
    """Check if the error is a throttling error."""
    error_str = str(error).lower()
    return any(keyword in error_str for keyword in [
        "throttl",
        "rate limit",
        "too many requests",
        "429",
        "serviceunav",
    ])


async def run_skill(prompt: str | None = None, days: int = DEFAULT_DAYS) -> list[str]:
    """Run the google-cloud-news-summary skill using Claude Agent SDK with subagents.

    The orchestrator handles RSS feed fetching, parsing, filtering, and
    duplicate checking, then delegates individual report creation to
    'report-generator' subagents via the Task tool for parallel execution.

    Args:
        prompt: The prompt to send to the skill. If None, uses default based on days.
        days: Number of days to look back for updates. Defaults to DEFAULT_DAYS.

    Returns:
        List of newly created report file paths (relative to project_dir).
    """
    # Generate default prompt if not provided
    if prompt is None:
        prompt = DEFAULT_PROMPT_TEMPLATE.format(days=days)

    print_separator()
    print("Google Cloud News Summary Automation (Subagent Mode)")
    print_separator()
    current_time = datetime.now()
    print(f"Start time: {current_time.isoformat()}")
    print(f"Days to look back: {days}")
    print(f"Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    print()

    # Add current date context and orchestrator instructions
    prompt_with_context = f"""Current date and time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')} (JST)

You are the orchestrator for Google Cloud news report generation.

1. Invoke the Skill tool with skill='google-cloud-news-summary' to get the workflow
2. Follow steps 1-4 of the skill workflow (FETCH, PARSE with --days {days}, FILTER, CHECK DUPLICATES)
3. DELEGATE: For each update, use the 'report-generator' subagent via Task tool
   - Batch size: 10 subagents at a time
   - Wait for each batch to complete before starting the next
   - TaskOutput timeout: 600000 (10 minutes)
   - CRITICAL: When you receive TaskOutput, respond with ONLY a one-line confirmation per task. Do NOT repeat subagent output to avoid "Prompt is too long" errors.

User's request: {prompt}"""

    # Show logging mode
    if logger.debug:
        print("Logging mode: DEBUG (full details)")
    elif logger.verbose:
        print("Logging mode: VERBOSE (timing + details)")
    else:
        print("Logging mode: NORMAL (set DEBUG=1 or VERBOSE=1 for more details)")
    print()

    # Configuration for Bedrock
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    print("Configuration:")
    print(f"  AWS Region: {aws_region}")
    print(f"  Primary Model: {PRIMARY_MODEL}")
    print(f"  Fallback Model: {FALLBACK_MODEL}")
    print("  Using Bedrock: Yes")
    print()

    # Initialize paths
    project_dir = Path(__file__).parent
    output_dir = project_dir / "reports"

    print(f"  Project directory: {project_dir}")
    print(f"  Output directory: {output_dir}")
    print()

    # Check for .mcp.json
    mcp_json_path = project_dir / ".mcp.json"
    if mcp_json_path.exists():
        print(f"  MCP config: {mcp_json_path} (found)")
        if logger.verbose:
            import json
            with open(mcp_json_path) as f:
                mcp_config = json.load(f)
            servers = list(mcp_config.get("mcpServers", {}).keys())
            print(f"  MCP servers configured: {servers}")
    else:
        logger.log_warn(f"MCP config not found: {mcp_json_path}")
    print()

    try:
        # Verify AWS credentials
        print("Verifying AWS credentials...")
        sts_client = boto3.client("sts", region_name=aws_region)
        identity = sts_client.get_caller_identity()
        print(f"  AWS Account: {identity['Account']}")
        print(f"  AWS ARN: {identity['Arn']}")
        print()

        # Snapshot existing reports before running the skill
        existing_reports = set()
        for md_file in output_dir.rglob("*.md"):
            existing_reports.add(str(md_file.relative_to(project_dir)))

        # Try with primary model, fallback on throttling
        models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]

        bedrock_env = {
            "CLAUDE_CODE_USE_BEDROCK": "1",
            "AWS_REGION": aws_region,
        }

        # Define the report-generator subagent prompt
        report_subagent_prompt = (
            "You are a Google Cloud news report generator. "
            "When given an update item and output file path:\n"
            "1. Invoke the Skill tool with skill='google-cloud-news-summary'\n"
            "2. Follow the skill's workflow to create the report\n"
            "3. Save to the specified output path"
        )

        for model_index, current_model in enumerate(models_to_try):
            print(f"Executing with model: {current_model}")
            print()
            print("Progress:", end="", flush=True)

            # Capture CLI stderr for debugging exit code errors
            stderr_lines: list[str] = []

            def _on_stderr(line: str) -> None:
                stderr_lines.append(line)
                if logger.debug:
                    print(
                        f"  [CLI stderr] {line[:200]}",
                        flush=True,
                    )

            # Configure Claude Agent SDK options with report-generator subagent
            # The orchestrator handles RSS fetching, parsing, filtering,
            # and duplicate checking, then delegates report creation to subagents.
            options = ClaudeAgentOptions(
                model=current_model,
                fallback_model=(
                    FALLBACK_MODEL
                    if current_model == PRIMARY_MODEL
                    else None
                ),
                env=bedrock_env,
                cwd=str(project_dir),
                setting_sources=["project"],
                allowed_tools=COMMON_TOOLS + ["Task"] + MCP_TOOLS,
                agents={
                    "report-generator": AgentDefinition(
                        description="Generate a report from an update item.",
                        prompt=report_subagent_prompt,
                        tools=COMMON_TOOLS + MCP_TOOLS,
                    ),
                },
                stderr=_on_stderr,
            )

            # Execute the query using Claude Agent SDK
            result_text = ""
            report_count = 0
            created_reports: list[str] = []
            skipped_reports: list[str] = []
            msg_count = 0
            current_task = ""
            result_received = False  # Track if ResultMessage was received

            logger.log_verbose(f"Starting query execution at {logger.elapsed()}")
            last_message_time = time.time()
            heartbeat_interval = 10  # seconds
            pending_tools: dict[str, str] = {}  # tool_id -> tool_name
            pending_tool_start: dict[str, float] = {}  # tool_id -> start_time

            try:
                async for message in query(prompt=prompt_with_context, options=options):
                    msg_count += 1
                    current_time = time.time()

                    # Show heartbeat if no message for a while
                    if current_time - last_message_time > heartbeat_interval:
                        heartbeat_msg = f"\n  [Heartbeat] Still waiting... ({logger.elapsed()})"
                        if pending_tools:
                            pending_list = list(pending_tools.values())
                            heartbeat_msg += f"\n  [Pending tools: {', '.join(pending_list)}]"
                        print(heartbeat_msg, flush=True)
                    last_message_time = current_time

                    # Debug: print message structure
                    if logger.debug:
                        msg_type = type(message).__name__
                        print(
                            f"\n[DEBUG] [{logger.elapsed()}] msg #{msg_count}: {msg_type}",
                            end="",
                            flush=True
                        )
                        if hasattr(message, "__dict__"):
                            attrs = {k: type(v).__name__ for k, v in message.__dict__.items()}
                            print(f" attrs={attrs}", end="", flush=True)

                    if isinstance(message, AssistantMessage):
                        content = getattr(message, "content", [])
                        for block in content if isinstance(content, list) else []:
                            if isinstance(block, TextBlock):
                                result_text += block.text
                                # Check for skip/duplicate mentions in text
                                text_lower = block.text.lower()
                                if "skip" in text_lower or "duplicate" in text_lower or "already exists" in text_lower:
                                    if current_task and current_task not in skipped_reports:
                                        skipped_reports.append(current_task)
                                        print(f"\n  -- Skip (duplicate): {current_task}", flush=True)

                            elif isinstance(block, ToolUseBlock):
                                tool_name = block.name
                                tool_input = block.input if hasattr(block, "input") else {}
                                tool_id_full = getattr(block, "id", "") if hasattr(block, "id") else ""
                                tool_id = tool_id_full[:8]

                                # Track pending tools
                                if tool_id_full:
                                    pending_tools[tool_id_full] = tool_name
                                    pending_tool_start[tool_id_full] = time.time()
                                    if logger.debug:
                                        print(f"\n  [Pending: {len(pending_tools)} tools]", end="", flush=True)

                                # Log tool invocation in verbose mode
                                if logger.verbose:
                                    input_preview = str(tool_input)[:100] if tool_input else ""
                                    logger.log_debug(f"Tool: {tool_name} id={tool_id} input={input_preview}...")

                                # TodoWrite - show task progress
                                if tool_name == "TodoWrite":
                                    todos = tool_input.get("todos", []) if isinstance(tool_input, dict) else []
                                    in_progress = [
                                        t for t in todos
                                        if isinstance(t, dict) and t.get("status") == "in_progress"
                                    ]
                                    if in_progress:
                                        task_content = in_progress[0].get("content", "")
                                        if task_content != current_task:
                                            current_task = task_content
                                            print(f"\n  [Task] {task_content[:60]} ({logger.elapsed()})", flush=True)
                                    else:
                                        completed = sum(
                                            1 for t in todos
                                            if isinstance(t, dict) and t.get("status") == "completed"
                                        )
                                        total = len(todos)
                                        if total > 0:
                                            print(f" ({completed}/{total} @ {logger.elapsed()})", end="", flush=True)

                                # Write - new report creation
                                elif tool_name == "Write":
                                    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
                                    if file_path and ("reports/" in file_path or "infographic/" in file_path):
                                        report_count += 1
                                        filename = file_path.split("/")[-1]
                                        created_reports.append(filename)
                                        print(f"\n  ** Creating: {filename} ({logger.elapsed()})", flush=True)
                                    else:
                                        if logger.verbose:
                                            fname = file_path.split("/")[-1] if file_path else "unknown"
                                            print(f"\n  [Write: {fname}] ({logger.elapsed()})", end="", flush=True)
                                        else:
                                            print(".", end="", flush=True)

                                # Read - file reading
                                elif tool_name == "Read":
                                    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
                                    if logger.verbose:
                                        fname = file_path.split("/")[-1] if file_path else "unknown"
                                        print(f"\n  [Read: {fname}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                                # Grep - searching
                                elif tool_name == "Grep":
                                    pattern = tool_input.get("pattern", "") if isinstance(tool_input, dict) else ""
                                    if logger.verbose:
                                        print(f"\n  [Grep: {pattern[:30]}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                                # Bash - command execution
                                elif tool_name == "Bash":
                                    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
                                    if logger.verbose:
                                        cmd_preview = command[:50].replace("\n", " ")
                                        print(f"\n  [Bash: {cmd_preview}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print("B", end="", flush=True)

                                # Edit - file editing
                                elif tool_name == "Edit":
                                    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
                                    if logger.verbose:
                                        fname = file_path.split("/")[-1] if file_path else "unknown"
                                        print(f"\n  [Edit: {fname}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                                # Glob - checking for existing reports
                                elif tool_name == "Glob":
                                    pattern = tool_input.get("pattern", "") if isinstance(tool_input, dict) else ""
                                    if "reports" in pattern or ".md" in pattern:
                                        print(f"\n  [Check duplicates] ({logger.elapsed()})", end="", flush=True)
                                    elif logger.verbose:
                                        print(f"\n  [Glob: {pattern[:40]}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                                # Skill invocation
                                elif tool_name == "Skill":
                                    skill_name = tool_input.get("skill", "") if isinstance(tool_input, dict) else ""
                                    print(f"\n  [Skill invoked: {skill_name}] ({logger.elapsed()})", flush=True)

                                # Task - subagent delegation
                                elif tool_name == "Task":
                                    desc = tool_input.get("description", "") if isinstance(tool_input, dict) else ""
                                    print(f"\n  -> Subagent task: {desc[:80]} ({logger.elapsed()})", flush=True)

                                # Google Cloud docs search
                                elif "mcp__google-developer-knowledge" in str(tool_name):
                                    if "search" in tool_name:
                                        search_phrase = ""
                                        if isinstance(tool_input, dict):
                                            search_phrase = tool_input.get("query", "")[:40]
                                        elapsed = logger.elapsed()
                                        print(
                                            f"\n  [Search Google docs: {search_phrase}] ({elapsed})",
                                            end="",
                                            flush=True
                                        )
                                    elif "get_document" in tool_name:
                                        parent = tool_input.get("parent", "") if isinstance(tool_input, dict) else ""
                                        parent_short = parent.split("/")[-1][:30] if parent else ""
                                        elapsed = logger.elapsed()
                                        print(
                                            f"\n  [Read Google docs: {parent_short}] ({elapsed})",
                                            end="",
                                            flush=True
                                        )
                                    else:
                                        print(".", end="", flush=True)

                                else:
                                    if logger.verbose:
                                        print(f"\n  [{tool_name}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                    elif isinstance(message, ResultMessage):
                        subtype = getattr(message, "subtype", None)
                        result_received = True
                        if subtype == "success":
                            print(f"\n\nCompleted! ({report_count} reports, {msg_count} messages, {logger.elapsed()})")
                        elif subtype == "error_during_execution":
                            error_msg = getattr(message, "error", None)
                            print(f"\n\nError during execution ({logger.elapsed()})", file=sys.stderr)
                            if error_msg:
                                logger.log_error(f"Error details: {error_msg}")
                        else:
                            print(f"\n\nResult: {subtype} ({logger.elapsed()})")

                    elif isinstance(message, SystemMessage):
                        subtype = getattr(message, "subtype", None)
                        if subtype == "init":
                            print(f" [Init] ({logger.elapsed()})", end="", flush=True)

                            # Check for MCP servers in message attributes
                            mcp_servers = getattr(message, "mcp_servers", [])

                            # Also check inside data dict if present
                            data = getattr(message, "data", {})
                            if isinstance(data, dict):
                                if logger.debug:
                                    print(f"\n  [Init data keys: {list(data.keys())}]", flush=True)
                                if "mcp_servers" in data:
                                    mcp_servers = data["mcp_servers"]
                                elif "mcpServers" in data:
                                    mcp_servers = data["mcpServers"]

                            if mcp_servers:
                                print(f"\n  MCP servers ({len(mcp_servers)}):", flush=True)
                                for server in mcp_servers:
                                    if isinstance(server, dict):
                                        name = server.get("name", "unknown")
                                        status = server.get("status", "unknown")
                                    else:
                                        name = getattr(server, "name", "unknown")
                                        status = getattr(server, "status", "unknown")
                                    status_icon = "+" if status == "connected" else "x"
                                    print(f"    [{status_icon}] {name}: {status}", flush=True)
                                failed = [
                                    s for s in mcp_servers
                                    if (
                                        s.get("status") if isinstance(s, dict)
                                        else getattr(s, "status", None)
                                    ) != "connected"
                                ]
                                if failed:
                                    logger.log_error(f"MCP connection failed: {failed}")
                            else:
                                logger.log_warn("No MCP servers found in init message")
                                if logger.debug and data:
                                    print(f"  [Init data: {str(data)[:500]}]", flush=True)
                        elif logger.verbose:
                            print(f"\n  [System:{subtype}] ({logger.elapsed()})", end="", flush=True)

                    elif isinstance(message, UserMessage):
                        # UserMessage contains tool execution results
                        # This is when the file has actually been written (after ToolUseBlock)
                        content = getattr(message, "content", [])
                        if isinstance(content, list):
                            for block in content:
                                if hasattr(block, "tool_use_id"):
                                    tool_id_full = getattr(block, "tool_use_id", "")
                                    tool_id = tool_id_full[:8]

                                    # Remove from pending
                                    tool_name = pending_tools.pop(tool_id_full, "unknown")
                                    pending_tool_start.pop(tool_id_full, None)

                                    # Check for error in result
                                    is_error = getattr(block, "is_error", False)
                                    content_preview = ""
                                    if hasattr(block, "content"):
                                        bc = block.content
                                        if isinstance(bc, str):
                                            content_preview = bc[:100].replace("\n", " ")
                                        elif isinstance(bc, list) and bc:
                                            content_preview = str(bc[0])[:100].replace("\n", " ")
                                    status = "ERROR" if is_error else "OK"

                                    if logger.debug:
                                        result_msg = (
                                            f"\n  [Result:{tool_id}] {tool_name} {status} "
                                            f"- {content_preview}..."
                                        )
                                        print(result_msg, flush=True)
                                        if pending_tools:
                                            pending_list = list(pending_tools.values())
                                            print(
                                                f"\n  [Still pending: {pending_list}]",
                                                flush=True
                                            )

                    else:
                        if not logger.debug:
                            print(".", end="", flush=True)

                # Success - break out of the retry loop
                break

            except Exception as e:
                error_str = str(e)

                # If ResultMessage was already received, the task completed
                # successfully but the CLI process exited with non-zero code.
                # This is a known SDK issue - treat as success.
                if result_received and "exit code" in error_str:
                    logger.log_warn(
                        f"CLI exited with error after ResultMessage: {error_str[:200]}"
                    )
                    print(
                        f"\n  (CLI exit code error ignored - task already completed)",
                        flush=True,
                    )
                    break

                logger.log_error(f"Exception at {logger.elapsed()}: {type(e).__name__}: {error_str[:200]}")

                if is_throttling_error(e) and model_index < len(models_to_try) - 1:
                    print(f"\n\nThrottling detected with {current_model} ({logger.elapsed()})")
                    print(f"Falling back to {models_to_try[model_index + 1]}...")
                    print()
                    continue
                else:
                    # Log additional context for debugging
                    logger.log_error(f"Messages processed: {msg_count}")
                    logger.log_error(f"Reports created: {report_count}")
                    if created_reports:
                        logger.log_error(f"Created files: {created_reports}")
                    # Dump CLI stderr for root cause analysis
                    if stderr_lines:
                        print()
                        print_separator("-")
                        print("CLI stderr output (last 50 lines):")
                        print_separator("-")
                        for sl in stderr_lines[-50:]:
                            print(f"  {sl}")
                    raise

        # Log the result
        print()
        print_separator()
        print("Agent Response:")
        print_separator()
        print(result_text if result_text else "(No text response)")
        print()

        # Show created reports in this session
        print_separator()
        print("Summary:")
        print_separator()
        print(f"Model used: {current_model}")

        # Created reports
        if created_reports:
            print(f"New reports created: {len(created_reports)}")
            for filename in created_reports:
                print(f"  + {filename}")
        else:
            print("New reports created: 0")

        # Skipped reports (duplicates)
        if skipped_reports:
            print()
            print(f"Skipped (duplicates): {len(skipped_reports)}")
            for task in skipped_reports:
                print(f"  - {task[:60]}")

        # Show latest reports from disk
        report_files = get_latest_reports(output_dir)
        if report_files:
            print()
            print(f"Latest reports on disk ({len(report_files)}):")
            for index, file in enumerate(report_files, 1):
                print(f"  {index}. {file}")

        print()
        print(f"End time: {datetime.now().isoformat()}")
        print(f"Total execution time: {logger.elapsed()}")
        print("Execution completed successfully")

        # Detect newly created report files by comparing with snapshot
        new_reports: list[str] = []
        for md_file in output_dir.rglob("*.md"):
            rel_path = str(md_file.relative_to(project_dir))
            if rel_path not in existing_reports:
                new_reports.append(rel_path)
        new_reports.sort()

        if new_reports:
            print()
            print(f"New report files detected on disk: {len(new_reports)}")
            for rp in new_reports:
                print(f"  + {rp}")

        return new_reports

    except Exception as e:
        print()
        print_separator()
        print("ERROR occurred during execution:")
        print_separator()
        print(f"Time: {datetime.now().isoformat()} (elapsed: {logger.elapsed()})")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}", file=sys.stderr)

        if hasattr(e, "__traceback__"):
            import traceback
            print()
            print("Stack trace:")
            traceback.print_exc()

        raise


def _report_to_infographic_path(report_path: str) -> str:
    """Convert a report path to the expected infographic filename.

    Example:
        reports/2026/2026-02-04-structured-outputs.md
        -> infographic/20260204-structured-outputs.html
    """
    filename = Path(report_path).stem  # e.g. 2026-02-04-structured-outputs
    parts = filename.split("-", 3)  # ['2026', '02', '04', 'structured-outputs']
    if len(parts) >= 4:
        date_prefix = f"{parts[0]}{parts[1]}{parts[2]}"
        slug = parts[3]
        return f"infographic/{date_prefix}-{slug}.html"
    return f"infographic/{filename}.html"


async def generate_infographics(report_paths: list[str]) -> list[str]:
    """Generate infographics using Claude Agent SDK subagents.

    Processes reports in batches of BATCH_SIZE, making a separate query()
    call per batch to avoid "Prompt is too long" errors.

    Args:
        report_paths: List of report file paths relative to project_dir.

    Returns:
        List of created infographic file paths.
    """
    BATCH_SIZE = 5

    if not report_paths:
        print("No reports to generate infographics for.")
        return []

    project_dir = Path(__file__).parent
    infographic_dir = project_dir / "infographic"
    infographic_dir.mkdir(exist_ok=True)

    # Filter out reports that already have infographics
    targets: list[str] = []
    for rp in report_paths:
        expected_html = _report_to_infographic_path(rp)
        if (project_dir / expected_html).exists():
            print(f"  Skip (infographic exists): {expected_html}")
            continue
        targets.append(rp)

    if not targets:
        print("All reports already have infographics.")
        return []

    print_separator()
    print(f"Infographic Generation: {len(targets)} report(s) via subagents")
    print_separator()
    print()

    subagent_prompt = (
        "You are an infographic generator. "
        "When given a report file path and output path:\n"
        "1. Invoke the Skill tool with skill='creating-infographic'\n"
        "2. Follow the skill's workflow to create the infographic\n"
        "3. Save to the specified output path"
    )

    models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]
    created: list[str] = []

    bedrock_env = {
        "CLAUDE_CODE_USE_BEDROCK": "1",
        "AWS_REGION": os.environ.get("AWS_REGION", "us-east-1"),
    }

    # Process in batches
    total_batches = (len(targets) + BATCH_SIZE - 1) // BATCH_SIZE
    for batch_idx in range(total_batches):
        batch_start = batch_idx * BATCH_SIZE
        batch_end = min(batch_start + BATCH_SIZE, len(targets))
        batch = targets[batch_start:batch_end]

        print(
            f"  Batch {batch_idx + 1}/{total_batches} "
            f"({len(batch)} reports)"
        )

        # Build task list for this batch
        task_lines = []
        for i, rp in enumerate(batch, 1):
            html_path = _report_to_infographic_path(rp)
            task_lines.append(
                f"  {i}. Report: '{rp}' -> Output: '{html_path}'"
            )
        task_list = "\n".join(task_lines)

        orchestrator_prompt = (
            f"You have {len(batch)} report(s) that each need an "
            f"infographic.\n"
            f"For EACH report below, use the 'infographic-generator' "
            f"subagent via the Task tool to generate the infographic. "
            f"Delegate ALL of them so they run in parallel.\n"
            f"When collecting TaskOutput, set timeout to 600000.\n\n"
            f"Reports to process:\n{task_list}\n\n"
            f"For each task, tell the subagent:\n"
            f"- Which report file to read\n"
            f"- Where to save the output HTML\n"
            f"Wait for all subagents to complete, then confirm done."
        )

        for model_index, current_model in enumerate(models_to_try):
            infographic_stderr: list[str] = []

            def _on_infographic_stderr(line: str) -> None:
                infographic_stderr.append(line)

            options = ClaudeAgentOptions(
                model=current_model,
                fallback_model=(
                    FALLBACK_MODEL
                    if current_model == PRIMARY_MODEL
                    else None
                ),
                env=bedrock_env,
                cwd=str(project_dir),
                setting_sources=["project"],
                allowed_tools=["Skill", "Read", "Write", "Edit", "Glob", "Bash", "Task"],
                agents={
                    "infographic-generator": AgentDefinition(
                        description="Generate an infographic from a report.",
                        prompt=subagent_prompt,
                        tools=["Skill", "Read", "Write", "Edit", "Glob", "Bash"],
                    ),
                },
                stderr=_on_infographic_stderr,
            )

            try:
                msg_count = 0
                start_time = time.time()
                infographic_result_received = False

                async for message in query(
                    prompt=orchestrator_prompt, options=options
                ):
                    msg_count += 1

                    if isinstance(message, AssistantMessage):
                        content = getattr(message, "content", [])
                        for block in (
                            content
                            if isinstance(content, list)
                            else []
                        ):
                            if isinstance(block, ToolUseBlock):
                                tool_name = block.name
                                tool_input = (
                                    block.input
                                    if hasattr(block, "input")
                                    else {}
                                )
                                if tool_name == "Task":
                                    desc = (
                                        tool_input.get(
                                            "description", ""
                                        )
                                        if isinstance(
                                            tool_input, dict
                                        )
                                        else ""
                                    )
                                    print(
                                        f"    -> {desc[:80]}",
                                        flush=True,
                                    )
                                elif tool_name == "Write":
                                    file_path = (
                                        tool_input.get(
                                            "file_path", ""
                                        )
                                        if isinstance(
                                            tool_input, dict
                                        )
                                        else ""
                                    )
                                    if "infographic/" in file_path:
                                        fname = (
                                            file_path.split("/")[-1]
                                        )
                                        print(
                                            f"    -> Creating: "
                                            f"{fname}",
                                            flush=True,
                                        )

                    elif isinstance(message, ResultMessage):
                        subtype = getattr(message, "subtype", None)
                        infographic_result_received = True
                        if subtype == "success":
                            elapsed = time.time() - start_time
                            print(
                                f"    Done ({msg_count} msgs, "
                                f"{elapsed:.0f}s)"
                            )
                        elif subtype == "error_during_execution":
                            error_msg = getattr(
                                message, "error", None
                            )
                            print(
                                f"    Error: {error_msg}"
                                if error_msg
                                else "    Error during execution"
                            )

                # Check which infographics were created in this batch
                for rp in batch:
                    html_path = _report_to_infographic_path(rp)
                    if (project_dir / html_path).exists():
                        created.append(html_path)
                    else:
                        name = Path(rp).stem
                        print(
                            f"    Warning: {html_path} not created"
                        )

                break  # Success, exit model retry loop

            except Exception as e:
                error_str = str(e)

                if (
                    infographic_result_received
                    and "exit code" in error_str
                ):
                    print(
                        f"    (CLI exit code error ignored)"
                    )
                    for rp in batch:
                        html_path = _report_to_infographic_path(rp)
                        if (project_dir / html_path).exists():
                            created.append(html_path)
                    break

                if (
                    is_throttling_error(e)
                    and model_index < len(models_to_try) - 1
                ):
                    print(
                        f"    Throttled, retrying with fallback..."
                    )
                    continue
                else:
                    print(
                        f"    Error: {type(e).__name__}: "
                        f"{str(e)[:100]}"
                    )
                    if infographic_stderr:
                        for sl in infographic_stderr[-10:]:
                            print(f"      {sl}")
                    # Check created files even on error
                    for rp in batch:
                        html_path = _report_to_infographic_path(rp)
                        if (project_dir / html_path).exists():
                            created.append(html_path)
                    break

    print()
    print_separator()
    print(f"Infographic Summary: {len(created)}/{len(targets)} created")
    print_separator()
    for path in created:
        print(f"  + {path}")

    return created


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the google-cloud-news-summary skill using Claude Agent SDK.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python run.py
      Run with default settings (past {DEFAULT_DAYS} days)

  python run.py --days 7
      Look back 7 days for updates (useful for catching up after failures)

  python run.py --days 1
      Look back only 1 day (for daily runs)

  python run.py "Vertex AI の最新アップデートを教えて"
      Report only Vertex AI updates

  python run.py --verbose
      Run with verbose logging (timing information)

  python run.py --debug
      Run with full debug logging (all message details)
        """,
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default=None,
        help="Prompt to send to the skill (optional, overrides --days)",
    )
    parser.add_argument(
        "--prompt", "-p",
        dest="prompt_flag",
        help="Prompt to send to the skill (alternative to positional argument)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_DAYS,
        help=f"Number of days to look back for updates (default: {DEFAULT_DAYS})",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging (timing and operation details)",
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug logging (full message details)",
    )
    return parser.parse_args()



def main() -> None:
    """Main entry point."""
    global logger

    args = parse_args()

    # Apply verbose/debug flags from command line
    if args.debug:
        os.environ["DEBUG"] = "1"
    if args.verbose:
        os.environ["VERBOSE"] = "1"

    # Reinitialize logger with updated environment
    logger = Logger()

    # Use --prompt flag if provided, otherwise use positional argument
    prompt = args.prompt_flag if args.prompt_flag else args.prompt
    days = args.days

    # Snapshot existing reports BEFORE Phase 1 so we can detect new ones
    # even if run_skill() raises an exception after reports are written to disk
    project_dir = Path(__file__).parent
    output_dir = project_dir / "reports"
    existing_reports = set()
    for md_file in output_dir.rglob("*.md"):
        existing_reports.add(str(md_file.relative_to(project_dir)))

    new_reports: list[str] = []
    phase1_failed = False

    try:
        # Phase 1: Generate reports
        new_reports = asyncio.run(run_skill(prompt=prompt, days=days))
    except Exception:
        # run_skill already printed error details.
        # Even if the SDK threw an error, sub-agents may have written
        # reports to disk. Detect them so Phase 2 can still run.
        phase1_failed = True
        for md_file in output_dir.rglob("*.md"):
            rel_path = str(md_file.relative_to(project_dir))
            if rel_path not in existing_reports:
                new_reports.append(rel_path)
        new_reports.sort()
        if new_reports:
            print(f"\nPhase 1 ended with error, but {len(new_reports)} new report(s) found on disk:")
            for rp in new_reports:
                print(f"  + {rp}")

    # Collect reports that have infographic links but missing HTML files
    missing_infographics: list[str] = []
    for md_file in output_dir.rglob("*.md"):
        rel_path = str(md_file.relative_to(project_dir))
        expected_html = _report_to_infographic_path(rel_path)
        if (project_dir / expected_html).exists():
            continue
        # Check if the report actually contains an infographic link
        try:
            content = md_file.read_text(encoding="utf-8")
            if "インフォグラフィックを見る" in content:
                if rel_path not in new_reports:
                    missing_infographics.append(rel_path)
        except Exception:
            pass

    if missing_infographics:
        missing_infographics.sort()
        print(f"\nFound {len(missing_infographics)} report(s) with infographic link but missing HTML:")
        for rp in missing_infographics:
            print(f"  ! {rp}")

    # Phase 2: Generate infographics for new reports + missing ones
    # Limit backfill batch size to avoid excessively long CI runs
    MAX_BACKFILL = int(os.environ.get("INFOGRAPHIC_BACKFILL_MAX", "10"))
    backfill = missing_infographics[:MAX_BACKFILL]
    if len(missing_infographics) > MAX_BACKFILL:
        print(
            f"\n  (Processing {MAX_BACKFILL} of "
            f"{len(missing_infographics)} missing; "
            f"remaining will be picked up in next runs)"
        )
    all_targets = new_reports + backfill
    if all_targets:
        print()
        asyncio.run(generate_infographics(all_targets))
    else:
        print("\nNo new reports created. Skipping infographic generation.")

    # Exit with error code if Phase 1 failed (after Phase 2 has had a chance to run)
    if phase1_failed:
        sys.exit(1)



if __name__ == "__main__":
    main()
