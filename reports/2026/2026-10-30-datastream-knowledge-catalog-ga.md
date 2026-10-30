# Datastream: Knowledge Catalog 統合が一般提供 (GA) に

**リリース日**: 2026-10-30

**サービス**: Datastream

**機能**: Knowledge Catalog 統合

**ステータス**: GA (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261030-datastream-knowledge-catalog-ga.html)

## 概要

Datastream と Knowledge Catalog の統合が一般提供 (GA) になりました。Knowledge Catalog はメタデータの保存・管理・アクセスのためのプラットフォームであり、今回の統合により、Datastream のリソース (ストリーム、接続プロファイル、プライベート接続構成) のテクニカルメタデータが自動的に Knowledge Catalog に取り込まれ、検索・閲覧できるようになります。

メタデータの同期は、Pub/Sub を利用したほぼリアルタイムのライブ同期と、Cloud Storage を経由した定期的なバッチ同期の 2 つのモードで行われ、カタログの内容がソースシステムと一貫した状態に保たれます。検索はキーワード検索に加えて自然言語検索にも対応しており、「BigQuery を宛先とする Datastream のストリームを一覧して」のような日常的な表現でリソースを探すことができます。

CDC (変更データキャプチャ) パイプラインを多数運用するデータエンジニアリングチームやデータガバナンス担当者にとって、組織内の Datastream リソースを横断的に可視化し、トラブルシューティングやパイプライン管理の運用性を高められるアップデートです。

**アップデート前の課題**

- Datastream のストリームや接続プロファイルの棚卸しには、Datastream のコンソールや API をプロジェクトごとに個別に確認する必要があった
- Datastream のリソース情報 (ストリームの状態、接続先、ネットワーク構成など) が組織のデータカタログに統合されておらず、他のデータ資産と同じ場所から検索できなかった
- パイプラインのトラブルシューティング時に、関連リソースのメタデータを横断的に把握する手段が限られていた

**アップデート後の改善**

- Datastream のストリーム・接続プロファイル・プライベート接続構成のメタデータが、デフォルトで自動的に Knowledge Catalog に検出・登録されるようになった
- ライブ同期 (Pub/Sub) とバッチ同期 (Cloud Storage) により、メタデータがほぼリアルタイムかつ一貫性を保って維持されるようになった
- キーワード検索 (例: `system=Datastream AND type=Stream`) と自然言語検索の両方で Datastream リソースを検索できるようになった
- GA となったことで、本番環境での利用が公式にサポートされるようになった

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph DS["🔄 Datastream リソース"]
        ST["📡 ストリーム"]
        CP["🔌 接続プロファイル"]
        PC["🔒 プライベート接続構成"]
    end
    PS["📨 Pub/Sub<br/>(ライブ同期)"]
    GCS[("🗄️ Cloud Storage<br/>(バッチ同期)")]
    KC["📚 Knowledge Catalog"]
    USER(["👤 データ利用者"])

    DS -->|メタデータ変更イベント| PS
    DS -->|定期的なフルエクスポート<br/>(チェックポイント)| GCS
    PS -->|ほぼリアルタイム更新| KC
    GCS -->|バッチ取り込み| KC
    USER -->|キーワード / 自然言語検索| KC
```

Datastream のメタデータは、変更イベントを Pub/Sub 経由で配信するライブ同期と、Cloud Storage へのフルエクスポートを取り込むバッチ同期の 2 経路で Knowledge Catalog に反映され、利用者はカタログから検索・閲覧できます。

## サービスアップデートの詳細

### 主要機能

1. **Datastream リソースの自動メタデータ検出**
   - すべてのストリーム、接続プロファイル、プライベート接続構成のメタデータがデフォルトで検出される
   - Knowledge Catalog 側では、予約済みのエントリグループ `@datastream` 配下にモデリングされる

2. **2 つの同期モード**
   - **ライブ同期**: メタデータの変更発生時に Datastream が Pub/Sub トピックへイベントを発行し、Knowledge Catalog がサブスクライブしてほぼリアルタイムに更新を反映
   - **バッチ同期**: Datastream が定期的にメタデータのフルエクスポート (チェックポイント) を所定の Cloud Storage バケットへ発行し、Knowledge Catalog が取り込み

3. **キーワード検索と自然言語検索**
   - キーワード検索: `system=Datastream AND type=Stream` のような構文、括弧や `AND` / `OR` 演算子による複合条件に対応
   - 自然言語検索: AI によるセマンティック検索で、「List all Datastream streams with BigQuery destination」のような日常的な表現で検索可能
   - コンソールの Knowledge Catalog 検索ページでは、Systems フィルタで Datastream を選択し、タイプエイリアス (Data stream / Connection profile / Connection) で絞り込み可能

## 技術仕様

### Knowledge Catalog でのモデリング

| Knowledge Catalog エンティティ | リソース識別子 |
|------|------|
| エントリグループ | `@datastream` |
| エントリタイプ | `datastream-stream` |
| エントリタイプ | `datastream-connection-profile` |
| エントリタイプ | `datastream-private-connection` |

### 取得されるメタデータ

| リソースタイプ | 取得されるメタデータ |
|------|------|
| ストリーム | 名前、ロケーション、状態 (RUNNING / PAUSED / FAILED など)、バックフィル戦略、ソース / 宛先の接続プロファイル名、ソース / 宛先の構成 |
| 接続プロファイル | 名前、ロケーション、タイプ (MYSQL / ORACLE / BIGQUERY など)、接続オプション、ホスト名・ポート・データベース名 |
| プライベート接続構成 | 名前、状態、接続方式 (Private Service Connect または VPC ピアリング)、VPC ネットワークとサブネットの詳細 |

### 必要な IAM ロール・権限

| 操作 | 必要なロール / 権限 |
|------|------|
| Datastream メタデータの検索・閲覧 | Datastream Viewer (`roles/datastream.viewer`) — `dataplex.projects.search` 権限を含む |
| ストリームの検索 | `datastream.streams.get` |
| 接続プロファイルの検索 | `datastream.connectionProfiles.get` |
| プライベート接続構成の検索 | `datastream.privateConnections.get` |
| エントリの検索 (検索に使用するプロジェクト側) | `roles/dataplex.catalogAdmin` / `roles/dataplex.catalogEditor` / `roles/dataplex.catalogViewer` のいずれか |

## 設定方法

### 前提条件

1. プロジェクトで Dataplex API を有効化する
2. 必要な IAM 権限 (上記の表を参照) を付与する

### 手順

#### ステップ 1: コンソールで Datastream アセットを検索する

1. Google Cloud コンソールで Knowledge Catalog の Search ページに移動する
2. 「Choose search platform」で「Knowledge Catalog」を選択する
3. Filters パネルの「Systems」で「Datastream」を選択する
4. 必要に応じて「Type aliases」で Data stream / Connection profile / Connection を選択して絞り込む

#### ステップ 2: 検索クエリを使用する

```text
# すべての Datastream アセットを表示
system=Datastream

# すべてのストリームを表示
system=Datastream AND type=Stream

# すべての接続プロファイルを表示
system=Datastream AND type=ConnectionProfile

# エントリタイプを直接指定する場合
type="projects/dataplex-types/locations/global/entryTypes/datastream-stream"
```

キーワード検索では括弧と論理演算子 (`AND` / `OR`) を使った複合条件も記述できます。

## メリット

### ビジネス面

- **データガバナンスの強化**: CDC パイプラインのメタデータが組織のデータカタログに統合され、データ資産の全体像を一元的に把握できる
- **運用の可視性向上**: ストリームの状態や接続構成をカタログから横断的に確認でき、トラブルシューティングとパイプライン管理が容易になる

### 技術面

- **自動・一貫したメタデータ取り込み**: ライブ同期とバッチ同期の組み合わせにより、手動のカタログ登録なしでメタデータの鮮度と一貫性が維持される
- **柔軟な検索手段**: 構文ベースのキーワード検索と AI による自然言語検索の両方に対応し、複雑な構文を覚えなくてもリソースを発見できる

## デメリット・制約事項

### 考慮すべき点

- 検索結果の閲覧には Datastream リソース側の権限 (`datastream.*.get`) とカタログ検索側の権限 (Dataplex Catalog ロール) の両方が必要で、検索結果に対する権限チェックは検索に選択したプロジェクトとは独立して行われる
- Knowledge Catalog への API 呼び出しやビジネスメタデータの付加には、標準の Knowledge Catalog 料金が適用される

## ユースケース

### ユースケース 1: 組織内の CDC パイプラインの棚卸し

**シナリオ**: 複数チームがそれぞれ Datastream ストリームを運用しており、ガバナンス担当者が組織全体のレプリケーションパイプラインを把握したい。

**実装例**:
```text
system=Datastream AND type=Stream
```

**効果**: プロジェクトを個別に巡回することなく、Knowledge Catalog の検索だけで全ストリームの一覧・状態・接続先を把握できる。

### ユースケース 2: 自然言語でのパイプライン調査

**シナリオ**: BigQuery を宛先とするストリームに影響するメンテナンスを計画しており、対象のストリームを素早く特定したい。

**実装例**:
```text
List all Datastream streams with BigQuery destination
```

**効果**: 検索構文を覚えていなくても、自然言語クエリで対象ストリームを特定でき、影響範囲の調査が迅速化する。

## 料金

Datastream のテクニカルメタデータを Knowledge Catalog に保存すること自体に料金はかかりません。API 呼び出しや追加のビジネスメタデータ付加 (エンリッチメント) には、標準の Knowledge Catalog 料金が適用されます。詳細は [Knowledge Catalog の料金ページ](https://docs.cloud.google.com/dataplex/pricing) を参照してください。

## 関連サービス・機能

- **Knowledge Catalog (Dataplex)**: メタデータの保存・管理・検索を提供するプラットフォーム。今回の統合先
- **Pub/Sub**: ライブ同期モードでメタデータ変更イベントの配信に使用される
- **Cloud Storage**: バッチ同期モードでメタデータのフルエクスポート (チェックポイント) の格納先として使用される
- **BigQuery**: Datastream の主要な宛先サービス。接続プロファイルのメタデータとしてカタログに登録される

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261030-datastream-knowledge-catalog-ga.html)
- [公式リリースノート](https://docs.cloud.google.com/datastream/docs/release-notes#October_30_2026)
- [ドキュメント: Manage your Datastream resources using Knowledge Catalog](https://docs.cloud.google.com/datastream/docs/knowledge-catalog-integration)
- [Knowledge Catalog のメタデータ管理](https://docs.cloud.google.com/dataplex/docs/catalog-overview)
- [Knowledge Catalog の検索構文](https://docs.cloud.google.com/dataplex/docs/search-syntax)
- [料金ページ (Knowledge Catalog)](https://docs.cloud.google.com/dataplex/pricing)

## まとめ

Datastream と Knowledge Catalog の統合が GA となり、CDC パイプラインのメタデータを組織のデータカタログで自動的かつほぼリアルタイムに管理できるようになりました。テクニカルメタデータの保存は無料のため、Datastream を利用中のチームはまず Dataplex API を有効化し、Knowledge Catalog での検索によるリソースの棚卸しと運用可視化を試すことを推奨します。

---

**タグ**: Datastream, Knowledge Catalog, Dataplex, メタデータ管理, データカタログ, CDC, GA
