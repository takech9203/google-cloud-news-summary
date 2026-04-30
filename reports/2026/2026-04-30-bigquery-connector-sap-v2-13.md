# SAP on Google Cloud: BigQuery Connector for SAP バージョン 2.13

**リリース日**: 2026-04-30

**サービス**: SAP on Google Cloud

**機能**: BigQuery Connector for SAP version 2.13

**ステータス**: GA (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260430-bigquery-connector-sap-v2-13.html)

## 概要

BigQuery Connector for SAP のバージョン 2.13 が一般提供 (GA) として公開されました。本バージョンでは、テーブルスキーマキャッシュ機能が有効な場合にパーティションテーブルのデータレプリケーションが失敗する問題が修正されています。

BigQuery Connector for SAP は、SAP Landscape Transformation Replication Server (SAP LT Replication Server) にインストールされ、SAP アプリケーションデータを BigQuery にほぼリアルタイムでレプリケーションするためのコネクタです。CDC レプリケーション (Pub/Sub 経由)、ストリーミングデータレプリケーション、Cloud Storage へのファイルベースレプリケーションの 3 つのレプリケーションパスをサポートしています。

テーブルスキーマキャッシュはバージョン 2.12 で導入された機能で、BigQuery API への tables.get 呼び出し回数を削減し、API クォータ制限エラーを防止するためのパフォーマンス最適化機能です。今回の修正により、パーティションテーブルを使用する環境でもこの最適化機能を安全に利用できるようになりました。

**アップデート前の課題**

- テーブルスキーマキャッシュ機能 (SCH_CACHE_ENABLE パラメータ) を有効にした環境で、パーティションテーブルへのデータレプリケーションが失敗していた
- パーティションテーブルを使用するユーザーは、スキーマキャッシュ機能を無効にして運用する必要があり、BigQuery API のクォータ制限に抵触するリスクがあった
- 高頻度レプリケーション環境で tables.get 呼び出しが過剰になり、パフォーマンスが低下する可能性があった

**アップデート後の改善**

- パーティションテーブルへのレプリケーションがスキーマキャッシュ機能有効時にも正常に動作するようになった
- パーティションテーブルを使用するすべてのレプリケーション環境でスキーマキャッシュを活用でき、BigQuery API クォータ消費が削減される
- パーティションテーブルと非パーティションテーブルが混在する環境でも、一貫した設定でパフォーマンス最適化が可能になった

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph SAP環境
        A[("🗄️ SAP データソース")]
        B["⚙️ SAP LT\nReplication Server"]
        C["🔌 BigQuery Connector\nfor SAP v2.13"]
    end

    subgraph キャッシュ層
        D["💾 ABAP Shared Objects\n(スキーマキャッシュ)"]
    end

    subgraph Google Cloud
        E["📡 BigQuery\nStreaming API"]
        F[("📊 BigQuery\nパーティションテーブル")]
    end

    A -->|RFC| B
    B -->|CDC データ| C
    C <-->|スキーマ参照\n(API呼び出し削減)| D
    C -->|チャンク送信| E
    E -->|INSERT| F
```

この図は、SAP データソースから BigQuery パーティションテーブルへのストリーミングデータレプリケーションフローを示しています。バージョン 2.13 では、ABAP Shared Objects メモリに格納されたスキーマキャッシュがパーティションテーブルでも正しく機能し、BigQuery API への不要な呼び出しを削減します。

## サービスアップデートの詳細

### 主要機能

1. **パーティションテーブル向けスキーマキャッシュの不具合修正**
   - テーブルスキーマキャッシュ機能 (SCH_CACHE_ENABLE) 有効時にパーティションテーブルへのレプリケーションが失敗する問題を解消
   - パーティション情報を含むスキーマ定義がキャッシュから正しく取得されるように修正

2. **テーブルスキーマキャッシュ機能 (バージョン 2.12 で導入)**
   - SAP ABAP Shared Objects メモリにテーブルスキーマ情報を格納
   - スキーマに変更がない場合は BigQuery API の tables.get 呼び出しをバイパス
   - BigQuery API クォータ制限 (TableService.getTable) の超過を防止

3. **3 つのレプリケーションパスのサポート**
   - CDC レプリケーション (Pub/Sub 経由): BigQuery テーブルを SAP ソースと同期
   - ストリーミングデータレプリケーション: 全変更をアペンドオンリーで記録
   - ファイルベースレプリケーション (Cloud Storage): JSON ファイルとして配信

## 技術仕様

### スキーマキャッシュの設定パラメータ

| パラメータ名 | 説明 | デフォルト値 | 有効な値 |
|------|------|------|------|
| SCH_CACHE_ENABLE | スキーマキャッシュを有効にし、BigQuery API の tables.get 呼び出しを削減 | False | True / False |

### 影響を受けるレプリケーションパス

| レプリケーションパス | スキーマキャッシュ対応 | パーティションテーブル対応 (v2.13) |
|------|------|------|
| ストリーミングデータレプリケーション | 対応 | 修正済み |
| CDC レプリケーション (Pub/Sub 経由) | Cache Validations で対応 | -- |
| ファイルベースレプリケーション (Cloud Storage) | -- | -- |

### 設定方法

スキーマキャッシュを有効にするには、以下の手順を実行します:

```
1. SAP GUI で /n/GOOG/SLT_SETTINGS トランザクションを実行
2. Settings Table ドロップダウンメニューから「Parameters」を選択
3. 実行アイコンをクリック
4. 行挿入アイコンをクリック
5. Parameter Name に「SCH_CACHE_ENABLE」を入力
6. Parameter Value に「X」を入力
7. 保存をクリック
```

## 設定方法

### 前提条件

1. BigQuery Connector for SAP バージョン 2.13 がインストールされていること
2. SAP LT Replication Server が稼働していること
3. BigQuery データセットが作成済みであること
4. IAM サービスアカウントに BigQuery Data Editor および BigQuery Job User ロールが付与されていること

### 手順

#### ステップ 1: BigQuery Connector for SAP の更新

BigQuery Connector for SAP をバージョン 2.13 に更新します。更新手順については公式ドキュメントの「Update BigQuery Connector for SAP」を参照してください。

#### ステップ 2: スキーマキャッシュの有効化

SAP GUI で `/n/GOOG/SLT_SETTINGS` トランザクションを実行し、SCH_CACHE_ENABLE パラメータを有効にします。

#### ステップ 3: パーティションテーブルへのレプリケーション確認

パーティションテーブルへのデータレプリケーションが正常に動作することを確認します。SAP LT Replication Server のアプリケーションログでエラーが発生していないことを検証してください。

## メリット

### ビジネス面

- **運用の安定性向上**: パーティションテーブルを使用するレプリケーション環境で、スキーマキャッシュによるパフォーマンス最適化を安心して利用できる
- **API コスト最適化**: BigQuery API 呼び出し回数の削減により、大規模レプリケーション環境でのクォータ消費を抑制

### 技術面

- **パフォーマンス改善**: スキーマキャッシュにより tables.get 呼び出しが削減され、レプリケーションスループットが向上
- **クォータ制限回避**: 高頻度レプリケーションシナリオで BigQuery API クォータ (TableService.getTable) の超過を防止
- **一貫した設定管理**: パーティションテーブルと非パーティションテーブルで同一のキャッシュ設定を使用可能

## デメリット・制約事項

### 制限事項

- スキーマキャッシュはストリーミングデータレプリケーション (insert-only) パスでのみ利用可能
- テーブルスキーマを変更した場合、キャッシュの手動クリアが必要になる場合がある
- CDC レプリケーション (Pub/Sub 経由) の場合は、別途 Cache Validations 機能を使用する必要がある

### 考慮すべき点

- スキーマ変更を頻繁に行う環境では、キャッシュの無効化タイミングに注意が必要
- バージョン 2.13 へのアップデート後、既存のレプリケーション設定の動作確認を推奨
- SAP LT Replication Server の ABAP Shared Objects メモリの利用量が増加する可能性がある

## ユースケース

### ユースケース 1: 大規模 SAP データウェアハウスのリアルタイム分析

**シナリオ**: 製造業の企業が、SAP ERP の販売データ・在庫データをパーティションテーブル (日付パーティション) で BigQuery に格納し、日次レポートやリアルタイムダッシュボードを運用している。高頻度のレプリケーションにより BigQuery API クォータ制限に達していたため、スキーマキャッシュを有効にしたいが、パーティションテーブルの問題により有効化できなかった。

**効果**: バージョン 2.13 に更新することで、パーティションテーブル環境でもスキーマキャッシュを安全に有効化でき、API クォータ問題を解消しつつ安定したリアルタイムデータ連携を実現

### ユースケース 2: マルチテーブルレプリケーション環境での統一設定

**シナリオ**: 小売業の企業が、数百の SAP テーブルを BigQuery にレプリケーションしており、一部のテーブルはパーティション化されている。パーティションテーブルの問題により、テーブルごとに個別のキャッシュ設定を管理する必要があった。

**効果**: バージョン 2.13 により、すべてのテーブルに対して統一的にスキーマキャッシュを有効化でき、設定管理の複雑さが解消される

## 料金

BigQuery Connector for SAP 自体は無料で提供されています。ただし、以下の関連サービスの利用料金が発生します:

- **BigQuery**: ストレージ料金とクエリ料金 (データ取り込みのストリーミング API 利用料を含む)
- **Pub/Sub** (CDC レプリケーション使用時): メッセージ配信料金
- **Cloud Storage** (ファイルベースレプリケーション使用時): ストレージ料金と API 操作料金
- **Compute Engine**: SAP LT Replication Server のホスティング料金

詳細は [BigQuery の料金ページ](https://cloud.google.com/bigquery/pricing) および [SAP on Google Cloud の料金](https://cloud.google.com/sap/pricing) を参照してください。

## 関連サービス・機能

- **BigQuery**: SAP データの最終的な分析先。パーティションテーブルにより大規模データの効率的な管理とクエリ最適化を実現
- **Pub/Sub**: CDC レプリケーションパスでメッセージブローカーとして機能し、SAP 変更データを BigQuery に配信
- **Cloud Storage**: ファイルベースレプリケーションのステージング先として使用
- **SAP LT Replication Server**: SAP データソースからの変更データキャプチャ (CDC) を担当するミドルウェア
- **Cloud IAM**: BigQuery Connector for SAP の認証・認可を管理するサービスアカウントとロール

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260430-bigquery-connector-sap-v2-13.html)
- [公式リリースノート](https://cloud.google.com/release-notes#April_30_2026)
- [BigQuery Connector for SAP の新機能](https://docs.cloud.google.com/sap/docs/bq-connector/whats-new)
- [BigQuery Connector for SAP 概要ドキュメント](https://docs.cloud.google.com/sap/docs/bq-connector/latest/overview)
- [テーブルスキーマキャッシュの設定](https://docs.cloud.google.com/sap/docs/bq-connector/latest/operations#table-schema-caching)
- [BigQuery Connector for SAP の計画ガイド](https://docs.cloud.google.com/sap/docs/bq-connector/latest/planning)
- [BigQuery Connector for SAP の更新方法](https://docs.cloud.google.com/sap/docs/bq-connector/latest/operations#bqc4sap-operations-bqc-update)

## まとめ

BigQuery Connector for SAP バージョン 2.13 は、テーブルスキーマキャッシュとパーティションテーブルの組み合わせで発生していた不具合を修正する重要なバグフィックスリリースです。パーティションテーブルを使用して SAP データを BigQuery にレプリケーションしている環境では、本バージョンへの更新後にスキーマキャッシュを有効化することで、API クォータ消費の削減とレプリケーションパフォーマンスの向上が期待できます。影響を受ける環境では早期のアップデートを推奨します。

---

**タグ**: #SAP #BigQuery #BigQueryConnectorForSAP #データレプリケーション #パーティションテーブル #スキーマキャッシュ #バグ修正 #GA
