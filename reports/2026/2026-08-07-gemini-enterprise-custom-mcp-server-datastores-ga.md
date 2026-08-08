# Gemini Enterprise: Custom MCP server data stores が一般提供 (GA)

**リリース日**: 2026-08-07

**サービス**: Gemini Enterprise

**機能**: Custom MCP server data stores

**ステータス**: GA (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260807-gemini-enterprise-custom-mcp-server-datastores-ga.html)

## 概要

Gemini Enterprise の Custom MCP server data stores が一般提供 (GA) になりました。カスタムの Model Context Protocol (MCP) サーバーを Gemini Enterprise に接続することで、企業のプライベートデータ、カスタム内部ツール、MCP 準拠のサードパーティシステムにセキュアにアクセスできます。

MCP サーバーが公開するツール (Gemini Enterprise 上では「アクション」と呼ばれる) はデータストアにインポートされ、管理者が有効化したアクションをエンドユーザーが自然言語で呼び出せるようになります。認証は「認証なし」と OAuth 2.0 (PKCE サポートあり) の 2 方式に対応し、Okta、Azure AD、Google などの ID プロバイダーと連携できます。

なお、この機能は**デフォルトで無効**です。Gemini Enterprise はマネージド組織ポリシー制約により MCP データストアの作成をデフォルトでブロックしており、有効化には Organization Policy Administrator (`roles/orgpolicy.policyAdmin`) による制約のオーバーライドが必要です。対象ユーザーは、社内 API・内部ツール・サードパーティシステムを Gemini Enterprise のエージェント体験に統合したい企業の管理者・プラットフォームチームです。

**アップデート前の課題**

- Custom MCP Server コネクタは Preview 段階の機能であり、GA 品質の保証がないため本番環境での採用判断が難しかった
- 企業のプライベートデータやカスタム内部ツールを Gemini Enterprise から利用するには、標準コネクタが用意されたデータソースに限られていた
- MCP 準拠のサードパーティシステムを Gemini Enterprise に統合する一般提供レベルの手段がなかった

**アップデート後の改善**

- Custom MCP server data stores が一般提供 (GA) となり、本番ワークロードでの利用を前提とした採用判断が可能になった
- カスタム MCP サーバー経由で、企業のプライベートデータ・カスタム内部ツール・MCP 準拠のサードパーティシステムに Gemini Enterprise からセキュアにアクセスできるようになった
- 組織ポリシー制約 (デフォルト無効)、Egress FQDN 許可リスト、VPC Service Controls との連携により、ガバナンスを効かせた形で段階的に開放できる

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph Org["🏢 組織 (ガバナンス)"]
        OPA["👤 組織ポリシー管理者"]
        Policy{{"📜 組織ポリシー<br/>Custom MCP 制約<br/>(デフォルト: ブロック)"}}
    end

    subgraph GE["☁️ Gemini Enterprise"]
        App(["👤 エンドユーザー"])
        Agent["🤖 エージェント"]
        DS["🗄️ Custom MCP<br/>データストア"]
    end

    subgraph Ext["🔌 カスタム MCP サーバー (HTTPS / StreamableHTTP)"]
        MCP["🛠️ MCP サーバー<br/>(tools/list · tools/call)"]
        Data[("🔒 プライベートデータ<br/>内部ツール · 3rd party")]
    end

    OPA -->|制約をオーバーライド| Policy
    Policy -.->|作成を許可| DS
    App -->|自然言語リクエスト| Agent
    Agent --> DS
    DS <-->|ツールディスカバリ / 実行<br/>(認証なし or OAuth 2.0)| MCP
    MCP --> Data
```

組織ポリシー管理者が制約をオーバーライドすると Custom MCP データストアを作成でき、Gemini Enterprise がカスタム MCP サーバーと StreamableHTTP で連携してプライベートデータや内部ツールにセキュアにアクセスするフローです。

## サービスアップデートの詳細

### 主要機能

1. **カスタム MCP サーバーの接続 (GA)**
   - 自社開発の MCP サーバーや MCP 準拠のサードパーティシステムを Gemini Enterprise のデータストア (コネクタ) として接続できる
   - MCP サーバーのツールは Gemini Enterprise に「アクション」としてインポートされ、エンドユーザーが自然言語で利用できる
   - トランスポートは StreamableHTTP のみをサポート (HTTPS 必須、URL は `/mcp` で終わることが多い)

2. **2 種類の認証方式**
   - **No authentication**: 認証不要の MCP サーバー向け。MCP Server URL のみで接続
   - **OAuth 2.0**: 認可 URL・トークン URL・クライアント ID/シークレット・スコープを設定。PKCE (RFC 7636) のサポートも選択可能
   - ID プロバイダー (Okta、Azure AD、Google など) に Gemini Enterprise を OAuth クライアントとして登録して連携する

3. **組織ポリシーによるガバナンス (デフォルト無効)**
   - マネージド組織ポリシー制約「Disable custom MCP server connector for Gemini Enterprise」により、MCP データストアの作成はデフォルトでブロックされる
   - 有効化には Organization Policy Administrator が対象プロジェクトで制約をオーバーライド (enforcement を OFF) する必要がある
   - Egress FQDN 許可リスト、許可データソース (`custom_mcp`)、VPC Service Controls と組み合わせた多層的な制御が可能

4. **アクションの選択的な有効化とユーザー確認制御**
   - デフォルトではすべてのアクションが無効。管理者が「Reload custom actions」(`tools/list` 呼び出し) でツール一覧を取得し、有効化するアクションを選択する (一度に最大 100 アクション)
   - デフォルトではすべてのアクション呼び出しにユーザー確認が必要。MCP ツール定義の `readOnlyHint` アノテーションにより読み取り専用ツールの確認をスキップできる

## 技術仕様

### Custom MCP server data stores の主な仕様

| 項目 | 詳細 |
|------|------|
| ステータス | 一般提供 (GA) |
| デフォルト状態 | 無効 (マネージド組織ポリシー制約でブロック) |
| 有効化に必要なロール | Organization Policy Administrator (`roles/orgpolicy.policyAdmin`) |
| データストア作成に必要なロール | Discovery Engine 編集者 (`roles/discoveryengine.editor`) |
| トランスポート | StreamableHTTP のみ (HTTPS 必須) |
| 認証方式 | No authentication または OAuth 2.0 (PKCE サポートあり) |
| ツールディスカバリ | `tools/list` エンドポイントの自動呼び出し |
| アクションの有効化 | デフォルトで全アクション無効。一度に最大 100 アクションまで有効化可能 |
| Agent Gateway | この方法で追加した MCP サーバーへのトラフィックは Agent Gateway を経由せず、Agent Gateway ポリシーは適用されない |

### 関連する組織ポリシー・セキュリティ制御

| ポリシー / 制御 | 役割 |
|----------------|------|
| Disable custom MCP server connector for Gemini Enterprise | Custom MCP データストア作成をデフォルトでブロック。作成にはオーバーライドが必要 |
| Restrict egress domains for data connectors (`allowedEgressFqdns`) | MCP サーバー URL・認可 URL・トークン URL の FQDN を明示的に許可 (ドメイン名のみでよい) |
| Restrict allowed data sources for data connectors (`allowedDataSources`) | プロジェクト強制または VPC Service Controls 保護が有効な場合、`custom_mcp` の追加が必要 |
| VPC Service Controls | VPCSC 保護プロジェクトでは上記ポリシーが自動的に強制される |

VPCSC が有効でなく `enforcedProjects` にも含まれないプロジェクトでは、Egress FQDN・許可データソースのポリシーは強制されず、Custom MCP 制約のオーバーライドのみで作成できます。

## 設定方法

### 前提条件

1. Organization Policy Administrator ロール (`roles/orgpolicy.policyAdmin`) を保有していること (組織ポリシーのオーバーライド用。プロジェクトが組織に属している場合のみ適用)
2. データストア作成者に Discovery Engine 編集者ロール (`roles/discoveryengine.editor`) が付与されていること
3. MCP サーバー URL・認可 URL・トークン URL の FQDN を許可済み Egress FQDN に追加していること
4. プロジェクト強制または VPC Service Controls 保護が有効な場合、`custom_mcp` を許可データソースに追加していること
5. OAuth 認証を使う場合: ID プロバイダーに Gemini Enterprise を OAuth クライアントとして登録 (リダイレクト URL: `https://vertexaisearch.cloud.google.com/oauth-redirect`) し、`client_id` と `client_secret` を取得していること

### 手順

#### ステップ 1: 組織ポリシー制約のオーバーライド

1. Google Cloud コンソールで「組織のポリシー」ページに移動
2. プロジェクトセレクタで、強制を変更したい**特定のプロジェクト**を選択 (組織レベルで設定すると組織内の全プロジェクトに影響するため注意)
3. フィルタに「Disable custom MCP server connector for Gemini Enterprise」と入力し、ポリシー名をクリック
4. 「ポリシーを管理」をクリックし、「親のポリシーをオーバーライドする」を選択
5. 新しいルールを追加して enforcement トグルを **OFF** に設定し、「ポリシーを設定」をクリック
6. ポリシーのステータスが「Not enforced」に更新されたことを確認

#### ステップ 2: Custom MCP server データストアの作成

1. Google Cloud コンソールで Gemini Enterprise ページに移動し、ナビゲーションメニューの「Data stores」をクリック
2. 「Create data store」をクリックし、データソース検索で「Custom MCP Server」を検索して「Add MCP server」をクリック
3. 認証設定 (No authentication または OAuth 2.0) を選択し、MCP Server URL などを入力。OAuth 2.0 の場合は「Verify Auth」で検証してから「Continue」
4. データコネクタのロケーション (マルチリージョン) とデータストア名を入力して「Create」
5. データストアの状態が「Creating」から「Active」に変わると利用可能

#### ステップ 3: アクションの有効化

1. 作成した Custom MCP server データストアを開き、「Actions」>「Reload custom actions」をクリック (この操作で `tools/list` が呼び出され、利用可能なツールが表示される)
2. 有効化するアクションを選択し、「Enable actions」をクリック

デフォルトではすべてのアクションが無効のため、この有効化操作が必須です。

## メリット

### ビジネス面

- **本番採用の判断が可能に**: GA となったことで、本番ワークロードを前提とした Custom MCP サーバー統合の採用判断ができる
- **既存資産の活用**: 社内 API や内部ツールを MCP サーバーとしてラップするだけで、Gemini Enterprise のエージェント体験に統合できる
- **エコシステムの拡大**: MCP 準拠のサードパーティシステムをそのまま接続でき、標準コネクタがないシステムもカバーできる

### 技術面

- **標準プロトコルによる統合**: オープンな MCP 仕様 (`tools/list` / `tools/call`) に準拠しており、ベンダーロックインの少ない統合が可能
- **ガバナンスを前提とした設計**: デフォルト無効の組織ポリシー制約、Egress FQDN 許可リスト、VPC Service Controls との連携により、セキュリティ部門の統制下で段階的に開放できる
- **きめ細かなアクション制御**: アクション単位の有効化と、`readOnlyHint` / `destructiveHint` アノテーションによるユーザー確認制御が可能

## デメリット・制約事項

### 制限事項

- 機能はデフォルトで無効であり、Organization Policy Administrator による組織ポリシー制約のオーバーライドが必須
- サポートされるトランスポートは StreamableHTTP のみ (HTTPS 必須)。stdio などその他のトランスポートは利用できない
- 有効化できるアクションは一度に最大 100 個まで
- この方法で追加した MCP サーバーへのトラフィックは Agent Gateway を経由せず、Agent Gateway ポリシーが適用されない

### 考慮すべき点

- 組織ポリシーのオーバーライドは**プロジェクト単位**で行うことが推奨される。組織レベルで設定すると全プロジェクトで Custom MCP データストアの作成が可能になるため、影響範囲に注意が必要
- VPCSC 保護プロジェクトや `enforcedProjects` 対象プロジェクトでは、Egress FQDN (`allowedEgressFqdns`) と許可データソース (`custom_mcp`) の設定漏れがあるとプロビジョニングがブロックされる
- デフォルトではすべてのアクション呼び出しにユーザー確認が必要 (破壊的操作の可能性を想定)。読み取り専用ツールで確認をスキップするには MCP サーバー側で `readOnlyHint` アノテーションの設定が必要
- 前日 (2026-08-06) の変更により Description フィールドは廃止されており、ルーティングは MCP サーバー側のツール定義・パラメータスキーマに依存する。ツール定義の品質がそのまま体験を左右する

## ユースケース

### ユースケース 1: 社内業務システムのエージェント統合

**シナリオ**: 社内の在庫管理・注文管理 API を MCP サーバーとしてラップし、従業員が Gemini Enterprise から自然言語で在庫照会や注文状況の確認をできるようにしたい。

**実装例**:
```python
# MCP サーバー側のツール定義 (StreamableHTTP / HTTPS で公開)
@mcp.tool(annotations={"readOnlyHint": True, "destructiveHint": False})
def get_inventory(product_id: str) -> dict:
    """指定した product_id の在庫数と倉庫所在地を返す"""
    ...
```

**効果**: GA 機能として本番導入でき、読み取り専用アノテーションによりユーザー確認なしのスムーズな照会体験を提供できる。

### ユースケース 2: MCP 準拠サードパーティ SaaS との連携

**シナリオ**: MCP エンドポイントを公開しているサードパーティ SaaS を、標準コネクタを待たずに Gemini Enterprise へ統合したい。OAuth 2.0 で各ユーザーの権限に基づいたアクセスを行う。

**効果**: OAuth 2.0 (PKCE 対応) によりユーザーごとの認可でセキュアに接続でき、管理者は必要なアクションだけを選択的に有効化してリスクを最小化できる。

### ユースケース 3: ガバナンス統制下での段階的な開放

**シナリオ**: セキュリティ部門の統制のもと、特定のプロジェクトに限定して Custom MCP データストアの利用を許可したい。

**効果**: 組織ポリシー制約はデフォルトでブロックのため、承認済みプロジェクトのみオーバーライドし、`allowedEgressFqdns` で接続先ドメインを限定することで、統制と利便性を両立できる。

## 料金

Custom MCP server data stores 自体の個別料金は Release Notes には記載されていません。Gemini Enterprise の料金の詳細は公式料金ページを参照してください。

- [Gemini Enterprise の料金](https://cloud.google.com/gemini-enterprise/pricing)

## 利用可能リージョン

データコネクタのロケーションはデータストア作成時にマルチリージョンから選択します。詳細は公式ドキュメントを参照してください。

## 関連サービス・機能

- **Model Context Protocol (MCP)**: ツール定義・`tools/list` / `tools/call`・アノテーション (`readOnlyHint` / `destructiveHint`) などの仕様を定めるオープンプロトコル。本機能の基盤
- **Organization Policy Service**: 「Disable custom MCP server connector for Gemini Enterprise」マネージド制約により本機能のデフォルト無効を実現。有効化のオーバーライド操作もこのサービスで行う
- **VPC Service Controls**: VPCSC 保護プロジェクトでは Egress FQDN・許可データソースのポリシーが自動的に強制される
- **IAM**: 組織ポリシーのオーバーライドに `roles/orgpolicy.policyAdmin`、データストア作成に `roles/discoveryengine.editor` が必要
- **Agent Gateway**: Gemini Enterprise エージェントプラットフォームのゲートウェイ。ただし Custom MCP server データストア経由のトラフィックは Agent Gateway を経由しない点に注意

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260807-gemini-enterprise-custom-mcp-server-datastores-ga.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#August_07_2026)
- [Set up your custom MCP server (公式ドキュメント)](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server)
- [Override the organization policy for Custom MCP data stores (公式ドキュメント)](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/override-constraint-for-custom-mcp-data-stores)
- [Gemini Enterprise の料金](https://cloud.google.com/gemini-enterprise/pricing)
- [関連レポート: Custom MCP server データストアから Description フィールドが削除 (2026-08-06)](./2026-08-06-gemini-enterprise-custom-mcp-datastore-description-removed.md)

## まとめ

Custom MCP server data stores の GA により、カスタム MCP サーバー経由で企業のプライベートデータ・内部ツール・MCP 準拠のサードパーティシステムを Gemini Enterprise に本番品質で統合できるようになりました。機能はデフォルトで無効のため、まず Organization Policy Administrator と連携して対象プロジェクトの組織ポリシー制約をオーバーライドし、Egress FQDN や許可データソースなどのガバナンス設定を整えたうえで、小規模なアクションセットから段階的に有効化することを推奨します。

---

**タグ**: #GeminiEnterprise #MCP #ModelContextProtocol #DataStore #Connector #GA #OrganizationPolicy #AI #Agent
