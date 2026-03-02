# Google SecOps (SIEM & SOAR): Release 6.3.78 のロールアウト開始

**リリース日**: 2026-03-01

**サービス**: Google SecOps (SIEM & SOAR)

**機能**: Release 6.3.78 - 内部およびお客様向けバグ修正

**ステータス**: Announcement

:bar_chart: [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260301-google-secops-release-6-3-78.html)

## 概要

Google SecOps の SIEM および SOAR コンポーネントに対して、Release 6.3.78 のロールアウトが第 1 フェーズのリージョンで開始されました。本リリースには内部バグ修正およびお客様から報告されたバグの修正が含まれています。

Google SecOps は、Google Cloud インフラストラクチャ上に構築されたセキュリティオペレーションプラットフォームであり、SIEM (Security Information and Event Management) と SOAR (Security Orchestration, Automation, and Response) の両機能を統合しています。今回のリリースは定期的なメンテナンスリリースであり、プラットフォームの安定性と信頼性の向上を目的としています。

## リリースのロールアウトスケジュール

Google SecOps SOAR のリリースは、2 段階のフェーズで各リージョンに展開されます。通常、日曜日にアップデートが実施され、第 2 フェーズのリージョンは第 1 フェーズの 1 週間後にアップグレードされます。

### 第 1 フェーズのリージョン

| リージョン |
|------|
| 日本 |
| インド |
| オーストラリア |
| カナダ |
| ドイツ |
| スイス |

### 第 2 フェーズのリージョン

| リージョン |
|------|
| シンガポール |
| カタール |
| サウジアラビア |
| イスラエル |
| 英国 (ロンドン) |
| イタリア |
| EU (マルチリージョン) |
| US (マルチリージョン) |

## サービスアップデートの詳細

### 対象コンポーネント

1. **Google SecOps SIEM**
   - Release 6.3.78 には内部およびお客様向けバグ修正が含まれています
   - SIEM は大量のセキュリティテレメトリデータの保持、分析、検索を行うプラットフォームであり、本リリースにより安定性が向上します

2. **Google SecOps SOAR**
   - Release 6.3.78 には内部およびお客様向けバグ修正が含まれています
   - SOAR はセキュリティワークフローの自動化と効率化を行うプラットフォームであり、本リリースにより信頼性が向上します

### 最近のリリース履歴

| リリース | 日付 | 内容 |
|---------|------|------|
| 6.3.78 | 2026-03-01 | 内部およびお客様向けバグ修正 |
| 6.3.77 | 2026-02-22 | Publisher Agent Version 2.6.4 (Python 3.7 サポート終了) |
| 6.3.76 | 2026-02-15 | 内部およびお客様向けバグ修正 |
| 6.3.75 | 2026-02-08 | 内部およびお客様向けバグ修正 |

## メリット

### 運用面

- **プラットフォームの安定性向上**: 内部バグ修正により、Google SecOps プラットフォーム全体の動作がより安定します
- **お客様報告の問題解決**: お客様から報告された問題が修正され、日常的なセキュリティ運用がよりスムーズになります

### 技術面

- **SIEM・SOAR 両方のコンポーネントが同時にアップデート**: 統合プラットフォームとして一貫性のあるバージョン管理が維持されます

## 考慮すべき点

- 具体的なバグ修正の詳細は公開されていません
- 第 1 フェーズのリージョン (日本、インド、オーストラリア、カナダ、ドイツ、スイス) から順次展開されるため、第 2 フェーズのリージョンでは約 1 週間後に適用されます
- 所属リージョンが不明な場合は、Google SecOps の担当者に確認してください

## 関連サービス・機能

- **Google SecOps SIEM**: セキュリティテレメトリの収集、正規化、分析、検索を行うクラウドサービス。UDM (Unified Data Model) による統一的なデータモデルを使用
- **Google SecOps SOAR**: セキュリティワークフローの自動化プラットフォーム。Playbook エンジンによる自動応答、ケース管理、統合管理機能を提供
- **Google SecOps プラットフォーム**: SIEM と SOAR を統合し、脅威の検出から調査、対応までのセキュリティライフサイクル全体をカバー

## 参考リンク

- :bar_chart: [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260301-google-secops-release-6-3-78.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#March_01_2026)
- [Google SecOps SOAR リリースノート](https://docs.cloud.google.com/chronicle/docs/soar/release-notes)
- [Google SecOps 概要ドキュメント](https://docs.cloud.google.com/chronicle/docs/secops/secops-overview)
- [リリースのロールアウトスケジュール](https://docs.cloud.google.com/chronicle/docs/soar/overview-and-introduction/soar-gradual-release)

## まとめ

Google SecOps Release 6.3.78 は、SIEM および SOAR の両コンポーネントにおける内部バグ修正とお客様向けバグ修正を含む定期メンテナンスリリースです。第 1 フェーズのリージョン (日本、インド、オーストラリア、カナダ、ドイツ、スイス) から順次展開されており、第 2 フェーズのリージョンには約 1 週間後に適用される予定です。Google SecOps をご利用のお客様は、通常通りの運用を継続しつつ、プラットフォームの安定性向上をご活用ください。

---

**タグ**: Google SecOps, SIEM, SOAR, Release 6.3.78, Bug Fix, Security Operations, Chronicle
