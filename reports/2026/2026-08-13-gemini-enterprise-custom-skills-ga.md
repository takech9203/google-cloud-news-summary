# Gemini Enterprise: カスタムスキルの作成・アップロード・共有機能が GA に

**リリース日**: 2026-08-13

**サービス**: Gemini Enterprise

**機能**: カスタムスキルの作成・アップロード・共有 (Create, upload, and share custom skills)

**ステータス**: GA (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260813-gemini-enterprise-custom-skills-ga.html)

## 概要

Gemini Enterprise で、エンドユーザーがカスタムスキルを作成・アップロード・共有できる機能が一般提供 (GA) になりました。スキルとは、Gemini Enterprise アシスタントに特定のタスクを実行させるための「再利用可能なカスタム指示」です。契約書のレビューやブランドボイスに沿った文章作成など、ドメイン固有の反復タスクをスキルとしてパッケージ化し、組織内で再利用できます。

スキルは [agentskills.io](https://agentskills.io/home) が管理するオープン標準に準拠しており、`skill.md` というプロンプトファイルを中核とするパッケージ形式です。パッケージにはスクリプト (Python / Bash)、参照ファイル、背景コンテキストを含めることができ、アシスタントはユーザーの質問やタスクに関連するスキルを自動的に呼び出します。

本機能を利用するには、管理者が Feature Management (機能管理) でスキルおよびスキル共有の設定を有効化する必要があります。管理者はスキルの利用可否の構成に加え、スキル共有リクエストの承認・却下、スキルの一時停止 (Suspend)・無効化 (Disable)・削除といったガバナンス操作も行えます。

**アップデート前の課題**

- スキル機能は「GA with allowlist」として提供されており、利用には Google アカウントマネージャーへの連絡と組織の許可リスト登録が必要だった
- 管理者向けの「Enable skills」トグルが Feature Management に用意されておらず、管理者がセルフサービスで機能を有効化できない期間があった (2026 年 7 月 9 日のリリースノートで案内)
- ドメイン固有のタスクをアシスタントに教えるには、肥大化したシステムプロンプトへの記述や、Agent Designer での個別エージェント作成に頼る必要があった

**アップデート後の改善**

- 許可リスト不要の GA となり、管理者が Feature Management のトグル操作だけでスキル機能と共有機能を有効化できるようになった
- エンドユーザーが Web アプリ上で自然言語または Markdown 編集によりスキルを作成し、Markdown / ZIP ファイルのインポート (アップロード) や他ユーザーへの共有ができるようになった
- 管理者によるスキル共有リクエストの承認フロー、スキルの一時停止・無効化・削除といったエンタープライズ向けガバナンス管理が利用可能になった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Admin["🛠️ 管理者 (Google Cloud コンソール)"]
        FM["⚙️ Feature Management<br/>Enable skills / Enable skill sharing"]
        REV{"✅ 共有リクエスト<br/>承認 / 却下"}
        GOV["🛡️ ガバナンス操作<br/>Suspend / Disable / Delete"]
    end

    subgraph User["👥 エンドユーザー (Gemini Enterprise Web アプリ)"]
        CREATE["📝 スキル作成<br/>(自然言語 / Markdown)"]
        IMPORT["📦 インポート<br/>(Markdown / ZIP)"]
        SHARE["🔗 スキル共有リクエスト"]
    end

    SKILL[("🧩 スキル<br/>skill.md + scripts/")]
    ASSISTANT["🤖 Gemini Enterprise<br/>アシスタント"]

    FM -->|機能を有効化| User
    CREATE --> SKILL
    IMPORT --> SKILL
    SHARE --> REV
    REV -->|承認| SKILL
    GOV -.->|状態管理| SKILL
    SKILL -->|@メンション / 自動選択| ASSISTANT
```

管理者が Feature Management でスキル機能を有効化すると、エンドユーザーはスキルの作成・インポート・共有が可能になり、アシスタントは会話の中で関連スキルを自動または手動で呼び出します。共有には管理者の承認フローを挟むことができます。

## サービスアップデートの詳細

### 主要機能

1. **スキルの作成 (エンドユーザー)**
   - Web アプリのナビゲーションメニューから「Skills」→「+ New skill」で作成
   - スキル名 (組織内で一意)、説明、指示 (Instructions) を設定。説明にはトリガー指示を含めることができ、アシスタントがスキルを使うべきかの判断に利用される
   - チャットボックスでの自然言語入力、または Markdown の直接編集で指示を記述可能

2. **スキルのインポート (アップロード)**
   - 既存のスキルを Markdown または ZIP ファイルとしてインポート可能
   - ZIP パッケージには `skill.md` (ルートディレクトリに必須) に加え、Python / Bash コードを含む `scripts/` ディレクトリを同梱できる
   - 名前・説明・指示はアップロードされたファイルから自動抽出される

3. **スキルの共有と管理者承認フロー**
   - エンドユーザーは作成したスキルを他のユーザーと共有可能
   - 管理者が「Enable skill sharing without admin approval」を有効にしていない場合、共有リクエストは管理者の承認 (Approve) / 却下 (Deny) を経て反映される

4. **管理者によるガバナンス**
   - Feature Management の 3 つのトグル (Enable skills / Enable skill sharing / Enable skill sharing without admin approval) で機能の開放範囲を制御
   - ユーザー作成スキルの一覧表示、一時停止 (Suspended)、無効化 (Disabled)、却下 (Private に戻す)、削除が可能

5. **スキルの利用方法**
   - **手動メンション**: チャットバーで `@スキル名` (例: `@Brand Voice`) で明示的に呼び出し
   - **直接依頼**: プロンプト内で「〇〇スキルを使ってレビューして」と依頼
   - **自動選択**: スキルの説明とトリガー指示に基づき、タスクに関連するスキルをアシスタントが自動的に使用
   - Skills ギャラリーから「Try it」でスキルを試すことも可能

6. **Google 提供のデフォルトスキル**
   - Brand Voice (ブランドガイドライン準拠)、Contract Creation (契約書ドラフト作成)、Contract Review (契約書レビュー)、Customer Briefing (顧客ブリーフィング)、Project Updates (プロジェクト状況の集約) が Google 管理スキルとして提供される
   - Google 管理スキルは直接編集できないが、「Duplicate to edit」で複製して編集可能

## 技術仕様

### スキルの構成要素

| 項目 | 詳細 |
|------|------|
| パッケージ形式 | `skill.md` (プロンプトファイル) を中核とするパッケージ。スクリプト・ファイル・背景コンテキストを同梱可能 |
| 準拠標準 | [agentskills.io](https://agentskills.io/home) が管理するオープン標準 |
| インポート形式 | Markdown ファイルまたは ZIP ファイル (`skill.md` がルートに必須) |
| スクリプト実行 | Python と Bash のみサポート |
| スキル名 | 組織内で一意である必要がある |
| 呼び出し方法 | @メンション / プロンプトでの直接依頼 / 自動選択 |

### スキルの状態 (管理者ビュー)

| 状態 | 説明 |
|------|------|
| Private | 他のユーザーに共有されておらず、スキル所有者のみ利用可能 |
| Suspended | 一時停止中。ギャラリーには「Suspended」ラベル付きで表示されるが、会話では呼び出せない。所有者は更新・テスト可能 |
| Disabled | ギャラリーから非表示となり、利用不可 |

### Feature Management のトグル

| トグル | 説明 |
|--------|------|
| Enable skills | ユーザーによるスキルの作成・使用を許可 |
| Enable skill sharing | ユーザーによるスキル共有を許可 (Enable skills が前提)。承認なし共有を有効にしない限り、管理者が共有リクエストを承認する必要がある |
| Enable skill sharing without admin approval | 管理者承認なしでの即時共有・利用を許可 (上記 2 つのトグルが前提) |

## 設定方法

### 前提条件

1. Gemini Enterprise の Standard、Plus、Pay-as-you-go、Frontline のいずれかのエディションのライセンス
2. 管理操作には Gemini Enterprise Admin IAM ロール (`roles/discoveryengine.agentspaceAdmin`) が必要

### 手順

#### ステップ 1: 管理者がスキル機能を有効化

1. Google Cloud コンソールで「Gemini Enterprise」ページに移動
2. 構成するアプリ名をクリック
3. 「Configurations」→「Feature Management」タブをクリック
4. 用途に応じて「Enable skills」「Enable skill sharing」「Enable skill sharing without admin approval」のトグルをオンにする

スキル機能はデフォルトで無効のため、この設定が必須です。

#### ステップ 2: エンドユーザーがスキルを作成またはインポート

1. Gemini Enterprise Web アプリにサインイン
2. ナビゲーションメニューで「Skills」をクリック
3. 「+ New skill」で新規作成 (一意の名前・説明・指示を入力)、または「Import」で Markdown / ZIP ファイルをインポート
4. 作成・インポートしたスキルはデフォルトで有効化される

#### ステップ 3: 管理者が共有リクエストをレビュー (承認制の場合)

1. Google Cloud コンソールの「Gemini Enterprise」ページで対象アプリの「Skills」を開く
2. Pending (保留中) の共有ステータスを持つスキルの「Review share request」をクリック
3. 共有先ユーザーを選択し、「Approve」(承認) または「Deny」(却下) をクリック

## メリット

### ビジネス面

- **組織ナレッジの再利用**: 契約書レビューの観点、ブランドガイドライン、報告書のフォーマットなど、部門固有のノウハウをスキル化して組織全体で共有・再利用できる
- **セルフサービスでの導入**: 許可リスト申請が不要になり、管理者のトグル操作のみで即座に全社導入できる
- **統制されたシェアリング**: 管理者承認フローにより、品質やコンプライアンスの観点で問題のあるスキルの拡散を防止できる

### 技術面

- **プロンプトの肥大化を回避**: 巨大なシステムプロンプトへの記述やファインチューニングに頼らず、モジュール化された指示でアシスタントにドメイン知識を追加できる
- **オープン標準準拠**: agentskills.io のオープン標準に準拠しているため、他のエージェント環境で作成したスキル資産を Markdown / ZIP でインポートして再利用しやすい
- **自動呼び出し**: スキルの説明とトリガー指示に基づきアシスタントが関連スキルを動的に選択するため、ユーザーがスキルの存在を意識しなくても恩恵を受けられる
- **段階的なガバナンス**: 一時停止 (所有者はテスト継続可能) → 無効化 → 却下 → 削除と、状況に応じた粒度でスキルのライフサイクルを管理できる

## デメリット・制約事項

### 制限事項

- スキルはエージェント (Agent Designer などで作成したエージェント) では利用できず、コアアシスタントとの会話でのみ有効
- スキル内のスクリプト実行は Python と Bash のみサポート
- Web アプリのエディタで作成できるのは単一の `skill.md` を持つスキルのみ。スクリプトや追加ファイルを含む複雑なスキルは ZIP でのインポートが必要
- Gemini Enterprise に統合したカスタム MCP (Model Context Protocol) サーバーとスキルは連携できない
- 自然言語でのスキル作成では、会話コンテキストやコネクタの内容を入力として利用できない
- 応答生成にスキルが使われても、UI 上でどのスキルが使用されたかは明示されない

### 考慮すべき点

- スキル機能はデフォルトで無効のため、管理者による Feature Management での有効化が必須
- 自動選択は期待どおりにトリガーされない場合がある (既知の問題)。確実に使わせたい場合は @メンションや直接依頼を推奨
- ZIP パッケージに複数ファイルを含めた場合、UI に表示されるのは `skill.md` のみ (他のファイルは内部的に実行時利用される)
- 却下 (Reject) 時に入力した理由はスキル所有者に表示されないという既知の制限があるため、別途フィードバック手段を用意するとよい
- Google 管理スキルは管理者コントロールで全ユーザーに対して一時停止・無効化できない (エンドユーザーが個別にオフにすることは可能)

## ユースケース

### ユースケース 1: 法務部門の契約書レビュー観点の標準化

**シナリオ**: 法務部門が自社の契約書レビューチェックリスト (準拠法、責任制限条項、解約条件など) をスキル化し、営業部門やパートナー管理部門に共有する。各部門の担当者は法務に都度依頼せずに一次レビューを実施できる。

**実装例**:
```markdown
# skill.md (契約書一次レビュースキル)
name: 契約書一次レビュー
description: 契約書ドラフトのレビュー依頼時に使用。責任制限・準拠法・
  解約条件・自動更新条項をチェックし、リスクを 3 段階で評価する。

## 指示
1. アップロードされた契約書から以下の条項を抽出する
   - 責任制限 (上限額・除外事由)
   - 準拠法・裁判管轄
   - 契約期間・自動更新・解約予告期間
2. 自社標準 (別紙ガイドライン) との差分を表形式で提示する
3. リスクを High / Medium / Low で評価し、法務エスカレーションの要否を示す
```

**効果**: レビュー観点が組織全体で標準化され、法務部門への一次確認依頼が削減される。共有時に管理者承認を挟むことで、ガイドライン改訂時の品質統制も維持できる。

### ユースケース 2: ブランドボイスに沿ったコンテンツ作成の全社展開

**シナリオ**: マーケティング部門がトーン & マナー、用字用語、禁止表現をまとめたブランドボイススキルを作成し、全社に共有する。各部門はプレスリリース、提案書、社外メールの作成時に `@ブランドボイス` で呼び出す。

**効果**: 部門ごとにばらついていた対外文書の品質・トーンが統一され、マーケティング部門による最終チェックの手戻りが減少する。Google 提供の Brand Voice スキルを複製 (Duplicate to edit) して自社向けにカスタマイズすることで、ゼロから作成する手間も省ける。

### ユースケース 3: 既存のスキル資産の移行・再利用

**シナリオ**: 開発チームが agentskills.io 標準に準拠して他のエージェント環境向けに作成済みのスキル (`skill.md` + `scripts/` の ZIP パッケージ) を、Gemini Enterprise にインポートしてビジネスユーザーにも開放する。

**効果**: オープン標準準拠のため、スキル資産を書き直すことなく Gemini Enterprise で再利用できる。Python / Bash スクリプトを含む高度なスキルも ZIP インポートで展開可能。

## 料金

スキル機能自体の追加料金に関する個別の記載はなく、Gemini Enterprise のエディション (Standard、Plus、Pay-as-you-go、Frontline) のライセンスに含まれる機能として提供されます。Gemini Enterprise はユーザー単位・月単位のサブスクリプション課金です。エディションごとの機能・クォータの詳細は以下を参照してください。

- [Gemini Enterprise エディション比較](https://docs.cloud.google.com/gemini/enterprise/docs/editions)
- [Gemini Enterprise の料金](https://cloud.google.com/gemini-enterprise/pricing)

## 利用可能リージョン

スキルに固有のロケーション制限はありません。ただし、スキルが利用できるかどうかはチャット会話で選択されているモデルに依存します。詳細は [Gemini Enterprise の既知の制限](https://docs.cloud.google.com/gemini/enterprise/docs/known-limitations) を参照してください。

## 関連サービス・機能

- **Agent Designer (Gemini Enterprise)**: ノーコードでエージェントを構築するツール。スキルが「再利用可能な部品としての反復タスク」に適するのに対し、承認を伴う複雑な複数ステップのワークフローにはエージェントが適する
- **Feature Management (Gemini Enterprise 管理)**: スキルのほか、エージェント共有やモデル選択など Web アプリのエンドユーザー機能を管理者が制御する仕組み
- **Gemini Enterprise Agent Platform (Skill Registry)**: 開発者向けに API / SDK でスキルを登録・管理する仕組み。`CreateSkill` API で ZIP パッケージ化したスキルをプログラマティックに登録できる
- **Agent Registry**: スタンドアロンスキルの登録・バージョン管理・公開元検証を行うガバナンス基盤。エンタープライズレベルのスキル管理を補完する

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260813-gemini-enterprise-custom-skills-ga.html)
- [公式リリースノート (2026 年 8 月 13 日)](https://docs.cloud.google.com/release-notes#August_13_2026)
- [ドキュメント: エンドユーザー向けスキルの作成と管理](https://docs.cloud.google.com/gemini/enterprise/docs/skills)
- [ドキュメント: 管理者向けスキルの管理](https://docs.cloud.google.com/gemini/enterprise/docs/manage-skills)
- [ドキュメント: Web アプリ機能の管理 (Feature Management)](https://docs.cloud.google.com/gemini/enterprise/docs/manage-web-app-features)
- [料金ページ](https://cloud.google.com/gemini-enterprise/pricing)

## まとめ

Gemini Enterprise のカスタムスキルが許可リスト不要の GA となり、エンドユーザー主導でのスキル作成・アップロード・共有と、管理者による承認・ガバナンスの両輪が揃いました。組織のドメイン知識をオープン標準準拠のスキルとして資産化できる重要なアップデートです。まずは管理者が Feature Management で「Enable skills」を有効化し、承認フロー付きの共有設定でスモールスタートすることを推奨します。

---

**タグ**: #GeminiEnterprise #Skills #GA #生成AI #エージェント #ガバナンス
