# Dataform: Developer Connect による Secure Source Manager リポジトリ連携 (Preview)

**リリース日**: 2026-10-13

**サービス**: Dataform

**機能**: Developer Connect を使用した Secure Source Manager リポジトリとの接続

**ステータス**: Preview

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261013-dataform-developer-connect-secure-source-manager.html)

## 概要

Dataform のリポジトリを、Developer Connect 経由で Secure Source Manager のリポジトリに接続できるようになりました。本機能は Preview として提供されます。

Secure Source Manager は、Google Cloud 上でホストされるシングルテナントのマネージド Git ソースコード管理サービスで、IAM、VPC Service Controls、Cloud Build と密接に統合されています。今回のアップデートにより、BigQuery 向けのデータ変換パイプラインを開発する Dataform のコード (SQLX ファイルなど) を、Google Cloud 内で完結するセキュアな Git リポジトリでバージョン管理できるようになります。

Developer Connect は、外部 Git プロバイダと Google Cloud サービスの連携を仲介するサービスであり、ガイド付きのインターフェースによって手動でのシークレット管理を不要にします。セキュリティ要件やコンプライアンス要件により、ソースコードを外部の Git ホスティングサービスに置けない組織 (金融、公共など FedRAMP High / HIPAA 準拠が必要な環境) にとって、Dataform の Git ワークフローを Google Cloud 内で完結できる選択肢となります。

**アップデート前の課題**

- Dataform のリモート Git リポジトリとして公式にサポートされていたのは GitHub、GitLab、Bitbucket、Azure DevOps Services であり、Secure Source Manager のリポジトリを接続する手段は提供されていなかった
- HTTPS / SSH によるリモートリポジトリ接続では、アクセストークンや SSH 秘密鍵を Secret Manager で手動管理し、Dataform サービスエージェントと共有する必要があった
- ソースコードを Google Cloud の外部に出せない組織では、Dataform のリモート Git 連携 (push / pull) を活用しにくかった

**アップデート後の改善**

- Developer Connect の接続と Git リポジトリリンクを介して、Dataform リポジトリを Secure Source Manager リポジトリに接続できるようになった
- Developer Connect がリポジトリ接続を仲介するため、トークンや SSH 鍵の手動でのシークレット管理が不要になった
- IAM、VPC Service Controls、CMEK に対応した Secure Source Manager 上で、Dataform のコードを Google Cloud 内で完結してバージョン管理できるようになった

## アーキテクチャ図

```mermaid
flowchart LR
    Dev([👤 データエンジニア]) --> WS["🛠️ Dataform<br>開発ワークスペース"]
    WS --> DFRepo["📦 Dataform<br>リポジトリ"]
    DFRepo <--> DC["🔗 Developer Connect<br>接続 + gitRepositoryLink"]
    DC <--> SSM[("🔒 Secure Source Manager<br>インスタンス / リポジトリ")]
    SSM --> CB["⚙️ Cloud Build<br>(CI/CD)"]
    DFRepo --> BQ[("📊 BigQuery")]

    subgraph Google Cloud (同一リージョン)
        DC
        SSM
    end
```

Dataform リポジトリは Developer Connect の接続とリポジトリリンクを介して Secure Source Manager リポジトリと連携します。Developer Connect の接続と Secure Source Manager インスタンスは同一リージョンに配置する必要があります。

## サービスアップデートの詳細

### 主要機能

1. **Secure Source Manager への接続 (Preview)**
   - Developer Connect の接続作成時に、ソースプロバイダとして Secure Source Manager を選択可能
   - 接続作成後、Secure Source Manager インスタンス内のリポジトリを `gitRepositoryLink` としてリンクし、Dataform リポジトリと接続できる

2. **シークレット管理の自動化**
   - Developer Connect がガイド付きインターフェースを提供し、HTTPS / SSH 接続で必要だった Secret Manager でのトークン・鍵の手動管理が不要
   - 認証シークレットの暗号化には、オプションで CMEK (顧客管理の暗号鍵) を利用可能

3. **プライベートネットワーク対応**
   - Secure Source Manager は Private IP と VPC Service Controls によるネットワーク分離に対応
   - Developer Connect の Git プロキシにより、インスタンスをパブリックインターネットに公開せずに Secure Source Manager リポジトリへのセキュアな読み取りアクセスが可能 (Private Google Access に対応)

## 技術仕様

### 接続の要件

| 項目 | 詳細 |
|------|------|
| ステータス | Preview |
| 必要な API | Developer Connect API (`developerconnect.googleapis.com`) |
| リージョン要件 | Developer Connect の接続と Secure Source Manager インスタンスは同一リージョンであること |
| サービスエージェント権限 | Developer Connect の P4SA に `roles/securesourcemanager.developerConnectLinker` を Secure Source Manager インスタンスのプロジェクトで付与 |
| 接続作成に必要なロール | `roles/developerconnect.admin` (接続・リンク作成)、`roles/resourcemanager.projectIamAdmin` (P4SA への権限付与) |
| Git プロキシの制約 | Secure Source Manager との組み合わせでは git の読み取り操作 (clone など) のみサポート。git push はプロキシ非対応 |

### Dataform 側の既存の接続方式との比較

| 接続方式 | シークレット管理 | 対応プロバイダ |
|----------|------------------|----------------|
| Developer Connect (推奨) | 不要 (Developer Connect が管理) | GitHub、GitLab、Bitbucket、**Secure Source Manager (新規・Preview)** |
| HTTPS | Secret Manager でアクセストークンを手動管理 | GitHub、GitLab |
| SSH | Secret Manager で SSH 秘密鍵を手動管理 | GitHub、GitLab、Bitbucket、Azure DevOps Services |

## 設定方法

### 前提条件

1. 稼働中の Secure Source Manager インスタンスが Google Cloud リージョンにデプロイされていること
2. Developer Connect API が有効化されていること
3. Dataform リポジトリが作成済みであること (組織ポリシー `dataform.restrictGitRemotes` でリモートリポジトリを制限している場合は、事前に許可リストへの追加が必要)

### 手順

#### ステップ 1: Developer Connect サービスエージェントの作成と権限付与

```bash
# Developer Connect のサービスエージェント (P4SA) を作成
gcloud beta services identity create \
  --service=developerconnect.googleapis.com \
  --project=PROJECT_ID
```

作成されたサービスエージェントに、Secure Source Manager インスタンスのプロジェクトで `roles/securesourcemanager.developerConnectLinker` ロールを付与します。

#### ステップ 2: Secure Source Manager への Developer Connect 接続を作成

```bash
gcloud developer-connect connections create CONNECTION_ID \
  --location=REGION \
  --project=CONNECTION_PROJECT_ID \
  --secure-source-manager-instance-config=projects/INSTANCE_PROJECT_ID/locations/REGION/instances/INSTANCE_ID
```

接続のリージョンは Secure Source Manager インスタンスと同一リージョンを指定します。Google Cloud コンソールの Developer Connect ページからも、ソースプロバイダとして Secure Source Manager を選択して接続を作成できます。

#### ステップ 3: リポジトリをリンクし Dataform と接続

Developer Connect のリポジトリページで「Link repository」からリポジトリリンクを作成した後、Dataform のリポジトリ設定 (「設定」>「Git に接続」) で「Developer Connect」プロトコルを選択し、リンク済みのリモートリポジトリとデフォルトブランチを指定して接続を完了します。

## メリット

### ビジネス面

- **コンプライアンス対応**: FedRAMP High / HIPAA 認定を持つ Secure Source Manager 上で Dataform のコードを管理でき、規制業界でのデータパイプライン開発に対応しやすくなる
- **Google Cloud 内で完結**: ソースコードを外部 SaaS に出すことなく、データ変換コードのバージョン管理から BigQuery での実行までを Google Cloud 内で完結できる

### 技術面

- **シークレット管理の排除**: HTTPS / SSH 接続で必要だったトークン・SSH 鍵の Secret Manager での手動管理と共有が不要になり、運用負荷と漏洩リスクを低減
- **統一的なアクセス制御**: 開発者とサービスアカウントのロールを単一の IAM で管理でき、VPC Service Controls による境界防御とも組み合わせられる

## デメリット・制約事項

### 制限事項

- 本機能は Preview であり、GA 前の機能として提供される
- Developer Connect の接続と Secure Source Manager インスタンスは同一リージョンに作成する必要がある
- Secure Source Manager との Developer Connect プロキシは git の読み取り操作 (clone など) のみをサポートし、プロキシ経由の git push はサポートされない
- 既存の接続を別の Secure Source Manager インスタンスに向け直すことはできない (プロキシの有効 / 無効などの設定変更は可能)

### 考慮すべき点

- Dataform リポジトリと Developer Connect の接続が異なるリージョンにある場合、プロキシ有効時にリージョン間データ転送費用が発生する可能性がある
- Developer Connect のサービスエージェントへの `roles/securesourcemanager.developerConnectLinker` 付与など、プロジェクトをまたぐ IAM 設定が必要になるため、権限設計を事前に整理しておく

## ユースケース

### ユースケース 1: 規制業界でのセキュアなデータ変換パイプライン開発

**シナリオ**: 金融機関のデータチームが、BigQuery 上のデータ変換 (ELT) を Dataform で開発している。コンプライアンス上、ソースコードを外部の Git ホスティングサービスに置くことができない。

**効果**: Secure Source Manager を VPC Service Controls の境界内に配置し、Dataform から Developer Connect 経由で接続することで、SQLX コードのバージョン管理・プルリクエストベースのレビューを Google Cloud 内で完結できる。

### ユースケース 2: Google Cloud ネイティブな CI/CD との統合

**シナリオ**: Cloud Source Repositories からの移行先として Secure Source Manager を採用し、Cloud Build と組み合わせた CI/CD を構築しているチームが、Dataform のコードも同じリポジトリ基盤で管理したい。

**効果**: Dataform のコードを Secure Source Manager に集約し、ブランチ保護ルール (レビュー必須、ステータスチェック必須) や Cloud Build トリガーと組み合わせた、統一的な開発ワークフローを実現できる。

## 料金

- **Dataform**: Dataform 自体の利用に伴う本機能固有の追加料金に関する公式情報は、リリースノートでは言及されていません
- **Secure Source Manager**: インスタンスごとに月額 $1,000 (公式製品ページ記載)
- **Developer Connect**: Dataform リポジトリと接続が異なるリージョンの場合、プロキシ有効時にリージョン間データ転送費用が発生する可能性があります。詳細は [Developer Connect の料金ページ](https://cloud.google.com/developer-connect/pricing) を参照してください

## 関連サービス・機能

- **Developer Connect**: 外部 Git プロバイダと Google Cloud サービスの接続を仲介し、シークレット管理を自動化するサービス。本アップデートの中核
- **Secure Source Manager**: シングルテナントのマネージド Git リポジトリサービス。IAM / VPC Service Controls / CMEK / Cloud Build と統合
- **BigQuery**: Dataform が変換パイプラインを実行する対象のデータウェアハウス
- **Cloud Build**: Secure Source Manager のトリガーファイルや Developer Connect の `gitRepositoryLink` と連携して CI/CD を構成可能
- **VPC Service Controls / Private Google Access**: Secure Source Manager をプライベートネットワーク内に閉じたまま利用するためのネットワーク制御機能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261013-dataform-developer-connect-secure-source-manager.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#October_13_2026)
- [Dataform: リモートリポジトリへの接続](https://docs.cloud.google.com/dataform/docs/connect-repository)
- [Developer Connect: Secure Source Manager への接続](https://docs.cloud.google.com/developer-connect/docs/connect-secure-source-manager)
- [Secure Source Manager 概要](https://docs.cloud.google.com/secure-source-manager/docs/overview)
- [Developer Connect 料金ページ](https://cloud.google.com/developer-connect/pricing)

## まとめ

Dataform のリポジトリを Developer Connect 経由で Secure Source Manager に接続できるようになり、データ変換コードのバージョン管理を Google Cloud 内で完結させる選択肢が加わりました。外部 Git サービスを利用できないセキュリティ・コンプライアンス要件を持つ組織は、Preview 段階である点とプロキシが読み取り専用である点に留意しつつ、検証環境での試用を検討することを推奨します。

---

**タグ**: Dataform, Developer Connect, Secure Source Manager, BigQuery, Git, DevOps, Preview
