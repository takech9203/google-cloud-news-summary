# Google SecOps SOAR: Release 6.3.94

**リリース日**: 2026-07-19

**サービス**: Google SecOps SOAR (Security Orchestration, Automation and Response)

**機能**: Release 6.3.94 メンテナンスリリース

**ステータス**: フェーズ 1 リージョンへのロールアウト中

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260719-google-secops-soar-release-6-3-94.html)

## 概要

Google SecOps SOAR の Release 6.3.94 が、2026 年 7 月 19 日にフェーズ 1 リージョンへのロールアウトを開始した。本リリースは内部バグ修正および顧客報告バグの修正を含むメンテナンスリリースである。

Google SecOps SOAR では 2025 年 3 月から段階的リリース方式を採用しており、まずフェーズ 1 リージョン (日本、インド、オーストラリア、カナダ、ドイツ、スイス) にデプロイされた後、約 1 週間後にフェーズ 2 リージョン (シンガポール、カタール、サウジアラビア、イスラエル、英国、イタリア、EU マルチリージョン、US マルチリージョン) にデプロイされる。

前回の Release 6.3.93 は 2026 年 7 月 12 日にフェーズ 1 に展開され、7 月 18 日に全リージョンで利用可能となった。Release 6.3.94 も同様のスケジュールで全リージョンへ展開される見込みである。

## サービスアップデートの詳細

### 主要内容

1. **内部バグ修正**
   - Google 内部で検出された不具合の修正
   - プラットフォームの安定性向上

2. **顧客報告バグ修正**
   - 顧客から報告された不具合の修正
   - 具体的な修正内容は非公開

### ロールアウトスケジュール

| フェーズ | リージョン | 予定 |
|---------|-----------|------|
| フェーズ 1 | 日本、インド、オーストラリア、カナダ、ドイツ、スイス | 2026-07-19 (展開中) |
| フェーズ 2 | シンガポール、カタール、サウジアラビア、イスラエル、英国 (ロンドン)、イタリア、EU (マルチリージョン)、US (マルチリージョン) | 約 1 週間後 |

## 技術仕様

### リリース情報

| 項目 | 詳細 |
|------|------|
| リリースバージョン | 6.3.94 |
| 前バージョン | 6.3.93 |
| リリースタイプ | メンテナンス (バグ修正) |
| デプロイ方式 | 2 段階フェーズドロールアウト |
| 対象 | SOAR スタンドアロンおよび Google SecOps 統合版 |

## デメリット・制約事項

### 考慮すべき点

- フェーズ 2 リージョンのユーザーは、全リージョン展開まで約 1 週間待つ必要がある
- 具体的なバグ修正内容が公開されていないため、自環境で発生している問題が修正対象かどうかは個別確認が必要
- 所属リージョンが不明な場合は Google SecOps 担当者に問い合わせが必要

## 関連サービス・機能

- **Google SecOps SIEM**: SOAR と統合されたセキュリティ情報イベント管理プラットフォーム
- **Publisher Agent**: リモート環境でのコネクタ実行を担うエージェント (最新版 2.7.0)
- **Google Cloud IAM**: SOAR パーミッショングループの移行先 (Stage 2 期限: 2026 年 9 月 30 日)

## 参考リンク

- [このアップデートのインフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260719-google-secops-soar-release-6-3-94.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#July_19_2026)
- [Google SecOps SOAR リリースノート](https://docs.cloud.google.com/chronicle/docs/soar/release-notes)
- [段階的リリース計画](https://docs.cloud.google.com/chronicle/docs/soar/overview-and-introduction/soar-gradual-release)

## まとめ

Google SecOps SOAR Release 6.3.94 は、内部および顧客報告のバグ修正を含む定期メンテナンスリリースである。フェーズ 1 リージョン (日本含む) では既に利用可能であり、フェーズ 2 リージョンへは約 1 週間後に展開される。特別な対応は不要だが、既知の不具合を抱えている場合はリリース後の動作確認を推奨する。

---

**タグ**: #GoogleSecOps #SOAR #SecurityOperations #BugFix #MaintenanceRelease #PhasedRollout
