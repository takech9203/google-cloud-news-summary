# Memorystore for Valkey: アクセス制御リスト (ACL) ポリシーが GA に

**リリース日**: 2026-08-31

**サービス**: Memorystore for Valkey

**機能**: アクセス制御リスト (ACL) ポリシーによるインスタンスアクセスの保護

**ステータス**: GA (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260831-memorystore-valkey-acl-ga.html)

## 概要

Memorystore for Valkey で、アクセス制御リスト (ACL) ポリシーを使用してインスタンスへのアクセスを保護する機能が一般提供 (GA) になりました。ACL ポリシーを定義することで、ユーザーやサービスアカウントがアクセスできる対象を特定のキー、コマンド、操作、Pub/Sub チャネルに制限する、きめ細かなセキュリティ制御を実現できます。

ACL ポリシーは `gcloud memorystore acl-policies` コマンドグループ (memorystore/v1 API) で管理するロケーションスコープのリソースです。ポリシーには「ユーザー名 + ACL ルール文字列」の組み合わせを複数登録でき、ルールの記法は Valkey OSS の ACL 仕様 (https://valkey.io/topics/acl/) に準拠します。ユーザー名には IAM ユーザーまたはサービスアカウントを指定でき、指定したユーザー名がそのまま Valkey OSS 側に設定されます。

複数のアプリケーションやチームが 1 つのインスタンスを共有する環境で、最小権限の原則に基づいたデータプレーンのアクセス制御を求めるユーザーに特に有用なアップデートです。なお、同日に Memorystore for Redis Cluster でも同様の ACL 機能が GA になっています (別レポート: `2026-08-31-memorystore-redis-cluster-acl-ga.md` で解説)。

**アップデート前の課題**

- Valkey OSS ネイティブの ACL 管理コマンド (`ACL SETUSER`、`ACL GETUSER`、`ACL LIST` など) は Memorystore for Valkey ではブロックされており (NOPERM エラー)、ユーザーが自身で Valkey ACL を構成する手段がなかった
- IAM 認証では "default" が唯一サポートされるユーザー名であり、ユーザーごとに権限を分離するきめ細かな制御ができなかった
- 公式のセキュリティベストプラクティスでは、ACL の実装をアプリケーション側の仲介レイヤーで行うことが推奨されており、ユーザー自身で制御ロジックを構築・運用する必要があった
- 接続を許可されたクライアントは、インスタンス内の広範なキーやコマンドにアクセスできてしまい、共有インスタンスでの最小権限の徹底が困難だった

**アップデート後の改善**

- ACL ポリシーをマネージドなリソースとして作成し、ユーザーごとにアクセス可能なキーパターン、コマンド、操作、Pub/Sub チャネルを制限できるようになった
- Valkey OSS 準拠の ACL ルール記法 (`on ~keys:* +get` など) をそのまま使用でき、既存の Valkey/Redis 運用知識を活かせる
- `gcloud memorystore acl-policies` の create / update (`--rules` / `--add-rules` / `--remove-rules` / `--clear-rules`) コマンドにより、ポリシーのライフサイクルを CLI / API で一元管理できるようになった
- GA となったことで、本番ワークロードでの利用が可能になった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Policy["📜 ACL ポリシー (ロケーションリソース)"]
        R1["👤 user1: on ~keys:* +get<br/>(特定キーの読み取りのみ)"]
        R2["👤 svc-a@...: on ~svc-a:* +@read +@write<br/>(自分のキー空間のみ)"]
    end

    Admin(["🧑‍💼 管理者"]) -->|"gcloud memorystore acl-policies<br/>create / update"| Policy
    Policy -->|適用| Instance[("🗄️ Memorystore for<br/>Valkey インスタンス")]

    App1(["📱 アプリ A (user1)"]) -->|"GET keys:*<br/>✅ 許可"| Instance
    App2(["📱 アプリ B"]) -->|"FLUSHALL / 他ユーザーのキー<br/>❌ 拒否"| Instance
```

管理者が ACL ポリシーにユーザーごとのルールを定義してインスタンスに適用することで、各アプリケーション・サービスのアクセスを特定のキー、コマンド、操作、Pub/Sub チャネルに制限できます。

## サービスアップデートの詳細

### 主要機能

1. **きめ細かなアクセス制限**
   - ユーザーおよびサービスのアクセスを、特定のキー、コマンド、操作、Pub/Sub チャネルに制限可能
   - Valkey OSS の ACL ルール記法に準拠したルール文字列で権限を表現 (例: `on ~keys:* +get`)

2. **ACL ポリシーのライフサイクル管理**
   - `gcloud memorystore acl-policies` コマンドグループで作成・更新が可能 (memorystore/v1 API。beta / alpha 版コマンドも利用可能)
   - 作成時は `--rules` (必須) でユーザーごとのルールを登録
   - 更新時は `--rules` (全置換) に加え、`--add-rules` / `--remove-rules` / `--clear-rules` による差分更新に対応
   - `--request-id` による冪等なリクエスト、`--async` による非同期実行に対応

3. **IAM ユーザー / サービスアカウントとの統合**
   - ルールの `username` には IAM ユーザーまたはサービスアカウントを指定
   - 指定したユーザー名は Valkey OSS 側にそのまま設定される

## 技術仕様

### ACL ポリシーの構成要素

| 項目 | 詳細 |
|------|------|
| リソーススコープ | ロケーション (`--location` で指定) |
| ルールの構成 | `username` (IAM ユーザー / サービスアカウント) + `rule` (ACL ルール文字列) |
| ルール記法 | Valkey OSS の ACL 仕様 (valkey.io/topics/acl) に準拠 |
| 制限対象 | キー、コマンド、操作、Pub/Sub チャネル |
| 管理 API | memorystore/v1 API (GA)。beta (v1beta) / alpha (v1alpha) 版も利用可能 |
| 冪等性 | `--request-id` による冪等なリクエストに対応 |

### ACL ルールの指定形式

```bash
# ショートハンド形式
--rules="username=USERNAME,rule=RULE"

# JSON 形式
--rules='[{"rule": "string", "username": "string"}]'

# ファイル形式 (YAML / JSON)
--rules=path_to_file.yaml
```

## 設定方法

### 前提条件

1. Memorystore for Valkey のインスタンスが作成済みであること
2. gcloud CLI が利用可能で、対象プロジェクト・ロケーションに対する適切な IAM 権限があること

### 手順

#### ステップ 1: ACL ポリシーを作成する

```bash
gcloud memorystore acl-policies create my-acl-policy \
  --location=us-east1 \
  --rules="username=user1,rule='on ~keys:* +get'"
```

ユーザーごとのルールを含む ACL ポリシーを作成します。`--rules` フラグを複数回指定することで、複数のルールを 1 つのポリシーに登録できます。

#### ステップ 2: ACL ポリシーを更新する

```bash
# ルールを追加
gcloud memorystore acl-policies update my-acl-policy \
  --location=us-east1 \
  --add-rules="username=svc-a@project.iam.gserviceaccount.com,rule='on ~svc-a:* +@read +@write'"

# ルールを削除
gcloud memorystore acl-policies update my-acl-policy \
  --location=us-east1 \
  --remove-rules="username=user1,rule='on ~keys:* +get'"
```

運用中のポリシーに対して、ルールの追加 (`--add-rules`)・削除 (`--remove-rules`)・全置換 (`--rules`)・全クリア (`--clear-rules`) が可能です。

## メリット

### ビジネス面

- **コンプライアンス対応の強化**: データプレーンでの最小権限の原則を実現でき、監査・セキュリティ要件への対応が容易になる
- **インスタンス共有によるコスト効率**: アクセス境界をポリシーで分離できるため、複数チーム・アプリケーションで 1 つのインスタンスを安全に共有しやすくなる

### 技術面

- **アプリケーション側の実装不要**: 従来ベストプラクティスとして推奨されていた「アプリケーション仲介レイヤーでの ACL 実装」を、マネージドな ACL ポリシーで代替できる
- **Valkey OSS 互換の記法**: 標準的な Valkey ACL ルールをそのまま利用でき、学習コストが低い
- **宣言的な管理**: gcloud CLI / API でルールをショートハンド・JSON・ファイル形式で宣言的に管理できる

## デメリット・制約事項

### 制限事項

- Valkey OSS ネイティブの ACL 管理コマンド (`ACL SETUSER`、`ACL LIST` など) は引き続きインスタンス上でブロックされており、ACL の管理は必ずマネージドな ACL ポリシーリソース経由で行う

### 考慮すべき点

- ACL ポリシーはロケーションスコープのリソースであり、ロケーション (リージョン) ごとに管理が必要
- ルール文字列は Valkey OSS の ACL 仕様に準拠するため、正しい権限設計には Valkey ACL 記法の理解が必要
- ACL はネットワーク分離 (Private Service Connect) や IAM による管理プレーン制御を置き換えるものではなく、これらと組み合わせた多層防御として利用する

## ユースケース

### ユースケース 1: マルチテナントの共有キャッシュインスタンス

**シナリオ**: 複数のマイクロサービスが 1 つの Memorystore for Valkey インスタンスをキャッシュとして共有しており、各サービスが自分のキー空間 (プレフィックス) のみにアクセスできるようにしたい。

**実装例**:
```bash
gcloud memorystore acl-policies create shared-cache-policy \
  --location=asia-northeast1 \
  --rules="username=svc-a@project.iam.gserviceaccount.com,rule='on ~svc-a:* +@read +@write'" \
  --rules="username=svc-b@project.iam.gserviceaccount.com,rule='on ~svc-b:* +@read +@write'"
```

**効果**: サービス間のキー空間の分離が強制され、あるサービスの不具合や侵害が他サービスのデータに波及するリスクを低減できる。

### ユースケース 2: Pub/Sub チャネル単位のアクセス制御

**シナリオ**: Valkey の Pub/Sub 機能を軽量メッセージブローカーとして使用しており、サービスごとに購読・発行できるチャネルを限定したい。

**効果**: ACL ポリシーで Pub/Sub チャネルへのアクセスをユーザー単位で制限でき、意図しないチャネルへのメッセージ発行・購読を防止できる。

### ユースケース 3: 読み取り専用アクセスの提供

**シナリオ**: 分析用のバッチジョブやダッシュボードには、特定のキーに対する読み取り専用アクセスのみを許可したい。

**効果**: 読み取り専用ユーザーによる誤った書き込みや危険なコマンド (FLUSHALL など) の実行を ACL レベルで防止できる。

## 料金

ACL ポリシー機能自体に関する追加料金の記載はリリースノートにはありません。Memorystore for Valkey の料金の詳細は、公式の料金ページを参照してください。

- [Memorystore for Valkey 料金ページ](https://cloud.google.com/memorystore/docs/valkey/pricing)

## 利用可能リージョン

ACL ポリシーはロケーション (リージョン) スコープのリソースとして作成します。Memorystore for Valkey が利用可能なリージョンについては、[公式ドキュメント](https://cloud.google.com/memorystore/docs/valkey)を参照してください。

## 関連サービス・機能

- **Memorystore for Redis Cluster**: 同日 (2026-08-31) に同様の ACL ポリシー機能が GA になっている (別レポート: `2026-08-31-memorystore-redis-cluster-acl-ga.md`)
- **IAM 認証 (Memorystore for Valkey)**: 管理プレーンおよび接続認証 (`memorystore.instances.connect` / `roles/memorystore.dbConnectionUser`) のアクセス制御を担う。ACL はデータプレーンのきめ細かな制御を補完する
- **Private Service Connect**: Memorystore for Valkey インスタンスへのネットワークアクセスを制限する接続基盤。ACL と組み合わせることで多層防御を構成できる
- **Valkey 9.1 (Preview)**: データベースレベルの ACL によるアクセス制御など、ACL 関連機能の拡充が続いている

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260831-memorystore-valkey-acl-ga.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#August_31_2026)
- [Memorystore for Valkey リリースノート](https://docs.cloud.google.com/memorystore/docs/valkey/release-notes)
- [gcloud memorystore acl-policies create リファレンス](https://docs.cloud.google.com/sdk/gcloud/reference/memorystore/acl-policies/create)
- [gcloud memorystore acl-policies update リファレンス](https://docs.cloud.google.com/sdk/gcloud/reference/memorystore/acl-policies/update)
- [Memorystore for Valkey セキュリティ概要](https://docs.cloud.google.com/memorystore/docs/valkey/security-overview)
- [Access control with IAM (Memorystore for Valkey)](https://docs.cloud.google.com/memorystore/docs/valkey/access-control)
- [Valkey OSS ACL ドキュメント](https://valkey.io/topics/acl/)
- [料金ページ](https://cloud.google.com/memorystore/docs/valkey/pricing)

## まとめ

Memorystore for Valkey の ACL ポリシーが GA となり、これまでネイティブ ACL コマンドがブロックされていたためアプリケーション側で実装する必要があったキー・コマンド・Pub/Sub チャネル単位のきめ細かなアクセス制御を、マネージドなポリシーとして本番環境で利用できるようになりました。共有インスタンスを運用しているチームは、`gcloud memorystore acl-policies` でポリシーを定義し、最小権限の原則に基づいたデータプレーンのアクセス制御への移行を検討することを推奨します。

---

**タグ**: #Memorystore #Valkey #ACL #セキュリティ #アクセス制御 #GA
