# Gemini Enterprise Agent Platform: Provisioned Throughput 注文ページの改善

**リリース日**: 2026-05-08

**サービス**: Gemini Enterprise Agent Platform

**機能**: Provisioned Throughput 注文ページの UI 改善

**ステータス**: 変更 (Change)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260508-gemini-enterprise-agent-platform-provisioned-throughput.html)

## 概要

Gemini Enterprise Agent Platform の Provisioned Throughput 注文ページに、注文管理を効率化する 3 つの UI 改善が実施されました。これにより、スケジュールされた注文の可視化、注文データのフィルタリング・ソート、および全リージョンにわたる注文データの CSV エクスポートが可能になりました。

この改善は、Provisioned Throughput を利用して生成 AI モデルのスループットを予約しているエンタープライズユーザーを対象としています。複数の注文や複数リージョンにまたがる大規模な運用を行っている組織にとって、注文管理の効率性が大幅に向上します。

**アップデート前の課題**

- スケジュールされた注文の開始日を一覧で確認する手段が限られていた
- 注文一覧のフィルタリングやソートができず、多数の注文を管理する際に非効率だった
- 全リージョンにわたる注文データを一括でエクスポートする方法がなく、レポーティングや監査に手間がかかった

**アップデート後の改善**

- Start Date カラムを使用して、スケジュールされた全注文を一覧表示できるようになった
- カラム名を使用した注文のフィルタリングとソートが可能になった
- 全リージョンを含む全注文データを CSV ファイルとしてダウンロードできるようになった

## サービスアップデートの詳細

### 主要機能

1. **Start Date カラムによるスケジュール注文の表示**
   - 注文ページに Start Date カラムが追加され、スケジュールされた全注文の開始日時を一覧で確認可能
   - Provisioned Throughput では注文時に最大 2 週間先までの開始日時を指定可能（Preview 機能）
   - スケジュール済みの注文と即時処理される注文を視覚的に区別できる

2. **カラム名によるフィルタリングとソート**
   - 注文一覧のカラム名をクリックまたは選択して、注文データのフィルタリングとソートが可能
   - 注文ステータス（Pending review、Approved、Active、Expired）による絞り込み
   - モデル名、リージョン、GSU 数などの条件で注文を効率的に検索可能

3. **CSV ファイルへの全注文データエクスポート**
   - 全リージョンにわたる注文データを CSV ファイルとして一括ダウンロード
   - 社内レポーティング、コスト分析、監査対応に活用可能
   - 従来はリージョンごとにしか確認できなかった情報を横断的に取得可能

## 技術仕様

### Provisioned Throughput 注文のステータス

| ステータス | 説明 |
|------|------|
| Pending review | 注文が送信され、利用可能なキャパシティに基づいて承認待ち |
| Approved | Google により承認済み、アクティベーション待ち |
| Active | アクティベーション完了、課金開始 |
| Expired | 注文期間が満了 |

### 必要な権限

| 権限 | 説明 |
|------|------|
| aiplatform.provisionedThroughputs.list | 全 Provisioned Throughput 注文の表示 |
| aiplatform.provisionedThroughputs.get | 特定の注文の詳細表示 |

注文の表示には `roles/aiplatform.provisionedThroughputAdmin` ロール、またはこれらの権限を含むカスタムロールが必要です。

## 設定方法

### 前提条件

1. Google Cloud プロジェクトで Gemini Enterprise Agent Platform API が有効化されていること
2. `roles/aiplatform.provisionedThroughputAdmin` ロールが付与されていること
3. アクティブな Provisioned Throughput 注文が存在すること

### 手順

#### ステップ 1: Provisioned Throughput ページへのアクセス

Google Cloud コンソールで Provisioned Throughput ページに移動します:

```
https://console.cloud.google.com/vertex-ai/provisioned-throughput
```

#### ステップ 2: 注文の表示とフィルタリング

1. リージョンを選択すると注文一覧が表示されます
2. Start Date カラムでスケジュールされた注文を確認します
3. カラムヘッダーをクリックしてソート、フィルタ条件を設定します

#### ステップ 3: CSV エクスポート

注文データを CSV ファイルとしてダウンロードします。このエクスポートには全リージョンのデータが含まれます。

## メリット

### ビジネス面

- **運用効率の向上**: 複数リージョンにまたがる注文を一括で把握・管理でき、管理工数を削減
- **監査・レポーティングの簡素化**: CSV エクスポートにより、コスト管理や社内報告に必要なデータを迅速に取得可能
- **計画的なリソース管理**: Start Date カラムによりスケジュール済み注文の全体像を把握し、キャパシティプランニングに活用可能

### 技術面

- **データの可視化向上**: フィルタリングとソートにより、特定の条件に合致する注文を即座に特定可能
- **全リージョン横断の統合ビュー**: CSV エクスポートでリージョンをまたいだデータを統合的に分析可能

## デメリット・制約事項

### 制限事項

- 注文の表示には適切な IAM 権限（`aiplatform.provisionedThroughputs.list`）が必要
- スケジュール注文の Start Date 指定は Google モデルのみ対応（オープンモデルではスケジューリング不可）

### 考慮すべき点

- CSV エクスポートには全リージョンのデータが含まれるため、大規模な組織ではファイルサイズが大きくなる可能性がある
- フィルタリング・ソートの具体的なカラムや条件の詳細は Google Cloud コンソールで確認が必要

## ユースケース

### ユースケース 1: マルチリージョン展開のコスト管理

**シナリオ**: 複数リージョン（us-central1、europe-west1、asia-northeast1 など）に Provisioned Throughput 注文を持つ企業が、月次のコストレポートを作成する必要がある。

**効果**: CSV エクスポート機能により、全リージョンの注文データを一括ダウンロードし、スプレッドシートやBI ツールで統合分析が可能。従来のリージョンごとの手動確認と比較して、レポート作成時間を大幅に短縮。

### ユースケース 2: スケジュール注文の計画管理

**シナリオ**: プロモーションキャンペーンに合わせて、将来の特定日時から Provisioned Throughput を有効化するスケジュール注文を複数設定している運用チーム。

**効果**: Start Date カラムにより、今後アクティブになる予定の全注文を時系列で確認でき、キャパシティの重複や不足を事前に検知可能。

### ユースケース 3: 大規模な注文ポートフォリオの管理

**シナリオ**: 数十のプロジェクトにわたって多数の Provisioned Throughput 注文を管理する SRE チーム。

**効果**: カラムによるフィルタリング・ソートにより、特定のモデルやステータスの注文を即座に絞り込み、期限切れ間近の注文や更新が必要な注文を迅速に特定可能。

## 料金

今回のアップデートは Provisioned Throughput 注文ページの UI 改善であり、追加料金は発生しません。Provisioned Throughput 自体の料金については、GSU（Generative AI Scale Unit）単位で課金される固定費・固定期間のサブスクリプションモデルです。

詳細な料金は [Provisioned Throughput 料金ページ](https://cloud.google.com/gemini-enterprise-agent-platform/pricing#provisioned-throughput) を参照してください。

## 関連サービス・機能

- **Gemini Enterprise Agent Platform**: Provisioned Throughput が提供される生成 AI プラットフォーム
- **Provisioned Throughput**: 生成 AI モデルのスループットを予約する固定費サブスクリプション
- **Google Cloud コンソール**: 注文ページの UI が改善されたインターフェース
- **Cloud Billing**: CSV エクスポートと組み合わせたコスト管理・分析に活用可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260508-gemini-enterprise-agent-platform-provisioned-throughput.html)
- [公式リリースノート](https://cloud.google.com/release-notes#May_08_2026)
- [Provisioned Throughput の購入](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/provisioned-throughput/purchase-provisioned-throughput)
- [Provisioned Throughput の概要](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/provisioned-throughput/overview)
- [Provisioned Throughput の使用](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/deploy/provisioned-throughput)
- [料金ページ](https://cloud.google.com/gemini-enterprise-agent-platform/pricing#provisioned-throughput)

## まとめ

今回の Provisioned Throughput 注文ページの改善は、Start Date カラムの追加、フィルタリング・ソート機能、全リージョン横断の CSV エクスポートという 3 つの実用的な機能強化です。特に複数リージョンで多数の注文を運用する大規模組織にとって、日常的な管理業務の効率化とコスト可視化に大きく貢献します。Google Cloud コンソールの Provisioned Throughput ページにアクセスして、新機能を確認することを推奨します。

---

**タグ**: #GeminiEnterpriseAgentPlatform #ProvisionedThroughput #UI改善 #注文管理 #CSVエクスポート #GoogleCloud
