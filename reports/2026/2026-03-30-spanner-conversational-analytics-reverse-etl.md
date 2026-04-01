# Spanner: 会話型分析 (Preview)、BigQuery マテリアライズドビュー (GA)、リバース ETL (GA)

**リリース日**: 2026-03-30

**サービス**: Cloud Spanner

**機能**: Conversational Analytics / BigQuery 非増分マテリアライズドビュー / リバース ETL

**ステータス**: Preview (会話型分析) / GA (マテリアライズドビュー、リバース ETL)

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260330-spanner-conversational-analytics-reverse-etl.html)

## 概要

今回のアップデートでは、Spanner に関連する 3 つの重要な機能が発表されました。1 つ目は、自然言語を使用して Spanner のオペレーショナルデータにクエリを実行できる「会話型分析 (Conversational Analytics)」機能が Preview として提供開始されたことです。この機能は Conversational Analytics API によって駆動され、複雑な人間の対話を正確なデータベースクエリに変換し、実用的なインサイトを提供します。

2 つ目は、BigQuery の非増分マテリアライズドビューを Spanner データ上に作成できる機能が GA (一般提供) となったことです。定期的に結果をキャッシュすることで、クエリパフォーマンスを向上させることができます。

3 つ目は、Cloud リソース接続と `EXPORT DATA` ステートメントを使用して、BigQuery から Spanner へのリバース ETL (抽出・変換・ロード) を実行できる機能が GA となったことです。これにより、BigQuery の分析能力と Spanner の低レイテンシ・高スループットを組み合わせたデータパイプラインが本番環境で利用可能になりました。

**アップデート前の課題**

- Spanner のオペレーショナルデータを分析するには SQL の専門知識が必要であり、ビジネスユーザーが直接データにアクセスして洞察を得ることが困難だった
- BigQuery で分析した結果を Spanner に戻してアプリケーションで利用するためのネイティブな手段がなく、カスタムの ETL パイプラインを構築する必要があった
- Spanner のデータに対する BigQuery のマテリアライズドビューは Preview 段階であり、本番ワークロードでの利用に制限があった

**アップデート後の改善**

- Conversational Analytics API により、自然言語で Spanner データに問い合わせが可能になり、SQL の専門知識がなくてもデータ分析が実現可能になった
- `EXPORT DATA` ステートメントと CLOUD_RESOURCE 接続を使用して、BigQuery から Spanner へのリバース ETL が GA として本番環境で利用可能になった
- BigQuery の非増分マテリアライズドビューが GA となり、Spanner データのクエリパフォーマンスを安定的に向上できるようになった

## アーキテクチャ図

```mermaid
flowchart TB
    subgraph Users["ユーザー"]
        BU["ビジネスユーザー"]
        DE["データエンジニア"]
        APP["アプリケーション"]
    end

    subgraph CA["会話型分析 (Preview)"]
        NL["自然言語クエリ"]
        API["Conversational Analytics API"]
        GEMINI["Gemini / 推論エンジン"]
    end

    subgraph Spanner["Cloud Spanner"]
        OD["オペレーショナルデータ"]
        ST["Spanner テーブル"]
    end

    subgraph BigQuery["BigQuery"]
        ED["Spanner 外部データセット"]
        MV["非増分マテリアライズドビュー (GA)"]
        AQ["分析クエリ結果"]
    end

    subgraph Connection["Cloud リソース接続"]
        CR["CLOUD_RESOURCE 接続"]
    end

    BU -->|自然言語| NL
    NL --> API
    API --> GEMINI
    GEMINI -->|SQL 生成| OD
    OD -->|クエリ結果| GEMINI
    GEMINI -->|回答| BU

    OD -->|フェデレーション| ED
    ED -->|定期キャッシュ| MV
    DE -->|クエリ| MV

    AQ -->|EXPORT DATA| CR
    CR -->|リバース ETL (GA)| ST
    ST -->|低レイテンシ提供| APP
```

この図は、今回のアップデートで強化された Spanner と BigQuery 間の 3 つのデータフローを示しています。上部は会話型分析による自然言語クエリの流れ、中央は BigQuery マテリアライズドビューによる分析最適化、下部は BigQuery から Spanner へのリバース ETL パイプラインを表しています。

## サービスアップデートの詳細

### 主要機能

1. **会話型分析 (Conversational Analytics) - Preview**
   - Conversational Analytics API (`geminidataanalytics.googleapis.com`) を使用して、自然言語で Spanner のオペレーショナルデータにクエリを実行可能
   - `QueryData` メソッドにより GoogleSQL for Spanner のデータベースに対して自然言語で問い合わせが可能
   - Gemini を活用した推論エンジンがユーザーの質問を解釈し、SQL クエリを生成して実行
   - データエージェントの作成により、ビジネスコンテキストや指示を提供してクエリの精度を向上可能
   - クエリテンプレートとクエリファセットによるエージェントコンテキストのカスタマイズに対応

2. **BigQuery 非増分マテリアライズドビュー over Spanner - GA**
   - `allow_non_incremental_definition` オプションを使用して、Spanner 外部データセットテーブルを参照するマテリアライズドビューを作成可能
   - `max_staleness` パラメータによりデータの鮮度を制御し、キャッシュされた結果と最新データのバランスを調整可能
   - `refresh_interval_minutes` で自動リフレッシュの間隔を設定可能
   - CLOUD_RESOURCE 接続を使用して Spanner 外部データセットを事前に作成する必要がある
   - スマートチューニングは非増分マテリアライズドビューには適用されないため、直接クエリする必要がある

3. **リバース ETL (BigQuery to Spanner) - GA**
   - `EXPORT DATA` ステートメントを使用して BigQuery テーブルから Spanner テーブルへデータをエクスポート可能
   - CLOUD_RESOURCE 接続により、ユーザーに Spanner への直接アクセス権を付与せずにエクスポートを実行可能
   - 継続的エクスポートにも対応しており、リアルタイムに近いデータ同期が可能
   - BigQuery Iceberg テーブルからのエクスポートにも対応
   - Enterprise 以上のリザベーションが必要 (オートスケーリング設定でコスト最適化可能)

## 技術仕様

### 会話型分析 API

| 項目 | 詳細 |
|------|------|
| API エンドポイント | `geminidataanalytics.googleapis.com` |
| 対応データソース | GoogleSQL for Spanner (QueryData メソッド) |
| エージェントコンテキスト | クエリテンプレート、クエリファセット |
| ステータス | Preview |
| 料金 | Preview 期間中は無料 |

### マテリアライズドビュー

| 項目 | 詳細 |
|------|------|
| タイプ | 非増分 (allow_non_incremental_definition) |
| 前提条件 | CLOUD_RESOURCE 接続による Spanner 外部データセット |
| リフレッシュ | 全体リフレッシュ (増分リフレッシュ非対応) |
| SQL 方言 | GoogleSQL のみ |
| ステータス | GA |

### リバース ETL

| 項目 | 詳細 |
|------|------|
| メソッド | EXPORT DATA ステートメント |
| 接続タイプ | CLOUD_RESOURCE 接続 (推奨) または直接アクセス |
| 出力形式 | CLOUD_SPANNER |
| 必要な IAM ロール | BigQuery Data Viewer, BigQuery User, Spanner Viewer, Spanner Database User |
| ステータス | GA |

### リバース ETL の設定例

```sql
EXPORT DATA
  WITH CONNECTION `PROJECT_ID.LOCATION.CONNECTION_NAME`
  OPTIONS (
    uri = "https://spanner.googleapis.com/projects/PROJECT_ID/instances/INSTANCE_ID/databases/DATABASE_ID",
    format = 'CLOUD_SPANNER',
    spanner_options = """{"table": "SPANNER_TABLE_NAME"}"""
  )
AS SELECT * FROM my_bq_dataset.table1;
```

### マテリアライズドビューの作成例

```sql
CREATE MATERIALIZED VIEW sample_dataset.sample_spanner_mv
OPTIONS (
  enable_refresh = true,
  refresh_interval_minutes = 60,
  max_staleness = INTERVAL "24" HOUR,
  allow_non_incremental_definition = true
)
AS SELECT COUNT(*) cnt
FROM spanner_external_dataset.spanner_table;
```

## 設定方法

### 前提条件

1. Google Cloud プロジェクトで Spanner API、BigQuery API、Vertex AI API が有効化されていること
2. Spanner Enterprise エディション以上のインスタンスが作成済みであること (会話型分析を利用する場合)
3. CLOUD_RESOURCE 接続が作成済みであること (マテリアライズドビュー、リバース ETL)

### 手順

#### ステップ 1: CLOUD_RESOURCE 接続の作成

```bash
bq mk --connection \
  --location=REGION \
  --project_id=PROJECT_ID \
  --connection_type=CLOUD_RESOURCE \
  CONNECTION_ID
```

接続を作成すると、BigQuery がシステムサービスアカウントを自動生成します。このサービスアカウントに Spanner へのアクセス権を付与する必要があります。

#### ステップ 2: サービスアカウントへの権限付与

```bash
# サービスアカウント ID を取得
bq show --connection PROJECT_ID.REGION.CONNECTION_ID

# Cloud Spanner Database User ロールを付与
gcloud spanner databases add-iam-policy-binding DATABASE_ID \
  --instance=INSTANCE_ID \
  --member="serviceAccount:SERVICE_ACCOUNT_ID" \
  --role="roles/spanner.databaseUser"
```

サービスアカウントに `roles/spanner.databaseUser` ロールを付与することで、Spanner データベースへの書き込みが可能になります。

#### ステップ 3: 会話型分析の有効化

```bash
# Conversational Analytics API を有効化
gcloud services enable geminidataanalytics.googleapis.com

# Spanner Studio からデータエージェントを作成
# Google Cloud コンソール > Spanner > データベース > Spanner Studio
```

Spanner Studio でデータエージェントを作成し、ビジネスコンテキストやシステム指示を設定することで、自然言語クエリの精度を向上させることができます。

## メリット

### ビジネス面

- **データ民主化**: SQL の専門知識がないビジネスユーザーでも、会話型分析を通じて Spanner のオペレーショナルデータから直接インサイトを取得可能
- **リアルタイムアプリケーション提供**: BigQuery での分析結果をリバース ETL で Spanner に書き戻すことで、低レイテンシでアプリケーションユーザーにデータを提供可能
- **運用コスト削減**: カスタム ETL パイプラインの構築・保守が不要になり、マネージドサービスとして BigQuery-Spanner 間のデータ連携が実現

### 技術面

- **クエリパフォーマンス向上**: BigQuery のマテリアライズドビューにより、Spanner データに対する繰り返しクエリのパフォーマンスが大幅に向上
- **権限管理の簡素化**: CLOUD_RESOURCE 接続により、ユーザーに Spanner への直接アクセスを付与せずにリバース ETL を実行可能
- **双方向データフロー**: Spanner から BigQuery への分析 (フェデレーション) と BigQuery から Spanner へのリバース ETL により、完全な双方向データパイプラインが実現

## デメリット・制約事項

### 制限事項

- 会話型分析は Preview 段階であり、本番環境や個人データの処理には推奨されない
- 非増分マテリアライズドビューはスマートチューニング非対応のため、直接クエリする必要がある
- リバース ETL には Enterprise 以上の BigQuery リザベーションが必要
- 会話型分析の QueryData メソッドは GoogleSQL for Spanner のみ対応 (PostgreSQL インターフェースは非対応)
- 非増分マテリアライズドビューは全体リフレッシュが必要であり、大規模データの場合はリフレッシュコストが高くなる可能性がある

### 考慮すべき点

- 会話型分析は AI ベースの機能であるため、生成された回答の正確性を検証することが推奨される
- リバース ETL で同一行キーの複数行をエクスポートする場合、Spanner では単一行にマージされ、どの BigQuery 行が採用されるかは保証されない
- マテリアライズドビューの `max_staleness` 間隔を超えてリフレッシュが行われなかった場合、クエリは基底の Spanner 外部データセットテーブルを直接読み取る
- エージェントコンテキストはデータベースへの読み取りアクセスを持つ全ユーザーに表示される点に注意 (ファイングレインドアクセスコントロール利用時)

## ユースケース

### ユースケース 1: 小売業の在庫分析と補充最適化

**シナリオ**: 小売企業が Spanner で管理している在庫データを BigQuery で分析し、補充の最適化結果を Spanner に書き戻してリアルタイムの在庫管理アプリケーションに反映する。

**実装例**:
```sql
-- BigQuery で補充推奨を計算
CREATE TABLE analytics_dataset.replenishment_recommendations AS
SELECT
  product_id,
  store_id,
  recommended_quantity,
  priority_score
FROM analytics_dataset.inventory_analysis
WHERE recommended_quantity > 0;

-- リバース ETL で Spanner に書き戻し
EXPORT DATA
  WITH CONNECTION `my_project.us-central1.spanner_conn`
  OPTIONS (
    uri = "https://spanner.googleapis.com/projects/my_project/instances/retail/databases/inventory",
    format = 'CLOUD_SPANNER',
    spanner_options = """{"table": "ReplenishmentOrders"}"""
  )
AS SELECT * FROM analytics_dataset.replenishment_recommendations;
```

**効果**: カスタム ETL パイプラインを構築することなく、BigQuery の分析結果をアプリケーション層にリアルタイムで反映可能。

### ユースケース 2: 経営層によるセルフサービス分析

**シナリオ**: 経営層が SQL を書くことなく、自然言語で「先月の売上トップ 10 の商品は？」「前年比で最も成長した地域は？」といった質問を Spanner のオペレーショナルデータに対して行う。

**効果**: データチームへの分析依頼の待ち時間を削減し、意思決定の迅速化を実現。Conversational Analytics API のデータエージェントにビジネスコンテキスト (用語定義や KPI 定義) を設定することで、精度の高い回答を得ることができる。

### ユースケース 3: 定期的なレポート用キャッシュの構築

**シナリオ**: BI ダッシュボードが Spanner のトランザクションデータを頻繁にクエリしており、オペレーショナル負荷が懸念される場合、BigQuery のマテリアライズドビューでクエリ結果をキャッシュする。

**実装例**:
```sql
CREATE MATERIALIZED VIEW reporting_dataset.daily_sales_summary
OPTIONS (
  enable_refresh = true,
  refresh_interval_minutes = 30,
  max_staleness = INTERVAL "2" HOUR,
  allow_non_incremental_definition = true
)
AS SELECT
  DATE(order_timestamp) AS order_date,
  region,
  SUM(total_amount) AS daily_total,
  COUNT(*) AS order_count
FROM spanner_external_dataset.orders
GROUP BY order_date, region;
```

**効果**: Spanner への直接クエリ負荷を軽減しつつ、許容可能なデータ鮮度で高速なレポートクエリを実現。

## 料金

各機能の料金体系は以下のとおりです。

### 料金例

| 項目 | 料金 |
|------|------|
| Spanner コンピューティング (リージョナル) | $0.90/ノード/時間 (オンデマンド) |
| Spanner ストレージ (SSD) | $0.30/GB/月 |
| Conversational Analytics API | Preview 期間中は無料 |
| BigQuery リザベーション (Enterprise) | $0.0625/スロット/時間 |
| BigQuery ストレージ | $0.02/GB/月 (アクティブ) |
| Data Boost (マテリアライズドビュー利用時) | Spanner Data Boost の料金が適用 |

Spanner の CUD (確約利用割引) を利用すると、1 年契約で 20%、3 年契約で 40% の割引が適用されます。リバース ETL の実行にはベースラインスロット容量をゼロに設定してオートスケーリングを有効にすることで、コストを最適化できます。

## 利用可能リージョン

- **Spanner**: 全てのリージョナル、デュアルリージョン、マルチリージョン構成で利用可能
- **会話型分析 (Preview)**: Conversational Analytics API のサポートリージョンに依存
- **リバース ETL / マテリアライズドビュー**: BigQuery と Spanner の両方がサポートするリージョンで利用可能。CLOUD_RESOURCE 接続は BigQuery リソースと同じリージョンに配置する必要あり

## 関連サービス・機能

- **BigQuery**: Spanner データのフェデレーションクエリ、マテリアライズドビュー、リバース ETL のソースとして使用。Spanner 外部データセットを通じてシームレスに連携
- **Conversational Analytics API**: Gemini を活用した自然言語クエリエンジン。Spanner の他に AlloyDB、Cloud SQL、BigQuery、Looker にも対応
- **Gemini for Google Cloud**: 会話型分析の推論エンジンとして使用。ユーザーの自然言語を解釈し、SQL クエリを生成
- **Spanner Data Boost**: BigQuery からの Spanner データ読み取り時に使用される計算リソース。オペレーショナルワークロードへの影響を最小化
- **Cloud リソース接続**: BigQuery と外部サービス間の安全な接続を提供。リバース ETL とマテリアライズドビューの両方で使用

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260330-spanner-conversational-analytics-reverse-etl.html)
- [公式リリースノート](https://docs.google.com/release-notes#March_30_2026)
- [Conversational Analytics for Spanner 概要](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics/spanner)
- [Conversational Analytics API ドキュメント](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/overview)
- [BigQuery から Spanner へのリバース ETL](https://docs.cloud.google.com/bigquery/docs/export-to-spanner)
- [BigQuery マテリアライズドビューの作成](https://docs.cloud.google.com/bigquery/docs/materialized-views-create)
- [Spanner エディション概要](https://docs.cloud.google.com/spanner/docs/editions-overview)
- [Spanner 料金ページ](https://cloud.google.com/spanner/pricing)

## まとめ

今回のアップデートにより、Spanner と BigQuery の間のデータフローが大幅に強化されました。会話型分析 (Preview) によるデータ民主化、BigQuery マテリアライズドビュー (GA) によるクエリパフォーマンス向上、リバース ETL (GA) による双方向データパイプラインの実現は、特にオペレーショナルデータベースと分析基盤を統合的に活用するユーザーにとって大きな価値をもたらします。まずはリバース ETL とマテリアライズドビューの GA 機能を本番環境で活用し、会話型分析については Preview で評価を開始することを推奨します。

---

**タグ**: #Spanner #BigQuery #ConversationalAnalytics #ReverseETL #MaterializedViews #GA #Preview #Gemini #DataAnalytics
