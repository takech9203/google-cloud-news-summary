# Google Cloud News Summary - プロジェクトサマリー

## 概要

Google Cloud の Release Notes と Blog から最新情報を自動収集し、日本語レポートとインフォグラフィックを生成するシステムです。

## プロジェクト構成

### ドキュメント

- `README.md` - 日本語ドキュメント
- `README-en.md` - 英語ドキュメント
- `CLAUDE.md` - Claude Code 指示
- `docs/SETUP.md` - CI/CD セットアップガイド

### スキル定義

- `.claude/skills/google-cloud-news-summary/SKILL.md` - メインスキル定義
- `.claude/skills/google-cloud-news-summary/report_template.md` - レポートテンプレート
- `.claude/skills/google-cloud-news-summary/scripts/parse_gcp_release_notes.py` - RSS パーサー
- `.claude/skills/creating-infographic/` - インフォグラフィック生成スキル (Google Cloud テーマ対応済み)

### 設定ファイル

- `.claude/settings.json` - Claude Code 権限設定
- `.mcp.json` - MCP サーバー設定 (Google Developer Knowledge MCP server)
- `.gitignore` - Git 除外設定
- `requirements.txt` - Python 依存関係
- `run.py` - メイン実行スクリプト

### CI/CD

- `.github/workflows/google-cloud-news-summary.yml` - GitHub Actions ワークフロー

### 出力ディレクトリ

- `reports/` - 生成されたレポート (年別)
- `infographic/` - 生成されたインフォグラフィック

## 情報ソース

| ソース | URL | フォーマット |
|--------|-----|--------------|
| Google Cloud Release Notes | https://cloud.google.com/release-notes | RSS/XML |
| Google Cloud Blog | https://cloud.google.com/blog/products/ | RSS/XML (今後実装予定) |

## MCP サーバー

Google Developer Knowledge MCP server を使用して、Google Cloud 公式ドキュメントの検索・取得が可能です。

## インフォグラフィックテーマ

Google Cloud ブランドカラーに準拠した 3 テーマを用意しています。

- Google Cloud Dark
- Google Cloud Light
- Google Cloud News

## 今後の実装予定

- Google Cloud Blog パーサー (`parse_gcp_blog.py`)
- Google Cloud API 変更履歴の収集
- Google Cloud Status Dashboard との連携

## 使用方法

```bash
pip install -r requirements.txt
python run.py
python run.py "Run the google-cloud-news-summary skill for Vertex AI updates"
```

CI/CD セットアップの詳細は `docs/SETUP.md` を参照してください。

## ライセンス

MIT License
