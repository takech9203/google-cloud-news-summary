#!/usr/bin/env python3
"""
Google Cloud News Summary 自動化スクリプト

Claude Agent SDK (Amazon Bedrock) を使用して google-cloud-news-summary スキルを実行します。
GitHub Actions で毎日自動実行されることを想定しています。

使用方法:
    python run.py                           # デフォルト設定で実行
    python run.py "カスタムプロンプト"       # カスタムプロンプトで実行
    python run.py --prompt "カスタムプロンプト"  # カスタムプロンプト (明示的フラグ)

環境変数:
    DEBUG=1         デバッグモード (詳細ログ出力)
    VERBOSE=1       詳細モード (タイミング情報出力)
    AWS_REGION      Bedrock の AWS リージョン (デフォルト: us-east-1)
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

# =============================================================================
# 設定
# =============================================================================

# 遡って取得する日数のデフォルト値。
# 日次実行では 3 日、キャッチアップ実行では --days 7 などを指定。
DEFAULT_DAYS = 3

# オーケストレーターに渡すデフォルトのプロンプトテンプレート。
# {days} プレースホルダーは実際の日数に置換される。
DEFAULT_PROMPT_TEMPLATE = (
    "Report Google Cloud news from the past {days} days. "
    "Fetch the RSS feed, filter updates, check for duplicates, "
    "and delegate report creation to subagents."
)

# モデル設定: 品質重視で Opus を使用、スロットリング時は Sonnet にフォールバック。
PRIMARY_MODEL = "global.anthropic.claude-opus-4-6-v1"
FALLBACK_MODEL = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"

# オーケストレーターと report-generator サブエージェントが使用するツール。
# Claude Code 組み込みのファイル操作・Web アクセス用ツール。
COMMON_TOOLS = [
    "Skill",      # .claude/skills/ のスキル定義を呼び出す
    "Read",       # ファイル読み込み
    "Write",      # ファイル書き込み
    "Edit",       # ファイル編集
    "MultiEdit",  # 複数ファイル編集
    "Glob",       # パターンでファイル検索
    "Grep",       # ファイル内容検索
    "Bash",       # シェルコマンド実行
    "WebFetch",   # Web ページ取得
]

# MCP (Model Context Protocol) ツール。
# Google Cloud ドキュメントと価格情報にアクセス。
# .mcp.json で API キーの設定が必要。
MCP_TOOLS = [
    "mcp__google-developer-knowledge__search_documents",
    "mcp__google-developer-knowledge__get_document",
    "mcp__google-developer-knowledge__batch_get_documents",
    "mcp__cloud-cost__get_pricing",
    "mcp__cloud-cost__compare_pricing",
    "mcp__cloud-cost__list_services",
]


# =============================================================================
# ロギング
# =============================================================================


class Logger:
    """デバッグモードと詳細モードに対応したロガー。

    環境変数で出力の詳細度を制御:
    - DEBUG=1: 全メッセージの詳細 (最も詳細)
    - VERBOSE=1: タイミングと操作の詳細
    - どちらもなし: 最小限の出力 (進捗ドットのみ)
    """

    def __init__(self) -> None:
        self.debug = os.environ.get("DEBUG", "").lower() in ("1", "true", "yes")
        self.verbose = os.environ.get("VERBOSE", "").lower() in ("1", "true", "yes") or self.debug
        self.start_time = time.time()
        self.last_timestamp = self.start_time

    def elapsed(self) -> str:
        """開始からの経過時間を返す。"""
        return f"{time.time() - self.start_time:.1f}s"

    def delta(self) -> str:
        """前回のタイムスタンプからの経過時間を返し、タイムスタンプを更新する。"""
        now = time.time()
        delta = now - self.last_timestamp
        self.last_timestamp = now
        return f"+{delta:.1f}s"

    def log(self, message: str, *, level: str = "INFO", force: bool = False) -> None:
        """タイムスタンプ付きでメッセージを出力する。"""
        if force or self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}", flush=True)

    def log_debug(self, message: str) -> None:
        """デバッグメッセージを出力 (デバッグモード時のみ)。"""
        if self.debug:
            self.log(message, level="DEBUG")

    def log_verbose(self, message: str) -> None:
        """詳細メッセージを出力 (verbose または debug モード時)。"""
        if self.verbose:
            self.log(message, level="VERBOSE")

    def log_error(self, message: str) -> None:
        """エラーメッセージを出力 (常に表示)。"""
        self.log(message, level="ERROR", force=True)

    def log_warn(self, message: str) -> None:
        """警告メッセージを出力 (常に表示)。"""
        self.log(message, level="WARN", force=True)


# グローバルロガーインスタンス
logger = Logger()


# =============================================================================
# ユーティリティ関数
# =============================================================================


def print_separator(char: str = "=", length: int = 60) -> None:
    """出力の視覚的な区切り線を表示する。"""
    print(char * length)


def get_latest_reports(output_dir: Path, limit: int = 5) -> list[str]:
    """
    最新のレポートファイル一覧を取得する。

    Args:
        output_dir: レポートが格納されているディレクトリ
        limit: 返すレポートの最大数

    Returns:
        レポートファイル名のリスト
    """
    reports = []

    try:
        if not output_dir.exists():
            return reports

        # 年ディレクトリを取得
        year_dirs = [
            d for d in output_dir.iterdir()
            if d.is_dir() and d.name.isdigit()
        ]
        year_dirs.sort(reverse=True)

        # 年ディレクトリから全 Markdown ファイルを取得
        for year_dir in year_dirs:
            for md_file in year_dir.glob("*.md"):
                reports.append({
                    "name": md_file.name,
                    "path": md_file,
                    "mtime": md_file.stat().st_mtime,
                })

        # 更新日時でソート (新しい順)
        reports.sort(key=lambda x: x["mtime"], reverse=True)

        return [r["name"] for r in reports[:limit]]

    except Exception as e:
        print(f"Warning: Could not read report directory: {e}", file=sys.stderr)
        return []


# =============================================================================
# インデックス生成関数
# =============================================================================
# レポートとインフォグラフィックディレクトリのインデックスファイルを生成する。
# GitHub Actions ワークフローでレポート/インフォグラフィック作成後に呼び出される。


def generate_reports_index(reports_dir: Path) -> bool:
    """
    レポートディレクトリのインデックスファイル (index.md, README.md) を生成する。

    Args:
        reports_dir: レポートディレクトリのパス

    Returns:
        インデックスが更新された場合は True、それ以外は False
    """
    if not reports_dir.exists():
        print(f"Reports directory not found: {reports_dir}", file=sys.stderr)
        return False

    # 年ごとにレポートを収集
    reports_by_year: dict[str, list[dict]] = {}

    year_dirs = [
        d for d in reports_dir.iterdir()
        if d.is_dir() and d.name.isdigit() and len(d.name) == 4
    ]

    for year_dir in year_dirs:
        year = year_dir.name
        reports_by_year[year] = []

        for md_file in year_dir.glob("*.md"):
            # 最初の H1 見出しからタイトルを抽出
            title = md_file.stem  # フォールバック: ファイル名
            try:
                with open(md_file, encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            break
            except Exception:
                pass

            # ファイル名から日付を抽出 (YYYY-MM-DD-*.md)
            date_match = md_file.name[:10] if len(md_file.name) >= 10 else ""

            reports_by_year[year].append({
                "filename": md_file.name,
                "title": title,
                "date": date_match,
                "path": f"{year}/{md_file.name}",
            })

        # 日付でソート (新しい順)
        reports_by_year[year].sort(key=lambda x: x["date"], reverse=True)

    # インデックスコンテンツを生成
    lines = [
        "# Google Cloud ニュースレポート一覧",
        "",
        "このページは、Google Cloud の最新ニュースとアップデートに関するレポートの一覧です。",
        "",
    ]

    # 年でソート (新しい順)
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

    # index.md と README.md の両方に書き込み
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
    インフォグラフィックディレクトリの index.html を生成する。

    Args:
        infographic_dir: インフォグラフィックディレクトリのパス

    Returns:
        インデックスが更新された場合は True、それ以外は False
    """
    import re

    if not infographic_dir.exists():
        print(f"Infographic directory not found: {infographic_dir}", file=sys.stderr)
        return False

    # 全 HTML ファイルを収集 (index.html は除外)
    html_files = []
    for html_file in infographic_dir.glob("*.html"):
        if html_file.name == "index.html":
            continue

        # HTML からタイトルを抽出
        title = html_file.stem
        try:
            with open(html_file, encoding="utf-8") as f:
                content = f.read()
                match = re.search(r"<title>([^<]+)</title>", content)
                if match:
                    title = match.group(1)
        except Exception:
            pass

        # ファイル名から日付を抽出 (YYYYMMDD-*.html)
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

    # 日付でソート (新しい順)
    html_files.sort(key=lambda x: x["date_raw"], reverse=True)

    # index.html を生成
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

    # タイムスタンプ行を除外して比較 (不要な更新を避けるため)
    def strip_timestamp(content: str) -> str:
        return re.sub(r"Generated by Google Cloud News Summary \| \d{4}-\d{2}-\d{2} \d{2}:\d{2}", "", content)

    if strip_timestamp(existing_content) != strip_timestamp(index_content):
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
        print(f"  Updated: {index_path}")
        return True

    return False


# =============================================================================
# コア関数
# =============================================================================


def is_throttling_error(error: Exception) -> bool:
    """API からのスロットリング/レート制限エラーかどうかを判定する。

    フォールバックモデルでリトライするかどうかの判断に使用。
    """
    error_str = str(error).lower()
    return any(keyword in error_str for keyword in [
        "throttl",
        "rate limit",
        "too many requests",
        "429",
        "serviceunav",
    ])


async def run_skill(prompt: str | None = None, days: int = DEFAULT_DAYS) -> list[str]:
    """Claude Agent SDK とサブエージェントを使って google-cloud-news-summary スキルを実行する。

    オーケストレーターが RSS フィード取得、パース、フィルタリング、重複チェックを行い、
    個別レポート作成は Task ツール経由で 'report-generator' サブエージェントに委譲して並列実行。

    Args:
        prompt: スキルに送るプロンプト。None の場合は days に基づくデフォルトを使用。
        days: 遡って取得する日数。デフォルトは DEFAULT_DAYS。

    Returns:
        新規作成されたレポートファイルパスのリスト (project_dir からの相対パス)。
    """
    # プロンプトが指定されていない場合はデフォルトを生成
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

    # 現在日時のコンテキストとオーケストレーター指示を追加
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

    # ロギングモードを表示
    if logger.debug:
        print("Logging mode: DEBUG (full details)")
    elif logger.verbose:
        print("Logging mode: VERBOSE (timing + details)")
    else:
        print("Logging mode: NORMAL (set DEBUG=1 or VERBOSE=1 for more details)")
    print()

    # Bedrock の設定
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    print("Configuration:")
    print(f"  AWS Region: {aws_region}")
    print(f"  Primary Model: {PRIMARY_MODEL}")
    print(f"  Fallback Model: {FALLBACK_MODEL}")
    print("  Using Bedrock: Yes")
    print()

    # パスの初期化
    project_dir = Path(__file__).parent
    output_dir = project_dir / "reports"

    print(f"  Project directory: {project_dir}")
    print(f"  Output directory: {output_dir}")
    print()

    # .mcp.json の確認
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
        # AWS 認証情報の確認
        print("Verifying AWS credentials...")
        sts_client = boto3.client("sts", region_name=aws_region)
        identity = sts_client.get_caller_identity()
        print(f"  AWS Account: {identity['Account']}")
        print(f"  AWS ARN: {identity['Arn']}")
        print()

        # スキル実行前に既存レポートのスナップショットを取得。
        # SDK がエラーを投げても新規作成ファイルを検出できるようにするため。
        existing_reports = set()
        for md_file in output_dir.rglob("*.md"):
            existing_reports.add(str(md_file.relative_to(project_dir)))

        # モデルリトライ戦略: まずプライマリモデル、スロットリング時はフォールバック。
        models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]

        # Bedrock 統合用の環境変数。
        bedrock_env = {
            "CLAUDE_CODE_USE_BEDROCK": "1",
            "AWS_REGION": aws_region,
        }

        # レポート生成用サブエージェントのプロンプト。
        # サブエージェントは Skill を呼び出して詳細なワークフロー指示を取得する。
        # これにより run.py はシンプルに保ち、SKILL.md に全ロジックを集約できる。
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

            # 終了コードエラーのデバッグ用に CLI stderr をキャプチャ
            stderr_lines: list[str] = []

            def _on_stderr(line: str) -> None:
                stderr_lines.append(line)
                if logger.debug:
                    print(
                        f"  [CLI stderr] {line[:200]}",
                        flush=True,
                    )

            # Claude Agent SDK オプションを設定 (report-generator サブエージェント付き)
            # オーケストレーターが RSS 取得、パース、フィルタリング、重複チェックを担当し、
            # レポート作成はサブエージェントに委譲する。
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

            # Claude Agent SDK を使ってクエリを実行。
            # SDK は非同期メッセージストリームを返し、それを処理して
            # 進捗を追跡し、作成/スキップされたレポートを検出する。
            result_text = ""
            report_count = 0
            created_reports: list[str] = []
            skipped_reports: list[str] = []
            msg_count = 0
            current_task = ""
            result_received = False  # ResultMessage を受信したかどうか

            logger.log_verbose(f"Starting query execution at {logger.elapsed()}")
            last_message_time = time.time()
            heartbeat_interval = 10  # N 秒間メッセージがない場合にハートビートを表示
            pending_tools: dict[str, str] = {}  # 実行中のツール呼び出しを追跡
            pending_tool_start: dict[str, float] = {}  # ツール実行時間を追跡

            try:
                # Claude Agent SDK ストリームからのメッセージを処理。
                # メッセージタイプ: AssistantMessage (ツール呼び出し、テキスト)、
                # ResultMessage (完了)、SystemMessage (初期化)、UserMessage (ツール結果)
                async for message in query(prompt=prompt_with_context, options=options):
                    msg_count += 1
                    current_time = time.time()

                    # しばらくメッセージがない場合はハートビートを表示
                    if current_time - last_message_time > heartbeat_interval:
                        heartbeat_msg = f"\n  [Heartbeat] Still waiting... ({logger.elapsed()})"
                        if pending_tools:
                            pending_list = list(pending_tools.values())
                            heartbeat_msg += f"\n  [Pending tools: {', '.join(pending_list)}]"
                        print(heartbeat_msg, flush=True)
                    last_message_time = current_time

                    # デバッグ: メッセージ構造を出力
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

                    # ---------------------------------------------------------
                    # AssistantMessage: Claude のレスポンス (テキストまたはツール呼び出し)
                    # - TextBlock: Claude からのプレーンテキスト応答
                    # - ToolUseBlock: Claude がツールを呼び出している (Write, Read, Bash など)
                    # ---------------------------------------------------------
                    if isinstance(message, AssistantMessage):
                        content = getattr(message, "content", [])
                        for block in content if isinstance(content, list) else []:
                            # TextBlock: テキスト応答を蓄積し、スキップメッセージを検出
                            if isinstance(block, TextBlock):
                                result_text += block.text
                                # テキスト内のスキップ/重複への言及をチェック
                                text_lower = block.text.lower()
                                if "skip" in text_lower or "duplicate" in text_lower or "already exists" in text_lower:
                                    if current_task and current_task not in skipped_reports:
                                        skipped_reports.append(current_task)
                                        print(f"\n  -- Skip (duplicate): {current_task}", flush=True)

                            # ToolUseBlock: Claude がツールを呼び出している
                            # これを追跡して進捗を表示し、レポート作成を検出する
                            elif isinstance(block, ToolUseBlock):
                                tool_name = block.name
                                tool_input = block.input if hasattr(block, "input") else {}
                                tool_id_full = getattr(block, "id", "") if hasattr(block, "id") else ""
                                tool_id = tool_id_full[:8]  # 表示用の短い ID

                                # ハートビート表示用に実行中ツールを追跡。
                                # heartbeat_interval 秒間メッセージが来ない場合、
                                # どのツールがまだ実行中かを表示してシステムが
                                # 停止していないことを示す。ツールは UserMessage (結果)
                                # が到着した時点で pending_tools から削除される。
                                if tool_id_full:
                                    pending_tools[tool_id_full] = tool_name
                                    pending_tool_start[tool_id_full] = time.time()
                                    if logger.debug:
                                        print(f"\n  [Pending: {len(pending_tools)} tools]", end="", flush=True)

                                # verbose モードでツール呼び出しをログ出力
                                if logger.verbose:
                                    input_preview = str(tool_input)[:100] if tool_input else ""
                                    logger.log_debug(f"Tool: {tool_name} id={tool_id} input={input_preview}...")

                                # ---------------------------------------------------------
                                # ツール別の進捗表示
                                # 各ツールタイプに応じたカスタム出力フォーマットで、
                                # 長時間実行中に意味のある進捗フィードバックを提供。
                                # ---------------------------------------------------------

                                # -------------------------------------------------
                                # TodoWrite ツール: Claude の内部タスク追跡
                                # Claude が自身の作業を追跡するために内部で使用する。
                                # 現在進行中のタスクを表示し、完了進捗 (例: "3/5") を表示。
                                # エージェントが何に取り組んでいるかを把握するのに役立つ。
                                # -------------------------------------------------
                                if tool_name == "TodoWrite":
                                    todos = tool_input.get("todos", []) if isinstance(tool_input, dict) else []
                                    # 現在進行中のタスクを検索
                                    in_progress = [
                                        t for t in todos
                                        if isinstance(t, dict) and t.get("status") == "in_progress"
                                    ]
                                    if in_progress:
                                        # タスク名が変わったら表示
                                        task_content = in_progress[0].get("content", "")
                                        if task_content != current_task:
                                            current_task = task_content
                                            print(f"\n  [Task] {task_content[:60]} ({logger.elapsed()})", flush=True)
                                    else:
                                        # 進行中タスクがない場合は完了進捗を表示
                                        completed = sum(
                                            1 for t in todos
                                            if isinstance(t, dict) and t.get("status") == "completed"
                                        )
                                        total = len(todos)
                                        if total > 0:
                                            print(f" ({completed}/{total} @ {logger.elapsed()})", end="", flush=True)

                                # -------------------------------------------------
                                # Write ツール: 新規ファイル作成
                                # 主な用途: 新規レポートとインフォグラフィックの作成。
                                # reports/ や infographic/ ディレクトリへの書き込み時は
                                # "** Creating:" でハイライト表示 (このスクリプトの主要出力)。
                                # その他の書き込みはシンプルな "." インジケータで表示。
                                # -------------------------------------------------
                                elif tool_name == "Write":
                                    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
                                    # レポート/インフォグラフィック作成をハイライト
                                    if file_path and ("reports/" in file_path or "infographic/" in file_path):
                                        report_count += 1
                                        filename = file_path.split("/")[-1]
                                        created_reports.append(filename)
                                        print(f"\n  ** Creating: {filename} ({logger.elapsed()})", flush=True)
                                    else:
                                        # その他のファイル書き込み (一時ファイルなど)
                                        if logger.verbose:
                                            fname = file_path.split("/")[-1] if file_path else "unknown"
                                            print(f"\n  [Write: {fname}] ({logger.elapsed()})", end="", flush=True)
                                        else:
                                            print(".", end="", flush=True)

                                # -------------------------------------------------
                                # Read ツール: ファイル内容の読み込み
                                # 既存レポート、テンプレート、RSS データ、スキル定義などを
                                # 読み込むために使用。エージェントは新しいコンテンツを作成する
                                # 前にファイルを読んでコンテキストを理解する。
                                # verbose モードではファイル名を、通常モードでは "." を表示。
                                # -------------------------------------------------
                                elif tool_name == "Read":
                                    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
                                    if logger.verbose:
                                        fname = file_path.split("/")[-1] if file_path else "unknown"
                                        print(f"\n  [Read: {fname}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                                # -------------------------------------------------
                                # Grep ツール: ファイル内容の検索
                                # ファイル内の特定パターンを検索するために使用。
                                # 例: 重複を避けるため既存レポートタイトルを検索。
                                # verbose モードでは検索パターンを表示。
                                # -------------------------------------------------
                                elif tool_name == "Grep":
                                    pattern = tool_input.get("pattern", "") if isinstance(tool_input, dict) else ""
                                    if logger.verbose:
                                        print(f"\n  [Grep: {pattern[:30]}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                                # -------------------------------------------------
                                # Bash ツール: シェルコマンドの実行
                                # RSS パーサースクリプト (parse_feed.py, parse_blog_feed.py)
                                # やその他のシステムコマンドの実行に使用。
                                # 他のツールと区別するため "B" インジケータを表示
                                # (bash は時間がかかることがあるため)。
                                # -------------------------------------------------
                                elif tool_name == "Bash":
                                    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
                                    if logger.verbose:
                                        cmd_preview = command[:50].replace("\n", " ")
                                        print(f"\n  [Bash: {cmd_preview}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print("B", end="", flush=True)

                                # -------------------------------------------------
                                # Edit ツール: 既存ファイルの編集
                                # レポートや設定ファイルの更新に使用。
                                # verbose モードではファイル名を、通常モードでは "." を表示。
                                # -------------------------------------------------
                                elif tool_name == "Edit":
                                    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
                                    if logger.verbose:
                                        fname = file_path.split("/")[-1] if file_path else "unknown"
                                        print(f"\n  [Edit: {fname}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                                # -------------------------------------------------
                                # Glob ツール: ファイルパターンマッチング
                                # 主に重複を避けるための既存レポートチェックに使用。
                                # パターンに "reports" や ".md" が含まれる場合は
                                # "[Check duplicates]" を表示して重複検出ステップ
                                # であることを示す。
                                # -------------------------------------------------
                                elif tool_name == "Glob":
                                    pattern = tool_input.get("pattern", "") if isinstance(tool_input, dict) else ""
                                    if "reports" in pattern or ".md" in pattern:
                                        print(f"\n  [Check duplicates] ({logger.elapsed()})", end="", flush=True)
                                    elif logger.verbose:
                                        print(f"\n  [Glob: {pattern[:40]}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                                # -------------------------------------------------
                                # Skill ツール: スキル定義の呼び出し
                                # スキルは .claude/skills/ ディレクトリに定義されている。
                                # オーケストレーターは 'google-cloud-news-summary' スキルを
                                # 呼び出し、そこにワークフロー指示 (RSS 取得、パース、
                                # フィルタリング、レポート作成) が記載されている。
                                # アーキテクチャの重要ポイント: 実際のワークフローロジックは
                                # SKILL.md にあり、このコードには含まれない。
                                # -------------------------------------------------
                                elif tool_name == "Skill":
                                    skill_name = tool_input.get("skill", "") if isinstance(tool_input, dict) else ""
                                    print(f"\n  [Skill invoked: {skill_name}] ({logger.elapsed()})", flush=True)

                                # -------------------------------------------------
                                # Task ツール: サブエージェントへの作業委譲
                                # オーケストレーターがこれを使ってサブエージェント
                                # (report-generator, infographic-generator) を生成し、
                                # 個別のレポート/インフォグラフィック作成を処理させる。
                                # 各サブエージェントは独自のコンテキストとツールで独立実行。
                                # -------------------------------------------------
                                elif tool_name == "Task":
                                    desc = tool_input.get("description", "") if isinstance(tool_input, dict) else ""
                                    print(f"\n  -> Subagent task: {desc[:80]} ({logger.elapsed()})", flush=True)

                                # -------------------------------------------------
                                # MCP ツール: Google Developer Knowledge API
                                # Model Context Protocol (MCP) サーバー経由で
                                # Google Cloud 公式ドキュメントにアクセスする。
                                # - search_documents: 関連ドキュメントを検索
                                # - get_document: ドキュメント全文を取得
                                # - batch_get_documents: 複数ドキュメントを一括取得
                                # -------------------------------------------------
                                elif "mcp__google-developer-knowledge" in str(tool_name):
                                    # search_documents: Google Cloud ドキュメント全文検索
                                    # エージェントが何の情報を探しているかを把握するため
                                    # 検索クエリを表示 (例: "Vertex AI pricing")
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
                                    # get_document / batch_get_documents: ドキュメント取得
                                    # どのドキュメントを読んでいるかを示すためパスを表示
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
                                        # その他の MCP 操作 (まれ)
                                        print(".", end="", flush=True)

                                # -------------------------------------------------
                                # フォールバック: 明示的に処理していないその他のツール
                                # デバッグ用に verbose モードではツール名を表示、
                                # 通常モードではアクティビティを示すシンプルな "." を表示。
                                # -------------------------------------------------
                                else:
                                    if logger.verbose:
                                        print(f"\n  [{tool_name}] ({logger.elapsed()})", end="", flush=True)
                                    else:
                                        print(".", end="", flush=True)

                    # ---------------------------------------------------------
                    # ResultMessage: SDK からの最終結果
                    # 完了を示す (成功またはエラー)
                    # ---------------------------------------------------------
                    elif isinstance(message, ResultMessage):
                        subtype = getattr(message, "subtype", None)
                        result_received = True  # CLI 終了コードエラー処理用
                        if subtype == "success":
                            print(f"\n\nCompleted! ({report_count} reports, {msg_count} messages, {logger.elapsed()})")
                        elif subtype == "error_during_execution":
                            error_msg = getattr(message, "error", None)
                            print(f"\n\nError during execution ({logger.elapsed()})", file=sys.stderr)
                            if error_msg:
                                logger.log_error(f"Error details: {error_msg}")
                        else:
                            print(f"\n\nResult: {subtype} ({logger.elapsed()})")

                    # ---------------------------------------------------------
                    # SystemMessage: SDK 初期化とシステムイベント
                    # MCP サーバー接続状態を含む
                    # ---------------------------------------------------------
                    elif isinstance(message, SystemMessage):
                        subtype = getattr(message, "subtype", None)
                        if subtype == "init":
                            print(f" [Init] ({logger.elapsed()})", end="", flush=True)

                            # メッセージ属性から MCP サーバーを確認
                            mcp_servers = getattr(message, "mcp_servers", [])

                            # data dict 内も確認
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

                    # ---------------------------------------------------------
                    # UserMessage: ツール実行結果
                    # ツール完了後に送信される。成功/エラー状態を含む。
                    # この時点でファイルは実際にディスクに書き込まれている。
                    # ---------------------------------------------------------
                    elif isinstance(message, UserMessage):
                        content = getattr(message, "content", [])
                        if isinstance(content, list):
                            for block in content:
                                if hasattr(block, "tool_use_id"):
                                    tool_id_full = getattr(block, "tool_use_id", "")
                                    tool_id = tool_id_full[:8]

                                    # pending から削除
                                    tool_name = pending_tools.pop(tool_id_full, "unknown")
                                    pending_tool_start.pop(tool_id_full, None)

                                    # 結果にエラーがないか確認
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

                # 成功 - リトライループを抜ける
                break

            except Exception as e:
                error_str = str(e)

                # ResultMessage を既に受信している場合、タスクは正常に完了したが
                # CLI プロセスが非ゼロコードで終了した。
                # これは既知の SDK の問題 - 成功として扱う。
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
                    # デバッグ用の追加コンテキストをログ出力
                    logger.log_error(f"Messages processed: {msg_count}")
                    logger.log_error(f"Reports created: {report_count}")
                    if created_reports:
                        logger.log_error(f"Created files: {created_reports}")
                    # 根本原因分析のため CLI stderr をダンプ
                    if stderr_lines:
                        print()
                        print_separator("-")
                        print("CLI stderr output (last 50 lines):")
                        print_separator("-")
                        for sl in stderr_lines[-50:]:
                            print(f"  {sl}")
                    raise

        # 結果をログ出力
        print()
        print_separator()
        print("Agent Response:")
        print_separator()
        print(result_text if result_text else "(No text response)")
        print()

        # このセッションで作成されたレポートを表示
        print_separator()
        print("Summary:")
        print_separator()
        print(f"Model used: {current_model}")

        # 作成されたレポート
        if created_reports:
            print(f"New reports created: {len(created_reports)}")
            for filename in created_reports:
                print(f"  + {filename}")
        else:
            print("New reports created: 0")

        # スキップされたレポート (重複)
        if skipped_reports:
            print()
            print(f"Skipped (duplicates): {len(skipped_reports)}")
            for task in skipped_reports:
                print(f"  - {task[:60]}")

        # ディスク上の最新レポートを表示
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

        # スナップショットと比較して新規作成されたレポートファイルを検出
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


# =============================================================================
# インフォグラフィック生成 (Phase 2)
# =============================================================================
# レポート作成後、creating-infographic スキルを使って
# 各レポートからビジュアルな HTML インフォグラフィックを生成する。


def _report_to_infographic_path(report_path: str) -> str:
    """レポートパスを期待されるインフォグラフィックファイル名に変換する。

    例:
        reports/2026/2026-02-04-structured-outputs.md
        -> infographic/20260204-structured-outputs.html
    """
    filename = Path(report_path).stem  # 例: 2026-02-04-structured-outputs
    parts = filename.split("-", 3)  # ['2026', '02', '04', 'structured-outputs']
    if len(parts) >= 4:
        date_prefix = f"{parts[0]}{parts[1]}{parts[2]}"
        slug = parts[3]
        return f"infographic/{date_prefix}-{slug}.html"
    return f"infographic/{filename}.html"


async def generate_infographics(report_paths: list[str]) -> list[str]:
    """Claude Agent SDK サブエージェントを使ってインフォグラフィックを生成する。

    "Prompt is too long" エラーを避けるため、BATCH_SIZE ごとにバッチ処理し、
    バッチごとに別々の query() 呼び出しを行う。

    Args:
        report_paths: project_dir からの相対パスのレポートファイルリスト。

    Returns:
        作成されたインフォグラフィックファイルパスのリスト。
    """
    BATCH_SIZE = 5

    if not report_paths:
        print("No reports to generate infographics for.")
        return []

    project_dir = Path(__file__).parent
    infographic_dir = project_dir / "infographic"
    infographic_dir.mkdir(exist_ok=True)

    # 既にインフォグラフィックがあるレポートを除外
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

    # インフォグラフィック生成用サブエージェントのプロンプト。
    # サブエージェントは Skill を呼び出して詳細なワークフロー指示を取得する。
    # これにより run.py はシンプルに保ち、SKILL.md に全ロジックを集約できる。
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

    # バッチ処理
    # Issue #584 回避策: バッチ間に遅延を入れてレースコンディションを防ぐ
    BATCH_DELAY_SECONDS = 2
    total_batches = (len(targets) + BATCH_SIZE - 1) // BATCH_SIZE
    for batch_idx in range(total_batches):
        # 2 バッチ目以降は遅延を入れる
        if batch_idx > 0:
            print(f"    (waiting {BATCH_DELAY_SECONDS}s before next batch...)")
            await asyncio.sleep(BATCH_DELAY_SECONDS)

        batch_start = batch_idx * BATCH_SIZE
        batch_end = min(batch_start + BATCH_SIZE, len(targets))
        batch = targets[batch_start:batch_end]

        print(
            f"  Batch {batch_idx + 1}/{total_batches} "
            f"({len(batch)} reports)"
        )

        # このバッチ用のタスクリストを構築
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

                # このバッチで作成されたインフォグラフィックを確認。
                # バッチ完了後に HTML ファイルが存在しない場合は
                # 警告をログ出力するが、他のバッチの処理は継続。
                for rp in batch:
                    html_path = _report_to_infographic_path(rp)
                    if (project_dir / html_path).exists():
                        created.append(html_path)
                    else:
                        print(
                            f"    Warning: {html_path} not created"
                        )

                break  # 成功、モデルリトライループを抜ける

            except Exception as e:
                error_str = str(e)

                # Issue #584 回避策: "Fatal error in message reader" または
                # "exit code" エラーは SDK のレースコンディションの可能性が高い。
                # ファイルが作成されていれば成功とみなす。
                is_known_sdk_issue = (
                    "Fatal error in message reader" in error_str
                    or "exit code" in error_str
                )

                if is_known_sdk_issue:
                    print(f"    (SDK error ignored, checking created files...)")
                    batch_created = 0
                    for rp in batch:
                        html_path = _report_to_infographic_path(rp)
                        if (project_dir / html_path).exists():
                            created.append(html_path)
                            batch_created += 1
                    print(f"    -> {batch_created}/{len(batch)} files created in this batch")
                    # 次のバッチ前に追加の遅延を入れる (Issue #584 回避策)
                    await asyncio.sleep(1)
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
                    # エラーでも作成されたファイルを確認
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


# =============================================================================
# コマンドラインインターフェース
# =============================================================================


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースする。"""
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



# =============================================================================
# エントリーポイント
# =============================================================================


def main() -> None:
    """自動化スクリプトのメインエントリーポイント。

    2 つのフェーズを実行:
    - Phase 1: Google Cloud Release Notes からレポートを生成
    - Phase 2: レポートからインフォグラフィックを生成

    各フェーズは独立して失敗可能。Phase 1 が部分的に成功した場合
    (エラー前に一部レポートが作成された場合) でも Phase 2 は実行される。
    """
    global logger

    args = parse_args()

    # コマンドラインから verbose/debug フラグを適用
    if args.debug:
        os.environ["DEBUG"] = "1"
    if args.verbose:
        os.environ["VERBOSE"] = "1"

    # 更新された環境でロガーを再初期化
    logger = Logger()

    # --prompt フラグがあればそれを使用、なければ位置引数を使用
    prompt = args.prompt_flag if args.prompt_flag else args.prompt
    days = args.days

    # Phase 1 の前に既存レポートのスナップショットを取得
    # run_skill() がレポート書き込み後に例外を投げても新規作成を検出できるようにする
    project_dir = Path(__file__).parent
    output_dir = project_dir / "reports"
    existing_reports = set()
    for md_file in output_dir.rglob("*.md"):
        existing_reports.add(str(md_file.relative_to(project_dir)))

    new_reports: list[str] = []
    phase1_failed = False

    try:
        # Phase 1: レポート生成
        new_reports = asyncio.run(run_skill(prompt=prompt, days=days))
    except Exception:
        # run_skill は既にエラー詳細を出力済み。
        # SDK がエラーを投げても、サブエージェントがレポートを
        # ディスクに書き込んでいる可能性がある。検出して Phase 2 を実行可能に。
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

    # インフォグラフィックリンクがあるが HTML ファイルがないレポートを収集
    missing_infographics: list[str] = []
    for md_file in output_dir.rglob("*.md"):
        rel_path = str(md_file.relative_to(project_dir))
        expected_html = _report_to_infographic_path(rel_path)
        if (project_dir / expected_html).exists():
            continue
        # レポートに実際にインフォグラフィックリンクが含まれているか確認
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

    # Phase 2: 新規レポート + 欠落分のインフォグラフィックを生成
    # CI 実行時間が長くなりすぎないようバックフィルのバッチサイズを制限
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

    # Phase 1 が失敗した場合はエラーコードで終了 (Phase 2 実行後)
    if phase1_failed:
        sys.exit(1)



if __name__ == "__main__":
    main()
