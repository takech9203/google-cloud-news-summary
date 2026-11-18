# Cloud SDK: gcloud CLI 594.0.0 - フラグ優先順位の Breaking Changes と主要コマンドの GA 昇格

**リリース日**: 2026-11-17

**サービス**: Cloud SDK (gcloud CLI)

**機能**: バージョン 594.0.0 - `--account` / `--project` フラグと位置引数の優先順位変更 (Breaking Changes) および主要コマンドの GA/Beta 昇格

**ステータス**: Breaking Changes + GA/Beta 昇格

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261117-cloud-sdk-594-breaking-changes.html)

## 概要

2026 年 11 月 17 日、Google Cloud CLI (gcloud) バージョン 594.0.0 がリリースされた。本リリースには、`gcloud auth`、`gcloud billing accounts`、`gcloud compute shared-vpc` の各コマンド群における **フラグと位置引数の優先順位に関する 3 件の Breaking Changes** が含まれており、これらのコマンドを利用するスクリプトや CI/CD パイプラインに影響する可能性がある。

従来、これらのコマンドでは位置引数 (例: `ACCOUNT_NAME`、`ACCOUNT_ID`、`PROJECT_ID`) の後に `--account` や `--project` フラグを指定すると、フラグの値が位置引数を上書きするという一貫性のない動作が存在した。594.0.0 ではこの問題が修正され、**位置引数が常に優先される** ようになった。また、`gcloud billing accounts` の IAM 系コマンドと `gcloud compute shared-vpc` では、位置引数が **必須化** され、フラグによる位置引数の代替指定ができなくなった。

あわせて、Cloud SQL のブルーグリーンデプロイメント、Cloud Run のリージョナルエンドポイント、Cloud Tasks のバッチ操作などの GA 昇格、GKE のクラスタスケールツーゼロ用フラグ追加など、多数の機能昇格・追加も含まれている。gcloud CLI を自動化基盤 (CI/CD、構成管理スクリプト) で利用しているすべてのユーザーは、アップグレード前に影響範囲を確認することを推奨する。

**アップデート前の課題**

このアップデート以前には、以下の問題が存在していた。

- `gcloud auth print-access-token ACCOUNT_NAME --account=OTHER` のように、位置引数の後に `--account` フラグを指定すると、フラグ値が位置引数を上書きしてしまい、意図しないアカウントの認証情報が使用される可能性があった
- `gcloud billing accounts get-iam-policy` などの IAM 系コマンドで、`ACCOUNT_ID` 位置引数を省略して `--account` フラグで代替できてしまい、認証用アカウント指定 (`--account` 本来の用途) と操作対象の課金アカウント指定が混同されるリスクがあった
- `gcloud compute shared-vpc` コマンドで `--project` フラグが `PROJECT_ID` 位置引数を上書きし、意図しないプロジェクトに対して共有 VPC 操作が実行される可能性があった
- フラグと位置引数の指定順によって動作が変わるため、スクリプトの挙動が予測しにくかった

**アップデート後の改善**

- 位置引数 (`ACCOUNT_NAME` / `ACCOUNT_ID` / `PROJECT_ID`) が **常にフラグより優先** されるようになり、指定順に依存しない一貫した動作になった
- `gcloud billing accounts` の IAM 系コマンドと `gcloud compute shared-vpc` では位置引数が必須化され、操作対象リソースの指定が明示的になった
- `--account` フラグは本来の用途 (認証に使用するアカウントの指定、および `gcloud auth` 系コマンドで位置引数が省略された場合の代替) に整理された
- 意図しないアカウント・プロジェクトに対する操作という潜在的な事故リスクが低減された

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Before["🔴 Before (593.x 以前)"]
        B1([👤 gcloud auth print-access-token<br>user-a@example.com --account=user-b@example.com])
        B2{引数の解決}
        B3[⚠️ 後に指定した --account が<br>位置引数を上書き]
        B4[user-b@example.com の<br>トークンを発行]
        B1 --> B2 --> B3 --> B4
    end

    subgraph After["🟢 After (594.0.0 以降)"]
        A1([👤 gcloud auth print-access-token<br>user-a@example.com --account=user-b@example.com])
        A2{引数の解決}
        A3[✅ 位置引数が常に優先<br>指定順に依存しない]
        A4[user-a@example.com の<br>トークンを発行]
        A1 --> A2 --> A3 --> A4
    end

    Before -.アップグレード.-> After
```

594.0.0 以降は、位置引数とフラグを同時に指定した場合、指定順にかかわらず位置引数が常に優先される。スクリプト内で両方を指定していた場合、使用されるアカウント / プロジェクトが変わる可能性がある。

## サービスアップデートの詳細

### Breaking Changes (3 件)

1. **gcloud auth 系コマンド: `--account` と `ACCOUNT_NAME` 位置引数の優先順位修正**
   - 対象コマンド: `gcloud auth print-access-token`、`print-identity-token`、`login`、`application-default login`、`activate-service-account`
   - 従来は位置引数の後に `--account` を指定するとフラグが位置引数 (旧名: `ACCOUNT`、現名: `ACCOUNT_NAME`) を上書きしていたが、修正後は位置引数が常に優先される
   - `ACCOUNT_NAME` が省略された場合は、引き続き `--account` が適用される

2. **gcloud billing accounts IAM 系コマンド: `ACCOUNT_ID` 位置引数の必須化**
   - 対象コマンド: `gcloud billing accounts get-iam-policy`、`set-iam-policy`、`add-iam-policy-binding`、`remove-iam-policy-binding`
   - 位置引数 (旧名: `ACCOUNT`、現名: `ACCOUNT_ID`) が常に優先されるようになった
   - **`ACCOUNT_ID` は常に必須** となり、`--account` フラグで省略した `ACCOUNT_ID` を代替することはできなくなった

3. **gcloud compute shared-vpc: `PROJECT_ID` 位置引数の必須化**
   - 対象コマンド: `gcloud compute shared-vpc` 配下のコマンド
   - 従来は位置引数の後に `--project` を指定するとフラグが `PROJECT_ID` を上書きしていたが、修正後は位置引数が常に優先される
   - **`PROJECT_ID` は常に必須** となり、`--project` フラグで省略した `PROJECT_ID` を代替することはできなくなった

### 主な GA 昇格・機能追加 (サマリ)

| サービス | 内容 | ステータス |
|---------|------|-----------|
| Cloud SQL | `gcloud sql blue-green-deployments` コマンド群 | GA |
| Cloud SQL | `--msdtc-enabled` / `--msdtc-rpc-auth-mode` フラグ (`instances create` / `patch`) | GA |
| Cloud Run | リージョナルエンドポイント対応 (`run deploy` / `services` / `revisions` / `jobs` / `worker-pools`) | GA |
| Cloud Run | ワーカープールのスケーリングフラグ (`--scaling`、`--scaling-cpu-target`、`--min`、`--max` など) | Beta |
| Cloud Tasks | `gcloud tasks batch-create` (JSON/YAML からのタスク一括作成) | GA |
| Cloud Tasks | `gcloud tasks delete` の `--tasks-from-file` / `--failed-tasks-file` (一括削除) | GA |
| Cloud Tasks | タスクレベルのリトライフラグ (`--max-attempts`、`--max-retry-duration` など) | GA |
| GKE | `--enable-cluster-scale-to-zero` / `--cluster-scale-to-zero-delay` フラグ追加 | 新規追加 |
| Compute Engine | Global External Passthrough NLB (`EXTERNAL_PASSTHROUGH`) 対応 (`forwarding-rules` / `backend-services`) | GA |
| Compute Engine | `imageOptimizationPolicy` 対応 (`url-maps import` / `export` / `validate`) | GA |
| BigLake | `gcloud biglake iceberg views` コマンド群 | Beta |
| Cloud Composer | `--rollback-image-version` フラグ追加 (`environments update`) | 新規追加 |
| Config Connector | バージョン 1.161.0 に更新 | 更新 |

## 技術仕様

### Breaking Changes の影響マトリクス

| コマンド | 変更内容 | 影響を受けるパターン |
|---------|---------|---------------------|
| `gcloud auth print-access-token` ほか auth 系 4 コマンド | 位置引数優先に変更 | 位置引数と `--account` を同時指定しているスクリプト |
| `gcloud billing accounts get-iam-policy` ほか IAM 系 3 コマンド | 位置引数優先 + `ACCOUNT_ID` 必須化 | `--account` のみで課金アカウントを指定していたスクリプト (**エラーになる**) |
| `gcloud compute shared-vpc` 配下 | 位置引数優先 + `PROJECT_ID` 必須化 | `--project` のみでプロジェクトを指定していたスクリプト (**エラーになる**) |

### 影響確認のポイント

```bash
# 影響を受ける可能性のあるパターンの例

# パターン 1: 位置引数とフラグの同時指定 (使用されるアカウントが変わる)
gcloud auth print-access-token user-a@example.com --account=user-b@example.com
# 593.x 以前: user-b のトークン → 594.0.0 以降: user-a のトークン

# パターン 2: 位置引数の省略 (594.0.0 以降はエラー)
gcloud billing accounts get-iam-policy --account=0X0X0X-0X0X0X-0X0X0X
# 594.0.0 以降: ACCOUNT_ID 位置引数が必須のためエラー

# パターン 3: 位置引数の省略 (594.0.0 以降はエラー)
gcloud compute shared-vpc enable --project=my-host-project
# 594.0.0 以降: PROJECT_ID 位置引数が必須のためエラー
```

## 設定方法

### 前提条件

1. gcloud CLI がインストールされていること
2. CI/CD パイプラインやスクリプトで使用している gcloud CLI のバージョンを把握していること

### 手順

#### ステップ 1: 現在のバージョンを確認

```bash
gcloud version
```

CI/CD 環境 (GitHub Actions、Cloud Build など) で使用されているイメージ内の gcloud バージョンも確認する。

#### ステップ 2: 影響を受けるコマンドパターンをスクリプトから検索

```bash
# リポジトリ内のスクリプトから影響を受ける可能性のあるコマンドを検索
grep -rnE "gcloud (auth (print-access-token|print-identity-token|login|application-default login|activate-service-account)|billing accounts (get-iam-policy|set-iam-policy|add-iam-policy-binding|remove-iam-policy-binding)|compute shared-vpc)" .
```

ヒットした箇所について、位置引数とフラグの併用、または位置引数の省略がないかを確認する。

#### ステップ 3: スクリプトの修正

```bash
# 修正例: billing accounts IAM コマンドは ACCOUNT_ID を位置引数で明示
# 修正前 (594.0.0 以降はエラー)
gcloud billing accounts get-iam-policy --account=0X0X0X-0X0X0X-0X0X0X

# 修正後
gcloud billing accounts get-iam-policy 0X0X0X-0X0X0X-0X0X0X

# 修正例: shared-vpc は PROJECT_ID を位置引数で明示
# 修正前 (594.0.0 以降はエラー)
gcloud compute shared-vpc enable --project=my-host-project

# 修正後
gcloud compute shared-vpc enable my-host-project
```

#### ステップ 4: gcloud CLI の更新

```bash
gcloud components update
```

修正の確認後、gcloud CLI を 594.0.0 以降に更新する。

## メリット

### ビジネス面

- **運用事故リスクの低減**: 意図しないアカウントや課金アカウント、プロジェクトに対する IAM 操作・VPC 操作という潜在的なセキュリティ / ガバナンスリスクが解消される
- **監査性の向上**: 操作対象リソースが位置引数で明示的に指定されるため、スクリプトのレビューや監査で対象を特定しやすくなる

### 技術面

- **一貫性のある引数解決**: フラグと位置引数の指定順に依存しない予測可能な動作となり、スクリプトの信頼性が向上する
- **フラグの役割の明確化**: `--account` は認証アカウントの指定、位置引数は操作対象の指定という役割分担が明確になる
- **自動化機能の拡充**: Cloud Tasks のバッチ操作 GA、Cloud Run リージョナルエンドポイント GA など、CI/CD・自動化で利用できる GA 機能が増加した

## デメリット・制約事項

### 制限事項

- `gcloud billing accounts` の IAM 系コマンドでは `ACCOUNT_ID` 位置引数が必須となり、`--account` フラグのみの指定ではエラーになる
- `gcloud compute shared-vpc` では `PROJECT_ID` 位置引数が必須となり、`--project` フラグのみの指定ではエラーになる

### 考慮すべき点

- **サイレントな動作変更に注意**: auth 系コマンドでは位置引数とフラグを併用していた場合、エラーにならずに **使用されるアカウントが変わる** ため、エラー検知では発見できない。スクリプトの棚卸しが必要
- CI/CD 環境のベースイメージ (Cloud Build のビルダーイメージ、GitHub Actions の setup-gcloud など) は自動的に新バージョンへ更新されることが多いため、更新タイミングを把握しておく
- `gcloud alpha/beta tasks delete` の `--from-file` フラグは非推奨となったため、`--tasks-from-file` への移行も合わせて行う

## ユースケース

### ユースケース 1: CI/CD パイプラインの影響調査と修正

**シナリオ**: 複数のサービスアカウントを切り替えながら gcloud コマンドを実行する CI/CD パイプラインで、`gcloud auth print-access-token` に位置引数と `--account` フラグの両方を指定していた。

**実装例**:
```bash
# 修正前: 位置引数とフラグが混在し、593.x 以前はフラグが優先されていた
TOKEN=$(gcloud auth print-access-token "$DEFAULT_ACCOUNT" --account="$DEPLOY_ACCOUNT")

# 修正後: 使用したいアカウントを位置引数で一意に指定
TOKEN=$(gcloud auth print-access-token "$DEPLOY_ACCOUNT")
```

**効果**: バージョンアップ後も意図したアカウントのトークンが確実に取得され、デプロイ先の取り違えを防止できる。

### ユースケース 2: Cloud Tasks バッチ操作 GA を活用したタスク運用の効率化

**シナリオ**: 大量のタスクを個別の `gcloud tasks create-http-task` 呼び出しで作成しており、実行時間と API 呼び出し数が課題だった。

**実装例**:
```bash
# JSON/YAML ファイルから複数タスクを一括作成 (GA)
gcloud tasks batch-create --queue=my-queue --location=us-central1 --tasks-file=tasks.yaml

# タスクレベルのリトライ設定 (GA) でキュー設定を個別に上書き
gcloud tasks create-http-task my-task \
  --queue=my-queue --url=https://example.com/handler \
  --max-attempts=3 --max-retry-duration=600s
```

**効果**: タスクの一括作成・一括削除により運用スクリプトが簡素化され、タスク単位のリトライ制御も GA 機能として本番利用できる。

## 料金

gcloud CLI (Cloud SDK) 自体は無料で利用できる。コマンドから操作する各サービス (Cloud SQL、Cloud Run、Cloud Tasks など) にはそれぞれのサービスの料金が適用される。

## 関連サービス・機能

- **Cloud Billing**: `gcloud billing accounts` IAM 系コマンドの Breaking Change の対象。課金アカウントの IAM 管理スクリプトに影響
- **共有 VPC (Shared VPC)**: `gcloud compute shared-vpc` の Breaking Change の対象。ホストプロジェクト管理の自動化スクリプトに影響
- **Cloud Build / GitHub Actions**: gcloud CLI を内包する CI/CD 環境。ベースイメージ更新時に 594.0.0 の変更が自動的に取り込まれるため影響確認が必要
- **Config Connector**: 本リリースで 1.161.0 に更新。Kubernetes マニフェストによる Google Cloud リソース管理に利用

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261117-cloud-sdk-594-breaking-changes.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#November_17_2026)
- [gcloud CLI リリースノート購読 (google-cloud-sdk-announce)](https://groups.google.com/forum/#!forum/google-cloud-sdk-announce)
- [gcloud auth login リファレンス](https://docs.cloud.google.com/sdk/gcloud/reference/auth/login)
- [gcloud auth application-default login リファレンス](https://docs.cloud.google.com/sdk/gcloud/reference/auth/application-default/login)

## まとめ

gcloud CLI 594.0.0 は、`--account` / `--project` フラグと位置引数の優先順位を修正する 3 件の Breaking Changes を含むリリースであり、auth 系コマンドでは **エラーにならずに使用アカウントが変わる** 可能性がある点が特に注意を要する。CI/CD パイプラインや運用スクリプトで対象コマンドを使用している場合は、アップグレード前に位置引数とフラグの併用・省略パターンを棚卸しし、位置引数で操作対象を明示する形へ修正することを推奨する。あわせて、Cloud SQL ブルーグリーンデプロイメントや Cloud Tasks バッチ操作など GA 昇格した機能の活用も検討したい。

---

**タグ**: Cloud SDK, gcloud CLI, Breaking Changes, CI/CD, Cloud Billing, Shared VPC, Cloud SQL, Cloud Run, Cloud Tasks, GKE
