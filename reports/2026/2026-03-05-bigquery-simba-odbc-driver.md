# BigQuery: Simba ODBC ドライバーアップデート

**リリース日**: 2026-03-05

**サービス**: BigQuery

**機能**: Simba ODBC Driver Update

**ステータス**: 一般提供 (GA)

:chart_with_upwards_trend: [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260305-bigquery-simba-odbc-driver.html)

## 概要

BigQuery 向け Simba ODBC ドライバーの更新版がリリースされた。Simba ODBC ドライバーは、BI ツールやレポーティングアプリケーション、ETL ツールなどから BigQuery に接続するための標準的な ODBC インターフェースを提供するコネクタである。insightsoftware 社が開発しており、Google Cloud Ready - BigQuery パートナー認定を受けている。

今回のアップデートにより、最新バージョンのドライバーがダウンロード可能となった。ODBC 3.80 データ標準に準拠し、Unicode サポート、32 ビットおよび 64 ビットの高性能コンピューティング環境をサポートしている。Windows、Linux、macOS の各プラットフォームで利用できる。

## サービスアップデートの詳細

### 主要機能

1. **マルチプラットフォーム対応**
   - Windows 32-bit / 64-bit (.msi)
   - Linux 32-bit / 64-bit (.tar.gz)
   - macOS (.dmg)

2. **High-Throughput API サポート**
   - BigQuery Storage Read API を使用した高速データ読み取りに対応
   - 大規模な結果セットの読み取りパフォーマンスを向上
   - 利用には `bigquery.readSessionUser` ロールが必要

3. **JobCreationMode 対応**
   - `JobCreationMode=2` の設定によりショートクエリモードに対応
   - .ini ファイルでの設定が可能

## 技術仕様

### ドライバー情報

| 項目 | 詳細 |
|------|------|
| ドライバー種別 | ODBC (Open Database Connectivity) |
| 準拠規格 | ODBC 3.80 |
| 開発元 | insightsoftware (Magnitude Simba) |
| 対応プラットフォーム | Windows (32/64-bit)、Linux (32/64-bit)、macOS |
| Unicode サポート | あり |

### 制限事項

- BigQuery のロード機能は非サポート
- BigQuery のエクスポート機能は非サポート
- クエリプレフィックスは非サポート
- DML の制限事項がすべて適用される
- パラメータ化クエリはクエリ検証のみ提供 (パフォーマンスへの影響なし)
- BigQuery 専用 (他のプロダクトやサービスでは使用不可)

## 設定方法

### 前提条件

1. Google Cloud プロジェクトと BigQuery へのアクセス権
2. High-Throughput API を使用する場合は `roles/bigquery.readSessionUser` ロール

### 手順

#### ステップ 1: ドライバーのダウンロード

OS に対応したインストーラーを [公式ダウンロードページ](https://cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers) からダウンロードする。

#### ステップ 2: インストールと設定

insightsoftware が提供するインストール・設定ガイドに従ってドライバーをインストールする。

#### ステップ 3: DSN の設定 (Linux/macOS の場合)

```ini
[ODBC Data Sources]
Sample DSN = Simba Google BigQuery ODBC Connector 64-bit

[Sample DSN]
JobCreationMode = 2
```

## 料金

Simba ODBC ドライバー自体は無料でダウンロード・利用可能であり、追加ライセンスは不要。ただし、ドライバーを通じて BigQuery を使用する際には以下の BigQuery 料金が適用される。

- クエリ実行に対する [コンピューティング料金](https://cloud.google.com/bigquery/pricing#compute-pricing-models)
- 大規模な結果セットをデスティネーションテーブルに書き込む場合の [ストレージ料金](https://cloud.google.com/bigquery/pricing#storage-pricing)
- High-Throughput API 機能を使用する場合の [BigQuery Storage Read API 料金](https://cloud.google.com/bigquery/pricing#data-extraction-pricing)

## 関連サービス・機能

- **Simba JDBC ドライバー**: Java アプリケーション向けの BigQuery 接続ドライバー (別途提供)
- **Google 開発 JDBC ドライバー**: Google が独自に開発した JDBC ドライバー (Preview)
- **BigQuery Storage Read API**: 大規模データの高速読み取りを可能にする API
- **BigQuery クライアントライブラリ**: Go、Python、Java 等の各言語向けクライアントライブラリ

## 参考リンク

- :chart_with_upwards_trend: [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260305-bigquery-simba-odbc-driver.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#March_05_2026)
- [ODBC/JDBC ドライバー ドキュメント](https://cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers)
- [BigQuery 料金ページ](https://cloud.google.com/bigquery/pricing)

## まとめ

BigQuery 向け Simba ODBC ドライバーの更新版がリリースされた。BI ツールや ETL ツールから ODBC 経由で BigQuery に接続しているユーザーは、最新バージョンへのアップデートを推奨する。詳細な変更内容についてはリリースノートテキストファイルを確認されたい。

---

**タグ**: #BigQuery #ODBC #Simba #ドライバーアップデート #コネクタ
