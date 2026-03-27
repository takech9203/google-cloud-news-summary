# BigQuery: EXPORT DATA to Spanner via Cloud resource connections (GA)

**リリース日**: 2026-03-26

**サービス**: BigQuery

**機能**: EXPORT DATA to Spanner via Cloud resource connections (GA)

**ステータス**: GA (Generally Available)

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260326-bigquery-export-data-spanner.html)

## 概要

BigQuery の `EXPORT DATA` ステートメントを使用して、Cloud リソース接続経由で BigQuery のデータを Spanner にエクスポートする機能が一般提供 (GA) となりました。これはリバース ETL（逆 ETL）ワークフローを実現する機能であり、BigQuery の分析結果を Spanner のオペレーショナルデータベースに直接書き戻すことが可能になります。

この機能により、BigQuery の強力な分析機能と Spanner の低レイテンシ・高スループットの特性を組み合わせた、エンドツーエンドのデータパイプラインを SQL のみで構築できます。データエンジニア、アナリティクスエンジニア、アプリケーション開発者にとって、分析結果をリアルタイムアプリケーションに反映させるための重要な機能です。

**アップデート前の課題**

- BigQuery の分析結果を Spanner に反映するには、Dataflow や Cloud Functions などの中間パイプラインを独自に構築・管理する必要があった
- リバース ETL のために外部の ETL ツールやカスタムスクリプトを使用する必要があり、運用コストが高かった
- BigQuery と Spanner 間のデータ連携にはリアルタイム性が確保しにくく、データの鮮度に課題があった

**アップデート後の改善**

- `EXPORT DATA` ステートメント一つで BigQuery から Spanner へのデータエクスポートが可能になった
- Cloud リソース接続を活用したアクセス委任により、セキュアなデータ転送が実現された
- 継続クエリ（Continuous queries）と組み合わせることで、リアルタイムのリバース ETL パイプラインが構築可能になった

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph BigQuery["BigQuery"]
        A["データウェアハウス\n(分析用テーブル)"] --> B["EXPORT DATA\nステートメント"]
        B --> C["スロット\n(コンピュート)"]
    end

    subgraph Connection["Cloud リソース接続"]
        D["サービスアカウント\n(アクセス委任)"]
    end

    subgraph Spanner["Cloud Spanner"]
        E["Spanner インスタンス"] --> F["宛先テーブル"]
    end

    C --> D
    D --> E

    style BigQuery fill:#4285F4,color:#fff
    style Connection fill:#FBBC04,color:#000
    style Spanner fill:#34A853,color:#fff
```

BigQuery がスロットを使用してデータを抽出・変換し、Cloud リソース接続のサービスアカウントを経由して Spanner API を通じて宛先テーブルにデータを書き込みます。

## サービスアップデートの詳細

### 主要機能

1. **EXPORT DATA ステートメントによる Spanner エクスポート**
   - SQL の `EXPORT DATA` ステートメントで BigQuery テーブルから Spanner テーブルへ直接データを書き込み可能
   - `format = 'CLOUD_SPANNER'` を指定し、宛先の Spanner インスタンス・データベース・テーブルを URI で指定
   - `spanner_options` で宛先テーブル名、優先度、リクエストタグなどの詳細設定が可能

2. **Cloud リソース接続によるアクセス委任**
   - Cloud リソース接続を作成すると、BigQuery が自動的にサービスアカウントを生成
   - このサービスアカウントに Spanner への書き込み権限を付与することで、セキュアなアクセス委任を実現
   - `WITH CONNECTION` 句で接続を指定して利用

3. **継続クエリ（Continuous Queries）対応**
   - BigQuery の継続クエリと組み合わせることで、リアルタイムのストリーミングエクスポートが可能
   - Enterprise または Enterprise Plus エディションのスロット予約と `CONTINUOUS` ジョブタイプが必要
   - ニアリアルタイムでの分析結果反映を実現

4. **型変換の自動対応**
   - BigQuery と Spanner 間のデータ型の自動変換をサポート
   - `BIGNUMERIC` から `NUMERIC`（PostgreSQL ダイアレクト）、`FLOAT64` から `FLOAT32`、`INT64` から `ENUM` などの変換に対応

## 技術仕様

### spanner_options の設定項目

| 項目 | 型 | 説明 |
|------|------|------|
| `table` | STRING | 必須。宛先の Spanner テーブル名 |
| `change_timestamp_column` | STRING | TIMESTAMP 型カラム名。最新の行更新を追跡するために使用 |
| `priority` | STRING | 書き込みリクエストの優先度。`LOW`、`MEDIUM`（デフォルト）、`HIGH` |
| `tag` | STRING | リクエストタグ。Spanner モニタリングでのトラフィック識別用。デフォルト: `bq_export` |

### 必要な IAM ロール

| ロール | リソース | 用途 |
|------|------|------|
| `roles/bigquery.dataViewer` | BigQuery テーブル | データの読み取り |
| `roles/bigquery.user` | プロジェクト | エクスポートジョブの実行 |
| `roles/spanner.viewer` | Spanner インスタンス | インスタンスパラメータの確認 |
| `roles/spanner.databaseUser` | Spanner データベース | データの書き込み |
| `roles/bigquery.connectionAdmin` | プロジェクト | Cloud リソース接続の作成 |

## 設定方法

### 前提条件

1. BigQuery Enterprise または Enterprise Plus エディションのスロット予約が作成済みであること
2. エクスポート先の Spanner データベースおよびテーブルが作成済みであること
3. BigQuery Connection API が有効化されていること

### 手順

#### ステップ 1: Cloud リソース接続の作成

```bash
bq mk --connection \
  --location=REGION \
  --project_id=PROJECT_ID \
  --connection_type=CLOUD_RESOURCE \
  CONNECTION_ID
```

接続を作成すると、BigQuery が自動的にサービスアカウントを生成します。以下のコマンドでサービスアカウント ID を確認します。

```bash
bq show --connection PROJECT_ID.REGION.CONNECTION_ID
```

#### ステップ 2: サービスアカウントへの権限付与

```bash
gcloud spanner databases add-iam-policy-binding DATABASE_ID \
  --instance=INSTANCE_ID \
  --member="serviceAccount:SERVICE_ACCOUNT_ID" \
  --role="roles/spanner.databaseUser"
```

Cloud リソース接続のサービスアカウントに、Spanner データベースへの書き込み権限を付与します。

#### ステップ 3: EXPORT DATA の実行

```sql
EXPORT DATA
  WITH CONNECTION `PROJECT_ID.REGION.CONNECTION_ID`
  OPTIONS (
    uri = "https://spanner.googleapis.com/projects/PROJECT_ID/instances/INSTANCE_ID/databases/DATABASE_ID",
    format = 'CLOUD_SPANNER',
    spanner_options = """{ "table": "TABLE_NAME" }"""
  )
AS
SELECT * FROM `PROJECT_ID.DATASET.SOURCE_TABLE`;
```

`WITH CONNECTION` 句で Cloud リソース接続を指定し、BigQuery のデータを Spanner テーブルにエクスポートします。

## メリット

### ビジネス面

- **運用コストの削減**: 中間パイプライン（Dataflow、Cloud Functions 等）の構築・運用が不要になり、インフラ管理コストを大幅に削減
- **Time-to-Value の短縮**: SQL のみで分析結果をオペレーショナルシステムに反映できるため、データ活用までのリードタイムが短縮
- **リアルタイムデータ活用**: 継続クエリと組み合わせることで、分析結果をニアリアルタイムでアプリケーションに反映可能

### 技術面

- **シンプルなアーキテクチャ**: ETL パイプラインを SQL 一文で実現でき、アーキテクチャの複雑性が大幅に低減
- **セキュアなアクセス委任**: Cloud リソース接続によるサービスアカウントベースのアクセス委任で、認証情報の直接管理が不要
- **スケーラビリティ**: BigQuery のスロットと Spanner のノードをスケールさせることで、エクスポートスループットが線形にスケール（ノードあたり約 5 MiB/s）

## デメリット・制約事項

### 制限事項

- BigQuery Enterprise または Enterprise Plus エディションのスロット予約が必要（オンデマンド課金では利用不可）
- 継続エクスポートには `CONTINUOUS` ジョブタイプの予約割り当てが必要
- 同一の rowkey を持つ複数行をエクスポートした場合、Spanner には 1 行のみ書き込まれる（どの行が書き込まれるかは保証されない）
- エクスポートジョブの最大実行時間は 6 時間

### 考慮すべき点

- リージョンをまたぐエクスポートはデータ抽出料金が発生するため、BigQuery と Spanner を同一リージョンに配置することを推奨
- `HIGH` 優先度を設定すると Spanner インスタンスの他のワークロードに影響する可能性がある
- 100 GB を超えるエクスポートでは Spanner ノードと BigQuery スロットの増強が必要
- 宛先テーブルの主キーに生成列が含まれる場合、クエリ内で対応する式を含めることでパフォーマンスが最適化される

## ユースケース

### ユースケース 1: ML 予測結果のアプリケーション反映

**シナリオ**: BigQuery ML で顧客のチャーン予測モデルを実行し、予測結果を Spanner に書き戻してリアルタイムアプリケーションで活用する。

**実装例**:
```sql
EXPORT DATA OPTIONS (
  uri = "https://spanner.googleapis.com/projects/my-project/instances/my-instance/databases/my-db",
  format = 'CLOUD_SPANNER',
  spanner_options = """{ "table": "customer_churn_predictions" }"""
)
AS
SELECT
  customer_id,
  predicted_churn_probability,
  recommended_action,
  CURRENT_TIMESTAMP() AS prediction_timestamp
FROM ML.PREDICT(
  MODEL `my_dataset.churn_model`,
  TABLE `my_dataset.customer_features`
);
```

**効果**: データサイエンティストが BigQuery で作成した予測モデルの結果を、追加のパイプライン構築なしでアプリケーション層に直接反映できる。

### ユースケース 2: リアルタイムダッシュボード用の集計データ配信

**シナリオ**: BigQuery で大量のトランザクションデータを集計し、結果を Spanner に格納して低レイテンシのダッシュボードアプリケーションから参照する。

**実装例**:
```sql
EXPORT DATA OPTIONS (
  uri = "https://spanner.googleapis.com/projects/my-project/instances/my-instance/databases/my-db",
  format = 'CLOUD_SPANNER',
  spanner_options = """{ "table": "daily_sales_summary" }"""
)
AS
SELECT
  region,
  product_category,
  CURRENT_DATE() AS report_date,
  SUM(sales_amount) AS total_sales,
  COUNT(DISTINCT customer_id) AS unique_customers
FROM `my_dataset.transactions`
WHERE DATE(transaction_timestamp) = CURRENT_DATE()
GROUP BY region, product_category;
```

**効果**: BigQuery のクォータやレイテンシの制約を受けず、Spanner の低レイテンシ読み取りでアプリケーションユーザーにデータを提供できる。

## 料金

EXPORT DATA ステートメントによる Spanner へのエクスポートには、BigQuery のキャパシティコンピュート料金が適用されます。

| 項目 | 料金体系 |
|------|------|
| BigQuery コンピュート | キャパシティコンピュート料金（スロット時間単位で課金） |
| リージョン間データ転送 | データ抽出料金が適用（同一リージョンの場合は無料） |
| Spanner ストレージ | エクスポート後のデータ保存に対して Spanner ストレージ料金が適用 |
| Spanner コンピュート | 書き込み処理に対して Spanner ノード/PU の使用量に基づいて課金 |

コスト最適化のために、ベースラインスロットを 0 に設定しオートスケーリングを有効にした予約の利用が推奨されます。

## 関連サービス・機能

- **Cloud Spanner**: エクスポート先のフルマネージドリレーショナルデータベース。グローバル分散、強整合性、高可用性を提供
- **BigQuery Continuous Queries**: 継続クエリと組み合わせることでリアルタイムのリバース ETL パイプラインを構築可能
- **BigQuery Reservations**: EXPORT DATA の実行に必要なスロット予約を管理
- **Cloud リソース接続**: BigQuery と外部サービス間のセキュアなアクセス委任を提供
- **Spanner Graph**: グラフデータモデルを使用する場合、BigQuery からの リバース ETL で Spanner Graph へのデータ投入にも利用可能

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260326-bigquery-export-data-spanner.html)
- [公式ドキュメント: Export data to Spanner (reverse ETL)](https://cloud.google.com/bigquery/docs/export-to-spanner)
- [EXPORT DATA ステートメントリファレンス](https://cloud.google.com/bigquery/docs/reference/standard-sql/export-statements)
- [Cloud リソース接続の作成と設定](https://cloud.google.com/bigquery/docs/create-cloud-resource-connection)
- [BigQuery 料金ページ](https://cloud.google.com/bigquery/pricing)
- [Spanner 料金ページ](https://cloud.google.com/spanner/pricing)

## まとめ

BigQuery の EXPORT DATA ステートメントによる Spanner へのエクスポートが GA となったことで、SQL のみでリバース ETL パイプラインを構築できるようになりました。中間パイプラインの構築・運用が不要になり、BigQuery の分析結果をオペレーショナルシステムに直接反映するアーキテクチャが大幅にシンプルになります。BigQuery と Spanner を組み合わせたデータ活用基盤を構築している組織は、この機能を活用してデータパイプラインの簡素化を検討することを推奨します。

---

**タグ**: BigQuery, Cloud Spanner, EXPORT DATA, リバース ETL, Cloud リソース接続, データパイプライン, GA
