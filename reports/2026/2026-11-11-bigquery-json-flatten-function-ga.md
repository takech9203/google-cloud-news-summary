# BigQuery: JSON_FLATTEN 関数が一般提供 (GA) に

**リリース日**: 2026-11-11

**サービス**: BigQuery

**機能**: JSON_FLATTEN 関数 (ネストされた JSON 配列のフラット化)

**ステータス**: GA (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261111-bigquery-json-flatten-function-ga.html)

## 概要

BigQuery の GoogleSQL に用意されている `JSON_FLATTEN` 関数が一般提供 (GA) になりました。この関数は、入力 JSON 値の中に直接含まれる非配列値、または連続してネストされた 1 つ以上の配列の子要素である非配列値をすべて抽出し、`ARRAY<JSON>` 型として返します。これにより、深さの異なるネスト構造を持つ JSON 配列を 1 回の関数呼び出しでフラット化できます。

JSON 関数カテゴリの中では「Transformers (変換系)」に分類される関数で、ログデータや API レスポンスなど、配列のネスト深度が一定でない半構造化データを扱うデータエンジニアやアナリストにとって有用な機能です。GA 化により、Pre-GA Offerings Terms の制約がなくなり、本番ワークロードで安心して利用できるようになりました。

**アップデート前の課題**

- `JSON_FLATTEN` は従来 Preview (Pre-GA) として提供されており、Pre-GA Offerings Terms が適用され、サポートも限定的で本番利用には向かなかった
- 標準の抽出関数 (`JSON_QUERY_ARRAY` など) は 1 階層の配列抽出が基本であり、ネスト深度が不揃いな配列 (例: `[[[1]], 2, [3]]`) を平坦化するには、JSONPath の `lax recursive` モードの利用や `UNNEST` の多段組み合わせなど、複雑なクエリの工夫が必要だった

**アップデート後の改善**

- `JSON_FLATTEN` が GA となり、SLA の対象として本番環境のクエリやパイプラインで利用できるようになった
- ネスト深度が異なる配列要素を含む JSON 値を、単一の関数呼び出しで `ARRAY<JSON>` にフラット化できる
- 返り値は `ARRAY<JSON>` のため、`UNNEST` と組み合わせて行展開し、`LAX_INT64` や `JSON_VALUE` などの関数でそのまま後続処理につなげられる

## アーキテクチャ図

```mermaid
flowchart LR
    A[📄 半構造化データ<br>JSON '[[[1, 2], 3], {&quot;a&quot;: 4}, true]'] --> B[🔧 JSON_FLATTEN]
    B --> C[📦 ARRAY&lt;JSON&gt;<br>[1, 2, 3, {&quot;a&quot;: 4}, true]]
    C --> D[🔄 UNNEST で行展開]
    D --> E[🔀 LAX_INT64 / JSON_VALUE<br>などで型変換]
    E --> F[(📊 BigQuery<br>分析・集計)]
```

ネストされた JSON 配列を `JSON_FLATTEN` で `ARRAY<JSON>` にフラット化し、`UNNEST` と変換関数を通じて通常の SQL 分析に接続するデータ変換フローです。

## サービスアップデートの詳細

### 主要機能

1. **連続ネスト配列のフラット化**
   - 入力 JSON 値に直接含まれる非配列値と、連続してネストされた配列の子要素である非配列値をすべて抽出する
   - 例: `JSON_FLATTEN(JSON '[[[1]], 2, [3]]')` は `[1, 2, 3]` を返す
   - ネスト深度が要素ごとに異なっていても、1 回の呼び出しで平坦化できる

2. **非配列値の配列化**
   - 入力がスカラー値の場合も要素数 1 の配列として返す
   - 例: `JSON_FLATTEN(JSON '1')` は `[1]` を返す

3. **JSON オブジェクト境界の尊重**
   - フラット化は「連続した配列のネスト」のみを対象とし、JSON オブジェクトに包まれた配列は展開しない
   - 例: `JSON_FLATTEN(JSON '{"a": [[1]]}')` は `[{"a":[[1]]}]` を返し、オブジェクト内部の配列はそのまま保持される

## 技術仕様

### 関数仕様

| 項目 | 詳細 |
|------|------|
| 構文 | `JSON_FLATTEN(json_expr)` |
| 引数 | `json_expr`: `JSON` 型 (例: `JSON '["Jane", ["John", "Jamie"]]'`) |
| 返り値型 | `ARRAY<JSON>` |
| NULL の扱い | `json_expr` が SQL `NULL` の場合、関数は SQL `NULL` を返す。配列内の JSON `null` は要素として保持される (例: `JSON_FLATTEN(JSON '[1, 2, null]')` → `[1, 2, null]`) |
| 分類 | JSON 関数のうち Transformers (変換系) カテゴリ |

### クエリ例

```sql
-- ネスト深度が不揃いな配列のフラット化
SELECT JSON_FLATTEN(JSON '[[[1, 2], 3], {"a": 4}, true]') AS json_flatten;
/*---------------------------+
 | json_flatten              |
 +---------------------------+
 | [1, 2, 3, {"a": 4}, true] |
 +---------------------------*/

-- JSON オブジェクト内の配列は展開されない
SELECT JSON_FLATTEN(JSON '{"a": [[1]]}') AS json_flatten;
/*---------------+
 | json_flatten  |
 +---------------+
 | [{"a":[[1]]}] |
 +---------------*/
```

## 設定方法

### 前提条件

1. BigQuery が有効化された Google Cloud プロジェクト
2. 入力が `JSON` 型であること (文字列の場合は `PARSE_JSON` で変換する)

### 手順

#### ステップ 1: JSON 型データに対して JSON_FLATTEN を実行

```sql
SELECT JSON_FLATTEN(JSON '[1, [2, 3], [[4]]]') AS flattened;
-- 結果: [1, 2, 3, 4]
```

GoogleSQL のクエリ内でそのまま呼び出せます。追加の設定や API の有効化は不要です。

#### ステップ 2: UNNEST と組み合わせて行展開・型変換

```sql
SELECT LAX_INT64(elem) AS value
FROM UNNEST(JSON_FLATTEN(JSON '[[[1, 2], 3], [4]]')) AS elem;
-- 各要素を 1 行ずつ INT64 として取得
```

返り値が `ARRAY<JSON>` のため、`UNNEST` で行展開し、`LAX_INT64` や `JSON_VALUE` などで SQL 型に変換して後続の分析に利用できます。

## メリット

### ビジネス面

- **本番利用の解禁**: GA 化により Pre-GA Offerings Terms の制約がなくなり、本番のデータパイプラインやレポーティングに組み込める
- **開発工数の削減**: ネスト構造を解きほぐすための複雑なクエリや前処理 (ETL) の実装・保守コストを削減できる

### 技術面

- **クエリの簡素化**: `lax recursive` JSONPath モードや多段 `UNNEST` を駆使していた不揃いなネスト配列の処理を、単一関数で宣言的に記述できる
- **堅牢性**: ネスト深度がレコードごとに変動するデータでも同一クエリで処理でき、スキーマ変動に強いパイプラインを構築できる

## デメリット・制約事項

### 制限事項

- フラット化の対象は「連続してネストされた配列」のみで、JSON オブジェクト内に包まれた配列は展開されない (オブジェクト内部まで再帰的に展開したい場合は、別途パス指定による抽出が必要)
- 入力は `JSON` 型のみ。JSON 形式の `STRING` に対しては `PARSE_JSON` による変換が先に必要

### 考慮すべき点

- 返り値は `ARRAY<JSON>` であり、各要素は JSON 型のまま。数値・文字列として扱うには `LAX_INT64` / `JSON_VALUE` などによる明示的な変換が必要
- 既に Preview 版の `JSON_FLATTEN` を利用している場合、GA 化に伴う構文変更はないため、そのまま利用を継続できる

## ユースケース

### ユースケース 1: ネスト深度が不揃いな API レスポンスの正規化

**シナリオ**: 外部 API から取得した JSON レスポンスに、バージョンやレコードにより配列のネスト深度が異なるフィールド (例: タグやカテゴリのリスト) が含まれており、BigQuery で一律に集計したい。

**実装例**:
```sql
SELECT
  id,
  JSON_VALUE(tag) AS tag
FROM
  events,
  UNNEST(JSON_FLATTEN(JSON_QUERY(payload, '$.tags'))) AS tag;
```

**効果**: ネスト深度のばらつきを意識せずにタグを行展開でき、前処理用の中間テーブルや UDF が不要になる。

### ユースケース 2: ログデータの値のフラット抽出

**シナリオ**: アプリケーションログの JSON ペイロードに多段配列で格納されたメトリクス値を、分析用にフラットな行形式へ変換する。

**効果**: `JSON_FLATTEN` + `UNNEST` の組み合わせだけでフラット化が完結し、クエリの可読性と保守性が向上する。

## 料金

`JSON_FLATTEN` は GoogleSQL の組み込み関数であり、関数自体への追加料金はありません。通常の BigQuery クエリ料金 (オンデマンドのスキャン量課金、またはエディションのスロット課金) が適用されます。詳細は料金ページを参照してください。

- [BigQuery 料金ページ](https://cloud.google.com/bigquery/pricing)

## 利用可能リージョン

リージョン固有の制限はリリースノートおよびドキュメントに記載されていません。BigQuery の GoogleSQL 関数として利用できます。

## 関連サービス・機能

- **JSON_QUERY / JSON_QUERY_ARRAY**: JSONPath を使って特定パスの値や配列を抽出する標準抽出関数。`JSON_FLATTEN` の入力を切り出す前処理として併用できる
- **JSONPath の lax / lax recursive モード**: 抽出時に配列を自動アンラップするモード。特定パスの抽出には lax recursive、値全体のフラット化には `JSON_FLATTEN` と使い分けられる
- **LAX_INT64 / LAX_STRING などの Lax コンバータ**: `JSON_FLATTEN` の返す JSON 要素を SQL 型へ柔軟に変換する関数
- **PARSE_JSON / TO_JSON**: `STRING` と `JSON` 型の相互変換。文字列で保存された JSON データを `JSON_FLATTEN` に渡す際に使用

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261111-bigquery-json-flatten-function-ga.html)
- [公式リリースノート (2026-11-11)](https://docs.cloud.google.com/release-notes#November_11_2026)
- [JSON 関数リファレンス - JSON_FLATTEN](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_flatten)
- [BigQuery 料金ページ](https://cloud.google.com/bigquery/pricing)

## まとめ

ネスト深度の不揃いな JSON 配列を単一関数でフラット化できる `JSON_FLATTEN` が GA となり、本番ワークロードで利用可能になりました。半構造化データの前処理クエリを簡素化できるため、`lax recursive` モードや多段 `UNNEST` で配列展開を実装している場合は、`JSON_FLATTEN` への置き換えを検討することをおすすめします。

---

**タグ**: #BigQuery #JSON #GoogleSQL #DataAnalytics #GA
