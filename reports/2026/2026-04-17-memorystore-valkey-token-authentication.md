# Memorystore for Valkey: Basic Token-Based Authentication

**リリース日**: 2026-04-17

**サービス**: Memorystore for Valkey

**機能**: Basic Token-Based Authentication (基本トークンベース認証)

**ステータス**: Preview

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260417-memorystore-valkey-token-authentication.html)

## 概要

Memorystore for Valkey に基本トークンベース認証 (Basic Token-Based Authentication) 機能が Preview として追加されました。この機能により、既存の IAM 認証に加えて、軽量なトークンベースの認証方式を使用してインスタンスへのアクセスを保護できるようになります。

基本トークンベース認証は、クライアントがトークンを使用してアイデンティティを検証する軽量なソリューションです。リソース要件が最小限であり、リソースオーバーヘッドも低いことが特徴です。特に、Memorystore for Redis やオンプレミス環境で既に基本トークンベース認証を使用しているワークロードがある場合、Memorystore for Valkey への移行をスムーズに行うことができます。

この機能は、シンプル認証 (デフォルトユーザーとしてトークンで認証) とマルチユーザー認証 (複数ユーザーによるアクセス管理) の 2 つの認証モードをサポートしています。新規インスタンスの作成時に有効化するだけでなく、既存のインスタンスに対しても随時有効化できます。

**アップデート前の課題**

Memorystore for Valkey のインスタンスへのアクセス制御は IAM 認証のみが利用可能でした。

- IAM 認証はアクセストークンの有効期限が短く (1 時間)、アプリケーション側でのトークン自動更新ロジックが必要だった
- Memorystore for Redis からの移行時に、既存のパスワード (AUTH) ベースの認証方式をそのまま引き継ぐことができなかった
- オンプレミスの Redis/Valkey 環境で使用していたシンプルなトークン認証を Memorystore for Valkey で再現できなかった

**アップデート後の改善**

- IAM 認証に加えて、軽量なトークンベース認証が選択肢として利用可能になった
- Memorystore for Redis やオンプレミス環境からの移行時に、既存の認証方式との後方互換性が確保された
- ゼロダウンタイムでのトークンローテーションにより、運用中のアプリケーションを停止せずにセキュリティ管理が可能になった
- 最大 1,000 のローカルユーザーを管理でき、マルチユーザー認証によるきめ細かなアクセス制御が可能になった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Client["クライアントアプリケーション"]
        App["アプリケーション"]
        SM["Secret Manager\n(トークン保管)"]
    end

    subgraph Auth["認証モード"]
        Simple["シンプル認証\n(デフォルトユーザー + トークン)"]
        Multi["マルチユーザー認証\n(ユーザー名 + トークン)"]
    end

    subgraph Memorystore["Memorystore for Valkey"]
        Instance[("Valkey インスタンス\n--authorization-mode=token-auth")]
        Default["デフォルトユーザー\n(自動作成)"]
        Users["ローカルユーザー\n(最大 1,000)"]
    end

    App -->|"トークン取得"| SM
    App -->|"AUTH トークン"| Simple
    App -->|"AUTH ユーザー名 + トークン"| Multi
    Simple --> Instance
    Multi --> Instance
    Instance --> Default
    Instance --> Users
```

クライアントアプリケーションは Secret Manager からトークンを取得し、シンプル認証またはマルチユーザー認証のいずれかの方式で Memorystore for Valkey インスタンスに接続します。インスタンスではデフォルトユーザーが自動作成され、追加のローカルユーザーも管理できます。

## サービスアップデートの詳細

### 主要機能

1. **シンプル認証 (Simple Authentication)**
   - デフォルトユーザーとしてトークンのみで認証する方式
   - インスタンス作成時または有効化時にデフォルトユーザーとトークンが自動生成される
   - 最もシンプルな認証方式で、単一ユーザーのアクセス制御に適している

2. **マルチユーザー認証 (Multi-user Authentication)**
   - ユーザー名とトークンの組み合わせで認証する方式
   - 複数のユーザーを作成し、それぞれに個別のトークンを割り当てることが可能
   - ユーザーごとのアクセス制御が必要な環境に適している

3. **ゼロダウンタイムトークンローテーション**
   - 各ユーザーは最大 2 つの認証トークンを保持可能
   - 新しいトークンを作成し、アプリケーションを更新してから古いトークンを削除することで、ダウンタイムなしのローテーションが可能
   - セキュリティポリシーに準拠した定期的なトークン更新を運用に組み込める

4. **監査ログ連携**
   - 認証トークンとユーザーに関連する操作について Admin Activity および Data Access 監査ログが生成される
   - Cloud Audit Logs との統合により、アクセスの監視と監査が可能

## 技術仕様

### 認証方式の比較

| 項目 | 基本トークンベース認証 (今回追加) | IAM 認証 (既存) |
|------|------|------|
| ステータス | Preview | GA |
| 認証方法 | ユーザー名 + トークン | IAM アクセストークン |
| トークン有効期間 | 明示的に削除するまで有効 | 1 時間 (自動更新が必要) |
| ユーザー管理 | 最大 1,000 ローカルユーザー | IAM プリンシパルで管理 |
| 接続方式 | URI 文字列またはフラグ | IAM トークン + valkey-cli |
| 無効化 | 有効化後は無効化不可 | インスタンスごとに設定可能 |
| Redis 互換性 | 高い (AUTH コマンド互換) | Redis とは異なる方式 |

### 接続方法

**URI 文字列を使用した接続:**

```bash
valkey-cli -u redis://USERNAME:TOKEN@IP_ADDRESS:PORT
```

**フラグを使用した接続:**

```bash
valkey-cli --user USERNAME -a TOKEN -h IP_ADDRESS -p PORT
```

## 設定方法

### 前提条件

1. Google Cloud プロジェクトで Memorystore for Valkey API が有効化されていること
2. `gcloud` CLI がインストールされていること
3. 適切な IAM 権限が付与されていること

### 手順

#### ステップ 1: 新規インスタンスでトークンベース認証を有効化して作成

```bash
gcloud beta memorystore instances create INSTANCE_ID \
  --location=REGION \
  --authorization-mode=token-auth
```

`INSTANCE_ID` はインスタンス ID、`REGION` はインスタンスを配置するリージョンに置き換えてください。

#### ステップ 2: 既存インスタンスでトークンベース認証を有効化

```bash
gcloud beta memorystore instances update INSTANCE_ID \
  --location=REGION \
  --authorization-mode=token-auth
```

有効化後、デフォルトユーザーとトークンが自動生成されます。既存の接続には影響ありませんが、新しい接続には認証が必要になります。

#### ステップ 3: 追加ユーザーの作成

```bash
gcloud beta memorystore instances create-token-auth-user INSTANCE_ID \
  --location=REGION \
  --token-auth-user=USERNAME
```

ユーザー作成時にトークンが自動生成されます。

#### ステップ 4: トークンのローテーション (ゼロダウンタイム)

```bash
# 1. 新しいトークンを作成 (両方のトークンが有効)
gcloud beta memorystore instances token-auth-users create-auth-token USERNAME \
  --instance=INSTANCE_ID \
  --location=REGION

# 2. アプリケーションを新しいトークンに更新

# 3. 古いトークンを削除
gcloud beta memorystore instances token-auth-users auth-tokens delete AUTH_TOKEN \
  --instance=INSTANCE_ID \
  --location=REGION \
  --token-auth-user=USERNAME
```

## メリット

### ビジネス面

- **移行コストの削減**: Memorystore for Redis やオンプレミス環境からの移行時に、既存の認証方式との後方互換性により、アプリケーション側の変更を最小限に抑えられる
- **運用負荷の軽減**: ゼロダウンタイムでのトークンローテーションにより、計画的なメンテナンスウィンドウが不要

### 技術面

- **軽量な認証**: リソース要件が最小限であり、IAM 認証と比較してオーバーヘッドが低い
- **柔軟なユーザー管理**: 最大 1,000 のローカルユーザーをサポートし、マルチテナント環境でのきめ細かなアクセス制御が可能
- **監査対応**: Admin Activity および Data Access 監査ログとの統合により、コンプライアンス要件への対応が容易

## デメリット・制約事項

### 制限事項

- 現在 Preview ステータスであり、本番環境での利用には Pre-GA の利用規約が適用される
- 有効化後は無効化できないため、設定変更は慎重に判断する必要がある
- デフォルトユーザーは削除できない
- 各ユーザーが保持できるトークンは最大 2 つまで
- `gcloud beta` コマンドを使用する必要がある (GA 版コマンドは未対応)

### 考慮すべき点

- トークンベース認証を有効化すると、新しいクライアント接続には認証が必須となるため、既存アプリケーションの更新が必要
- セキュリティベストプラクティスとして、TLS (In-Transit Encryption) と組み合わせて使用することが推奨される (トークンが平文で送信されることを防止)
- トークンはアプリケーションコードにハードコードせず、Secret Manager に保管することが推奨される

## ユースケース

### ユースケース 1: Memorystore for Redis からの移行

**シナリオ**: 既存の Memorystore for Redis インスタンスで AUTH パスワードベースの認証を使用しており、Memorystore for Valkey へ移行したい場合。

**実装例**:
```bash
# Valkey インスタンスをトークンベース認証で作成
gcloud beta memorystore instances create my-valkey-instance \
  --location=asia-northeast1 \
  --authorization-mode=token-auth

# アプリケーションの接続設定を更新
valkey-cli -u redis://default:TOKEN@INSTANCE_IP:6379
```

**効果**: 既存の AUTH コマンド互換の認証方式を維持しつつ、Valkey の新機能を活用できる。アプリケーション側の認証ロジックの変更が最小限で済む。

### ユースケース 2: マルチテナント環境でのアクセス制御

**シナリオ**: 複数のマイクロサービスが同一の Memorystore for Valkey インスタンスにアクセスする環境で、サービスごとに異なる認証情報を割り当てたい場合。

**効果**: 各サービスに固有のユーザーとトークンを割り当てることで、アクセスの追跡と制御が容易になる。不正アクセスの発生時にも、該当ユーザーのトークンのみを無効化することで影響範囲を限定できる。

## 料金

基本トークンベース認証の利用に追加料金は発生しません。Memorystore for Valkey の通常のインスタンス料金が適用されます。

料金はノードタイプ、シャード数、リプリカ数に基づいて計算されます。Committed Use Discounts (CUD) を利用することで、1 年契約で 20%、3 年契約で 40% の割引が適用されます。

詳細な料金情報については [Memorystore for Valkey の料金ページ](https://cloud.google.com/memorystore/valkey/pricing) を参照してください。

## 利用可能リージョン

基本トークンベース認証は、Memorystore for Valkey が利用可能なすべてのリージョンで使用できます。主なリージョンは以下の通りです。

- **アジア太平洋**: asia-northeast1 (東京)、asia-northeast2 (大阪)、asia-northeast3 (ソウル)、asia-east1 (台湾)、asia-south1 (ムンバイ)、asia-southeast1 (シンガポール)、australia-southeast1 (シドニー) など
- **米国**: us-central1 (アイオワ)、us-east1 (サウスカロライナ)、us-west1 (オレゴン) など
- **ヨーロッパ**: europe-west1 (ベルギー)、europe-west3 (フランクフルト)、europe-north1 (フィンランド) など

全リージョン一覧は [Memorystore for Valkey のロケーション](https://cloud.google.com/memorystore/docs/valkey/locations) を参照してください。

## 関連サービス・機能

- **IAM 認証 (Memorystore for Valkey)**: 既存の認証方式。IAM ポリシーによるアクセス制御を提供。基本トークンベース認証とは異なるアプローチで、組織レベルのアクセス管理に適している
- **Secret Manager**: トークンの安全な保管と取得に推奨されるサービス。認証トークンをアプリケーションコードにハードコードすることを避けるために使用
- **In-Transit Encryption (TLS)**: 基本トークンベース認証と組み合わせて使用することが推奨される。トークンがネットワーク上で平文送信されることを防止
- **Cloud Audit Logs**: 認証トークンとユーザー操作の監査ログを提供。セキュリティ監視とコンプライアンス対応に活用
- **Memorystore for Redis**: 移行元として想定されるサービス。基本トークンベース認証により、Redis の AUTH 方式からのスムーズな移行が可能

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260417-memorystore-valkey-token-authentication.html)
- [公式リリースノート](https://cloud.google.com/release-notes#April_17_2026)
- [基本トークンベース認証の管理 - ドキュメント](https://cloud.google.com/memorystore/docs/valkey/manage-basic-auth)
- [IAM 認証について](https://cloud.google.com/memorystore/docs/valkey/about-iam-auth)
- [In-Transit Encryption について](https://cloud.google.com/memorystore/docs/valkey/about-in-transit-encryption)
- [料金ページ](https://cloud.google.com/memorystore/valkey/pricing)

## まとめ

Memorystore for Valkey に基本トークンベース認証が Preview として追加されたことで、IAM 認証に加えて軽量で広くサポートされた認証方式が利用可能になりました。特に Memorystore for Redis やオンプレミス環境からの移行を検討している場合、後方互換性のある認証方式によりスムーズな移行が実現できます。Preview ステータスであるため本番環境への導入は慎重に検討する必要がありますが、開発・検証環境での評価を開始し、GA 昇格に備えることを推奨します。

---

**タグ**: #Memorystore #Valkey #Authentication #Security #TokenAuth #Preview #Migration #Redis
