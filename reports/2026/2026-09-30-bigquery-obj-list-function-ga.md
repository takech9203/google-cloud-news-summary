# BigQuery: OBJ.LIST 関数が一般提供 (GA)

**リリース日**: 2026-09-30

**サービス**: BigQuery

**機能**: OBJ.LIST 関数による非構造化データの即時的な発見と分析

**ステータス**: GA (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260930-bigquery-obj-list-function-ga.html)

## 概要

BigQuery の `OBJ.LIST` 関数が一般提供 (GA) になりました。`OBJ.LIST` 関数は、Cloud Storage に保存されたファイルのメタデータと ObjectRef 値のテーブルを返す関数で、非構造化データの即時的な発見と分析 (spontaneous discovery and analysis) を可能にします。対象となる Cloud Storage のデータには、ドキュメント、画像、音声などが含まれ、すべての Cloud Storage ストレージクラスのオブジェクトを発見できます。

これまで Cloud Storage 上の非構造化データを BigQuery から参照するには、永続的なオブジェクトテーブルを作成するか、ObjectRef 値を手動で構築する必要がありました。`OBJ.LIST` を使うと、永続テーブルを作成することなく、SQL クエリの中で直接 Cloud Storage のオブジェクト一覧とメタデータを取得できます。返される ObjectRef 値はそのまま `AI.GENERATE` や `AI.IF` などの AI 関数に渡せるため、非構造化データを構造化データへ変換する ETL パイプラインを素早く構築できます。

データアナリストやデータエンジニアが、Cloud Storage 上の画像・PDF・音声ファイルなどをアドホックに探索し、生成 AI 関数と組み合わせて分析するユースケースに適しています。

**アップデート前の課題**

- Cloud Storage 上のオブジェクトを BigQuery から参照するには、`CREATE EXTERNAL TABLE` で永続的なオブジェクトテーブルを事前に作成する必要があった
- ObjectRef 値を利用するには、オブジェクトテーブルを使うか `OBJ.MAKE_REF` 関数で手動で構築する必要があった
- アドホックな探索・分析のためだけにテーブル定義を管理するのは手間がかかった

**アップデート後の改善**

- 永続的なオブジェクトテーブルを作成せずに、クエリ内で直接 Cloud Storage オブジェクトのメタデータと ObjectRef 値を取得できるようになった
- ObjectRef 値を手動で構築する必要がなくなり、Cloud Storage オブジェクトを AI 関数へ素早く渡して、非構造化データを構造化データへ変換する ETL パイプラインを構築できるようになった
- ワイルドカード (`*`) により特定のファイル種別 (例: `*.pdf`) に絞った即時的な発見が可能になった

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph GCS["🪣 Cloud Storage"]
        OBJ["📄 ドキュメント / 🖼️ 画像 / 🎙️ 音声<br>(全ストレージクラス)"]
    end

    subgraph BQ["🔷 BigQuery"]
        LIST["🔍 OBJ.LIST('gs://bucket/*.png')"]
        META[("📋 メタデータテーブル<br>uri / content_type / size /<br>updated / generation / ref")]
        AI["🤖 AI 関数<br>AI.GENERATE / AI.IF"]
        RESULT[("📊 構造化データ")]
    end

    USER(["👤 アナリスト"]) -->|SQL クエリ| LIST
    OBJ -->|メタデータ取得| LIST
    LIST --> META
    META -->|ObjectRef (ref 列)| AI
    AI --> RESULT
```

`OBJ.LIST` は Cloud Storage オブジェクトのメタデータと ObjectRef 値のテーブルを動的に生成し、永続テーブルなしで AI 関数と組み合わせた非構造化データ分析パイプラインを実現します。

## サービスアップデートの詳細

### 主要機能

1. **非構造化データの即時的な発見 (spontaneous discovery)**
   - `OBJ.LIST(uri [, authorizer])` の形式で、Cloud Storage 上のオブジェクトのメタデータと ObjectRef 値をテーブルとして返す
   - ドキュメント、画像、音声などを対象とし、すべての Cloud Storage ストレージクラスのオブジェクトを発見できる
   - 永続的なオブジェクトテーブルの作成が不要

2. **ワイルドカードによるフィルタリング**
   - 各パスで 1 つのアスタリスク (`*`) ワイルドカードを使用して対象オブジェクトを絞り込める
   - 例: `gs://bucket_name/*.pdf` で PDF オブジェクトのみを一覧化

3. **AI 関数とのシームレスな連携**
   - 出力テーブルの `ref` 列 (ObjectRef 値) を `AI.GENERATE` や `AI.IF` などの OBJ / AI 関数へそのまま渡せる
   - 非構造化データを構造化データへ変換する ETL パイプラインを素早く構築できる

4. **アクセス制御の選択**
   - `authorizer` 引数に Cloud Resource 接続を指定すると委任アクセス (delegated access) になる
   - `authorizer` を省略した場合、返される ObjectRef は直接アクセス (direct access) を使用する

## 技術仕様

### 関数定義

| 項目 | 詳細 |
|------|------|
| 構文 | `OBJ.LIST(uri [, authorizer])` |
| `uri` | Cloud Storage オブジェクトの URI を含む STRING 値 (例: `gs://mybucket/flowers/12345.jpg`)。スカラーサブクエリや `CONCAT` などの文字列操作関数は非対応。各パスで 1 つの `*` ワイルドカードを使用可能 |
| `authorizer` | 委任アクセスに使用する Cloud Resource 接続を含む STRING 値 (省略時は直接アクセス) |
| 出力 | Cloud Storage で見つかったオブジェクトを表すメタデータのテーブル |

### 出力テーブルの列

| 列名 | 型 | 説明 |
|------|-----|------|
| `uri` | STRING | オブジェクトの Cloud Storage URI |
| `content_type` | STRING | オブジェクトの MIME タイプ (例: `image/jpeg`、`application/pdf`) |
| `size` | INT64 | オブジェクトのサイズ (バイト) |
| `md5_hash` | STRING | オブジェクトの MD5 ハッシュ |
| `updated` | TIMESTAMP | オブジェクトの最終更新時刻 |
| `metadata` | ARRAY<STRUCT<name STRING, value STRING>> | 追加の Cloud Storage メタデータ |
| `generation` | INT64 | オブジェクトのバージョンを識別する値 (Object Versioning の使用有無にかかわらず全オブジェクトに存在) |
| `ref` | ObjectRef | オブジェクトを表す ObjectRef 値。他の OBJ 関数や AI 関数に渡せる |

## 設定方法

### 前提条件

1. 分析対象のオブジェクトが保存された Cloud Storage バケットがあること
2. 直接アクセスの場合は、クエリ実行者が対象オブジェクトへのアクセス権を持つこと。委任アクセスの場合は、データ管理者が [Cloud Resource 接続](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection)の権限を設定していること

### 手順

#### ステップ 1: OBJ.LIST でオブジェクトを一覧化

```sql
-- 直接アクセスで PNG ファイルのメタデータを一覧化
SELECT uri, content_type, size
FROM OBJ.LIST('gs://mybucket/images/*.png')
ORDER BY uri;
```

永続テーブルを作成せずに、指定したパスのオブジェクトのメタデータと ObjectRef 値を取得します。

#### ステップ 2: AI 関数と組み合わせて分析

```sql
-- 犬の画像が含まれる PNG ファイルのみを一覧化
SELECT uri, content_type, size
FROM OBJ.LIST('gs://mybucket/images/*.png')
WHERE AI.IF(('Does this image contain a dog?', ref))
ORDER BY uri;
```

`ref` 列を `AI.IF` などの AI 関数に渡すことで、非構造化データの内容に基づくフィルタリングや分析ができます。

## メリット

### ビジネス面

- **分析の迅速化**: テーブル定義や事前準備なしに、Cloud Storage 上の非構造化データをその場で発見・分析でき、インサイト獲得までの時間を短縮できる
- **運用負荷の軽減**: アドホックな探索のためだけに永続的なオブジェクトテーブルを作成・管理する必要がなくなる

### 技術面

- **ObjectRef 構築の自動化**: ObjectRef 値を手動で構築する必要がなくなり、AI 関数への受け渡しが簡素化される
- **ETL パイプラインの迅速な構築**: Cloud Storage オブジェクトを AI 関数へ素早く取り込み、非構造化データから構造化データへの変換パイプラインを構築できる
- **柔軟なアクセス制御**: `authorizer` 引数の有無により、直接アクセスと委任アクセスを使い分けられる

## デメリット・制約事項

### 制限事項

- 末尾がスラッシュの URI (例: `gs://mybucket/flowers/`) や、連続するスラッシュを含む URI (例: `gs://mybucket/flowers//12345.jpg`) はエラーになる
- `uri` 引数でスカラーサブクエリや `CONCAT` などの文字列操作関数は使用できない
- ワイルドカード (`*`) は各パスで 1 つのみ使用可能
- `OBJ.LIST` はオブジェクトメタデータを動的に生成するため、オブジェクトテーブルと同様の基盤的な動作・制限を共有する
- BigQuery 接続を使用する場合、接続のロケーションとクエリのロケーションは Cloud Storage バケットのリージョンと互換性がある必要がある
- Cloud Storage データへのアクセスは、組織の VPC Service Controls の境界 (perimeter) に従う

### 考慮すべき点

- バケットに継続的に到着する新規オブジェクトを追跡する、永続的で自己更新型のテーブルが必要な場合は、`OBJ.LIST` ではなく標準の [BigQuery オブジェクトテーブル](https://docs.cloud.google.com/bigquery/docs/object-table-introduction)を作成するべき
- `OBJ.LIST` 自体はメタデータのみを処理するが、返された ObjectRef を `AI.GENERATE` や `AI.IF` などのファイル内容を読み取る下流の AI 関数へ渡すと、その処理分のコストが発生する

## ユースケース

### ユースケース 1: 画像コンテンツに基づくアドホックなフィルタリング

**シナリオ**: Cloud Storage バケットに保存された大量の画像から、特定の内容 (例: 犬が写っている画像) を含むものだけを即座に特定したい。

**実装例**:
```sql
SELECT uri, content_type, size
FROM OBJ.LIST('gs://mybucket/images/*.png')
WHERE AI.IF(('Does this image contain a dog?', ref))
ORDER BY uri;
```

**効果**: オブジェクトテーブルの作成や ObjectRef の手動構築なしに、画像の内容に基づくフィルタリングを 1 つの SQL クエリで実現できる。

### ユースケース 2: 複数画像の横断的な AI 分析

**シナリオ**: 商品画像群に共通するビジュアルテーマやブランディング要素を生成 AI で要約したい。

**実装例**:
```sql
WITH product_images AS (
  SELECT ref
  FROM OBJ.LIST('gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/*.png')
  LIMIT 3
)
SELECT AI.GENERATE(
  ('What are the common visual themes or branding elements across these pet products?',
   ARRAY_AGG(ref))
).result AS comparison_summary
FROM product_images;
```

**効果**: Cloud Storage 上の画像を即時に発見し、`AI.GENERATE` と組み合わせて複数オブジェクトの横断分析を SQL のみで実行できる。

## 料金

公式ドキュメント ([マルチモーダルデータの分析](https://docs.cloud.google.com/bigquery/docs/analyze-multimodal-data)) によると、マルチモーダルデータ利用時のコストは以下のとおりです。

- `OBJ.LIST` などの OBJ 関数はメタデータのみを処理し、ファイルの中身 (バイト) は読み取らない
- 返された ObjectRef を `AI.GENERATE` や `AI.IF` などのファイル内容を読み取る下流の AI 関数に渡した時点でコストが発生する
- ObjectRef 値に対して実行するクエリには BigQuery のコンピューティング料金が発生する
- 生成 AI 関数の使用時には Gemini Enterprise Agent Platform の料金が発生する

詳細は [BigQuery の料金ページ](https://cloud.google.com/bigquery/pricing)を参照してください。

## 利用可能リージョン

リージョン別の提供状況は公式ドキュメントで明示されていませんが、BigQuery 接続を使用する場合、接続のロケーションとクエリのロケーションが Cloud Storage バケットのリージョンと互換性がある必要があります。詳細は [ObjectRef 関数のドキュメント](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions)を参照してください。

## 関連サービス・機能

- **Cloud Storage**: `OBJ.LIST` の発見対象となる非構造化データ (ドキュメント、画像、音声) の保存先。すべてのストレージクラスのオブジェクトを発見できる
- **BigQuery オブジェクトテーブル**: バケットへ継続的に到着する新規オブジェクトを追跡する、永続的で自己更新型のテーブルが必要な場合の選択肢
- **OBJ.MAKE_REF 関数**: テーブルに保存済みの URI から ObjectRef 値を作成する場合に使用する関数
- **AI 関数 (AI.GENERATE / AI.IF など)**: `OBJ.LIST` が返す `ref` 列 (ObjectRef) を渡して、非構造化データの内容を分析・変換できる
- **Cloud Storage Insights データセット**: ObjectRef 値を含む `ref` 列を持つ、Cloud Storage データ分析用のリンク済み BigQuery データセット
- **VPC Service Controls**: Cloud Storage データへのアクセスを統制するセキュリティ境界

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260930-bigquery-obj-list-function-ga.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#September_30_2026)
- [ObjectRef 関数リファレンス (OBJ.LIST)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions)
- [ObjectRef 値の操作](https://docs.cloud.google.com/bigquery/docs/work-with-objectref)
- [マルチモーダルデータの分析](https://docs.cloud.google.com/bigquery/docs/analyze-multimodal-data)
- [オブジェクトテーブルの概要](https://docs.cloud.google.com/bigquery/docs/object-table-introduction)
- [料金ページ](https://cloud.google.com/bigquery/pricing)

## まとめ

`OBJ.LIST` 関数の GA により、永続的なオブジェクトテーブルを作成することなく、Cloud Storage 上の非構造化データを SQL だけで即時に発見し、AI 関数と組み合わせて分析できるようになりました。アドホックな探索には `OBJ.LIST`、継続的な新規オブジェクト追跡にはオブジェクトテーブルという使い分けを押さえた上で、画像・ドキュメント・音声を対象とするマルチモーダル分析パイプラインの構築を検討することを推奨します。

---

**タグ**: BigQuery, OBJ.LIST, ObjectRef, Cloud Storage, 非構造化データ, マルチモーダル, AI 関数, GA
