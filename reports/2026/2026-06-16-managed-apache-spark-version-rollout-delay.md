# Managed Service for Apache Spark: サブマイナーバージョンロールアウト延期

**リリース日**: 2026-06-16

**サービス**: Managed Service for Apache Spark (旧 Dataproc on Compute Engine)

**機能**: サブマイナーバージョンのロールアウトスケジュール変更

**ステータス**: Announcement

:chart_with_upwards_trend: [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260616-managed-apache-spark-version-rollout-delay.html)

## 概要

Managed Service for Apache Spark (旧 Dataproc on Compute Engine) において、事前構成チャネル (pre-configured channels) を使用しない新しいサブマイナーバージョンのロールアウト開始日が、当初予定の 2026 年 6 月 15 日から 2026 年 6 月 22 日に延期されることが発表された。

これはスケジュール変更のみのアナウンスであり、機能面での変更はない。ロールアウトの仕組み自体は変わらず、開始日が 1 週間延期されたのみである。

## サービスアップデートの詳細

### ロールアウトスケジュールの変更

| 項目 | 詳細 |
|------|------|
| 当初予定日 | 2026 年 6 月 15 日 |
| 変更後の開始日 | 2026 年 6 月 22 日 |
| 延期期間 | 1 週間 |
| 対象 | 事前構成チャネルを使用しないサブマイナーバージョン |

### 「事前構成チャネルなしのサブマイナーバージョン」とは

Managed Service for Apache Spark では、クラスタ作成時にイメージバージョンを指定する。サブマイナーバージョンは、セキュリティパッチやコンポーネントの修正を含む増分アップデートである。

- **事前構成チャネル (pre-configured channels)**: 特定のバージョンチャネルに紐づけられたイメージバージョン。チャネルを設定しているユーザーは自動的に適切なバージョンが選択される
- **チャネルなしのバージョン**: チャネル設定を行っていないユーザー向けのバージョン。明示的にイメージバージョンをピン留めしない限り、ロールアウト後にデフォルトとして選択される可能性がある

### 関連するタイムライン

公式ドキュメントによると、以下のスケジュールが設定されている:

| 日付 | イベント |
|------|---------|
| 2026 年 6 月 22 日 | サブマイナーバージョンのロールアウト開始 (延期後) |
| 2026 年 8 月 25 日まで | ピン留めしない限りデフォルトとして選択されない (テスト期間) |
| 2026 年 8 月 25 日以降 | チャネル未設定のバージョンがデフォルトになる |
| 2026 年 8 月 25 日 | 1.x および 2.0 イメージバージョンが利用不可になる |

## メリット

### ユーザーへの影響

- **テスト期間の確保**: ロールアウト開始が延期されたことで、準備のための時間が追加で 1 週間確保された
- **段階的移行**: 8 月 25 日までの間、新バージョンはピン留めしない限りデフォルトにならないため、ユーザーは自分のペースでテスト・検証が可能

## 推奨アクション

- **イメージバージョンのピン留め**: 本番環境では特定のサブマイナーバージョンをピン留めすることを推奨。これにより、意図しないバージョン変更を防止できる
- **テスト計画の策定**: 6 月 22 日以降にロールアウトされる新バージョンを、8 月 25 日のデフォルト化前にテスト環境で検証することを推奨
- **1.x / 2.0 からの移行**: 8 月 25 日に 1.x および 2.0 イメージが利用不可となるため、該当バージョンを使用している場合は早急に移行計画を策定すること

## 参考リンク

- :chart_with_upwards_trend: [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260616-managed-apache-spark-version-rollout-delay.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#June_16_2026)
- [イメージバージョン一覧](https://docs.cloud.google.com/dataproc/docs/concepts/versioning/dataproc-version-clusters#supported-dataproc-image-versions)
- [Managed Service for Apache Spark バージョニング概要](https://docs.cloud.google.com/managed-spark/docs/concepts/versioning/overview)
- [クラスタの再作成とアップデート](https://docs.cloud.google.com/managed-spark/docs/guides/recreate-cluster)

## まとめ

今回のアップデートは、Managed Service for Apache Spark のサブマイナーバージョンロールアウト開始日が 1 週間延期されたという軽微なスケジュール変更である。ユーザーへの直接的な影響は限定的だが、8 月 25 日のデフォルト化に向けたテスト計画を見直す良い機会となる。特に 1.x / 2.0 イメージを使用中のユーザーは、同日にこれらのバージョンが利用不可となるため、移行準備を進めることが重要である。

---

**タグ**: #ManagedServiceForApacheSpark #Dataproc #Versioning #ImageVersion #ScheduleChange
