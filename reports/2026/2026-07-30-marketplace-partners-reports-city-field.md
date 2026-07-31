# Google Cloud Marketplace (Partners): Customer Insights レポートと Detailed Disbursements レポートに city フィールドを追加

**リリース日**: 2026-07-30

**サービス**: Google Cloud Marketplace (Partners)

**機能**: Customer Insights レポートおよび Detailed Disbursements レポートへの city (市区町村) フィールドの追加

**ステータス**: Change (変更)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260730-marketplace-partners-reports-city-field.html)

## 概要

Google Cloud Marketplace でプロダクトを販売するパートナー (ISV・リセラー) 向けのレポートである Customer Insights レポートと Detailed Disbursements レポートに、顧客の市区町村を示す `city` フィールドが追加されました。

Customer Insights レポートは顧客ごとの利用状況や収益を追跡するためのレポート、Detailed Disbursements レポートは Google からパートナーへの支払い (ディスバースメント) の内訳を SKU・アカウント・プライベートオファー単位で確認するためのレポートです。これまで顧客の所在地情報としては国 (`country`)、州・省 (`state_or_province`)、郵便番号 (`postal_code`) が提供されていましたが、今回のアップデートにより市区町村レベルの粒度で顧客の地理情報を把握できるようになりました。

**アップデート前の課題**

- Detailed Disbursements レポートの顧客所在地情報は国・州/省・郵便番号レベルにとどまり、市区町村単位での分析には郵便番号からの変換など追加の加工が必要だった

**アップデート後の改善**

- 両レポートで顧客の市区町村 (`city`) を直接確認できるようになり、都市単位での売上分析や顧客セグメンテーションが容易になった
- Customer Insights レポートと Detailed Disbursements レポートの間で、都市レベルの地理情報を揃えて突き合わせできるようになった

## サービスアップデートの詳細

### 主要機能

1. **Customer Insights レポートへの `city` フィールド追加**
   - 顧客の市区町村 (該当する場合) を示すフィールド
   - 既存の `country`、`state_or_province`、`postal_code` と並ぶ顧客所在地情報として提供される

2. **Detailed Disbursements レポートへの `city` フィールド追加**
   - カテゴリ「Customer info」の列として追加 (公式ドキュメント上の追加時期は July 2026)
   - 顧客の市区町村 (該当する場合) を示す

## 技術仕様

### 追加されたフィールド

| 項目 | 詳細 |
|------|------|
| フィールド名 | `city` |
| 対象レポート | Customer Insights レポート、Detailed Disbursements レポート |
| 内容 | 顧客の市区町村 (該当する場合、if applicable) |
| カテゴリ (Detailed Disbursements) | Customer info |

### 既存の顧客所在地フィールドとの関係

| フィールド | 説明 |
|-----------|------|
| `country` | 顧客の国 |
| `state_or_province` | 顧客の州または省 (該当する場合) |
| `city` | 顧客の市区町村 (該当する場合) — **今回追加** |
| `postal_code` | 顧客の郵便番号 (該当する場合)。個人アカウントの場合はレポートから除外 |

## メリット

### ビジネス面

- **地理分析の粒度向上**: 都市単位で顧客分布や収益を分析でき、地域別のマーケティング施策や営業戦略の立案に活用できる
- **レポート間の整合性**: Customer Insights レポートと Detailed Disbursements レポートの両方で都市情報を参照でき、突き合わせ分析がしやすくなる

### 技術面

- **追加加工の削減**: 郵便番号から都市を推定するといった前処理が不要になり、BigQuery エクスポートなどでの集計クエリがシンプルになる

## デメリット・制約事項

### 考慮すべき点

- `city` は「該当する場合 (if applicable)」に提供されるため、すべての行に値が入るとは限らない
- 公式ドキュメントには、Cloud Marketplace の機能追加に伴い既存レポートへ列が随時追加されるため、レポートの自動処理は列数ではなく列名ベースで動作するように構成すべきと明記されている。列の追加によりパイプラインが壊れないか確認が必要

## ユースケース

### ユースケース 1: 都市別の売上・利用状況分析

**シナリオ**: Marketplace に SaaS プロダクトを出品している ISV が、どの都市の顧客からの利用が多いかを把握し、地域イベントやローカライズ施策の優先順位を決めたい。

**効果**: Customer Insights レポートの `city` フィールドを使い、BigQuery エクスポートに対する集計クエリだけで都市別の利用量・収益を可視化できる。

### ユースケース 2: ディスバースメントの地理的内訳の把握

**シナリオ**: 経理・財務チームが Detailed Disbursements レポートをもとに、支払額を顧客の所在地 (国・州・都市) ごとに集計してレポーティングしたい。

**効果**: 追加された `city` 列により、支払データの都市レベルの内訳を追加加工なしで作成できる。

## 関連サービス・機能

- **BigQuery**: Marketplace レポートは BigQuery にエクスポートでき、追加された `city` 列を含めて SQL で分析できる
- **Cloud Marketplace Charges & Usage レポート**: Detailed Disbursements レポートの `c_u_account_id` フィールドで突き合わせが可能な関連レポート

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260730-marketplace-partners-reports-city-field.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#July_30_2026)
- [Customer Insights report fields (公式ドキュメント)](https://docs.cloud.google.com/marketplace/docs/partners/reports/report-customer-insight)
- [Detailed Disbursements report fields (公式ドキュメント)](https://docs.cloud.google.com/marketplace/docs/partners/reports/report-detailed-disbursement)

## まとめ

Google Cloud Marketplace のパートナー向けレポートに顧客の市区町村を示す `city` フィールドが追加され、都市レベルでの顧客分析や支払内訳の把握が容易になりました。レポートを自動処理している場合は、列名ベースの処理になっているかを確認したうえで、新しい `city` 列を分析パイプラインに取り込むことを推奨します。

---

**タグ**: #GoogleCloudMarketplace #Partners #CustomerInsights #DetailedDisbursements #Reports #Change
