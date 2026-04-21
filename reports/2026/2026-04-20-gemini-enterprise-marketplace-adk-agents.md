# Gemini Enterprise: Marketplace エージェントアクセスリクエスト & ADK エージェント登録 (GA)

**リリース日**: 2026-04-20

**サービス**: Gemini Enterprise

**機能**: Cloud Marketplace エージェントのアクセスリクエスト / Vertex AI Agent Engine 上の ADK エージェント登録

**ステータス**: Feature (ADK エージェント登録は GA)

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260420-gemini-enterprise-marketplace-adk-agents.html)

## 概要

Gemini Enterprise に 2 つのエージェント関連機能が追加された。1 つ目は、エンドユーザーが Agent Gallery から Google Cloud Marketplace に公開されている AI エージェントへのアクセスをリクエストできる機能である。管理者はこれらのエージェントの可視性を設定し、購入リクエストの確認やアクセスリクエストの管理を行える。2 つ目は、Vertex AI Agent Engine 上でホストされている ADK (Agent Development Kit) エージェントを Gemini Enterprise に登録する機能が GA (一般提供) となったことである。異なる Google Cloud プロジェクトで実行されている ADK エージェントのクロスプロジェクト登録にも対応している。

これらのアップデートにより、Gemini Enterprise はエージェントエコシステムのハブとしての位置付けを強化している。Cloud Marketplace を通じてサードパーティベンダーの AI エージェントを組織内に導入する経路が整備され、同時に自社開発した ADK エージェントを Gemini Enterprise のユーザーインターフェースから利用可能にするワークフローが本番環境に対応した。

対象ユーザーは、Gemini Enterprise を導入している組織の IT 管理者、エージェント開発者、およびエンドユーザーである。特に、AI エージェントを活用した業務自動化やナレッジワーカー支援を推進している企業にとって重要なアップデートとなる。

**アップデート前の課題**

- エンドユーザーは Cloud Marketplace の AI エージェントを Agent Gallery から直接リクエストする手段がなく、管理者に個別に依頼する必要があった
- 管理者は Marketplace エージェントの可視性を細かく制御する設定が限られており、ユーザーに対して適切なエージェント情報を提供しにくかった
- ADK エージェントの Gemini Enterprise への登録は Preview 段階であり、本番ワークロードでの利用には制約があった
- 異なる Google Cloud プロジェクトにホストされた ADK エージェントを Gemini Enterprise に登録するにはクロスプロジェクト設定の手順が明確でなかった

**アップデート後の改善**

- エンドユーザーが Agent Gallery の Marketplace セクションから直接エージェントへのアクセスをリクエストでき、承認後は「From your organization」セクションに自動的に表示される
- 管理者は Marketplace エージェントの可視性を 4 段階 (アクセス可能なエージェントのみ / 統合済みエージェントのみ / 調達済みエージェント / すべて表示) で細かく制御できるようになった
- ADK エージェント登録が GA となり、SLA に基づいた本番環境での運用が可能になった
- クロスプロジェクト ADK エージェントの登録手順が明確化され、異なるプロジェクト間でのエージェント共有が容易になった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Users["ユーザー"]
        EU(["👤 エンドユーザー"])
        Admin(["🔧 管理者"])
    end

    subgraph GE["Gemini Enterprise"]
        AG["🏪 Agent Gallery"]
        AR["📋 アクセスリクエスト<br/>管理"]
        REG["📝 エージェント<br/>レジストリ"]
    end

    subgraph Sources["エージェントソース"]
        subgraph MP["Cloud Marketplace"]
            A2A["🤖 A2A エージェント<br/>(サードパーティ)"]
        end
        subgraph VAE["Vertex AI Agent Engine"]
            ADK1["🧩 ADK エージェント<br/>(同一プロジェクト)"]
            ADK2["🧩 ADK エージェント<br/>(別プロジェクト)"]
        end
    end

    EU -->|アクセスリクエスト| AG
    AG -->|リクエスト通知| AR
    Admin -->|承認 / 可視性設定| AR
    AR -->|承認済み| REG

    Admin -->|エージェント登録| REG
    REG <-->|A2A プロトコル| A2A
    REG <-->|Discovery Engine API| ADK1
    REG <-.->|クロスプロジェクト接続<br/>(VPC-SC 準拠)| ADK2

    classDef user fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#1565C0
    classDef ge fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#333333
    classDef mp fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#333333
    classDef vae fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px,color:#333333
    classDef agent fill:#FAFAFA,stroke:#999999,stroke-width:1px,color:#333333

    class EU,Admin user
    class AG,AR,REG ge
    class A2A agent
    class ADK1,ADK2 agent
```

ユーザーは Agent Gallery を通じて Marketplace エージェントのアクセスをリクエストし、管理者が承認する。ADK エージェントは Vertex AI Agent Engine 上でホストされ、同一プロジェクトまたはクロスプロジェクトで Gemini Enterprise に登録される。

## サービスアップデートの詳細

### 主要機能

1. **Cloud Marketplace エージェントのアクセスリクエスト**
   - エンドユーザーは Agent Gallery の「Marketplace」セクションからエージェントを選択し、「Request access」をクリックするだけでアクセスをリクエストできる
   - リクエストが承認されると、ユーザーにベルアイコンで通知が届き、「From your organization」セクションにエージェントが表示される
   - 承認済みエージェントは会話中に `@agent_name` でメンションして利用可能
   - Marketplace エージェントは Agent2Agent (A2A) プロトコルを使用して通信を行う

2. **Marketplace エージェントの可視性管理 (管理者向け)**
   - 管理者は Google Cloud コンソールから Marketplace エージェントの表示範囲を設定可能
   - 4 段階の可視性オプション: 「アクセス可能なエージェントのみ」「統合済みエージェントのみ」「調達済みエージェント (デフォルト)」「すべて表示」
   - 調達担当者の連絡先を設定し、未調達エージェントへのアクセスリクエスト時に通知を受け取れる

3. **ADK エージェントの Gemini Enterprise 登録 (GA)**
   - Vertex AI Agent Engine 上にデプロイされた ADK エージェントを Gemini Enterprise に登録し、Agent Gallery から利用可能にする
   - VPC Service Controls (VPC-SC) 準拠のセキュアな通信を実現
   - エージェントはユーザーのメールアドレスを受け取り、個人ごとにパーソナライズされた応答を提供可能
   - Google Cloud コンソールまたは REST API からの登録に対応

4. **クロスプロジェクト ADK エージェントサポート**
   - Gemini Enterprise アプリとは異なる Google Cloud プロジェクトにホストされた ADK エージェントも登録可能
   - Google Cloud のセキュアなプライベートネットワーキングを使用
   - サービスエージェント (`service-PROJECT_NUMBER@gcp-sa-discoveryengine.iam.gserviceaccount.com`) に Discovery Engine Service Agent ロールを付与することで実現

## 技術仕様

### Marketplace エージェントの可視性設定

| 設定オプション | 説明 |
|--------------|------|
| Only show accessible agents | Marketplace セクション自体を非表示。ユーザーがアクセスできないエージェントは表示されない |
| Only show already integrated agents | 統合済みエージェントのみ表示 (アクセス済み + リクエスト可能) |
| Only show procured agents (デフォルト) | 調達済みの Cloud Marketplace エージェントをすべて表示 |
| Show all | アクセス権のないものも含め、すべての Cloud Marketplace エージェントを表示 |

### ADK エージェント登録 API

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: PROJECT_ID" \
  "https://ENDPOINT_LOCATION-discoveryengine.googleapis.com/v1alpha/projects/PROJECT_ID/locations/global/collections/default_collection/engines/APP_ID/assistants/default_assistant/agents" \
  -d '{
    "displayName": "DISPLAY_NAME",
    "description": "DESCRIPTION",
    "icon": {
      "uri": "ICON_URI"
    },
    "adkAgentDefinition": {
      "provisionedReasoningEngine": {
        "reasoningEngine": "projects/PROJECT_ID/locations/AGENT_ENGINE_LOCATION/reasoningEngines/AGENT_ENGINE_ID"
      }
    }
  }'
```

### ロケーション互換性 (ADK エージェント)

Gemini Enterprise アプリのロケーションと Vertex AI Agent Engine のリージョンには互換性の制約がある。

| Gemini Enterprise アプリのロケーション | 許可される Agent Engine リージョン |
|--------------------------------------|----------------------------------|
| global | 任意のサポート対象リージョン |
| us | `us-` で始まるリージョン (例: us-central1, us-east4) |
| eu | `europe-` で始まるリージョン (例: europe-west1, europe-west3) |

### エージェントガバナンス

| ガバナンス項目 | 説明 |
|--------------|------|
| セキュア通信 | Vertex AI Agent Engine と Gemini Enterprise 間の接続は VPC-SC 準拠 |
| クロスプロジェクトサポート | Google Cloud のセキュアなプライベートネットワーキングを使用 |
| パーソナライズ | エージェントはユーザーのメールアドレスを受け取り、個人に合わせた応答が可能 |
| セキュリティ保護 | ADK エージェント / Marketplace エージェントの Model Armor 保護は REST API でエージェントコード内に設定が必要 |

## 設定方法

### 前提条件

1. Gemini Enterprise のサブスクリプション (Standard、Plus、または Frontline エディション) が有効であること
2. Gemini Enterprise Admin ロール (`discoveryengine.agentspaceAdmin`) が付与されていること
3. Discovery Engine API が有効化されていること
4. 既存の Gemini Enterprise アプリが作成済みであること

### 手順

#### ステップ 1: Marketplace エージェントの可視性設定 (管理者)

1. Google Cloud コンソールで Gemini Enterprise ページに移動
2. 設定対象のアプリ名をクリック
3. **Agents** をクリック
4. 設定アイコンをクリックして「Agent settings & config」パネルを開く
5. **Marketplace visibility** セクションで、適切な可視性オプションを選択
6. 必要に応じて **Procurement contacts** に連絡先メールアドレスを追加
7. **Done** をクリックして保存

#### ステップ 2: Marketplace エージェントの追加 (管理者)

1. Google Cloud コンソールで Gemini Enterprise ページに移動
2. アプリ名をクリックし、**Agents** > **Add Agents** を選択
3. 「Choose an agent type」で **Agents via Marketplace** の **Add** をクリック
4. 追加したいエージェントを検索して選択し、**Next** をクリック
5. エージェントの詳細を確認し、**Next** をクリック
6. 認証情報を入力し、**Finish** をクリック

#### ステップ 3: ADK エージェントの登録 (管理者)

1. Google Cloud コンソールで Gemini Enterprise ページに移動
2. アプリ名をクリックし、**Agents** > **Add Agents** を選択
3. Agent Engine エージェントを選択
4. 表示名、説明、Agent Engine のリソースパスを入力
   - リソースパス形式: `projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID`
5. **Save** をクリック

#### ステップ 4: クロスプロジェクト ADK エージェントの権限設定 (必要な場合)

```bash
# Gemini Enterprise のサービスエージェント メールアドレスを特定
# 形式: service-PROJECT_NUMBER@gcp-sa-discoveryengine.iam.gserviceaccount.com

# ADK エージェントがホストされているプロジェクトで IAM ロールを付与
gcloud projects add-iam-policy-binding AGENT_PROJECT_ID \
  --member="serviceAccount:service-GE_PROJECT_NUMBER@gcp-sa-discoveryengine.iam.gserviceaccount.com" \
  --role="roles/discoveryengine.serviceAgent"
```

## メリット

### ビジネス面

- **エージェントエコシステムの迅速な導入**: Cloud Marketplace を通じて、検証済みのサードパーティ AI エージェントを組織内に迅速に導入できる。調達プロセスが Marketplace に統合されており、Google 課金を通じた一元管理が可能
- **セルフサービス型のエージェントアクセス**: エンドユーザーが自ら必要なエージェントを発見しリクエストできるため、IT 管理者への個別依頼が不要になり、エージェント活用の障壁が低下する
- **自社 AI エージェントの社内展開**: ADK で開発した自社固有のエージェントを Gemini Enterprise の統一インターフェースから全社展開できるため、エージェント開発の ROI を最大化できる

### 技術面

- **VPC-SC 準拠のセキュリティ**: ADK エージェントとの通信は VPC Service Controls に準拠しており、エンタープライズグレードのセキュリティ要件を満たす
- **クロスプロジェクト対応**: エージェント開発プロジェクトと Gemini Enterprise プロジェクトを分離できるため、開発チームと運用チームの責任分界が明確になる
- **A2A プロトコルによる標準化**: Marketplace エージェントは Agent2Agent (A2A) オープンプロトコルを使用し、異なるフレームワークやベンダーのエージェント間でのシームレスな通信を実現する
- **GA レベルの信頼性**: ADK エージェント登録が GA となったことで、SLA に基づいた本番環境での安定運用が保証される

## デメリット・制約事項

### 制限事項

- Marketplace エージェントのセキュリティ保護には、エージェントのアプリケーションコード内で REST API を使用して Model Armor を設定する必要がある。Google Cloud コンソールの Model Armor 設定は自動的に Marketplace エージェントや ADK エージェントには適用されない
- Gemini Enterprise Frontline エディションでは、ユーザーは管理者がプロビジョニングしたエージェントのみアクセス可能であり、Agent Gallery のフル機能は利用できない
- Gemini Enterprise Business エディションでは Agent Marketplace へのアクセスは利用できない
- ADK エージェントのロケーション互換性制約があり、Gemini Enterprise アプリのロケーションと Agent Engine のリージョンが一致する必要がある

### 考慮すべき点

- Marketplace エージェントは A2A プロトコルを使用するため、エージェントベンダーによる Agent Card の維持管理が必要であり、ベンダーのサポート体制を事前に確認する必要がある
- クロスプロジェクト ADK エージェントを使用する場合、Gemini Enterprise のサービスエージェントに対して ADK エージェント側プロジェクトで適切な IAM ロールを付与する必要があり、セキュリティポリシーとの整合性を確認する必要がある
- Marketplace エージェントの料金モデルはエージェントごとに異なり (無料 / サブスクリプション / 従量課金 / 複合型)、コスト管理に注意が必要

## ユースケース

### ユースケース 1: サードパーティ AI エージェントの組織導入

**シナリオ**: 大規模組織で、営業チームが CRM データ分析に特化した AI エージェントを、カスタマーサポートチームがチケット管理エージェントを必要としている。

**効果**: 各チームのユーザーが Agent Gallery の Marketplace セクションから必要なエージェントを検索し、アクセスをリクエストする。管理者が承認するだけで、ユーザーは Gemini Enterprise の統一インターフェースから各エージェントを利用開始できる。個別のツール導入や設定が不要になり、エージェント活用までのリードタイムが大幅に短縮される。

### ユースケース 2: 社内 ADK エージェントの全社展開

**シナリオ**: AI 開発チームが Vertex AI Agent Engine 上に ADK を使用して社内ナレッジ検索エージェントを構築した。開発は専用の Google Cloud プロジェクトで行っているが、全社の Gemini Enterprise ユーザーに提供したい。

**効果**: クロスプロジェクト ADK エージェント登録機能を使用し、開発プロジェクトの ADK エージェントを Gemini Enterprise に登録する。ユーザーは Agent Gallery の「From your organization」セクションからエージェントを選択するだけで利用可能になる。開発環境と本番環境を分離しながら、エージェントの全社展開が実現できる。

### ユースケース 3: マルチエージェント連携による業務自動化

**シナリオ**: 財務レポートの作成プロセスで、データ収集 (Marketplace エージェント)、分析 (自社 ADK エージェント)、レポート生成 (Gemini Enterprise 組み込み機能) を連携させたい。

**効果**: Marketplace からデータ収集に特化したエージェントを導入し、自社開発の分析エージェントと組み合わせることで、A2A プロトコルを通じたマルチエージェント連携が可能になる。Gemini Enterprise が各エージェントのオーケストレーション層として機能し、複雑な業務プロセスの自動化を実現する。

## 料金

Gemini Enterprise の料金はエディション別のサブスクリプション制である。Marketplace エージェントおよび ADK エージェントの登録・管理機能はサブスクリプションに含まれる。

ただし、Marketplace エージェント自体の料金は個別のエージェントごとに異なる。

| 料金モデル | 説明 |
|-----------|------|
| Free | Google Cloud リソースの利用料金のみ |
| Subscription | 月額固定料金 (日割り対応) |
| Usage-based | エージェント固有のメトリクスに基づく従量課金 |
| Combined | 基本サブスクリプション + 従量課金 |

Vertex AI Agent Engine の利用料金は別途発生する。具体的な料金については以下を参照。

- [Gemini Enterprise エディション比較](https://docs.cloud.google.com/gemini/enterprise/docs/editions)
- [Marketplace AI エージェントの料金モデル](https://docs.cloud.google.com/marketplace/docs/partners/ai-agents/pricing-models)

## 利用可能リージョン

ADK エージェント登録機能は Gemini Enterprise がサポートするマルチリージョン (global、us、eu) およびインカントリーリージョン (ca、in) で利用可能。Agent Engine のリージョンは Gemini Enterprise アプリのロケーションとの互換性制約がある (技術仕様セクション参照)。

## 関連サービス・機能

- **Vertex AI Agent Engine**: ADK エージェントのホスティングおよび実行環境。エージェントのデプロイ、管理、スケーリングを提供するフルマネージドサービス
- **Agent Development Kit (ADK)**: Google が提供するオープンソースのエージェント開発フレームワーク。Gemini モデルに最適化されているが、モデル非依存で設計されている
- **Google Cloud Marketplace**: AI エージェントの調達・課金プラットフォーム。A2A プロトコルに対応したエージェントを提供
- **Agent2Agent (A2A) プロトコル**: エージェント間のシームレスな通信を実現するオープンスタンダード。Marketplace エージェントはこのプロトコルを使用
- **Model Armor**: エージェントのセキュリティ保護機能。ADK エージェントおよび Marketplace エージェントでは REST API を通じた設定が必要
- **Discovery Engine API**: Gemini Enterprise のバックエンド API。エージェントの登録・管理に使用される

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260420-gemini-enterprise-marketplace-adk-agents.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#April_20_2026)
- [Agent Gallery でエージェントを閲覧する](https://docs.cloud.google.com/gemini/enterprise/docs/agent-gallery)
- [Cloud Marketplace から A2A エージェントを追加・管理する](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-marketplace-agents)
- [Vertex AI Agent Engine 上の ADK エージェントを登録・管理する](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-adk-agent)
- [クロスプロジェクト ADK エージェントの設定](https://docs.cloud.google.com/gemini/enterprise/docs/configure-cross-project-adk-agents)
- [Agent Development Kit 概要](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview)
- [Gemini Enterprise エディション比較](https://docs.cloud.google.com/gemini/enterprise/docs/editions)
- [Cloud Marketplace での AI エージェント提供](https://docs.cloud.google.com/marketplace/docs/partners/ai-agents)

## まとめ

Gemini Enterprise に Cloud Marketplace エージェントのアクセスリクエスト機能と ADK エージェント登録の GA が同時に追加され、エージェントエコシステムの統合ハブとしての機能が大幅に強化された。エンドユーザーのセルフサービス型エージェントアクセスと管理者の細かな可視性制御、そして ADK エージェントのクロスプロジェクト対応により、組織全体でのエージェント活用が加速する。AI エージェントの導入を検討している組織は、Marketplace からのサードパーティエージェント活用と自社 ADK エージェントの Gemini Enterprise 統合の両面から検討を進めることを推奨する。

---

**タグ**: #GeminiEnterprise #CloudMarketplace #AgentGallery #ADK #AgentDevelopmentKit #VertexAI #AgentEngine #A2A #Agent2Agent #GA
