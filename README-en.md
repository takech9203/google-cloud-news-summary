# Google Cloud News Summary <!-- omit in toc -->

**English** | [日本語](README.md)

A Claude Agent SDK skill that retrieves information from Google Cloud What's New and Release Notes, and generates detailed explanation reports in Japanese.

- [Architecture](#architecture)
  - [System Overview (High-level)](#system-overview-high-level)
- [Project Structure](#project-structure)
- [MCP Servers](#mcp-servers)
- [Execution](#execution)
  - [CI/CD with Claude Agent SDK](#cicd-with-claude-agent-sdk)
  - [Local Development](#local-development)
- [Information Sources](#information-sources)
- [Output](#output)
- [References](#references)
  - [Claude Agent SDK](#claude-agent-sdk)
  - [CI/CD Setup](#cicd-setup)
- [License](#license)

## Architecture

This skill uses the Claude Agent SDK and is scheduled to run from GitHub Actions. `run.py` acts as a two-phase orchestrator: Phase 1 invokes Claude via Bedrock API to generate Japanese reports following the SKILL.md definition, and Phase 2 launches an orchestrator agent that delegates to `infographic-generator` subagents via the Task tool for parallel infographic generation.

### System Overview (High-level)

```mermaid
flowchart TD
    Trigger["⏰ CI/CD Scheduled Trigger"]
    SDK["🐍 run.py (Claude Agent SDK)"]

    Trigger --> SDK

    subgraph Phase1["Phase 1: Report Generation"]
        direction TB
        Skill["📋 google-cloud-news-summary Skill"]

        subgraph Collect["Data Collection"]
            direction LR
            Bash["💻 Bash (curl)"]
            Feeds["📡 RSS/Atom Feeds"]
            Parse["🐍 Parse XML"]
            Bash --> Feeds --> Parse
        end

        Filter["🔍 Filter & Check"]
        Generate["📝 Generate Report"]
        Reports["📁 reports/"]

        Skill --> Collect
        Parse --> Filter
        Filter --> Generate
        Generate --> Reports
    end

    subgraph Phase2["Phase 2: Infographic Generation"]
        direction TB
        InfSkill["🎨 creating-infographic Skill"]
        Infographic["📊 infographic/"]
        InfSkill --> Infographic
    end

    SDK --> Phase1
    Reports -.->|"Parallel subagents<br/>(via Task tool)"| Phase2

    classDef ci fill:#F3E5F5,stroke:#CE93D8,stroke-width:2px,color:#6A1B9A
    classDef sdk fill:#E1BEE7,stroke:#CE93D8,stroke-width:2px,color:#6A1B9A
    classDef agent fill:#E8EAF6,stroke:#9FA8DA,stroke-width:2px,color:#283593
    classDef bash fill:#FFF3E0,stroke:#FFB74D,stroke-width:2px,color:#E65100
    classDef sources fill:#E3F2FD,stroke:#90CAF9,stroke-width:2px,color:#1565C0
    classDef process fill:#FFECB3,stroke:#FFD54F,stroke-width:2px,color:#F57C00
    classDef output fill:#E8F5E9,stroke:#A5D6A7,stroke-width:2px,color:#2E7D32
    classDef frame fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666

    class Trigger ci
    class SDK sdk
    class Skill,InfSkill agent
    class Bash bash
    class Feeds sources
    class Parse,Filter,Generate process
    class Reports,Infographic output
    class Phase1,Phase2,Collect frame
```

**Overall Flow:**

This skill runs periodically from CI/CD, with `run.py` orchestrating two phases.

1. **Phase 1 - Report Generation**: Retrieve information from RSS/Atom feeds, create structured Japanese reports based on templates (google-cloud-news-summary skill)
2. **Phase 2 - Infographic Generation**: The main agent delegates to `infographic-generator` subagents defined via `AgentDefinition`, spawning them in parallel via the Task tool to generate HTML infographics (creating-infographic skill)

## Project Structure

```
google-cloud-news-summary/
├── .claude/                           # Claude Code settings
│   ├── settings.json                  # Permissions & MCP config
│   └── skills/
│       ├── google-cloud-news-summary/ # Skill definition (report generation)
│       │   ├── SKILL.md               # Skill instructions
│       │   ├── report_template.md     # Report template
│       │   └── scripts/               # Parser scripts
│       │       └── parse_gcp_release_notes.py  # GCP Release Notes parser
│       └── creating-infographic/      # Skill definition (infographic generation)
│           ├── SKILL.md               # Skill instructions
│           └── themes/                # Theme definitions
├── .github/workflows/                 # GitHub Actions
├── .mcp.json                          # MCP server configuration
├── reports/                           # Generated reports (by year)
│   ├── 2025/
│   └── 2026/
├── infographic/                       # Generated infographics (HTML)
├── docs/                              # Documentation
│   ├── SETUP.md                       # CI/CD setup guide (Japanese)
│   └── SETUP-en.md                    # CI/CD setup guide (English)
├── CLAUDE.md                          # Claude Code instructions
├── README.md                          # Japanese documentation
├── README-en.md                       # English documentation
├── requirements.txt                   # Python dependencies
└── run.py                             # CI/CD entry point (two-phase orchestrator)
```

**Note**: Skills are defined at project-level (`.claude/skills/`) to ensure they work in CI/CD environments where user-level skills (`~/.claude/skills/`) are not available. `run.py` orchestrates Phase 1 (report generation) and Phase 2 (parallel infographic generation via subagents).

## MCP Servers

This project uses MCP servers configured in `.mcp.json`. The MCP configuration is automatically loaded by the Claude Agent SDK via `setting_sources=["project"]`.

| Server Name | Endpoint | Description |
|-------------|----------|-------------|
| google-developer-knowledge | `https://developerknowledge.googleapis.com/mcp` | Search and retrieve Google Cloud official documentation |
| cloud-cost | `npx cloud-cost-mcp` | Multi-cloud pricing comparison (GCP 287 instances, 40+ regions) |

**MCP server vs RSS feed**:

The MCP server (`search_documents`) can search documentation pages on `docs.cloud.google.com` and is useful for supplementing detailed information about individual updates. However, it does not support date filtering, so RSS feeds + curl are used to retrieve the latest updates list.

| Purpose | Method |
|---------|--------|
| Retrieve latest update list | RSS feed (curl + parser script) |
| Supplement detailed info for individual updates | MCP server (`search_documents`) |
| Retrieve pricing information | MCP server (`cloud-cost`) / curl fallback |

### google-developer-knowledge

A remote MCP server for searching and retrieving official documentation for Google Cloud, Firebase, Android, Maps, and more. It offers three tools:

- `search_documents`: Search documentation
- `get_document`: Retrieve full document content from search results
- `batch_get_documents`: Batch retrieve multiple documents

**Setup**:

1. Enable the [Developer Knowledge API](https://console.cloud.google.com/apis/library/developerknowledge.googleapis.com) in your Google Cloud project
2. Create an API key restricted to the Developer Knowledge API
3. Enable the MCP server:
   ```bash
   gcloud components update
   gcloud beta services mcp enable developerknowledge.googleapis.com --project=YOUR_PROJECT_ID
   ```
   > If `gcloud beta services mcp` is not found, update gcloud CLI to the latest version with `gcloud components update`.
4. Replace `YOUR_API_KEY` in `.mcp.json` with your actual API key
   - Local development: Edit `.mcp.json` directly
   - GitHub Actions: Set `GCP_DEVELOPER_KNOWLEDGE_API_KEY` in repository Secrets (automatically substituted in workflow)

**Reference**: [Developer Knowledge MCP server documentation](https://developers.google.com/knowledge/mcp)

### cloud-cost

A local MCP server specialized in multi-cloud pricing comparison. No API key required; it fetches real-time pricing data from public APIs (`instances.vantage.sh`, etc.).

**Key features:**

- GCP 287 instance types across 40+ regions
- Compute, storage, egress, and Kubernetes pricing comparison
- Full workload cost estimation
- Cross-cloud comparison with AWS / Azure / OCI

**Main tools:**

- `compare_compute`: Compare VM/instance pricing
- `compare_storage`: Compare storage pricing
- `compare_kubernetes`: Compare managed Kubernetes (GKE, etc.) pricing
- `refresh_gcp_pricing`: Refresh GCP pricing data

**Setup**: No additional configuration needed if Node.js is installed. Automatically downloaded and started via `npx cloud-cost-mcp`.

**Reference**: [cloud-cost-mcp (GitHub)](https://github.com/jasonwilbur/cloud-cost-mcp)

## Execution

### CI/CD with Claude Agent SDK

This skill is automatically executed from GitHub Actions using the Claude Agent SDK.

**Setup Instructions**: Running in CI/CD requires configuring AWS IAM OIDC provider, IAM role, and CI/CD variables. See the following documentation for detailed instructions:

📖 **[CI/CD Setup Guide (docs/SETUP-en.md)](docs/SETUP-en.md)**

The setup guide includes:

- Creating AWS IAM OIDC provider and IAM role (with automation script)
- Configuring GitHub Actions variables
- Troubleshooting

### Local Development

**Using Claude Code CLI**:
```bash
cd ~/.claude/skills/google-cloud-news-summary
claude "Report the latest Google Cloud news"
```

**Using run.py**:
```bash
cd google-cloud-news-summary
pip install -r requirements.txt

# Default prompt (past week)
python run.py

# Custom prompt - Filter by specific service
python run.py "Run the google-cloud-news-summary skill for Vertex AI updates"

# Custom prompt - Specify time period
python run.py "Run the google-cloud-news-summary skill for GCP updates from the past 2 weeks"
```

**Notes**:
- `run.py` requires AWS credentials configured for Bedrock access
- Include "Run the google-cloud-news-summary skill" in prompts to ensure the skill is invoked
- Current datetime is automatically added to the prompt for accurate date filtering

## Information Sources

| Source | URL | Format | Retrieval Method |
|--------|-----|--------|------------------|
| Google Cloud Release Notes | https://cloud.google.com/release-notes | RSS/XML | curl + parse_gcp_release_notes.py |
| Google Cloud Blog | https://cloud.google.com/blog/products/ | RSS/XML | curl + parser (to be implemented) |

## Output

Two types of artifacts are generated.

- **Reports**: Japanese Markdown, `reports/{YYYY}/{YYYY}-{MM}-{DD}-{slug}.md`
- **Infographics**: HTML, `infographic/{YYYYMMDD}-{slug}.html`

## References

### Claude Agent SDK
- [Claude Agent SDK - Skills](https://platform.claude.com/docs/en/agent-sdk/skills) - Agent Skills in the SDK
- [Claude Agent SDK - Subagents](https://platform.claude.com/docs/en/agent-sdk/subagents) - Subagents in the SDK (parallel execution)
- [Claude Agent SDK - MCP](https://platform.claude.com/docs/en/agent-sdk/mcp) - MCP in the SDK
- [Claude Agent SDK - Python](https://platform.claude.com/docs/en/agent-sdk/python) - Python SDK Reference

### CI/CD Setup
- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials) - Official action to configure AWS credentials in GitHub Actions
- [GitHub Actions: Configuring OpenID Connect in AWS](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)

## License

MIT License - See [LICENSE](LICENSE) for details.
