# Claude Code 指示

このプロジェクトは Google Cloud の最新ニュースとアップデートを自動収集し、日本語レポートとインフォグラフィックを生成するシステムです。

## プロジェクト概要

- **目的**: Google Cloud の Release Notes と Blog から最新情報を取得し、構造化された日本語レポートを作成
- **実行環境**: GitHub Actions (Claude Agent SDK 使用)
- **出力**: Markdown レポート + HTML インフォグラフィック

## スキル

このプロジェクトには 2 つのスキルが定義されています。

1. **google-cloud-news-summary**: Google Cloud の最新ニュースを収集してレポートを作成
2. **creating-infographic**: レポートから HTML インフォグラフィックを生成

## 作業時の注意事項

### レポート作成

- スキルは `.claude/skills/google-cloud-news-summary/SKILL.md` に定義されています
- レポートテンプレートは `.claude/skills/google-cloud-news-summary/report_template.md` を使用
- 出力先: `reports/{YYYY}/{YYYY}-{MM}-{DD}-{slug}.md`

### パーサースクリプト

- `.claude/skills/google-cloud-news-summary/scripts/` にあります
- RSS/Atom フィードをパースして JSON を出力
- 期間フィルタリング機能付き

### インフォグラフィック

- スキルは `.claude/skills/creating-infographic/SKILL.md` に定義されています
- テーマは `.claude/skills/creating-infographic/themes/` にあります
- 出力先: `infographic/{YYYYMMDD}-{slug}.html`

## CI/CD

- GitHub Actions: `.github/workflows/`
- 毎日自動実行され、新しいレポートとインフォグラフィックを生成

### Subagent アーキテクチャ

`run.py` はレポート作成とインフォグラフィック作成の両方で subagent パターンを採用しています。

- Phase 1 (レポート作成): オーケストレーターが RSS 取得・パース・フィルタリング・重複チェックを行い、`report-generator` subagent に個別レポート作成を委譲 (並列実行)
- Phase 2 (インフォグラフィック作成): `infographic-generator` subagent に個別インフォグラフィック作成を委譲 (並列実行)

## MCP サーバー

このプロジェクトでは Google Developer Knowledge MCP server を使用しています。

- **エンドポイント**: `https://developerknowledge.googleapis.com/mcp`
- **ツール**: `search_documents`, `get_document`, `batch_get_documents`
- **用途**: Google Cloud 公式ドキュメントの検索・取得

設定は `.mcp.json` に定義されています。API キーの設定が必要です。

## ローカル開発

```bash
# 依存関係のインストール
pip install -r requirements.txt

# スキルの実行
python run.py

# カスタムプロンプト
python run.py "Run the google-cloud-news-summary skill for Vertex AI updates"
```

## 参考資料

- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk)
- [Google Cloud Release Notes](https://cloud.google.com/release-notes)
- [Google Cloud Blog](https://cloud.google.com/blog/products/)
