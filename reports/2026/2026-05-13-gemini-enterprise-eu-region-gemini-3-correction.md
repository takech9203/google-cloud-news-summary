# Gemini Enterprise: EU リージョンにおける Gemini 3 モデルの提供ステータス訂正

**リリース日**: 2026-05-13

**サービス**: Gemini Enterprise

**機能**: EU リージョンにおける Gemini 3.1 Pro / 3 Flash の提供状況の訂正

**ステータス**: Announcement (Correction)

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260513-gemini-enterprise-eu-region-gemini-3-correction.html)

## 概要

Google Cloud は、Gemini Enterprise における Gemini 3.1 Pro および Gemini 3 Flash モデルの EU リージョンでの提供状況について訂正を発表しました。以前のドキュメントおよびリリースノートでは、これらのモデルが EU リージョンで「利用可能」と記載されていましたが、正しくは「coming soon（近日提供予定）」であることが明らかになりました。

この訂正は、Data Residency（DRZ）および ML Regional Processing（MLP）の両方に影響します。現時点では、Gemini 3.1 Pro と Gemini 3 Flash の DRZ および MLP は US/global マルチリージョンでのみサポートされており、EU マルチリージョンおよびインカントリーリージョン（IN、SG、UK、CA）では「coming soon」のステータスとなっています。

EU リージョンでの展開を計画していた組織は、これらのモデルの EU リージョン対応が正式に発表されるまで、デプロイメント計画の見直しが必要です。

**アップデート前の課題**

- ドキュメント上では Gemini 3.1 Pro および 3 Flash が EU リージョンで「利用可能」と記載されており、ユーザーが利用可能と誤認していた
- EU リージョンでのデプロイメントを計画・開始していた顧客が存在した可能性がある
- データレジデンシー要件に基づき EU リージョンでの利用を前提とした設計を行っていたケースがあり得る

**アップデート後の改善**

- 正確な提供ステータスが「coming soon」に訂正され、ユーザーが正しい情報に基づいて計画を立てられるようになった
- EU リージョンでのデータレジデンシー（DRZ）および ML リージョナルプロセッシング（MLP）が近日対応予定であることが明確化された
- 現時点での正確な利用可能リージョン（US/global のみ）が明示された

## サービスアップデートの詳細

### Gemini 3 モデルのリージョン別提供状況（訂正後）

| モデル | US/global マルチリージョン | EU マルチリージョン | インカントリーリージョン (IN, SG, UK, CA) |
|--------|---------------------------|--------------------|-----------------------------------------|
| Gemini 3.1 Pro | DRZ サポート済み / MLP サポート済み | DRZ coming soon / MLP coming soon | DRZ coming soon / MLP coming soon |
| Gemini 3 Flash | DRZ サポート済み / MLP サポート済み | DRZ coming soon / MLP coming soon | DRZ coming soon / MLP coming soon |

### Limited Availability の位置づけ

Gemini 3 シリーズモデルは、Gemini Enterprise 内で Pre-GA Offering の Limited Availability ステータスとして提供されています。主な制約は以下の通りです:

1. **Pre-GA Offering**
   - 将来的にプロダクショングレードの GA SLO が提供される予定だが、現時点では完全な GA 契約上のコミットメント（ライフタイムサポートや標準 12 か月廃止予告など）は提供されない

2. **アクセス方法の制限**
   - Limited Availability のモデル機能は、Gemini インターフェースおよび統合サーフェスを通じてのみ利用可能
   - Vertex AI API 経由での直接アクセスは不可

3. **データ処理**
   - Cloud Data Processing Addendum に基づく個人データの処理が可能

## デメリット・制約事項

### 制限事項

- EU リージョンでの Gemini 3.1 Pro / 3 Flash の利用は現時点では不可（coming soon）
- インカントリーリージョン（IN、SG、UK、CA）でも同様に coming soon ステータス
- Vertex AI API 経由での直接アクセスは Limited Availability では利用不可
- GA レベルの SLO やサポートは Pre-GA Offering の段階では提供されない

### EU ベースの顧客への影響

- GDPR やその他の EU データ規制に基づき EU リージョン内でのデータ処理を要件としていた場合、Gemini 3 シリーズモデルの利用を一時的に延期する必要がある
- EU リージョン対応までの間は、Gemini 2.5 Pro / 2.5 Flash（EU リージョンで DRZ/MLP サポート済み）の利用を検討する必要がある
- EU リージョンでの提供開始時期は未定であり、計画に不確実性が残る

## 利用可能リージョン

### 現時点での Gemini Enterprise 全体のリージョン対応

| リージョン種別 | リージョン名 | Gemini 3.1 Pro / 3 Flash ステータス |
|---------------|-------------|--------------------------------------|
| マルチリージョン | US | 利用可能（DRZ/MLP サポート済み） |
| マルチリージョン | EU | coming soon |
| マルチリージョン | global | 利用可能（DRZ/MLP サポート済み） |
| インカントリー | CA | coming soon |
| インカントリー | IN | coming soon |
| インカントリー | SG | coming soon |
| インカントリー | UK | coming soon |

### 代替モデルの EU リージョン対応状況

| モデル | EU マルチリージョン |
|--------|---------------------|
| Gemini 2.5 Flash | DRZ サポート済み / MLP サポート済み |
| Gemini 2.5 Pro | DRZ サポート済み / MLP サポート済み |

## 関連サービス・機能

- **Gemini Enterprise Standard/Plus Editions**: データレジデンシーおよび ML リージョナルプロセッシングの対象エディション
- **Vertex AI**: Gemini 3 モデルの API アクセスは Vertex AI 経由では Limited Availability では利用不可
- **Gemini Code Assist**: Gemini 3.1 Pro / 3.0 Flash は VS Code と IntelliJ で Preview として利用可能（別サービス）
- **Model Armor**: EU リージョンで DRZ/MLP サポート済み（Gemini 3 モデルとは独立）

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260513-gemini-enterprise-eu-region-gemini-3-correction.html)
- [公式リリースノート](https://cloud.google.com/release-notes#May_13_2026)
- [Gemini Enterprise ロケーション情報](https://docs.cloud.google.com/gemini/enterprise/docs/locations)
- [Gemini 3.1 Pro / 3 Flash の制限事項](https://docs.cloud.google.com/gemini/enterprise/docs/known-limitations#using-gemini-3-preview)

## まとめ

Gemini 3.1 Pro および Gemini 3 Flash の EU リージョンでの提供は「coming soon」であり、以前の「利用可能」という記載は誤りでした。EU リージョンでのデータレジデンシー要件がある顧客は、正式な EU リージョン対応の発表を待つか、EU で既にサポートされている Gemini 2.5 シリーズモデルの利用を検討してください。

---

**タグ**: #GeminiEnterprise #Gemini3 #EUリージョン #データレジデンシー #訂正 #LimitedAvailability
