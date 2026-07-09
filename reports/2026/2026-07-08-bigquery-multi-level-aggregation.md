# BigQuery: マルチレベル集計 (Multi-level Aggregation) と Simba ODBC ドライバー更新

**リリース日**: 2026-07-08

**サービス**: BigQuery

**機能**: マルチレベル集計 (GoogleSQL) / Simba ODBC ドライバー更新

**ステータス**: Preview (マルチレベル集計) / GA (Simba ODBC ドライバー)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260708-bigquery-multi-level-aggregation.html)

## 概要

BigQuery の GoogleSQL において、集計関数を別の集計関数の引数として使用できる「マルチレベル集計 (Multi-level Aggregation)」機能が Preview として利用可能になりました。標準 SQL では集計関数のネストが許可されていないため、多段階の集計処理にはサブクエリが必要でしたが、この新機能により単一のクエリで簡潔に表現できるようになります。

また、BigQuery 向けの Simba ODBC ドライバーの最新バージョン (3.3.1.1001) が公開されました。このドライバーは、ODBC 接続を介して BigQuery にアクセスするための標準的な接続手段を提供します。

**アップデート前の課題**

- 多段階の集計処理 (例: 日次売上の合計を算出した後にその平均を計算) にはサブクエリや CTE を使った複雑なクエリ構造が必要だった
- クエリの可読性が低下し、メンテナンスが困難になるケースがあった
- サブクエリのネストにより、クエリの構造的複雑さが増大していた

**アップデート後の改善**

- 集計関数の引数に別の集計関数を直接記述でき、`GROUP BY` 修飾子で中間集計のグルーピングを指定可能になった
- サブクエリ不要で多段階集計を表現でき、クエリが大幅に簡潔化された
- コードの可読性とメンテナンス性が向上した

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph "従来のアプローチ (サブクエリ必須)"
        A1[元データ] --> B1[内部クエリ: GROUP BY で集計]
        B1 --> C1[中間結果テーブル]
        C1 --> D1[外部クエリ: さらに集計]
        D1 --> E1[最終結果]
    end

    subgraph "マルチレベル集計 (新機能)"
        A2[元データ] --> B2["AVG(SUM(revenue) GROUP BY DATE(time))"]
        B2 --> C2[内部集計: SUM で中間結果を計算]
        C2 --> D2[外部集計: AVG で最終結果を計算]
        D2 --> E2[最終結果]
    end
```

マルチレベル集計では、外部の集計関数に `GROUP BY` 修飾子を付与することで、内部の集計関数が中間グループごとに評価され、その結果が外部の集計関数に渡されます。

## サービスアップデートの詳細

### 主要機能

1. **マルチレベル集計 (Multi-level Aggregation)**
   - 集計関数の引数として別の集計関数を使用可能
   - 外部の集計関数に `GROUP BY` 句を付与して中間グルーピングを定義
   - 最大 2 レベルまでのネストをサポート (3 レベル以上はエラー)

2. **GROUP BY 修飾子**
   - 集計関数呼び出し内に `GROUP BY` 句を記述する新しい構文
   - 内部集計のグルーピングキーを明示的に指定
   - `DISTINCT` 句との併用もサポート

3. **Simba ODBC ドライバー v3.3.1.1001**
   - Windows (32-bit / 64-bit)、Linux、macOS に対応
   - BigQuery Storage Read API (High-Throughput API) をサポート
   - insightsoftware による開発・メンテナンス

## 技術仕様

### マルチレベル集計の構文

| 項目 | 詳細 |
|------|------|
| 構文 | `OUTER_AGG(INNER_AGG(expr) GROUP BY grouping_expr)` |
| 最大ネスト深度 | 2 レベル (外部 + 内部) |
| ステータス | Preview |
| サポート対象 | 関数引数、DISTINCT 句、GROUP BY 修飾子 |

### 制約事項の詳細

| 制約 | 説明 |
|------|------|
| HAVING MAX/MIN | GROUP BY 句と併用不可 |
| ORDER BY / LIMIT | マルチレベル集計関数内では使用不可 |
| IGNORE/RESPECT NULLS | マルチレベル集計関数内では使用不可 |
| PIVOT 演算子 | マルチレベル集計関数は使用不可 |
| 差分プライバシー | マルチレベル集計と併用不可 |
| 集計しきい値句 | マルチレベル集計と併用不可 |
| 連続クエリ | マルチレベル集計と併用不可 |
| 照合順序付きキー | マルチレベル集計のグルーピングキーでは使用不可 |

### 構文例

```sql
-- マルチレベル集計: 製品ごとの日次売上平均を算出
SELECT
  Product,
  AVG(SUM(revenue) GROUP BY DATE(time)) AS avg_daily_sales
FROM Sales
GROUP BY Product
ORDER BY Product;
```

## 設定方法

### 前提条件

1. BigQuery プロジェクトへのアクセス権限
2. GoogleSQL の使用 (マルチレベル集計は GoogleSQL のみ対応)

### 手順

#### ステップ 1: マルチレベル集計の使用

```sql
-- 従来のサブクエリ方式
SELECT Product, AVG(daily_sales) AS avg_daily_sales
FROM (
  SELECT Product, SUM(revenue) AS daily_sales
  FROM Sales
  GROUP BY Product, DATE(time)
)
GROUP BY Product;

-- マルチレベル集計方式 (新機能)
SELECT
  Product,
  AVG(SUM(revenue) GROUP BY DATE(time)) AS avg_daily_sales
FROM Sales
GROUP BY Product;
```

両者は同じ結果を返しますが、マルチレベル集計方式ではサブクエリが不要です。

#### ステップ 2: Simba ODBC ドライバーの更新

```bash
# Linux の場合
wget https://storage.googleapis.com/simba-bq-release/odbc/SimbaODBCDriverforGoogleBigQuery_3.3.1.1001-Linux.tar.gz
tar -xzf SimbaODBCDriverforGoogleBigQuery_3.3.1.1001-Linux.tar.gz
```

インストールガイドに従って DSN を設定してください。

## メリット

### ビジネス面

- **分析クエリの開発効率向上**: 複雑な多段階集計をシンプルに記述でき、データアナリストの生産性が向上
- **レポート作成の迅速化**: 日次/週次/月次の階層的な集計をワンステップで実現

### 技術面

- **クエリの簡潔化**: サブクエリのネストが不要になり、コード行数が削減
- **可読性の向上**: 集計ロジックが一箇所に集約され、意図が明確に伝わる
- **メンテナンス性の改善**: 変更が必要な際に修正箇所が限定される

## デメリット・制約事項

### 制限事項

- 最大 2 レベルまでのネストのみサポート (3 レベル以上はエラー)
- PIVOT 演算子、差分プライバシー、集計しきい値句、連続クエリとの併用不可
- ORDER BY、LIMIT、IGNORE NULLS / RESPECT NULLS はマルチレベル集計内で使用不可
- HAVING MAX / HAVING MIN は GROUP BY 句と併用不可
- COUNT(* GROUP BY field) のような空の集計関数リストは使用不可

### 考慮すべき点

- Preview 段階のため、本番環境での利用には注意が必要
- サポートが限定的である可能性がある (フィードバックは bigquery-sql-preview-support@googlegroups.com へ)
- 既存のサブクエリベースのクエリからの移行は段階的に行うことを推奨

## ユースケース

### ユースケース 1: 日次売上の平均算出

**シナリオ**: EC サイトの売上データから、製品カテゴリごとに日次売上合計の平均を算出したい場合

**実装例**:
```sql
SELECT
  category,
  AVG(SUM(amount) GROUP BY sale_date) AS avg_daily_sales,
  MAX(SUM(amount) GROUP BY sale_date) AS max_daily_sales
FROM transactions
GROUP BY category;
```

**効果**: サブクエリなしで多段階の集計分析が可能。クエリの開発時間を短縮し、ダッシュボードのクエリを簡潔に保てる。

### ユースケース 2: 月次レポートにおける週次集計の統計

**シナリオ**: ユーザーアクティビティデータから、月ごとに週次アクティブユーザー数の平均・最大・最小を算出

**実装例**:
```sql
SELECT
  FORMAT_DATE('%Y-%m', activity_date) AS month,
  AVG(COUNT(DISTINCT user_id) GROUP BY DATE_TRUNC(activity_date, WEEK)) AS avg_weekly_active_users
FROM user_activity
GROUP BY month;
```

**効果**: 週次と月次の2段階集計を単一クエリで実現し、レポート生成パイプラインを簡素化。

### ユースケース 3: センサーデータの階層的集計

**シナリオ**: IoT センサーからの時系列データで、時間ごとの平均値をさらに日単位で集計する場合

**実装例**:
```sql
SELECT
  sensor_id,
  AVG(AVG(temperature) GROUP BY TIMESTAMP_TRUNC(reading_time, HOUR)) AS avg_hourly_temperature
FROM sensor_readings
GROUP BY sensor_id;
```

**効果**: 大量のセンサーデータの階層的な要約を効率的に実行可能。

## 料金

マルチレベル集計機能自体に追加料金はありません。通常の BigQuery クエリ実行としての料金が適用されます。

| 項目 | 料金 |
|------|------|
| オンデマンドクエリ | 処理データ量に基づく標準料金 |
| Simba ODBC ドライバー | 無料 (ダウンロード・ライセンス不要) |

## 関連サービス・機能

- **BigQuery GoogleSQL**: マルチレベル集計が追加された SQL 方言
- **BigQuery BI Engine**: 集計クエリの高速化と組み合わせて利用可能
- **Looker / Looker Studio**: マルチレベル集計を活用したダッシュボード構築
- **Simba ODBC/JDBC ドライバー**: サードパーティツールからの BigQuery 接続
- **Google 開発 ODBC ドライバー (Preview)**: Simba ODBC の代替として利用可能な Google 公式ドライバー

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260708-bigquery-multi-level-aggregation.html)
- [公式リリースノート](https://cloud.google.com/bigquery/docs/release-notes)
- [マルチレベル集計ドキュメント](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate-function-calls#multi_level_aggregation)
- [Simba ODBC ドライバー](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers#current_odbc_driver)
- [料金ページ](https://cloud.google.com/bigquery/pricing)

## まとめ

BigQuery のマルチレベル集計機能は、多段階の集計処理を大幅に簡素化する強力な SQL 拡張です。Preview 段階ではありますが、データ分析ワークフローの生産性向上に大きく貢献する機能であり、特に時系列データの階層的な集計や KPI レポートの生成において活用が期待されます。既存のサブクエリベースのクエリを段階的に移行し、コードの簡潔化を図ることを推奨します。

---

**タグ**: #BigQuery #GoogleSQL #MultiLevelAggregation #SQL #集計関数 #ODBC #SimbaDriver #Preview
