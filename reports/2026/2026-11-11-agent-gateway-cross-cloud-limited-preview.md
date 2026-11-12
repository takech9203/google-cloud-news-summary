# Gemini Enterprise Agent Platform: Agent Gateway for cross-cloud (Limited Preview)

**リリース日**: 2026-11-11

**サービス**: Gemini Enterprise Agent Platform

**機能**: CNCF 準拠 Kubernetes クラスタ上のエージェントを Agent Gateway for cross-cloud でガバナンス

**ステータス**: Limited Preview

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261111-agent-gateway-cross-cloud-limited-preview.html)

## 概要

Gemini Enterprise Agent Platform の **Agent Gateway for cross-cloud** が Limited Preview として発表されました。この機能は、Agent Platform のガバナンス機能を Google Cloud の外部で稼働する CNCF (Cloud Native Computing Foundation) 準拠の Kubernetes クラスタ上のエージェントにまで拡張するものです。対象となる環境には Amazon Elastic Kubernetes Service (Amazon EKS)、Azure Kubernetes Service (AKS)、Red Hat OpenShift、ベアメタルクラスタが含まれます。

最大の特徴は「エージェントは今の場所で動かし続けながら、ガバナンスは 1 か所 (Google Cloud) から行う」という点です。各エージェントに検証可能なアイデンティティを付与し、エージェントと MCP サーバーを Agent Registry に登録し、LLM / MCP / A2A (Agent-to-Agent) のトラフィックを既存のサービスメッシュやネットワークスタックを利用してローカルの Agent Gateway プロキシ経由でルーティングします。プロキシはアクセス制御と Model Armor の安全性ポリシーを適用し、アクセスログとエージェントトレースを Cloud Logging と Cloud Trace に送信します。

マルチクラウドや自社データセンターでエージェントを運用しつつ、1 つのガバナンスポリシー・1 つのレジストリ・1 つの可観測性ビューで全エージェントを統制したいエンタープライズの、プラットフォームチームやセキュリティチームが主な対象です。利用には[アクセス申請フォーム](https://docs.google.com/forms/d/e/1FAIpQLSeUpnNRtYQjLRblii-KoUbJJ7DjEV6fvQAfO21IAXgVSqFjpw/viewform)からのリクエストが必要です。

**アップデート前の課題**

- Agent Gateway は Google Cloud 上のランタイム (Agent Runtime、Gemini Enterprise) で稼働するエージェント向けに提供されており、Google Cloud 外の Kubernetes クラスタで稼働するエージェントは Agent Platform のガバナンス (Agent Identity、Agent Registry、ポリシー適用) の対象外だった
- EKS / AKS / OpenShift / ベアメタルなどに分散したエージェントに対しては、クラウドごと・環境ごとに個別のアクセス制御や安全性対策を実装する必要があり、ポリシーの一貫性を保つことが難しかった
- Google Cloud 外のエージェントのアクセスログやトレースを Cloud Logging / Cloud Trace に集約する標準的な仕組みがなく、エージェント活動の統一的な可視化が困難だった

**アップデート後の改善**

- CNCF 準拠の Kubernetes クラスタであれば、Google Cloud 外 (EKS、AKS、OpenShift、ベアメタル) のエージェントも Agent Platform のガバナンス対象に含められるようになった
- Workload Identity Federation により Kubernetes のワークロード認証情報を Agent Identity 認証情報と交換し、各エージェントに検証可能なアイデンティティを付与できるようになった
- Google Cloud の管理プレーンで一元定義したアクセスポリシーと Model Armor 安全性ポリシーを、クラスタ内のローカル Agent Gateway プロキシ (Envoy ベース) が適用する構成が可能になった
- 外部クラスタ上のエージェントのアクセスログとトレースが Cloud Logging / Cloud Trace に送信され、Agent Registry / Agent Observability を全エージェントに拡張できるようになった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph GC["☁️ Google Cloud (管理プレーン)"]
        REG["📒 Agent Registry<br>(エージェント / MCP サーバー登録)"]
        POL["🛡️ ポリシー定義<br>(アクセス制御 / Model Armor)"]
        WIF["🔑 Workload Identity Federation<br>(Agent Identity 発行)"]
        OBS["📊 Cloud Logging / Cloud Trace<br>(アクセスログ / トレース)"]
    end

    subgraph EXT["🌐 外部 Kubernetes クラスタ (EKS / AKS / OpenShift / ベアメタル)"]
        AGENT(["🤖 エージェント"])
        GW["🚪 Agent Gateway プロキシ<br>(Envoy ベース / ローカル適用)"]
        DEST["🧰 LLM / MCP / A2A 宛先"]
    end

    AGENT -->|"既存のサービスメッシュ /<br>ネットワーク経由でルーティング"| GW
    GW -->|ポリシー適用後に転送| DEST
    GW -.->|K8s 認証情報を交換| WIF
    GW -.->|ポリシーチェック (Model Armor など)| POL
    GW -.->|ログ / トレース送信| OBS
    REG -.->|登録情報を参照| GW
```

Google Cloud 側の管理プレーンでアイデンティティ・レジストリ・ポリシーを一元管理し、外部クラスタ内にデプロイした Envoy ベースの Agent Gateway プロキシがローカルでポリシーを適用します。エージェントのトラフィック自体は外部環境内に留まり、Model Armor スクリーニングなど設定したポリシーチェックのみが Google Cloud に送信されます。

## サービスアップデートの詳細

### 主要機能

1. **CNCF 準拠 Kubernetes クラスタへのガバナンス拡張**
   - Amazon EKS、Azure AKS、Red Hat OpenShift、自社データセンターのベアメタルクラスタなど、Google Cloud 外の Kubernetes クラスタ上のエージェントが対象
   - エージェントの稼働場所を変えずに、Google Cloud からガバナンスを一元管理
   - 軽量な Envoy ベースの Agent Gateway プロキシと関連コンポーネントを自身のクラスタにデプロイする自己管理型プロキシモデル

2. **検証可能なエージェントアイデンティティ**
   - Workload Identity Federation を通じて Kubernetes ワークロード認証情報を Agent Identity 認証情報と交換
   - 各エージェントに検証可能なアイデンティティを付与し、アイデンティティベースのアクセス制御を実現

3. **Agent Registry への登録と Agent-to-Anywhere トラフィックのガバナンス**
   - 外部クラスタ上のエージェントと MCP サーバーを Agent Registry に登録
   - LLM、MCP、A2A トラフィックを既存のサービスメッシュ / ネットワークスタックでローカルの Agent Gateway プロキシへルーティング
   - 中央で定義したアクセスポリシーと Model Armor 安全性ポリシーをプロキシが適用

4. **Agent Observability の拡張**
   - アクセスログを Cloud Logging へ、エージェントトレースを Cloud Trace へ送信
   - マルチクラウドに分散したエージェント活動を Google Cloud 上で統一的に可視化

## 技術仕様

### デプロイモデルにおける位置づけ

| 項目 | 詳細 |
|------|------|
| エージェントホスト環境 | Google Cloud 外の CNCF 準拠 Kubernetes クラスタ (EKS / AKS / OpenShift / ベアメタルなど) |
| プロキシインフラ | 自身のクラスタにデプロイする自己管理型の Envoy ベースプロキシ |
| 管理プレーン | Google Cloud 側でエージェントアイデンティティ、Agent Registry エントリ、ポリシーを定義 |
| トラフィックの扱い | エージェントトラフィックは自環境内に留まり、設定したポリシーチェック (Model Armor など) のみ Google Cloud に送信 |
| ネットワーク | クラスタ内のネットワーキング (エージェントトラフィックのゲートウェイへのルーティング) はユーザー側の責任 |
| アイデンティティ | Workload Identity Federation による Kubernetes 認証情報と Agent Identity 認証情報の交換 |
| 可観測性 | アクセスログ → Cloud Logging、トレース → Cloud Trace |

### サポートされるプロトコル

Agent Gateway は、すべてのデプロイモデルで標準的な HTTP ベースのエージェント通信プロトコルをサポートします。

| プロトコル | 内容 |
|------------|------|
| MCP (Model Context Protocol) | SSE または HTTP POST によるアウトバウンド / インバウンドの MCP ツール呼び出しをガバナンス。JSON-RPC リクエストを検査してツール名とメソッド属性を抽出し、ツール単位の細かなアクセスポリシーを適用可能 |
| A2A (Agent-to-Agent) | エージェント間のタスク委譲・実行 API をガバナンス |
| REST / gRPC | HTTP/1.1 および HTTP/2 (gRPC) トラフィックをサポート |

### 制限事項 (Agent Gateway 全般)

- Agent Gateway インスタンス 1 つにつき、Agent Registry に登録されたリソースを最大 5,000 までガバナンス可能

## 設定方法

### 前提条件

1. Limited Preview のため、[アクセス申請フォーム](https://docs.google.com/forms/d/e/1FAIpQLSeUpnNRtYQjLRblii-KoUbJJ7DjEV6fvQAfO21IAXgVSqFjpw/viewform)からアクセスをリクエストして承認を受けていること
2. CNCF 準拠の Kubernetes クラスタ (EKS / AKS / OpenShift / ベアメタルなど) でエージェントが稼働していること
3. Google Cloud 側で Workload Identity Federation を構成する権限 (`roles/iam.workloadIdentityPoolAdmin`、`roles/iam.serviceAccountAdmin` など) があること
4. クラスタ側でエージェントトラフィックをローカルの Agent Gateway プロキシへルーティングできるネットワーク構成 (既存のサービスメッシュやネットワークスタック) があること

### 手順 (概要)

詳細な手順は公式ドキュメント「Set up Agent Gateway for cross-cloud」を参照してください。以下は構成要素の概要です。

#### ステップ 1: Workload Identity Federation の構成

```bash
# 例: EKS クラスタの OIDC issuer URL を確認
aws eks describe-cluster --name CLUSTER_NAME \
  --query "cluster.identity.oidc.issuer" --output text

# Workload Identity Pool を作成
gcloud iam workload-identity-pools create POOL_ID \
  --location="global" \
  --display-name="DISPLAY_NAME"

# 外部クラスタを OIDC プロバイダとして追加
gcloud iam workload-identity-pools providers create-oidc PROVIDER_ID \
  --location="global" \
  --workload-identity-pool="POOL_ID" \
  --issuer-uri="ISSUER_URL" \
  --attribute-mapping="MAPPINGS"
```

外部クラスタの Kubernetes ServiceAccount トークンを Google Cloud の認証情報と交換できるようにし、エージェントに検証可能な Agent Identity を付与します (AKS の場合は OIDC issuer 機能の有効化が必要)。

#### ステップ 2: Agent Registry への登録とゲートウェイの構成

```bash
# Agent Gateway の管理には gcloud network-services agent-gateways を使用
gcloud network-services agent-gateways --help
```

Google Cloud 側の管理プロジェクトでエージェントと MCP サーバーを Agent Registry に登録し、アクセスポリシーや Model Armor テンプレートを定義します。

#### ステップ 3: ローカルプロキシのデプロイとトラフィックルーティング

軽量な Envoy ベースの Agent Gateway プロキシと関連コンポーネントを外部クラスタにデプロイし、既存のサービスメッシュ / ネットワークスタックを使ってエージェントの LLM / MCP / A2A トラフィックをプロキシ経由にルーティングします。

## メリット

### ビジネス面

- **マルチクラウド戦略とガバナンスの両立**: エージェントを EKS / AKS / オンプレミスなど最適な場所で運用し続けながら、セキュリティ・コンプライアンス統制は Google Cloud に一元化できる
- **移行不要でガバナンスを導入**: エージェントの再配置やアプリケーションコードの変更を前提とせず、既存のクラスタ環境にガバナンスレイヤーを追加できる
- **Limited Preview 期間中は無償**: Agent Gateway for cross-cloud 自体は Limited Preview 中は無料で利用でき、低リスクで評価を開始できる

### 技術面

- **単一のポリシー・レジストリ・可観測性ビュー**: 全クラウドのエージェントに対して 1 つのガバナンスポリシー、1 つの Agent Registry、Cloud Logging / Cloud Trace による 1 つの可視化基盤を適用できる
- **データ主権への配慮**: エージェントトラフィック自体は自環境内に留まり、Model Armor スクリーニングなど設定したポリシーチェックのみが Google Cloud へ送信される
- **プロトコルレベルの細かな制御**: MCP の JSON-RPC リクエストを検査してツール名・メソッド属性ベースの認可を適用でき、A2A / REST / gRPC にも対応
- **標準技術ベース**: Envoy プロキシと Workload Identity Federation という実績のある標準技術の組み合わせで構成され、既存のサービスメッシュと統合可能

## デメリット・制約事項

### 制限事項

- Limited Preview のため、アクセス申請フォームによるリクエストと承認が必要
- 対象は CNCF 準拠の Kubernetes クラスタに限定される
- Agent Gateway インスタンス 1 つあたり、Agent Registry 登録リソースは最大 5,000 まで
- Preview 段階の機能であり、機能や提供時期は変更される可能性がある

### 考慮すべき点

- 外部クラスタ内のプロキシインフラ (Envoy ベースの Agent Gateway と関連コンポーネント) は自己管理であり、デプロイ・運用・アップグレードの責任はユーザー側にある
- エージェントトラフィックをゲートウェイへルーティングするためのクラスタネットワーキング設計 (サービスメッシュ等) はユーザーの責任範囲
- Model Armor、Cloud Logging、Cloud Trace など組み合わせて構成するサービスは各サービスの標準料金で課金される
- ポリシーチェック (Model Armor など) は Google Cloud への呼び出しを伴うため、外部クラスタから Google Cloud API へのネットワーク到達性とレイテンシを考慮する必要がある

## ユースケース

### ユースケース 1: マルチクラウド企業におけるエージェントガバナンスの一元化

**シナリオ**: AWS (EKS) と Azure (AKS) の両方で LLM エージェントを運用している企業が、クラウドごとにバラバラだったエージェントのアクセス制御・プロンプト安全性対策・監査ログを統一したい。

**実装例**:
```text
1. Google Cloud に管理プロジェクトを用意し、Workload Identity Federation で
   EKS / AKS の各クラスタを OIDC プロバイダとして登録
2. 各クラスタのエージェントと MCP サーバーを Agent Registry に登録
3. アクセスポリシーと Model Armor テンプレートを管理プロジェクトで一元定義
4. 各クラスタに Envoy ベースの Agent Gateway プロキシをデプロイし、
   LLM / MCP / A2A トラフィックをプロキシ経由にルーティング
```

**効果**: クラウドごとの個別実装を排除し、全エージェントに一貫した最小権限ポリシーと Model Armor による安全性スクリーニングを適用。監査ログとトレースは Cloud Logging / Cloud Trace に集約され、監査対応が簡素化される。

### ユースケース 2: オンプレミス (OpenShift / ベアメタル) エージェントの可視化と統制

**シナリオ**: データ主権要件により自社データセンターの OpenShift クラスタでエージェントを稼働させているが、エージェントがどのツール (MCP サーバー) をいつ呼び出しているかを可視化し、未承認ツールへのアクセスを防ぎたい。

**効果**: エージェントトラフィックはデータセンター内に留めたまま、MCP の JSON-RPC 検査によるツール単位のアクセス制御を適用。アクセスログとトレースのみを Cloud Logging / Cloud Trace に送信し、データ主権を維持しながらエージェント活動を可視化できる。

## 料金

Agent Gateway for cross-cloud は **Limited Preview 期間中は無償** で利用できます。

ただし、組み合わせて構成する以下のサービスは各サービスの標準料金で課金されます。

| サービス | 課金 |
|----------|------|
| Agent Gateway for cross-cloud | Limited Preview 中は無料 |
| Model Armor | 標準料金 |
| Cloud Logging | 標準料金 |
| Cloud Trace | 標準料金 |

## 関連サービス・機能

- **Agent Registry**: エージェントと MCP サーバーを登録する中央レジストリ。本機能により Google Cloud 外のエージェントも登録対象に拡張される
- **Agent Identity / Workload Identity Federation**: Kubernetes ワークロード認証情報を Google Cloud の検証可能なアイデンティティと交換する基盤
- **Model Armor**: プロンプト / レスポンスの安全性スクリーニング。中央で定義したテンプレートをローカルプロキシが適用する
- **Cloud Logging / Cloud Trace**: 外部クラスタ上のエージェントのアクセスログとトレースの集約先 (Agent Observability)
- **Agent Gateway on Google Cloud**: Agent Runtime / Gemini Enterprise 向けの Google 管理型ゲートウェイ。GKE / Cloud Run 向けの自己管理型デプロイモデルも順次提供予定で、本機能はそのクロスクラウド版に相当する
- **セマンティックガバナンスポリシー**: 前日 (2026-11-10) に発表されたクロスプロジェクトガバナンスと組み合わせることで、マルチプロジェクト + マルチクラウドの統合ガバナンスが視野に入る

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261111-agent-gateway-cross-cloud-limited-preview.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#November_11_2026)
- [Agent Gateway 概要 (デプロイモデル / cross-cloud)](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview)
- [Workload Identity Federation with Kubernetes](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-kubernetes)
- [アクセス申請フォーム (Limited Preview)](https://docs.google.com/forms/d/e/1FAIpQLSeUpnNRtYQjLRblii-KoUbJJ7DjEV6fvQAfO21IAXgVSqFjpw/viewform)

## まとめ

Agent Gateway for cross-cloud は、Google Cloud のエージェントガバナンス (Agent Identity、Agent Registry、ポリシー適用、可観測性) を EKS / AKS / OpenShift / ベアメタルといった Google Cloud 外の Kubernetes 環境へ拡張する戦略的なアップデートです。マルチクラウドやオンプレミスでエージェントを運用する組織は、エージェントを移行することなく統一ガバナンスを導入できます。Limited Preview 中は無償のため、該当環境を持つプラットフォーム / セキュリティチームはアクセス申請のうえ、Workload Identity Federation とローカルプロキシ構成の検証から始めることを推奨します。

---

**タグ**: #GeminiEnterpriseAgentPlatform #AgentGateway #CrossCloud #Kubernetes #EKS #AKS #OpenShift #ModelArmor #AgentRegistry #LimitedPreview #AIエージェント #ガバナンス
