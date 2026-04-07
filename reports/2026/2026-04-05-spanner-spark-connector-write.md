# Spanner: Spark Spanner コネクタによる DataFrame の書き込みサポート

**リリース日**: 2026-04-05

**サービス**: Spanner

**機能**: Spark Spanner コネクタによる DataFrame の書き込みサポート

**ステータス**: Feature

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260405-spanner-spark-connector-write.html)

## 概要

Spark Spanner コネクタに、Spark DataFrame を Spanner テーブルに書き込む機能が追加されました。これにより、Spark data source API を使用して、Apache Spark で処理したデータを直接 Cloud Spanner に保存できるようになります。

これまで Spark Spanner コネクタは Spanner テーブルやグラフからの読み取り (Read) のみをサポートしていましたが、今回のアップデートで書き込み (Write) が可能になり、双方向のデータ連携が実現しました。Dataproc クラスタ上で動作する Spark ジョブから、ETL パイプラインの最終段階として Spanner に直接データを投入するワークフローが構築できます。

対象ユーザーは、Dataproc と Spanner を組み合わせたデータパイプラインを構築するデータエンジニアや、Spark ベースの分析基盤から Spanner にデータを反映させたい開発者です。

**アップデート前の課題**

- Spark Spanner コネクタは読み取り専用であり、Spark で処理した結果を Spanner に書き戻すにはカスタムコードや別の手段が必要だった
- Spark の分析結果を Spanner に反映するには、Spanner クライアントライブラリを直接使用する追加実装が必要だった
- 読み取りと書き込みで異なるインターフェースを使い分ける必要があり、パイプラインの複雑性が増していた

**アップデート後の改善**

- Spark data source API の標準的な `df.write.format('cloud-spanner')` 構文で Spanner テーブルへの書き込みが可能になった
- 読み取りと書き込みの両方を同一コネクタで統一的に扱えるようになり、パイプライン設計がシンプルになった
- PySpark および Scala から同じインターフェースで書き込みが可能

## アーキテクチャ図

```mermaid
flowchart LR
    A["データソース<br/>(CSV, Parquet, DB など)"] --> B["Spark DataFrame<br/>(Dataproc クラスタ)"]
    B --> C["データ変換・加工<br/>(Spark SQL / DataFrame API)"]
    C --> D["Spark Spanner コネクタ<br/>(cloud-spanner format)"]
    D --> E["Cloud Spanner<br/>テーブル"]

    style A fill:#E3F2FD,stroke:#1565C0
    style B fill:#FFF3E0,stroke:#E65100
    style C fill:#FFF3E0,stroke:#E65100
    style D fill:#E8F5E9,stroke:#2E7D32
    style E fill:#E8EAF6,stroke:#283593
```

Spark DataFrame で読み込み・加工したデータが、Spark Spanner コネクタを経由して Cloud Spanner テーブルに書き込まれるデータフローを示しています。

## サービスアップデートの詳細

### 主要機能

1. **Spark data source API による書き込み**
   - `df.write.format('cloud-spanner')` を使用して、標準的な Spark の書き込み API で Spanner テーブルにデータを保存
   - `mode("append")` による追記書き込みをサポート

2. **接続パラメータの指定**
   - `projectId`、`instanceId`、`databaseId`、`table` の各オプションで書き込み先の Spanner テーブルを指定
   - 読み取り時と同様のパラメータ体系で統一的に利用可能

3. **PySpark および Scala のサポート**
   - Python (PySpark) と Scala の両方から同じインターフェースで書き込みが可能
   - Dataproc ジョブとしての実行、および spark-submit による実行の両方に対応

## 技術仕様

### コネクタの仕様

| 項目 | 詳細 |
|------|------|
| コネクタ形式 | `cloud-spanner` |
| 対応 Spark バージョン | 3.1 以降 |
| コネクタ JAR の場所 | `gs://spark-lib/spanner/spark-3.1-spanner-CONNECTOR_VERSION.jar` |
| 対応言語 | PySpark, Scala |
| 書き込みモード | `append` |
| ソースコード | [GitHub: GoogleCloudDataproc/spark-spanner-connector](https://github.com/GoogleCloudDataproc/spark-spanner-connector) |

### 書き込みオプション

| オプション | 説明 | 必須 |
|-----------|------|------|
| `projectId` | Google Cloud プロジェクト ID | はい |
| `instanceId` | Spanner インスタンス ID | はい |
| `databaseId` | Spanner データベース ID | はい |
| `table` | 書き込み先テーブル名 | はい |

## 設定方法

### 前提条件

1. Dataproc クラスタ (イメージバージョン 2.1 以降) が作成済みであること
2. 書き込み先の Spanner インスタンスおよびデータベース、テーブルが作成済みであること
3. Compute Engine デフォルトサービスアカウントに以下の IAM ロールが付与されていること:
   - `roles/dataproc.worker` (Dataproc Worker)
   - `roles/spanner.databaseUser` (Cloud Spanner Database User)

### 手順

#### ステップ 1: PySpark スクリプトの作成

```python
"""Spanner PySpark write example."""
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Spanner Write App').getOrCreate()

columns = ['id', 'name', 'email']
data = [
    (1, 'John Doe', 'john.doe@example.com'),
    (2, 'Jane Doe', 'jane.doe@example.com')
]

df = spark.createDataFrame(data, columns)

df.write.format('cloud-spanner') \
    .option("projectId", "PROJECT_ID") \
    .option("instanceId", "INSTANCE_ID") \
    .option("databaseId", "DATABASE_ID") \
    .option("table", "TABLE_NAME") \
    .mode("append") \
    .save()
```

`PROJECT_ID`、`INSTANCE_ID`、`DATABASE_ID`、`TABLE_NAME` を実際の値に置き換えてください。

#### ステップ 2: Dataproc ジョブの送信

```bash
gcloud dataproc jobs submit pyspark write_spanner.py \
    --cluster=CLUSTER_NAME \
    --region=REGION \
    --jars=gs://spark-lib/spanner/spark-3.1-spanner-CONNECTOR_VERSION.jar
```

`CONNECTOR_VERSION` には、[GitHub リリースページ](https://github.com/GoogleCloudDataproc/spark-spanner-connector/releases) から適切なバージョンを選択してください。

## メリット

### ビジネス面

- **データパイプラインの簡素化**: Spark での分析結果を直接 Spanner に書き込めるため、中間ストレージや追加の ETL ツールが不要になり、パイプラインの運用コストを削減できる
- **開発速度の向上**: 標準的な Spark API を使用するため、既存の Spark スキルを持つチームがすぐに活用可能

### 技術面

- **統一的な API**: 読み取りと書き込みの両方を `cloud-spanner` フォーマットで統一的に扱えるため、コードの一貫性が向上
- **Spark エコシステムとの統合**: Spark data source API 準拠のため、他の Spark コネクタと同様のパターンで利用可能

## デメリット・制約事項

### 制限事項

- Dataproc クラスタ上での実行が前提であり、ローカル環境での利用にはクラスタへの接続設定が必要
- 書き込み先の Spanner テーブルは事前に作成しておく必要がある

### 考慮すべき点

- 大量データの書き込み時は Spanner のスループットとノード数に応じたパフォーマンスチューニングが必要
- IAM ロール (`roles/spanner.databaseUser`) の付与が必要であり、最小権限の原則に基づいた権限管理を推奨

## ユースケース

### ユースケース 1: バッチ ETL パイプライン

**シナリオ**: Cloud Storage 上の大量の CSV / Parquet データを Spark で加工し、正規化・クレンジングした結果を Spanner のトランザクションテーブルに投入する。

**実装例**:
```python
# Cloud Storage からデータを読み込み
raw_df = spark.read.parquet("gs://my-bucket/raw-data/")

# データ加工
processed_df = raw_df.filter(raw_df.status == "active") \
    .select("user_id", "name", "email")

# Spanner に書き込み
processed_df.write.format('cloud-spanner') \
    .option("projectId", "my-project") \
    .option("instanceId", "my-instance") \
    .option("databaseId", "my-database") \
    .option("table", "Users") \
    .mode("append") \
    .save()
```

**効果**: 中間ストレージを経由せずに Spark の処理結果を直接 Spanner に格納できるため、パイプラインのレイテンシと複雑性が大幅に削減される。

### ユースケース 2: 機械学習の推論結果の保存

**シナリオ**: Spark MLlib で実行した推論結果 (スコアリング、分類結果など) を、アプリケーションが参照する Spanner テーブルに書き込み、リアルタイムサービングに活用する。

**効果**: 推論パイプラインと結果の永続化が単一の Spark ジョブ内で完結し、アプリケーション側から低レイテンシで推論結果を取得できる。

## 料金

Spark Spanner コネクタ自体に追加料金は発生しません。ただし、以下のサービスの利用料金が適用されます。

| サービス | 料金の考慮事項 |
|---------|---------------|
| Dataproc | クラスタのノード数・稼働時間に基づく料金 |
| Cloud Spanner | ノード数、ストレージ、読み取り/書き込みオペレーション数に基づく料金 |
| Cloud Storage | コネクタ JAR ファイルの取得に伴う最小限のネットワーク料金 |

## 関連サービス・機能

- **Dataproc**: Spark Spanner コネクタのランタイム環境として使用。Dataproc クラスタ上で Spark ジョブを実行
- **Cloud Spanner**: 書き込み先のフルマネージド分散リレーショナルデータベース
- **BigQuery**: 同様に Spanner との連携機能を持ち、BigQuery から Spanner へのデータエクスポート (EXPORT DATA) も GA で利用可能
- **Spanner Data Boost**: 読み取り時にメインインスタンスへの影響をほぼゼロにする機能。コネクタの読み取り側で `enableDataBoost` オプションとして利用可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260405-spanner-spark-connector-write.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#April_05_2026)
- [ドキュメント: Use the Spark Spanner connector](https://docs.cloud.google.com/dataproc/docs/tutorials/spanner-connector-spark-example#write-spanner-tables)
- [GitHub: spark-spanner-connector](https://github.com/GoogleCloudDataproc/spark-spanner-connector)
- [Spanner 料金ページ](https://cloud.google.com/spanner/pricing)
- [Dataproc 料金ページ](https://cloud.google.com/dataproc/pricing)

## まとめ

Spark Spanner コネクタに書き込み機能が追加されたことで、Dataproc 上の Spark ジョブから Spanner テーブルへのデータ投入が標準的な Spark API で可能になりました。これにより、読み取りと書き込みの双方向データ連携が統一的なインターフェースで実現し、ETL パイプラインの設計がよりシンプルになります。Dataproc と Spanner を組み合わせたデータパイプラインを運用しているチームは、既存の書き込みロジックをコネクタベースに移行することを検討してください。

---

**タグ**: #Spanner #Dataproc #Spark #SparkConnector #ETL #DataFrame #DataPipeline
