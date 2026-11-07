# Agent Registry: スタンドアロンスキルの GA とスキルセキュリティスキャン・ガバナンス機能の提供開始

**リリース日**: 2026-11-06

**サービス**: Agent Registry

**機能**: スタンドアロンスキルの一般提供 (GA) + スキルセキュリティスキャン・ガバナンス (CMEK は Preview)

**ステータス**: GA (スタンドアロンスキル) / 提供開始 (セキュリティスキャン・ガバナンス) / Preview (CMEK)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261106-agent-registry-standalone-skills-ga.html)

## 概要

Agent Registry のスタンドアロンスキル (standalone skills) が一般提供 (GA) になりました。スタンドアロンスキルは、エージェントへの指示 (SKILL.md)、オプションのスクリプト、ドメイン知識をモジュール化されたパッケージとしてまとめたもので、特定のエージェントデプロイメントから独立して管理できます。GA により、トップレベルの `Skill` リソースの登録・検索・ガバナンス、イミュータブルな `SkillRevision` パッケージによるバージョン管理、検証済み `Publisher` 情報の確認が本番環境で利用できるようになりました。

あわせて、スキルのセキュリティスキャンとガバナンス機能も提供開始されました。アップロードされたスキルリビジョンを LLM ベースのスキャナーで自動スキャンし、不正なデータ持ち出し (data exfiltration)、認証情報の露出、プロンプトインジェクションなどのリスクを `Finding` リソースとして検出できます。カスタム組織ポリシー制約による組織全体でのスキャンポリシー強制、最小権限のスキル管理アクセス (IAM ロール)、そして顧客管理の暗号鍵 (CMEK) によるスキルペイロードの保管時保護 (Preview) もサポートされます。

このアップデートは、複数のチーム・プロジェクトにまたがって AI エージェントのスキル (再利用可能なタスクロジック) を安全に共有・統制したいプラットフォームチームやセキュリティ管理者にとって重要なマイルストーンです。2026 年 7 月の Preview 公開から約 4 か月での GA 到達となります。

**アップデート前の課題**

- スタンドアロンスキルのガバナンス機能は 2026 年 7 月から Preview 段階であり、本番ワークロードでの利用には Pre-GA 提供条件が適用されていた
- スキルパッケージに悪意ある指示 (プロンプトインジェクション) や認証情報の埋め込みが含まれていても、レジストリ側で自動検出する仕組みがなく、開発者による手動レビューに依存していた
- 組織全体で「スキャンを無効化したスキルの登録を禁止する」といったポリシーを一元的に強制する手段がなかった
- スキルペイロードの保管時暗号化は Google のデフォルト暗号化のみで、鍵を顧客側で管理する選択肢がなかった

**アップデート後の改善**

- スタンドアロンスキル (`Skill`、`SkillRevision`、`Publisher` の 3 階層リソース) が GA となり、本番環境での登録・バージョン管理・セマンティック検索・ガバナンスが正式サポートされた
- 新しいスキルリビジョンのアップロード時に LLM ベースのセキュリティスキャンが自動実行され (デフォルトで `ENABLED_BLOCKING`)、検出された問題は読み取り専用の `Finding` リソースとして確認できるようになった
- `agentregistry.googleapis.com/Skill` リソースに対するカスタム組織ポリシー制約で、スキャン無効化の禁止やブロッキングモードの強制を組織・フォルダ単位で適用できるようになった
- `roles/agentregistry.user` などの事前定義ロールにより、エージェントや MCP サーバーの編集権限を与えずにスキル管理のみを許可する最小権限アクセスが可能になった
- Cloud KMS の CMEK でスキルペイロードを保管時に保護できるようになった (Preview、`us` / `eu` ロケーション)

## アーキテクチャ図

```mermaid
flowchart TD
    Dev([👩‍💻 スキル開発者]) -->|ZIP アップロード<br>SKILL.md + scripts| Skill

    subgraph AR["🗂️ Agent Registry (ガバナンスプロジェクト)"]
        Pub["✅ Publisher<br>(所有者・検証ティア)"] --> Skill["📦 Skill<br>(コンテナ / defaultRevision)"]
        Skill --> Rev["🔒 SkillRevision<br>(イミュータブルな版)"]
        Rev -->|自動スキャン<br>(非同期)| Scanner["🤖 LLM セキュリティスキャナー"]
        Scanner -->|検出結果| Finding["⚠️ Finding リソース"]
    end

    OrgPolicy["🏛️ カスタム組織ポリシー<br>(スキャンポリシー強制)"] -.->|CREATE / UPDATE を制御| Skill
    KMS[("🔑 Cloud KMS<br>CMEK (Preview)")] -.->|保管時暗号化| Rev
    Finding -->|ブロッキング時は<br>DL・昇格をブロック| Agent([🤖 エージェント / 利用者])
    Skill -->|検索・解決・DL| Agent
```

スキル開発者が ZIP パッケージをアップロードすると、Agent Registry が `SkillRevision` としてバージョン管理し、LLM ベースのスキャナーが非同期にセキュリティスキャンを実行します。検出された問題は `Finding` リソースとして公開され、ブロッキングポリシーの場合は問題のあるリビジョンのダウンロードやデフォルトリビジョンへの昇格がブロックされます。

## サービスアップデートの詳細

### 主要機能

1. **スタンドアロンスキルの 3 階層リソースモデル (GA)**
   - **Publisher**: スキルの出所・検証ティア・命名プレフィックスを確立。Google 管理パブリッシャー (`FIRST_PARTY`、例: `cloud.google.com`) と、カスタムスキルに自動割り当てされるプライベートパブリッシャー (`PRIVATE`) の 2 種類
   - **Skill (コンテナ)**: 利用者が実行時に発見・解決するトップレベルリソース。デフォルトで提供するリビジョンへのポインタ (`defaultRevision`) を保持
   - **SkillRevision**: スキルパッケージのイミュータブルなスナップショット。更新時は既存パッケージを変更せず新しいリビジョンを作成するため、決定論的な実行、制御されたロールバック、監査可能性が確保される
   - スキル識別子は URN 形式 (例: `urn:skill:projects-PROJECT_NUMBER:locations:global:private-incident-triage`)

2. **パッケージ仕様とバリデーション**
   - オープン標準の [Agent Skills Specification](https://agentskills.io/specification) に準拠した ZIP アーカイブとしてパッケージング
   - アーカイブのルートに SKILL.md (YAML フロントマター + 自然言語の指示) が必須
   - 登録時に仕様準拠とペイロード制約を検証し、メタデータを検索用にインデックス化

3. **自動セキュリティスキャン**
   - スキルリビジョンのアップロード時に、SKILL.md・スクリプト・アセットを LLM で解析し、不正なデータ持ち出し、認証情報の露出、プロンプトインジェクションなどを検出
   - 検出結果は読み取り専用の `Finding` リソース (`projects/PROJECT_NUMBER/locations/LOCATION/findings/FINDING_ID`) として公開
   - 3 つのスキャンポリシー: `ENABLED_BLOCKING` (デフォルト: 問題検出時にダウンロードとデフォルトリビジョン昇格をブロック)、`ENABLED_NONBLOCKING` (監査モード: 警告付きで許可)、`DISABLED` (スキャン無効)
   - 注意: LLM による解析は確率的であり、偽陽性・偽陰性が発生しうるため、検出結果は開発者による確認が必要

4. **組織ポリシーによるスキャン強制**
   - `agentregistry.googleapis.com/Skill` リソースタイプに対するカスタム組織ポリシー制約を定義し、`CREATE` / `UPDATE` 操作時にスキャンポリシーを評価
   - 例: `resource.scanningConfig.policy == "DISABLED"` を `DENY` して、スキャン無効化スキルの登録を組織全体で禁止
   - Resource Manager タグによる条件付き除外 (テスト用プロジェクトの免除など) にも対応

5. **最小権限のスキル管理アクセス**
   - `roles/agentregistry.user` ロールにより、エージェント・MCP サーバー・エンドポイントの編集権限を付与せずに、スキルとスキルリビジョンの作成・更新・削除とスキャン設定のみを許可可能
   - スキルリソース単位の IAM ポリシー (`agentregistry.skills.getIamPolicy` / `setIamPolicy`) にも対応し、プロジェクト全体の権限を付与せずに特定スキルへのアクセスを制御できる

6. **CMEK によるスキルペイロードの保護 (Preview)**
   - Cloud KMS の顧客管理暗号鍵でスキルリビジョンのペイロードを保管時に暗号化
   - 対象ロケーションの `SkillEncryptionSpec` リソースを構成して利用 (対応ロケーション: `us` / `eu`)

## 技術仕様

### リソースモデルとライフサイクル

| 項目 | 詳細 |
|------|------|
| リソース階層 | `Publisher` → `Skill` (コンテナ) → `SkillRevision` (イミュータブル) |
| リビジョンのリソース名 | `projects/PROJECT_NUMBER/locations/LOCATION/skills/SKILL_ID/revisions/REVISION_ID` |
| ライフサイクル状態 (targetState) | `DRAFT` / `ACTIVE` / `DISABLED` / `DEPRECATED` / `DECOMMISSIONED` |
| パブリッシャー種別 | `FIRST_PARTY` (Google 管理・全プロジェクトで発見可能) / `PRIVATE` (`private-` プレフィックス自動付与) |
| パッケージ仕様 | Agent Skills Specification 準拠の ZIP (ルートに SKILL.md 必須) |

### ペイロード制約 (インジェスト時)

| 制約項目 | 上限 |
|----------|------|
| ZIP アーカイブサイズ (圧縮後) | 最大 1 MB |
| 展開後の合計サイズ (スキャン有効時) | 最大 10 MB |
| 個別ファイルサイズ (スキャン有効時) | 最大 1 MB |
| ディレクトリのネスト深度 | 最大 8 階層 |

スキャン有効時にサイズ上限を超えると、リビジョン作成が `INVALID_ARGUMENT` エラーで失敗するか、スキャンステータスが `UNSUPPORTED_FORMAT` になります。

### IAM ロール (最小権限設計)

| ロール | 用途 |
|--------|------|
| `roles/agentregistry.user` | スキル・スキルリビジョンの作成/更新/削除、スキャン設定。エージェントや MCP サーバーの編集権限なし |
| `roles/agentregistry.viewer` | スキル・リビジョン・パブリッシャー等の読み取り専用アクセス |
| `roles/agentregistry.editor` | スキルに加え、エージェント・MCP サーバー・エンドポイントの編集 |
| `roles/agentregistry.admin` | 全リソースへのフルアクセス。セキュリティ Finding の閲覧、CMEK 構成、スキル IAM ポリシー管理 |
| `roles/orgpolicy.policyAdmin` | 組織・フォルダレベルでのスキャンポリシー強制 |

`roles/agentregistry.admin` / `roles/agentregistry.editor` は信頼できる管理者のみに付与し、エージェント自身には付与しないことが推奨されています (ツールアノテーションの悪意ある変更や不正エージェントの登録を防ぐため)。

### CMEK の要件 (Preview)

| 項目 | 詳細 |
|------|------|
| 対応スキルロケーション | `us` / `eu` のみ (`global` は非対応) |
| 必要な Cloud KMS 鍵ロケーション | `us` → `us`、`eu` → `europe` (マルチリージョンの対称鍵) |
| 構成タイミング | 対象ロケーションにスキルを登録する**前**に `SkillEncryptionSpec` を構成 (スキル作成後は変更不可) |
| 必要な権限付与 | Agent Registry サービスエージェントに `roles/cloudkms.cryptoKeyEncrypterDecrypter` |

## 設定方法

### 前提条件

1. [Agent Registry のセットアップ](https://docs.cloud.google.com/agent-registry/setup) が完了していること (ガバナンスプロジェクト、または複数プロジェクト構成の場合は管理プロジェクト)
2. 適切な IAM ロール (`roles/agentregistry.user` など) が付与されていること
3. CMEK を使用する場合: Cloud KMS API の有効化、対応するマルチリージョンでのキーリング・対称鍵の作成

### 手順

#### ステップ 1: スキャンポリシー付きでスキルを登録

```bash
gcloud agent-registry skills create SKILL_ID \
  --project=PROJECT_ID \
  --location=LOCATION \
  --display-name="DISPLAY_NAME" \
  --description="DESCRIPTION" \
  --payload="LOCAL_ZIP_PATH"
```

新規スキルのスキャンポリシーはデフォルトで `ENABLED_BLOCKING` です。スキャンが完了して問題が検出されなかった場合のみ、初期リビジョンが自動的に Active 状態に遷移します。

#### ステップ 2: 組織ポリシーでスキャンを強制

```yaml
# skills-scan-constraint.yaml
name: organizations/ORGANIZATION_ID/customConstraints/custom.skillsScanningEnforcement
resourceTypes:
- agentregistry.googleapis.com/Skill
methodTypes:
- CREATE
- UPDATE
condition: resource.scanningConfig.policy == "DISABLED"
actionType: DENY
displayName: Prevent Disabling Skills Scanning
description: Prevents creating or updating skills with scanning disabled.
```

```bash
gcloud org-policies set-custom-constraint skills-scan-constraint.yaml
gcloud org-policies set-policy skills-scan-policy.yaml
```

すべてのスキルでブロッキングモードを必須にする場合は、`condition: resource.scanningConfig.policy == "ENABLED_BLOCKING"` と `actionType: ALLOW` を設定します。

#### ステップ 3: CMEK の構成 (Preview、任意)

```bash
gcloud alpha agent-registry skill-encryption-spec update \
  --project=PROJECT_ID \
  --location=SKILL_LOCATION \
  --kms-key=projects/KMS_PROJECT_ID/locations/KMS_LOCATION/keyRings/KEY_RING/cryptoKeys/KEY_NAME
```

対象ロケーション (`us` または `eu`) にスキルを登録する前に実行する必要があります。

#### ステップ 4: ライフサイクル状態の管理

```bash
gcloud agent-registry skills update SKILL_ID \
  --project=PROJECT_ID \
  --location=LOCATION \
  --target-state=DISABLED
```

`DRAFT` / `ACTIVE` / `DISABLED` / `DEPRECATED` / `DECOMMISSIONED` の各状態に遷移できます。

## メリット

### ビジネス面

- **エンタープライズガバナンスの確立**: GA により SLA が適用され、本番環境でスキルの一元管理・共有・統制を安心して導入できる
- **サプライチェーンリスクの低減**: 侵害されたスキルや悪意あるスキルがエージェントに到達する前に自動スキャンで検出・ブロックでき、AI エージェントのサプライチェーンセキュリティを強化できる
- **コンプライアンス対応**: 組織ポリシーによる全社的なスキャン強制と CMEK による鍵管理で、規制要件や社内セキュリティポリシーに対応しやすくなる

### 技術面

- **決定論的な実行と安全なロールバック**: イミュータブルな `SkillRevision` に特定バージョンをピン留めでき、問題発生時は `defaultRevision` ポインタを以前のリビジョンに戻すだけでロールバックできる
- **最小権限の運用**: `roles/agentregistry.user` やスキルリソース単位の IAM ポリシーにより、スキル管理者とレジストリ管理者の職務分離が可能
- **監査可能性**: 過去のリビジョンが明示的に削除されるまで保持され、履歴の検査が可能

## デメリット・制約事項

### 制限事項

- セキュリティスキャンは LLM ベースの確率的な解析であり、偽陽性・偽陰性が発生する可能性がある。実行ごとに結果が変動したり、検出詳細にハルシネーションが含まれる可能性があるため、修正適用前に開発者による確認・検証が必須
- スキャン有効時のペイロードサイズ制限 (展開後合計 10 MB、個別ファイル 1 MB) が適用される
- スキャン設定の変更は設定変更後に作成されたリビジョンにのみ適用され、既存リビジョンは遡及スキャンされない
- CMEK は Preview であり、対応ロケーションは `us` / `eu` のみ (`global` は非対応)。スキルが既に存在するロケーションでは鍵の設定・変更ができない
- カスタム `Publisher` リソースは登録できない (プライベートスキルには自動的に `private-` プレフィックスが付与される)

### 考慮すべき点

- `ENABLED_BLOCKING` (デフォルト) では、スキャン保留中や Finding が存在するリビジョンのダウンロード・デフォルトリビジョン昇格がブロックされるため、CI/CD パイプラインでのリリースフローに影響する可能性がある
- デフォルトリビジョンに設定されているリビジョンを削除すると、ポインタがクリアされてスキルが `DISABLED` 状態に遷移する
- スキャン料金は 2026 年 12 月 31 日まで無料だが、2027 年 1 月 1 日から従量課金が始まるため、リビジョン作成頻度が高い場合はコストを見積もっておく

## ユースケース

### ユースケース 1: 組織全体でのセキュアなスキル共有基盤

**シナリオ**: 複数の開発チームがそれぞれ AI エージェント用のスキル (インシデントトリアージ、レポート作成など) を開発しており、プラットフォームチームが品質とセキュリティを統制しながら全社で再利用できるようにしたい。

**実装例**:
```bash
# プラットフォームチーム: 組織ポリシーでスキャン無効化を禁止
gcloud org-policies set-custom-constraint skills-scan-constraint.yaml
gcloud org-policies set-policy skills-scan-policy.yaml

# 開発チーム: roles/agentregistry.user のみでスキルを登録・バージョン管理
gcloud agent-registry skills create incident-triage \
  --project=governance-project \
  --location=global \
  --display-name="Incident Triage" \
  --payload="./incident-triage.zip"
```

**効果**: 開発チームはレジストリ全体の管理権限なしでスキルを自律的に管理でき、プラットフォームチームはすべてのスキルが自動スキャンを通過することを組織ポリシーで保証できる。

### ユースケース 2: 規制業界でのスキルペイロード保護

**シナリオ**: 金融機関が社内ノウハウを含むスキルパッケージを Agent Registry で管理したいが、保管時暗号化の鍵を自社で管理することが社内規程で求められている。

**効果**: `us` または `eu` ロケーションで `SkillEncryptionSpec` に Cloud KMS の CMEK を構成することで、鍵のローテーション・アクセス制御・監査ログ・ライフサイクルを自社で管理しながらスキルを登録できる (Preview)。

## 料金

Agent Registry でのスキルの登録・保存・検索・管理は無料です。課金が発生するのはスキル脆弱性スキャンのみです。

| 機能 | 料金 (USD) | 適用時期 |
|------|-----------|----------|
| レジストリ保存 (エージェント、MCP サーバー、スキル、リビジョン等) | 無料 ($0.00) | 常時 |
| 検索・ディスカバリ・API 操作 | 無料 ($0.00) | 常時 |
| スキル脆弱性スキャン | 無料 ($0.00) | 2026 年 12 月 31 日まで |
| スキル脆弱性スキャン | $8.00 / 100 万入力トークン | 2027 年 1 月 1 日から |

### 料金例

| 使用量 | 料金 (2027 年 1 月以降、概算) |
|--------|-------------------------------|
| 10 KB の ZIP (約 2,500 入力トークン) のリビジョン 1 回スキャン | 約 $0.02 |
| 同リビジョンの検索・メタデータ更新・ダウンロード | $0.00 |

課金対象はアップロードしたスキルパッケージ内の入力トークン (SKILL.md、スクリプト、テキストアセット) のみで、内部のシステムプロンプトや出力トークンには課金されません。`DISABLED` ポリシーのスキル、既存リビジョン、Google 管理スキルにはスキャン料金が発生しません。

## 利用可能リージョン

- スキルのレジストリロケーションとしては `global` などが利用できます (詳細は[ドキュメント](https://docs.cloud.google.com/agent-registry/skills-architecture)を参照)
- CMEK (Preview) は `us` および `eu` ロケーションのみ対応で、それぞれ Cloud KMS の `us` / `europe` マルチリージョン鍵が必要です

## 関連サービス・機能

- **Cloud KMS**: CMEK によるスキルペイロードの保管時暗号化で使用。鍵のローテーション、アクセス制御、監査ログを顧客側で管理
- **Organization Policy Service**: `agentregistry.googleapis.com/Skill` に対するカスタム制約でスキャンポリシーを組織・フォルダ単位で強制。`gcp.restrictNonCmekServices` 等の CMEK 組織ポリシーとも連携
- **IAM**: 事前定義ロール (`agentregistry.user` / `viewer` / `editor` / `admin`) とスキルリソース単位の IAM ポリシーによるアクセス制御
- **Resource Manager (タグ)**: 組織ポリシーの条件付き除外 (テストプロジェクトの免除など) に使用
- **Agent Gateway / Identity-Aware Proxy (IAP)**: 登録済みリソースへのエージェント通信は IAP のイーグレスポリシー (`roles/iap.egressor`) で制御
- **Cloud Storage**: スキル ZIP アーカイブを Cloud Storage バケットからインポートする場合は標準の Cloud Storage 料金が適用

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261106-agent-registry-standalone-skills-ga.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#November_06_2026)
- [Skills architecture](https://docs.cloud.google.com/agent-registry/skills-architecture)
- [Register skills](https://docs.cloud.google.com/agent-registry/register-skills)
- [Manage skills](https://docs.cloud.google.com/agent-registry/manage-skills)
- [Scan skills for security issues](https://docs.cloud.google.com/agent-registry/scan-skills)
- [Configure CMEK for skills](https://docs.cloud.google.com/agent-registry/register-skills#configure-cmek)
- [Agent Registry roles and permissions](https://docs.cloud.google.com/agent-registry/roles-permissions)
- [料金ページ](https://docs.cloud.google.com/agent-registry/pricing)
- [Agent Skills Specification](https://agentskills.io/specification)

## まとめ

Agent Registry のスタンドアロンスキルが GA となり、AI エージェントの再利用可能なタスクロジックを本番環境でバージョン管理・検索・統制できる基盤が整いました。LLM ベースの自動セキュリティスキャン、組織ポリシーによる強制、最小権限 IAM、CMEK (Preview) の組み合わせにより、エージェントスキルのサプライチェーンセキュリティをエンタープライズレベルで確保できます。エージェント基盤を運用している組織は、スキャンポリシーのデフォルト (`ENABLED_BLOCKING`) がリリースフローに与える影響の確認と、2027 年 1 月から始まるスキャン課金のコスト見積もりを進めることを推奨します。

---

**タグ**: Agent Registry, AI エージェント, スキル, GA, セキュリティスキャン, ガバナンス, CMEK, 組織ポリシー, IAM, Cloud KMS
