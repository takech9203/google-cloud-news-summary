# Google Cloud Marketplace Partners: レポート配信の高速化 (D+2 から D+1 へ)

**リリース日**: 2026-05-27

**サービス**: Google Cloud Marketplace Partners

**機能**: レポート配信の高速化 (D+2 から D+1)

**ステータス**: GA (一般提供)

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260527-marketplace-partners-report-acceleration.html)

## 概要

Google Cloud Marketplace のパートナー向けレポート配信が大幅に高速化されました。これまでデータ処理と配信に 2 日 (D+2) を要していた Customer Insights レポートが、1 日 (D+1) で配信されるようになります。

この改善により、Cloud Marketplace パートナーは顧客の利用状況データをこれまでより 1 日早く入手できるようになり、ビジネス上の意思決定や顧客対応の迅速化が期待できます。Customer Insights レポートには、顧客の情報やソフトウェアの利用状況（デプロイされた VM 数など）が含まれており、パートナーにとって重要なビジネスインテリジェンスの源泉です。

対象となるのは Google Cloud Marketplace に製品を出品しているすべてのパートナーです。BigQuery エクスポート、CSV エクスポート (Google Drive / Cloud Storage) のいずれの配信方法を利用している場合も、この高速化の恩恵を受けることができます。

**アップデート前の課題**

- Customer Insights レポートの日次配信は太平洋時間 (PT) 基準で 2 日遅れ (D+2) であり、例えば 6 月 1 日のデータは 6 月 3 日に配信されていた
- パートナーは顧客の利用状況を把握するまでに最短でも 2 日間待つ必要があった
- ビジネス判断や顧客サポートにおいて、データの鮮度に関する課題があった

**アップデート後の改善**

- 日次レポートの配信が D+1 に短縮され、例えば 6 月 1 日のデータは 6 月 2 日に配信される
- パートナーはより新鮮な顧客データに基づいた意思決定が可能になった
- Customer Incremental Insights レポートを含む関連レポートの配信も同様に高速化された

## アーキテクチャ図

```mermaid
architecture-beta
    group marketplace[Cloud Marketplace]
    group partner_systems[パートナーシステム]

    service customer(server)[顧客利用] in marketplace
    service billing(database)[Cloud Billing] in marketplace
    service processor(server)[レポート処理エンジン] in marketplace
    service bq(database)[BigQuery Export] in partner_systems
    service csv(disk)[CSV Export] in partner_systems
    service drive(disk)[Google Drive] in partner_systems
    service gcs(disk)[Cloud Storage] in partner_systems

    customer:R --> L:billing
    billing:R --> L:processor
    processor:R --> L:bq
    processor:B --> T:csv
    csv:R --> L:drive
    csv:B --> T:gcs
```

上図は、Google Cloud Marketplace における顧客利用データからパートナーレポート配信までのデータフローを示しています。顧客のソフトウェア利用データが Cloud Billing を通じてレポート処理エンジンに渡り、BigQuery または CSV (Google Drive / Cloud Storage) としてパートナーに配信されます。今回のアップデートにより、レポート処理エンジンでの処理遅延が D+2 から D+1 に短縮されました。

## サービスアップデートの詳細

### 主要機能

1. **レポート配信遅延の短縮**
   - Customer Insights レポートの処理・配信遅延が 2 日 (D+2) から 1 日 (D+1) に短縮
   - 太平洋時間 (PT) 基準で翌日にレポートが生成される
   - 例: 6 月 1 日のデータは 6 月 2 日に配信 (以前は 6 月 3 日)

2. **全配信方法での対応**
   - BigQuery エクスポート: `marketplace_report` リンクデータセットへの配信が高速化
   - CSV エクスポート: Google Drive / Cloud Storage への配信が高速化
   - Customer Incremental Insights レポートも同様に D+1 配信

3. **既存設定での自動適用**
   - パートナー側での設定変更は不要
   - 既存のレポート配信設定がそのまま利用可能
   - BigQuery クエリやデータパイプラインへの影響なし

## 技術仕様

### レポート配信スケジュール比較

| 項目 | アップデート前 | アップデート後 |
|------|---------------|---------------|
| 日次レポート配信遅延 | D+2 (2 日後) | D+1 (1 日後) |
| 月次レポート配信 | 翌月 2 日目 | 翌月 2 日目 (変更なし) |
| タイムゾーン基準 | 太平洋時間 (PT) | 太平洋時間 (PT) |
| Incremental Insights | D+2 | D+1 |

### 対象レポートタイプ

| レポート種別 | 配信高速化の適用 |
|-------------|-----------------|
| Customer Insights (日次) | 適用 |
| Customer Insights (月次) | 変更なし |
| Customer Incremental Insights (日次) | 適用 |
| Detailed Disbursements | 対象外 (月次のみ) |
| Charges and Usage | 対象外 (月次のみ) |

### BigQuery テーブル構造

```sql
-- Customer Insights レポートの確認
SELECT
  report_date,
  date,
  company,
  domain,
  external_account_id,
  sku_id,
  usage,
  unit
FROM
  `marketplace_report.insights`
WHERE
  _PARTITIONDATE = '2026-05-27'  -- D+1: 5月26日のデータが5月27日に配信
ORDER BY
  date DESC;
```

## 設定方法

### 前提条件

1. Google Cloud Marketplace パートナーとして登録済みであること
2. Producer Portal でレポート配信先が設定済みであること

### 手順

#### ステップ 1: レポート配信状況の確認

```bash
# Producer Portal のレポートページにアクセス
# https://console.cloud.google.com/producer-portal/partner-report?project=YOUR_PUBLIC_PROJECT_ID
```

今回のアップデートはパートナー側での設定変更を必要としません。既存のレポート配信設定が自動的に D+1 スケジュールに移行されます。

#### ステップ 2: Incremental Insights レポートの有効化 (推奨)

```bash
# BigQuery Export が有効な場合: 自動的に Incremental Insights が有効
# CSV Export の場合: Producer Portal > Reports > Configure reports で
# "Customer incremental insights" チェックボックスを有効にする
```

Incremental Insights レポートを有効にすることで、遅延報告されたデータも含むより正確なレポートを受け取ることができます。

#### ステップ 3: レポート通知の設定 (推奨)

```bash
# Essential Contacts API を有効化し、
# Cloud Billing カテゴリに通知先を追加
gcloud services enable essentialcontacts.googleapis.com --project=YOUR_PROJECT_ID
```

レポートの遅延や再生成が発生した場合に通知を受け取るための設定です。

## メリット

### ビジネス面

- **意思決定の迅速化**: 顧客データを 1 日早く入手できることで、ビジネス判断のサイクルが短縮される
- **顧客対応の改善**: 利用状況の変化をより早く検知でき、プロアクティブなカスタマーサクセスが可能になる
- **収益機会の早期発見**: 利用量の増減パターンをより迅速に把握し、アップセル・クロスセルの機会を特定できる

### 技術面

- **データパイプラインの効率化**: より新鮮なデータがパイプラインに流れることで、ダッシュボードやアラートの精度が向上する
- **設定変更不要**: 既存のインテグレーションやクエリをそのまま利用可能
- **Incremental Insights との連携**: 遅延報告データの反映もより迅速になり、データの整合性確認が容易になる

## デメリット・制約事項

### 制限事項

- 月次レポート (Monthly Insights) の配信スケジュールは変更なし (翌月 2 日目のまま)
- Detailed Disbursements レポートや Charges and Usage レポートは今回の高速化の対象外
- タイムゾーンは引き続き太平洋時間 (PT) 基準であり、日本時間 (JST) では日付の境界に注意が必要

### 考慮すべき点

- D+1 配信への変更に伴い、データ処理パイプラインのスケジューリングを見直す必要がある場合がある (例: D+2 を前提としたジョブスケジュール)
- 遅延報告されたデータは引き続き Incremental Insights レポートで補完される仕組みのため、D+1 のレポートが最終的なデータとは限らない
- パートナーが独自に構築した監視・アラートシステムのタイミング調整が必要になる場合がある

## ユースケース

### ユースケース 1: SaaS パートナーの顧客利用状況モニタリング

**シナリオ**: SaaS 製品を Cloud Marketplace で提供するパートナーが、顧客の日次利用状況をモニタリングし、利用量の急激な変化を検知してカスタマーサクセスチームに通知する。

**実装例**:
```sql
-- BigQuery で前日の利用状況を確認するクエリ (D+1 で実行可能に)
SELECT
  company,
  external_account_id,
  SUM(usage) AS total_usage,
  LAG(SUM(usage)) OVER (PARTITION BY external_account_id ORDER BY date) AS prev_day_usage
FROM
  `marketplace_report.insights`
WHERE
  _PARTITIONDATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY
  company, external_account_id, date
HAVING
  total_usage < prev_day_usage * 0.5  -- 利用量が前日比50%以下に低下
ORDER BY
  date DESC;
```

**効果**: 以前は D+2 の遅延により顧客の利用量低下に気づくまでに最短 3 日 (利用日 + D+2) かかっていたが、D+1 により最短 2 日 (利用日 + D+1) で検知可能になる。

### ユースケース 2: VM 製品パートナーの収益ダッシュボード

**シナリオ**: VM ベースの製品を提供するパートナーが、リアルタイムに近い収益ダッシュボードを運用し、経営陣にデイリーレポートを提供する。

**効果**: ダッシュボードのデータ鮮度が 1 日改善され、前日までの収益状況をより正確に把握できるようになる。経営判断のスピードが向上し、四半期目標に対する進捗追跡がより正確になる。

## 料金

このアップデートによる追加料金は発生しません。

### 料金に関する注意事項

| 項目 | 料金 |
|------|------|
| レポート配信の高速化 | 無料 (追加料金なし) |
| BigQuery ストレージ (レポートデータ) | パートナー負担なし |
| BigQuery クエリ | パートナーのプロジェクトで通常の BigQuery 料金が適用 |
| Cloud Storage (CSV 配信先) | パートナーのバケットに通常のストレージ料金が適用 |

## 利用可能リージョン

このアップデートはグローバルに適用されます。Cloud Marketplace パートナーレポートは地域に依存せず、すべてのパートナーが自動的に D+1 配信の恩恵を受けます。なお、BigQuery エクスポート先のリンクデータセットは US マルチリージョンに作成されます。

## 関連サービス・機能

- **Cloud Marketplace Producer Portal**: パートナーがレポート設定を管理するための管理コンソール
- **BigQuery**: レポートデータのエクスポート先として利用可能で、SQL による分析が可能
- **Cloud Storage**: CSV 形式のレポート配信先として利用可能
- **Essential Contacts API**: レポートの遅延や再生成に関する通知を受け取るためのサービス
- **Customer Incremental Insights**: 遅延報告されたデータを補完するためのレポート機能

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260527-marketplace-partners-report-acceleration.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#May_27_2026)
- [Customer Insights レポートのドキュメント](https://docs.cloud.google.com/marketplace/docs/partners/reports/report-customer-insight)
- [レポート配信設定](https://docs.cloud.google.com/marketplace/docs/partners/reports/set-up-reports)
- [利用可能なレポートタイプ](https://docs.cloud.google.com/marketplace/docs/partners/reports/report-types)

## まとめ

Google Cloud Marketplace パートナー向け Customer Insights レポートの配信が D+2 から D+1 に短縮されたことで、パートナーはより迅速に顧客の利用状況データを入手し、ビジネス判断に活用できるようになりました。パートナー側での設定変更は不要で、既存のすべての配信設定に自動的に適用されます。今すぐ Incremental Insights レポートを有効にし、データパイプラインのスケジュールを D+1 に合わせて最適化することを推奨します。

---

**タグ**: #GoogleCloudMarketplace #パートナーレポート #CustomerInsights #レポート高速化 #GA
