# Gemini Enterprise: Workflow Builder (旧 Agent Designer) の一般提供開始

**リリース日**: 2026-09-03

**サービス**: Gemini Enterprise

**機能**: Workflow Builder (旧 Agent Designer) の一般提供 (GA)

**ステータス**: GA (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260903-gemini-enterprise-workflow-builder-ga.html)

## 概要

Gemini Enterprise において、**Workflow Builder** (旧称: Agent Designer) が一般提供 (GA) になりました。Workflow Builder は、組織内のユーザーがノーコード / ローコードでマルチステップの自動化ワークフローを構築し、タスクを効率化してエンタープライズデータに接続できるインタラクティブなプラットフォームです。自然言語プロンプトによるエージェント作成と、ビジュアルなフローキャンバスによる詳細な編集の両方に対応します。

今回の GA リリースでは、スケジュール実行・オンデマンド実行・チャットからの @-メンション呼び出しに対応した「ワークフロー」、会話型の「チャットエージェント」、既存の A2A / ADK エージェントのインポート、Google Workspace およびサードパーティツールへのエンタープライズコネクタ、強化された Agent Gallery、組織全体の管理者制御といった主要機能が提供されます。

対象ユーザーは、開発者に限らず、業務プロセスの自動化を進めたいビジネスユーザーから、組織全体のエージェントを統制したい管理者まで幅広く、「全社員がエージェントを構築・活用できる」ことを目指した機能群です。エージェントが実行できるアクションやアクセスできるデータは、管理者がプロビジョニングしたデータコネクタ・ツール・権限の範囲に厳密に制限されるため、エンタープライズレベルのコンプライアンスとデータ保全が維持されます。

**アップデート前の課題**

- Agent Designer (ノーコードエージェント構築ツール) はプレビュー段階であり、本番業務での利用に対する GA レベルの位置づけがなかった
- 外部で構築した A2A / ADK エージェントを Gemini Enterprise に取り込んで一元的に管理・共有・統制する手段が限定的だった
- チャット会話の中からワークフローやカスタムエージェントを直接呼び出す統一的な方法がなかった

**アップデート後の改善**

- Workflow Builder が GA となり、マルチステップの自動化ワークフローを本番用途で構築・運用できるようになった
- ワークフローをスケジュール実行、手動のオンデマンド実行、チャット内の @-メンションの 3 通りで起動できるようになった
- 既存の A2A / ADK エージェントをインポートし、一元管理・共有・エンタープライズガバナンスの対象にできるようになった
- Google Workspace (Gmail、Google カレンダー、Google Chat、Google ドライブ) とサードパーティツール (Slack、Jira、ServiceNow、Confluence、Microsoft OneDrive、SharePoint、Outlook) への接続により、データ検索とアクション実行が可能になった
- 管理者は Google Cloud コンソールから、ワークフローとチャットエージェントの専用トグルを含む機能の組織全体での有効化 / 無効化を管理できるようになった

## アーキテクチャ図

```mermaid
flowchart LR
    U([👤 ビジネスユーザー]) -->|自然言語で構築| WB[🛠️ Workflow Builder]
    U -->|@-メンション| CHAT[💬 Gemini Enterprise チャット]
    ADM([🛡️ 管理者]) -->|機能トグル管理<br/>Google Cloud コンソール| WB

    WB --> WF[⚙️ ワークフロー<br/>スケジュール / オンデマンド実行]
    WB --> CA[🤖 チャットエージェント]
    IMP[📥 A2A / ADK エージェント<br/>インポート] --> GAL[🖼️ Agent Gallery<br/>検索 / フィルタ / ピン留め]
    WF --> GAL
    CA --> GAL
    GAL --> CHAT

    WF --> GWS[📧 Google Workspace<br/>Gmail / カレンダー / Chat / ドライブ]
    WF --> TP[🧩 サードパーティ<br/>Slack / Jira / ServiceNow / Confluence /<br/>OneDrive / SharePoint / Outlook]
```

Workflow Builder で構築したワークフローとチャットエージェント、およびインポートした A2A / ADK エージェントは Agent Gallery を通じて組織内に共有され、チャットから @-メンションで呼び出せます。ワークフローはエンタープライズコネクタ経由で Google Workspace やサードパーティツールのデータ検索・アクション実行を行います。

## サービスアップデートの詳細

### 主要機能

1. **ワークフローとオンデマンド実行**
   - トリガー、ステップ、アクションを組み合わせたマルチステップの自動化ワークフローを構築できる
   - 自動スケジュール実行、手動でのオンデマンド実行、Gemini Enterprise チャット会話内での @-メンションによる実行の 3 通りの起動方法に対応
   - AI による自動化と人間の介入 (レビュー・承認・情報リクエストなどの Human-in-the-loop ステップ) を組み合わせられる
   - 条件分岐、データフィルタリング、ループなどのフロー制御ステップに対応

2. **チャットエージェント**
   - 会話型のインタラクションで特定タスクを完了するエージェントを構築できる
   - チャット会話から @-メンションで呼び出せる
   - シングルステップ / マルチステップ (サブエージェントを持つ構成) の両方に対応

3. **会話内からの呼び出し (In conversation)**
   - チャット会話からワークフローを @-メンションで直接呼び出せる
   - Q&A やデータ参照から定型プロセスの起動まで、チャットを起点に完結できる

4. **エージェントインポート**
   - 既存の A2A (Agent2Agent Protocol) エージェントと ADK (Agent Development Kit) エージェントを Gemini Enterprise にインポートできる
   - 一元的な管理、組織内での共有、エンタープライズガバナンス (Agent Gateway 経由のポリシー適用など) の対象にできる

5. **エンタープライズコネクタ**
   - Google Workspace: Gmail、Google カレンダー、Google Chat、Google ドライブ
   - サードパーティ: Slack、Jira、ServiceNow、Confluence、Microsoft OneDrive、SharePoint、Outlook
   - データの検索に加え、メッセージ送信やレコード管理などの書き込みアクション実行に対応

6. **強化された Agent Gallery**
   - 組織全体のエージェントと Google 製エージェントをキーワード検索で発見できる
   - フィルタチップによる絞り込みとピン留めによる整理に対応

7. **管理者制御**
   - 管理者は Google Cloud コンソールで機能の利用可否を組織全体で管理できる
   - ワークフローとチャットエージェントそれぞれに専用のトグルが用意されている

### 作成方法

Workflow Builder では以下の方法でエージェントを作成できます。

- **自然言語プロンプト**: 「昨日のメールを要約して」のように機能を平易な言葉で記述すると、ステップ・条件・アクションを含むワークフローの雛形が自動生成される
- **ビジュアルエディタ (フロービルダー)**: 生成された雛形のステップの追加・削除・再構成を GUI で行える
- **テンプレート**: 一般的なビジネスユースケース向けのビルド済みテンプレートから開始できる
- **自然言語による編集**: 既存ワークフローへの変更内容を自然言語で記述して編集できる (一部のノードタイプは手動編集のみ)

## 技術仕様

### エージェントタイプ

| エージェントタイプ | 説明 | 適した用途 |
|------|------|------|
| チャットエージェント | 会話型インタラクションで特定タスクを完了。応答はユーザー入力に依存し、主に非決定的。シングルステップ / マルチステップの両方に対応 | 自由形式の会話、ユーザー入力でフローが変わる動的タスク、Q&A・データ参照 (例: Jira チケットの状態確認、メールスレッドの要約) |
| ワークフロー | 設定されたトリガーに基づき、AI 自動化と人間の介入を組み合わせた一連のステップ / アクションを実行。ロジックは決定的 / 非決定的の両方が可能 | 定義された順序ロジックを持つマルチステップ処理 (例: Gmail とカレンダーをまたぐオンボーディング自動化)、AI 生成 + 人間の承認、条件分岐を伴う複雑なオーケストレーション |

### 対応コネクタ

| 区分 | コネクタ |
|------|------|
| Google Workspace | Gmail、Google カレンダー、Google Chat、Google ドライブ |
| サードパーティ | Slack、Jira、ServiceNow、Confluence、Microsoft OneDrive、SharePoint、Outlook |

### A2A エージェントインポートのリージョン整合性

Agent Registry からのエージェントインポートでは、データレジデンシー要件遵守のため、アプリ・Agent Gateway・Agent Registry の 3 コンポーネントのリージョン整合が必要です。

| Gemini Enterprise アプリのロケーション | Agent Gateway のロケーション | Agent Registry のロケーション |
|------|------|------|
| global | us-central1 | us-central1、us、または global |
| us | us-central1 | us-central1 または us |
| eu | europe-west1 | europe-west1 または eu |

## 設定方法

### 前提条件

1. Gemini Enterprise 管理者が、アプリの機能管理設定で Workflow Builder の機能トグルを有効化していること
2. 必要なデータストアが接続された Gemini Enterprise Web アプリがあること
3. (A2A エージェントインポートの場合) Gemini Enterprise Admin ロールを持ち、Agent Gateway 経由でエージェントトラフィックをルーティングするゲートウェイが設定済みであること

### 手順

#### ステップ 1: 自然言語でエージェントを作成する

1. Gemini Enterprise Web アプリをブラウザで開く
2. サイドバーで「Agents」をクリックし、「Create agent」をクリック
3. 「Describe your agent」フィールドにエージェントの機能を記述する (例: 「メッセージに優先順位を付けてプロフェッショナルな返信を下書きする」)
4. 送信すると、フロービルダーにワークフローの雛形が生成される

#### ステップ 2: ワークフローを編集・テスト・公開する

1. フロービルダーで任意のステップをクリックし、構成パネルで設定を編集する
2. 「Preview」タブでワークフローの動作をテストする
3. 準備ができたら「Turn on」をクリックして有効化する
   - スケジュール済みワークフローは設定されたスケジュールで開始
   - イベントトリガー型ワークフローは設定されたイベントの待ち受けを開始

## メリット

### ビジネス面

- **全社的な自動化の民主化**: 開発者でなくても、自然言語とビジュアルエディタで業務自動化ワークフローを構築でき、組織全体の生産性向上につながる
- **既存ツールとのシームレスな連携**: Google Workspace に加え Slack、Jira、ServiceNow などの主要な業務ツールと接続でき、既存の業務フローに組み込みやすい
- **GA によるプロダクション適合性**: プレビュー段階の Agent Designer から GA に昇格したことで、本番業務での採用判断がしやすくなった

### 技術面

- **エージェント資産の一元管理**: 外部で構築した A2A / ADK エージェントをインポートし、Agent Gallery での共有とガバナンスの対象にできる
- **ガバナンスの担保**: エージェントの実行可能なアクションとアクセス可能なデータは管理者が許可した範囲に限定され、専用トグルで組織全体の機能提供を制御できる
- **柔軟な実行モデル**: スケジュール、オンデマンド、チャット内 @-メンション、イベントトリガーと複数の起動方法があり、ユースケースに応じて選択できる
- **Human-in-the-loop 対応**: 人間のレビュー・承認ステップをワークフローに組み込め、AI の出力を統制下で活用できる

## デメリット・制約事項

### 制限事項

- Workflow Builder の利用には、管理者が機能管理設定で機能トグルを有効化している必要がある
- 自然言語プロンプトで追加・編集できないノードタイプがあり、その場合は手動編集が必要
- Agent Registry からのエージェントインポートは、アプリに設定された Agent Gateway に関連付けられたレジストリからのみ可能
- ガバナンスポリシーは Agent Gateway に関連付けられた単一レジストリ内のエージェントにのみ適用できる
- Gemini Enterprise エージェント同士、または Gemini Enterprise エージェントとデータコネクタ間の直接通信には Agent Gateway のポリシー適用が働かない
- A2A エージェントのインポートではアプリ・Agent Gateway・Agent Registry のリージョン整合が厳密に強制される

### 考慮すべき点

- Agent Registry 経由でインポートしたエージェントを利用する場合、ユーザーのクエリ文字列やツールパラメータがエージェント (およびエージェントが呼び出すツールや MCP サーバー) に送信され、提供元の利用規約とプライバシーポリシーが適用される
- コネクタは書き込みアクション (メッセージ送信、レコード更新など) も実行できるため、接続するツールの権限設計を事前に整理しておく必要がある
- 利用可能な機能はエディションにより異なるため、契約中のエディションでの提供範囲を確認する必要がある

## ユースケース

### ユースケース 1: 従業員オンボーディングの自動化

**シナリオ**: 人事部門が、新入社員のオンボーディングチェックリスト (アカウント案内メールの送信、オリエンテーションの予定登録、チームチャネルへの通知など) を Gmail、Google カレンダー、Google Chat をまたいで手作業で実施している。

**実装例**:
```
1. Workflow Builder で「新入社員のオンボーディングチェックリストを自動化する」と自然言語で記述
2. 生成された雛形に Gmail (案内メール送信)、Google カレンダー (予定登録)、
   Google Chat (チーム通知) のコネクタアクションを設定
3. 人事担当者の承認 (Human-in-the-loop) ステップを挟んで有効化
```

**効果**: 複数ツールをまたぐ定型作業が自動化され、抜け漏れの防止と担当者の工数削減を実現。承認ステップにより統制も維持できる。

### ユースケース 2: チャットからの営業リード振り分け

**シナリオ**: 営業企画チームが、地域と予算に基づいて営業リードを各チームに振り分けるプロセスを運用しており、条件分岐が多く手作業ではミスが起きやすい。

**効果**: 条件分岐 (フロー制御ステップ) を備えたワークフローとして構築し、チャットから @-メンションでオンデマンド実行、または Jira / ServiceNow と連携して自動処理。振り分けロジックが標準化され、処理の一貫性とスピードが向上する。

### ユースケース 3: 既存 ADK エージェントの全社展開

**シナリオ**: 開発チームが ADK で構築したカスタムエージェントを、部門単位の利用から全社利用に広げたいが、管理・共有・統制の仕組みがない。

**効果**: エージェントインポート機能で Gemini Enterprise に取り込み、Agent Gallery で公開。キーワード検索・フィルタ・ピン留めで発見性を高めつつ、管理者制御とガバナンスポリシーの下で安全に全社展開できる。

## 料金

Workflow Builder を含むノーコードエージェント構築ツールの利用可否と料金は、Gemini Enterprise のエディション (Business、Standard、Plus、Pay-as-you-go、Frontline) によって異なります。Pay-as-you-go エディションでは、ノーコードエージェントの利用は Agent Platform の料金体系に基づく従量課金となります (エージェント作成自体には料金はかかりません)。

詳細は以下を参照してください。

- [Gemini Enterprise エディションの比較](https://docs.cloud.google.com/gemini/enterprise/docs/editions)
- [クォータと超過利用](https://docs.cloud.google.com/gemini/enterprise/docs/quotas-and-overages)
- [Gemini Enterprise 料金](https://cloud.google.com/gemini-enterprise)

## 利用可能リージョン

Gemini Enterprise アプリのロケーションは global、us、eu が提供されています。A2A エージェントインポートを利用する場合は、前述のとおり Agent Gateway / Agent Registry とのリージョン整合が必要です。最新のリージョン情報は [公式ドキュメント](https://docs.cloud.google.com/gemini/enterprise/docs/workflow-builder) を参照してください。

## 関連サービス・機能

- **Agent Development Kit (ADK)**: コードベースでエージェントを開発するフレームワーク。ADK で構築したエージェントを Workflow Builder のエージェントインポートで Gemini Enterprise に取り込める
- **Agent2Agent (A2A) Protocol**: 異なるビルダー・プラットフォームのエージェント同士が相互発見・連携・タスク委譲を行うためのオープンプロトコル。A2A エージェントをインポート対象にできる
- **Agent Registry / Agent Gateway**: A2A エージェントの発見・追跡・管理を行うカタログと、トラフィック制御・ポリシー適用を行うゲートウェイ。インポートしたエージェントのガバナンスに使用
- **Google Workspace**: Gmail、Google カレンダー、Google Chat、Google ドライブがコネクタとしてワークフローから利用可能
- **MCP サーバー**: ワークフローのステップまたは Gemini Agent ステップのツールとして MCP サーバーを接続できる

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260903-gemini-enterprise-workflow-builder-ga.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#September_03_2026)
- [Workflow Builder ドキュメント](https://docs.cloud.google.com/gemini/enterprise/docs/workflow-builder)
- [ワークフローの概要](https://docs.cloud.google.com/gemini/enterprise/docs/workflow-builder/workflow-agents)
- [自然言語でエージェントを作成する](https://docs.cloud.google.com/gemini/enterprise/docs/workflow-builder/create-natural-language)
- [Agent Registry からのエージェントのインポートとガバナンス](https://docs.cloud.google.com/gemini/enterprise/docs/import-govern-agent-registry)
- [Gemini Enterprise エディション](https://docs.cloud.google.com/gemini/enterprise/docs/editions)

## まとめ

Workflow Builder の GA により、Gemini Enterprise は「チャットで質問する AI」から「業務プロセスを自動実行するエージェント基盤」へと大きく前進しました。ノーコード / ローコードでの構築、豊富なエンタープライズコネクタ、A2A / ADK エージェントのインポート、管理者による統制が揃ったことで、全社規模でのエージェント活用を本格的に検討できる段階になっています。まずは管理者側で機能トグルとコネクタの権限設計を整理し、テンプレートや自然言語生成を使った小規模なワークフローから試験導入することを推奨します。

---

**タグ**: #GeminiEnterprise #WorkflowBuilder #AIエージェント #ノーコード #A2A #ADK #GA
