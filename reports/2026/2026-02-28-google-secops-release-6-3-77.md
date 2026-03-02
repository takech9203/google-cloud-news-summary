# Google SecOps (SIEM & SOAR): Release 6.3.77 が全リージョンで利用可能に

**リリース日**: 2026-02-28

**サービス**: Google SecOps (SIEM & SOAR)

**機能**: Release 6.3.77 が全リージョンで利用可能

**ステータス**: Announcement

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260228-google-secops-release-6-3-77.html)

## 概要

Google SecOps の SIEM および SOAR コンポーネントにおいて、Release 6.3.77 が全リージョンで利用可能になった。本リリースは 2026 年 2 月 22 日に第 1 フェーズのリージョン（日本、インド、オーストラリア、カナダ、ドイツ、スイス）への展開が開始され、その後第 2 フェーズのリージョン（シンガポール、カタール、サウジアラビア、イスラエル、英国、イタリア、EU マルチリージョン、US マルチリージョン）への展開を経て、2 月 28 日に全リージョンでの提供が完了した。

本リリースの主な変更点として、Publisher Agent Version 2.6.4 においてリモートエージェントでの Python 3.7 サポートが削除された。Google SecOps のリモートエージェントを利用しているユーザーは、Python 3.11 への移行が必要となる。

## サービスアップデートの詳細

### 主要な変更点

1. **Publisher Agent Version 2.6.4 - Python 3.7 サポートの削除**
   - リモートエージェントにおいて Python 3.7 のサポートが削除された
   - Python 3.7 は 2025 年 1 月に非推奨が発表されており、今回のリリースでリモートエージェントからの正式な削除が実施された
   - リモートエージェントで Python 3.7 を使用しているユーザーは、Python 3.11 へのアップグレードが必要

## 技術仕様

### リリース展開スケジュール

| フェーズ | リージョン | 展開日 |
|----------|-----------|--------|
| 第 1 フェーズ | 日本、インド、オーストラリア、カナダ、ドイツ、スイス | 2026-02-22 |
| 第 2 フェーズ | シンガポール、カタール、サウジアラビア、イスラエル、英国 (London)、イタリア、EU (マルチリージョン)、US (マルチリージョン) | 第 1 フェーズの 1 週間後 |
| 全リージョン | 全リージョン | 2026-02-28 |

### Python バージョン対応状況

| 項目 | 詳細 |
|------|------|
| 削除されたバージョン | Python 3.7 |
| 推奨バージョン | Python 3.11 |
| 影響範囲 | リモートエージェント (Publisher Agent) |
| Publisher Agent バージョン | 2.6.4 |

## 対応手順

### 前提条件

1. Google SecOps SOAR のリモートエージェントを利用していること
2. 現在のリモートエージェントが Python 3.7 で動作していないことを確認すること

### 必要なアクション

#### Python 3.7 からの移行

リモートエージェントで Python 3.7 を使用している場合は、Python 3.11 へのアップグレードが必要である。Marketplace インテグレーションの Python バージョンアップグレードについては、[公式ドキュメント](https://cloud.google.com/chronicle/docs/soar/respond/integrations-setup/upgrade-python-versions)を参照すること。

## デメリット・制約事項

### 考慮すべき点

- Python 3.7 で動作するリモートエージェントを使用している場合、本リリースの適用後にエージェントが動作しなくなる可能性がある
- Python 2.7 および 3.7 向けに構築されたインテグレーションでは、Integration Rollback 機能がサポートされない

## 利用可能リージョン

Release 6.3.77 は以下の全リージョンで利用可能である。

- **第 1 フェーズリージョン**: 日本、インド、オーストラリア、カナダ、ドイツ、スイス
- **第 2 フェーズリージョン**: シンガポール、カタール、サウジアラビア、イスラエル、英国 (London)、イタリア、EU (マルチリージョン)、US (マルチリージョン)

## 関連サービス・機能

- **Google SecOps SIEM**: セキュリティ情報・イベント管理機能。UDM イベントの検索、検出ルール、ダッシュボードなどを提供
- **Google SecOps SOAR**: セキュリティオーケストレーション、自動化、レスポンス機能。プレイブック、インテグレーション、ケース管理などを提供
- **Publisher Agent (リモートエージェント)**: オンプレミスやリモート環境からのデータ収集・アクション実行を可能にするエージェント

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260228-google-secops-release-6-3-77.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#February_28_2026)
- [Google SecOps SOAR リリースノート](https://cloud.google.com/chronicle/docs/soar/release-notes)
- [Google SecOps リリースノート](https://cloud.google.com/chronicle/docs/secops/release-notes)
- [SOAR 段階的リリース計画](https://cloud.google.com/chronicle/docs/soar/overview-and-introduction/soar-gradual-release)
- [Python バージョンアップグレードガイド](https://cloud.google.com/chronicle/docs/soar/respond/integrations-setup/upgrade-python-versions)

## まとめ

Google SecOps Release 6.3.77 が全リージョンで利用可能となり、Publisher Agent 2.6.4 におけるPython 3.7 サポートの削除が全ユーザーに適用された。リモートエージェントで Python 3.7 を使用しているユーザーは、速やかに Python 3.11 への移行を実施することが推奨される。

---

**タグ**: Google SecOps, SIEM, SOAR, Release 6.3.77, Publisher Agent, Python 3.7, リモートエージェント, セキュリティ
