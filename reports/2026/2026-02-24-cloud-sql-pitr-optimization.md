# Cloud SQL: Point-in-Time Recovery (PITR) インスタンス作成の高速化

**リリース日**: 2026-02-24
**サービス**: Cloud SQL for MySQL, Cloud SQL for PostgreSQL
**機能**: PITR 有効時のインスタンス作成最適化
**ステータス**: GA (一般提供)

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260224-cloud-sql-pitr-optimization.html)

## 概要

Cloud SQL において、Point-in-Time Recovery (PITR) が有効な状態でのインスタンス作成時間が短縮された。Google Cloud コンソールではデフォルトで PITR が有効になっているため、多くのユーザーがこの改善の恩恵を受けることができる。この最適化は Cloud SQL for MySQL と Cloud SQL for PostgreSQL の両方に適用される。

技術的には、PITR が有効な場合のインスタンス作成時に、従来の標準バックアップの代わりに Instant Snapshot (インスタントスナップショット) を使用する仕組みに変更された。Instant Snapshot はメタデータのみの操作であるため、データサイズに依存しない高速な処理が可能となる。取得された Instant Snapshot は、バックグラウンドで標準バックアップに変換され、リストア操作に対応する。

このアップデートは、データベースインスタンスのプロビジョニング速度を重視する開発者、データベース管理者、および DevOps エンジニアにとって特に有益である。

**アップデート前の課題**

- PITR が有効な状態でインスタンスを作成すると、標準バックアップの取得が必要だったため、インスタンスの作成完了までに長い時間がかかっていた
- 標準バックアップはデータを Cloud Storage にコピーする必要があり、データベースサイズに比例して作成時間が増加していた
- Google Cloud コンソールではデフォルトで PITR が有効なため、多くのユーザーが意図せず長いインスタンス作成時間を経験していた

**アップデート後の改善**

- PITR 有効時のインスタンス作成に Instant Snapshot を使用することで、作成時間が大幅に短縮された
- Instant Snapshot はメタデータのみの操作であるため、データベースサイズに関わらず高速に完了する
- Instant Snapshot は自動的にバックグラウンドで標準バックアップに変換されるため、リストア機能に影響はない

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph before["従来のインスタンス作成フロー"]
        A1["ユーザー\nインスタンス作成要求"] --> B1["Cloud SQL\nインスタンス初期化"]
        B1 --> C1["標準バックアップ取得\n(Cloud Storage へコピー)"]
        C1 --> D1["PITR 有効化"]
        D1 --> E1["インスタンス利用可能\n(データサイズに比例して時間増大)"]
    end

    subgraph after["最適化後のインスタンス作成フロー"]
        A2["ユーザー\nインスタンス作成要求"] --> B2["Cloud SQL\nインスタンス初期化"]
        B2 --> C2["Instant Snapshot 取得\n(メタデータ操作のみ)"]
        C2 --> D2["PITR 有効化"]
        D2 --> E2["インスタンス利用可能\n(高速完了)"]
        C2 -.->|"バックグラウンド変換"| F2["標準バックアップ\n(リストア用)"]
    end

    style before fill:#fee,stroke:#c33
    style after fill:#efe,stroke:#3c3
    style C2 fill:#cfc,stroke:#393
    style F2 fill:#ffc,stroke:#993
```

従来の標準バックアップベースのフローと、Instant Snapshot を活用した最適化後のフローの比較。最適化後はメタデータ操作のみでインスタンスが利用可能になり、標準バックアップへの変換はバックグラウンドで実行される。

## サービスアップデートの詳細

### 主要機能

1. **Instant Snapshot を活用した高速インスタンス作成**
   - PITR 有効時のインスタンス作成において、初回バックアップに Instant Snapshot を使用
   - Instant Snapshot はソースディスクと同じゾーンに保存されるメタデータのみの操作
   - データサイズに依存せず、数秒から数分でスナップショット取得が完了

2. **バックグラウンドでの標準バックアップ変換**
   - 初期の Instant Snapshot は、バックグラウンドで自動的に標準バックアップに変換される
   - 標準バックアップへの変換により、リストア操作やクロスリージョンのデータ保護がサポートされる
   - ユーザー側での追加操作は不要

3. **対象データベースエンジン**
   - Cloud SQL for MySQL: バイナリログベースの PITR に対応
   - Cloud SQL for PostgreSQL: WAL (Write-Ahead Logging) ベースの PITR に対応

## 技術仕様

### PITR のデフォルト動作

| 項目 | Cloud SQL Enterprise Plus edition | Cloud SQL Enterprise edition |
|------|-----------------------------------|------------------------------|
| PITR デフォルト有効化 | 作成方法を問わず、デフォルトで有効 | Google Cloud コンソールでのみデフォルト有効。gcloud CLI / Terraform / API では無効 |
| トランザクションログ保持期間 | 最大 35 日 | 最大 7 日 |
| 可用性 SLA | 99.99% (メンテナンス含む) | 99.95% (メンテナンス除く) |

### Instant Snapshot と標準スナップショットの比較

| 特性 | Instant Snapshot | 標準スナップショット |
|------|------------------|----------------------|
| 保存場所 | ソースディスクと同一ゾーン/リージョン | 1 つ以上のリージョン (ゾーン/リージョンに依存しない) |
| データ冗長性 | 冗長化なし (同一ゾーンのみ) | 複数ロケーションに冗長化 |
| リカバリ時間 (RTO) | 最短 (最も高速) | 中程度 |
| ソースディスク削除時の挙動 | 削除される | 保持される |
| ディスクサイズへの依存 | なし (メタデータ操作) | あり (データサイズに比例) |

### PITR 設定 (gcloud CLI)

```bash
# MySQL: PITR を有効化してインスタンスを作成
gcloud sql instances create INSTANCE_NAME \
  --database-version=MYSQL_8_0 \
  --tier=db-custom-2-7680 \
  --region=asia-northeast1 \
  --backup-start-time=20:00 \
  --enable-bin-log \
  --retained-transaction-log-days=7

# PostgreSQL: PITR を有効化してインスタンスを作成
gcloud sql instances create INSTANCE_NAME \
  --database-version=POSTGRES_14 \
  --tier=db-custom-2-7680 \
  --region=asia-northeast1 \
  --backup-start-time=20:00 \
  --enable-point-in-time-recovery \
  --retained-transaction-log-days=7
```

### Terraform 設定例

```hcl
# MySQL インスタンス (PITR 有効)
resource "google_sql_database_instance" "mysql_pitr" {
  name             = "mysql-instance-pitr"
  region           = "asia-northeast1"
  database_version = "MYSQL_8_0"

  settings {
    tier = "db-custom-2-7680"
    backup_configuration {
      enabled                        = true
      binary_log_enabled             = true
      start_time                     = "20:55"
      transaction_log_retention_days = 3
    }
  }
}

# PostgreSQL インスタンス (PITR 有効)
resource "google_sql_database_instance" "postgres_pitr" {
  name             = "postgres-instance-pitr"
  region           = "asia-northeast1"
  database_version = "POSTGRES_14"

  settings {
    tier = "db-custom-2-7680"
    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "20:55"
      transaction_log_retention_days = 3
    }
  }

  deletion_protection = true
}
```

## 設定方法

### 前提条件

1. Google Cloud プロジェクトが作成されていること
2. Cloud SQL Admin API が有効であること
3. 適切な IAM 権限 (`roles/cloudsql.admin` または `roles/cloudsql.editor`) が付与されていること

### 手順

#### ステップ 1: Google Cloud コンソールでインスタンスを作成

Google Cloud コンソールでインスタンスを作成する場合、PITR はデフォルトで有効になっている。特別な設定は不要で、自動的に Instant Snapshot を活用した高速作成が適用される。

```bash
# コンソール URL
# https://console.cloud.google.com/sql/instances/create
```

コンソールの「Data Protection」セクションで「Enable point-in-time recovery」が有効になっていることを確認する。

#### ステップ 2: 既存インスタンスで PITR を有効化する場合

```bash
# 既存インスタンスの設定を確認
gcloud sql instances describe INSTANCE_NAME

# MySQL: PITR を有効化
gcloud sql instances patch INSTANCE_NAME \
  --enable-bin-log

# PostgreSQL: PITR を有効化
gcloud sql instances patch INSTANCE_NAME \
  --enable-point-in-time-recovery

# 設定を確認
gcloud sql instances describe INSTANCE_NAME
```

バックアップ設定セクションで、MySQL の場合は `binaryLogEnabled: true`、PostgreSQL の場合は `pointInTimeRecoveryEnabled: true` が表示されていることを確認する。

## メリット

### ビジネス面

- **開発・テスト環境の迅速な構築**: データベースインスタンスの作成時間短縮により、開発チームの生産性が向上する。CI/CD パイプラインでのデータベースプロビジョニングが高速化される
- **運用コストの削減**: インスタンス作成の待ち時間が減少し、運用担当者の作業効率が改善される

### 技術面

- **データサイズ非依存の高速化**: Instant Snapshot がメタデータのみの操作であるため、大規模データベースでも一定時間でインスタンスを作成できる
- **リストア機能への影響なし**: バックグラウンドで Instant Snapshot から標準バックアップへの自動変換が行われるため、PITR によるリストア機能は完全に維持される
- **追加設定不要**: 最適化は Cloud SQL 側で自動的に適用されるため、ユーザー側で設定変更や追加操作は不要

## デメリット・制約事項

### 制限事項

- Instant Snapshot はソースディスクと同一ゾーンに保存されるため、ゾーン障害時には利用できない。ただし、バックグラウンドで標準バックアップに変換されるため、最終的なデータ保護レベルに影響はない
- Cloud SQL Enterprise edition では、gcloud CLI / Terraform / Cloud SQL Admin API でインスタンスを作成した場合、PITR はデフォルトで無効。この最適化の恩恵を受けるには手動で PITR を有効化する必要がある

### 考慮すべき点

- Instant Snapshot から標準バックアップへのバックグラウンド変換中は、標準バックアップに依存するリストア操作が制限される可能性がある
- MySQL と PostgreSQL でトランザクションログの仕組みが異なる (MySQL: バイナリログ、PostgreSQL: WAL) ため、PITR の設定パラメータが異なる

## ユースケース

### ユースケース 1: CI/CD パイプラインでのデータベース自動プロビジョニング

**シナリオ**: マイクロサービスの CI/CD パイプラインにおいて、テスト実行前に Cloud SQL インスタンスを毎回作成し、テスト完了後に削除するフロー。PITR が有効な本番同等の設定でインスタンスを作成する必要がある。

**実装例**:
```bash
# CI/CD パイプラインでのインスタンス作成 (PITR 有効)
gcloud sql instances create test-db-${BUILD_ID} \
  --database-version=POSTGRES_14 \
  --tier=db-custom-2-7680 \
  --region=asia-northeast1 \
  --enable-point-in-time-recovery \
  --backup-start-time=00:00

# テスト実行
run_integration_tests

# クリーンアップ
gcloud sql instances delete test-db-${BUILD_ID} --quiet
```

**効果**: インスタンス作成時間の短縮により、CI/CD パイプライン全体の実行時間が削減される。特に大規模データベースを使用するテスト環境で顕著な効果が期待できる。

### ユースケース 2: 災害復旧 (DR) テスト環境の迅速な構築

**シナリオ**: 定期的な DR テストにおいて、本番環境と同等の Cloud SQL インスタンスを迅速に作成し、フェイルオーバー手順を検証する。

**効果**: DR テスト用インスタンスの作成が高速化されることで、テストの実施頻度を上げやすくなり、DR 対策の信頼性が向上する。

## 料金

PITR インスタンス作成の高速化自体に追加料金はない。Cloud SQL の料金は従来通り、以下の要素で構成される。

- **インスタンス料金**: vCPU とメモリに基づく時間課金
- **ストレージ料金**: プロビジョニングされたストレージ容量に基づく課金
- **バックアップ料金**: バックアップに使用されるストレージ容量に基づく課金
- **ネットワーク料金**: 送信データ転送量に基づく課金

詳細な料金については [Cloud SQL 料金ページ](https://cloud.google.com/sql/pricing) を参照。

## 利用可能リージョン

この最適化は Cloud SQL for MySQL および Cloud SQL for PostgreSQL が利用可能なすべてのリージョンで適用される。詳細なリージョン一覧については [Cloud SQL ロケーション](https://cloud.google.com/sql/docs/mysql/locations) を参照。

## 関連サービス・機能

- **Compute Engine Instant Snapshots**: Cloud SQL の PITR 最適化の基盤技術。メタデータのみの操作で高速なディスクスナップショットを実現する
- **Cloud SQL Enhanced Backups**: Backup and DR Service を活用した一元的なバックアップ管理機能。強制保持、スケジューリング、モニタリングを提供する
- **Cloud SQL Fast Clone**: Instant Snapshot を使用した高速クローン機能。同一ゾーン内でのクローン作成をメタデータ操作のみで実行する
- **Cloud Monitoring**: Cloud SQL インスタンスのバックアップステータスやパフォーマンスメトリクスの監視に使用

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260224-cloud-sql-pitr-optimization.html)
- [公式リリースノート](https://cloud.google.com/release-notes#February_24_2026)
- [Cloud SQL for MySQL: PITR の構成](https://cloud.google.com/sql/docs/mysql/backup-recovery/configure-pitr)
- [Cloud SQL for PostgreSQL: PITR の構成](https://cloud.google.com/sql/docs/postgres/backup-recovery/configure-pitr)
- [Compute Engine: Instant Snapshots](https://cloud.google.com/compute/docs/disks/instant-snapshots)
- [Cloud SQL エディションの概要](https://cloud.google.com/sql/docs/mysql/editions-intro)
- [Cloud SQL 料金ページ](https://cloud.google.com/sql/pricing)

## まとめ

Cloud SQL における PITR 有効時のインスタンス作成高速化は、Instant Snapshot 技術を活用することでデータベースサイズに依存しない一定時間でのプロビジョニングを実現した重要な改善である。Google Cloud コンソールではデフォルトで PITR が有効なため、特別な設定変更なく多くのユーザーがこの恩恵を受けられる。データベースの開発・テスト環境の構築や CI/CD パイプラインの効率化を検討しているチームは、この最適化を活用してワークフローの高速化を図ることを推奨する。

---

**タグ**: #CloudSQL #MySQL #PostgreSQL #PITR #PointInTimeRecovery #InstantSnapshot #バックアップ #データベース #パフォーマンス最適化
