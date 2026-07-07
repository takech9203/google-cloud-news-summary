# Gemini Enterprise: 日本・英国リージョンのサポート開始

**リリース日**: 2026-07-06

**サービス**: Gemini Enterprise

**機能**: 日本 (asia-northeast1) および英国 (europe-west2) リージョンのサポート

**ステータス**: GA with allowlist (許可リスト付き一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260706-gemini-enterprise-japan-uk-regions.html)

## 概要

Gemini Enterprise アプリが日本 (`asia-northeast1`) および英国 (`europe-west2`) リージョンで利用可能になりました。これらのリージョンでは、保存時データレジデンシー (at-rest DRZ) および機械学習処理 (MLP) がリージョン内で完結します。また、最新の Gemini 3.5 Flash モデルもこれらのリージョンでリージョン内 DRZ および MLP 付きで利用できます。

このアップデートは、日本および英国のデータ主権要件やコンプライアンス規制に対応するための重要なマイルストーンです。規制上の理由でデータを国内に保持する必要がある組織が、Gemini Enterprise の高度な AI 機能を活用できるようになります。NotebookLM Enterprise でも同様にこれらのリージョンが利用可能です。

利用するには Google アカウントチームへの連絡による許可リストへの登録が必要です。一部機能に制限があるため、本番環境への導入前にドキュメントの確認が推奨されます。

**アップデート前の課題**

- 日本・英国の組織は Gemini Enterprise を利用する際、データが US または EU のマルチリージョンに保存・処理される必要があった
- 国内データレジデンシー要件を持つ規制産業 (金融、医療、公共機関等) では Gemini Enterprise の採用が困難だった
- AI/ML 処理がリージョン外で行われるため、データ主権に関するコンプライアンス上の懸念があった

**アップデート後の改善**

- 日本 (`asia-northeast1`) および英国 (`europe-west2`) でデータの保存と ML 処理がリージョン内で完結するようになった
- 国内データレジデンシー要件を持つ組織でも Gemini Enterprise を利用可能になった
- 最新の Gemini 3.5 Flash モデルをリージョン内 DRZ/MLP 付きで利用可能になった
- NotebookLM Enterprise でも同様のリージョンサポートが追加された

## アーキテクチャ図

```mermaid
architecture-beta
    group japan(cloud)[Japan Region: asia-northeast1]
    group uk(cloud)[UK Region: europe-west2]
    group global(cloud)[Global / US / EU Multi-regions]

    service gemini_jp(server)[Gemini Enterprise] in japan
    service drz_jp(database)[At-rest DRZ] in japan
    service mlp_jp(server)[MLP Processing] in japan
    service flash_jp(server)[Gemini 3.5 Flash] in japan

    service gemini_uk(server)[Gemini Enterprise] in uk
    service drz_uk(database)[At-rest DRZ] in uk
    service mlp_uk(server)[MLP Processing] in uk
    service flash_uk(server)[Gemini 3.5 Flash] in uk

    service gemini_global(server)[Gemini Enterprise] in global
    service all_features(server)[Full Feature Set] in global

    gemini_jp:R --> L:drz_jp
    gemini_jp:R --> L:mlp_jp
    gemini_jp:R --> L:flash_jp

    gemini_uk:R --> L:drz_uk
    gemini_uk:R --> L:mlp_uk
    gemini_uk:R --> L:flash_uk

    gemini_global:R --> L:all_features
```

日本および英国のインカントリーリージョンでは、Gemini Enterprise の基本機能、DRZ、MLP、および Gemini 3.5 Flash モデルがリージョン内で完結します。一部の高度な機能 (Grounding with Google Search、画像生成、動画生成等) は引き続きグローバルリージョンでのみ利用可能です。

## サービスアップデートの詳細

### 主要機能

1. **Gemini Enterprise 基本機能のリージョン内提供**
   - アクセス制御データ、ブレンド検索、Workspace 検索、ピープルサーチ
   - コア検索インフラストラクチャ、Assistant、回答生成
   - インジェスト/フェデレーテッドコネクタ、ドキュメント理解、分析
   - フロントエンド、Canvas、Agent Registry、Agent Designer
   - カスタムエージェントおよび Agent Engine Platform

2. **Gemini 3.5 Flash モデルのリージョン内サポート**
   - 日本 (`asia-northeast1`) および英国 (`europe-west2`) で at-rest DRZ と MLP の両方をサポート
   - リージョン内で推論処理が完結

3. **NotebookLM Enterprise のリージョンサポート**
   - 基本機能 (ソース追加、エンベディング生成、クエリ、チャット、要約生成) が利用可能
   - 日本・英国リージョンで at-rest DRZ および MLP をサポート

4. **Model Armor のリージョンサポート**
   - at-rest DRZ および MLP をサポート
   - AI セーフティ機能をリージョン内で利用可能

## 技術仕様

### リージョン別機能サポート状況

| 機能 | 日本 (asia-northeast1) | 英国 (europe-west2) | 備考 |
|------|----------------------|-------------------|------|
| 基本機能 | DRZ + MLP サポート | DRZ + MLP サポート | GA with allowlist |
| Gemini 3.5 Flash | DRZ + MLP サポート | DRZ + MLP サポート | - |
| Gemini 2.5 Pro | DRZ + MLP サポート | 非対応 | 日本のみ対応 |
| Gemini 3.1 Pro | DRZ/MLP 非対応 | DRZ/MLP 非対応 | Limited Availability |
| Model Armor | DRZ + MLP サポート | DRZ + MLP サポート | - |
| CMEK | DRZ + MLP サポート | DRZ + MLP サポート | - |
| オートコンプリート | DRZ + MLP サポート | DRZ + MLP サポート | 一部機能制限あり |
| Dynamic Facets | グローバルのみ | グローバルのみ | - |
| Grounding with Google Search | グローバルのみ | グローバルのみ | - |
| Web Grounding | DRZ/MLP 非対応 | DRZ/MLP 非対応 | - |
| 画像生成 | DRZ/MLP 非対応 | DRZ/MLP 非対応 | - |
| 動画生成 | グローバルのみ | グローバルのみ | - |

### NotebookLM Enterprise 機能サポート状況

| 機能 | 日本 (asia-northeast1) | 英国 (europe-west2) | 備考 |
|------|----------------------|-------------------|------|
| 基本機能 | DRZ + MLP サポート | DRZ + MLP サポート | - |
| Content Studio | 利用不可 | 利用不可 | 音声、スライド、インフォグラフィック、動画 |
| Discover Sources | DRZ/MLP 非対応 | DRZ/MLP 非対応 | Google Search 連携のため |

## 設定方法

### 前提条件

1. Google アカウントチームに連絡し、許可リストへの登録を依頼
2. Gemini Enterprise または NotebookLM Enterprise のライセンスを保有していること
3. Google Cloud プロジェクトが適切に構成されていること

### 手順

#### ステップ 1: 許可リストへの登録申請

Google アカウントチームに連絡し、日本 (`asia-northeast1`) または英国 (`europe-west2`) リージョンへのアクセスをリクエストします。

#### ステップ 2: アプリのロケーション選択

```
Google Cloud Console > Gemini Enterprise > アプリ作成
  > ロケーション: asia-northeast1 (日本) または europe-west2 (英国) を選択
```

コンソールでアプリを作成する際に、リージョンとして `asia-northeast1` (日本) または `europe-west2` (英国) を選択します。

#### ステップ 3: API エンドポイントの設定

```bash
# 日本リージョンの API エンドポイント例
https://asia-northeast1-discoveryengine.googleapis.com/v1/projects/PROJECT_ID/locations/asia-northeast1/...

# 英国リージョンの API エンドポイント例
https://europe-west2-discoveryengine.googleapis.com/v1/projects/PROJECT_ID/locations/europe-west2/...
```

API 呼び出しでは、エンドポイントプレフィックスとロケーションパラメータを適切なリージョンに設定します。

## メリット

### ビジネス面

- **データ主権コンプライアンスの実現**: 日本の個人情報保護法や英国の UK GDPR に対応し、国内にデータを保持しながら AI 機能を活用可能
- **規制産業での AI 採用促進**: 金融機関、医療機関、政府機関など、データの国外移転に制限がある組織でも Gemini Enterprise を導入可能
- **競争力の維持**: データレジデンシー要件を満たしつつ、最新の AI モデル (Gemini 3.5 Flash) を活用した業務効率化を実現

### 技術面

- **リージョン内データ完結**: 保存時データおよび ML 処理がリージョン内で完結し、データの越境転送が発生しない
- **最新モデルの利用**: Gemini 3.5 Flash をリージョン内 DRZ/MLP 付きで利用可能
- **統合セキュリティ**: Model Armor および CMEK がリージョン内でサポートされ、エンタープライズレベルのセキュリティを確保

## デメリット・制約事項

### 制限事項

- 許可リストへの登録が必要 (セルフサービスでの利用開始は不可)
- Grounding with Google Search はグローバルリージョンでのみ利用可能
- 画像生成および動画生成機能はリージョン内で利用不可
- Web Grounding for Enterprise はリージョン内 DRZ/MLP 非対応
- NotebookLM Enterprise の Content Studio (音声概要、スライドデッキ、インフォグラフィック、動画概要) は利用不可
- Gemini 3.1 Pro モデルはインカントリーリージョンで DRZ/MLP 非対応
- Dynamic Facets はグローバルリージョンでのみ利用可能
- オートコンプリートのテールマッチサジェスチョンおよび高度なドキュメントデータモードはグローバルリージョンでのみ利用可能

### 考慮すべき点

- グローバルリージョンと比較してレスポンスタイムが異なる可能性がある (Google はレイテンシ最適化の観点からはグローバルを推奨)
- 利用可能な機能セットがグローバルリージョンより限定的であるため、ワークロード要件との適合性を事前に確認が必要
- 今後の機能追加がグローバルリージョンに先行して提供される可能性がある

## ユースケース

### ユースケース 1: 日本の金融機関におけるナレッジ検索

**シナリオ**: 大手銀行が社内のコンプライアンス文書、規制ガイドライン、顧客対応マニュアルを Gemini Enterprise で検索可能にしたいが、金融庁の規制により顧客データや機密文書を日本国外に移転できない。

**効果**: `asia-northeast1` リージョンを使用することで、全てのデータを日本国内に保持しながら、AI を活用した高度なドキュメント検索・要約機能を利用可能。規制要件を満たしつつ、行員の業務効率が大幅に向上。

### ユースケース 2: 英国の医療機関における研究支援

**シナリオ**: NHS (英国国民保健サービス) 傘下の研究機関が、医学論文や臨床試験データを NotebookLM Enterprise で分析したいが、UK GDPR により患者関連データを英国外に移転できない。

**効果**: `europe-west2` リージョンを使用することで、患者データのプライバシーを保護しながら NotebookLM Enterprise の基本機能 (ソース追加、クエリ、チャット、要約生成) を活用可能。研究プロセスの効率化を実現。

### ユースケース 3: 日本の製造業における技術文書管理

**シナリオ**: 大手製造メーカーが製品設計書、品質管理ドキュメント、特許関連文書を Gemini Enterprise で管理・検索したい。知的財産保護の観点から、データを日本国内に保持する必要がある。

**効果**: Gemini Enterprise の Agent Engine Platform およびカスタムエージェント機能を `asia-northeast1` リージョンで利用し、技術文書に特化した AI アシスタントを構築。Gemini 3.5 Flash モデルによる高速な応答生成で、エンジニアの情報アクセスが効率化。

## 利用可能リージョン

現在、Gemini Enterprise のインカントリーリージョンとして以下が利用可能です (全て GA with allowlist):

| リージョン | リージョン名 | 今回追加 |
|----------|------------|---------|
| カナダ | ca | - |
| インド | in | - |
| 日本 | asia-northeast1 | 対象 |
| シンガポール | sg | - |
| 英国 | europe-west2 | 対象 |

マルチリージョン (US、EU) では許可リストなしで利用可能です。セキュリティや規制上の要件がない場合は、Google はレスポンスタイム、最新モデルバージョン、最新機能の観点からグローバルロケーションの使用を推奨しています。

## 関連サービス・機能

- **NotebookLM Enterprise**: 同様に日本・英国リージョンで利用可能。基本機能の DRZ/MLP をサポート
- **Gemini Enterprise Agent Platform**: Agent Registry、Agent Designer、カスタムエージェントがリージョン内で利用可能
- **Agent Engine**: Memory Bank、Sessions、Runtime がリージョン内 DRZ をサポート
- **Model Armor**: AI セーフティ機能をリージョン内で利用可能
- **CMEK (Customer-Managed Encryption Keys)**: リージョン内でカスタマーマネージド暗号鍵を使用可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260706-gemini-enterprise-japan-uk-regions.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#July_06_2026)
- [Data residency for Gemini Enterprise Standard and Plus Editions](https://docs.cloud.google.com/gemini/enterprise/docs/locations)
- [Gemini Enterprise ドキュメント](https://docs.cloud.google.com/gemini/enterprise/docs)
- [Limitations for multi-regions and in-country regions](https://docs.cloud.google.com/gemini/enterprise/docs/locations#limitations)

## まとめ

Gemini Enterprise の日本 (`asia-northeast1`) および英国 (`europe-west2`) リージョンサポートは、データ主権要件を持つ組織が最新の AI 機能を活用するための重要な進展です。利用するには Google アカウントチームへの連絡が必要ですが、登録後は保存データおよび ML 処理が完全にリージョン内で完結するため、国内データレジデンシー要件を満たしながら Gemini Enterprise と NotebookLM Enterprise の基本機能および Gemini 3.5 Flash モデルを活用できます。一部機能に制限があるため、導入前にワークロード要件との適合性を確認し、制限事項のドキュメントを参照することを推奨します。

---

**タグ**: #GeminiEnterprise #DataResidency #Japan #UK #asia-northeast1 #europe-west2 #DRZ #MLP #NotebookLM #Gemini3.5Flash #コンプライアンス #GA
