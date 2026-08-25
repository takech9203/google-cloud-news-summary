# Cloud SDK (gcloud CLI): 582.0.0 リリース - Cloud SQL Proxy V1 削除などの破壊的変更

**リリース日**: 2026-08-25

**サービス**: Cloud SDK (gcloud CLI)

**機能**: バージョン 582.0.0 - 破壊的変更 (Cloud SQL Proxy V1 コンポーネント削除、MCP 関連コマンド削除) と新機能追加

**ステータス**: GA (破壊的変更を含む)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260825-cloud-sdk-582-breaking-changes.html)

## 概要

Google Cloud CLI (gcloud CLI) のバージョン 582.0.0 がリリースされた。本リリースの最大のポイントは、**レガシーの Cloud SQL Proxy V1 コンポーネント (`cloud_sql_proxy`) が gcloud CLI から完全に削除された**ことである。今後、gcloud CLI のすべての connect 系コマンドは Cloud SQL Auth Proxy V2 (`cloud-sql-proxy`) のみに依存する。V2 コンポーネントは 2024 年 4 月の 472.0.0 リリースで gcloud コンポーネントとして提供が開始されており、約 2 年半の移行期間を経て V1 が削除された形となる。

破壊的変更としてはこのほか、API Registry の `gcloud api-registry mcp servers list` / `gcloud api-registry mcp tools list` コマンドの削除 (同様の機能は Agent Registry を参照)、および Cloud Services の `gcloud beta services mcp policies get/get-effective/test-enabled` コマンドの削除 (MCP ポリシーは不要であり no-op であったため) が含まれる。

新機能面では、Cloud Run の `gcloud run instances` の beta 昇格、Compute Engine のバックエンドサービス向けセキュリティ設定フラグ群の追加、Cloud Managed Kafka の `broker-disk` フラグの GA、Developer Connect の account-connectors コマンドの GA、新しい `gcloud beta orchestration-pipelines` コマンドグループの追加など、幅広いサービスで機能強化が行われている。CI/CD パイプラインや運用スクリプトで `cloud_sql_proxy` (V1) を利用している場合は、即座に対応が必要となる重要なリリースである。

**アップデート前の課題**

- Cloud SQL Proxy V1 (`cloud_sql_proxy`) と V2 (`cloud-sql-proxy`) の 2 つのコンポーネントが並存しており、どちらを使うべきか分かりにくかった
- V1 は既に非推奨であったにもかかわらず、gcloud コンポーネントとして残っていたため、レガシーな V1 に依存したスクリプトや CI/CD パイプラインが温存されやすかった
- API Registry / Cloud Services に、実質的に機能しない (no-op の) MCP 関連コマンドが残っていた

**アップデート後の改善**

- Cloud SQL への接続手段が Cloud SQL Auth Proxy V2 (`cloud-sql-proxy`) に一本化され、`gcloud sql connect` などの connect 系コマンドは V2 のみを利用するようになった
- V2 では `--auto-iam-authn` フラグによる IAM データベース認証など、V1 より改善された機能・フラグ体系を利用できる
- 機能しない MCP 関連コマンドが整理され、CLI のコマンド体系がクリーンになった (エージェント関連機能は Agent Registry に集約)

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Before["Before: gcloud CLI 581.x 以前"]
        U1([👤 ユーザー / CI パイプライン]) --> G1["💻 gcloud CLI"]
        G1 --> P1["⚠️ cloud_sql_proxy (V1)<br/>レガシー・非推奨"]
        G1 --> P2v["✅ cloud-sql-proxy (V2)"]
    end

    subgraph After["After: gcloud CLI 582.0.0"]
        U2([👤 ユーザー / CI パイプライン]) --> G2["💻 gcloud CLI"]
        G2 --> P2["✅ cloud-sql-proxy (V2)<br/>Cloud SQL Auth Proxy V2 に一本化"]
        P2 --> SQL[("🗄️ Cloud SQL<br/>MySQL / PostgreSQL / SQL Server")]
    end

    Before -.->|"582.0.0 で V1 削除"| After
```

gcloud CLI 582.0.0 では Cloud SQL Proxy V1 コンポーネントが削除され、connect 系コマンドを含む Cloud SQL への接続経路が Cloud SQL Auth Proxy V2 に完全に一本化された。

## サービスアップデートの詳細

### 破壊的変更 (Breaking Changes)

1. **Cloud SQL Proxy V1 コンポーネント (`cloud_sql_proxy`) の削除**
   - レガシーの Cloud SQL Proxy V1 コンポーネントが gcloud CLI から削除された
   - すべての connect 系コマンド (`gcloud sql connect` など) は Cloud SQL Auth Proxy V2 (`cloud-sql-proxy`) のみに依存するようになった
   - V2 コンポーネントは 472.0.0 (2024-04-16) から `gcloud components install cloud-sql-proxy` で提供されており、V1 からの移行が推奨されてきた
   - V1 固有の `--enable_iam_login` フラグは、V2 では `--auto-iam-authn` フラグに置き換えられている

2. **API Registry: MCP 関連 list コマンドの削除**
   - `gcloud api-registry mcp servers list` および `gcloud api-registry mcp tools list` が削除された
   - 同様の機能が必要な場合は Agent Registry を参照

3. **Cloud Services: MCP ポリシーコマンドの削除**
   - `gcloud beta services mcp policies get` / `get-effective` / `test-enabled` が削除された
   - MCP ポリシーは不要であり、これらのコマンドは実質的に何も行わない (no-op) ものであったため

### 主な新機能・変更点

1. **Cloud Run**
   - `gcloud run instances` が beta に昇格
   - beta の `gcloud run jobs` に `--delay-execution` フラグを追加
   - beta の `gcloud run deploy` に `--run-upload` フラグを追加

2. **Compute Engine**
   - `composite-health-checks test-iam-permissions` コマンドを追加
   - バックエンドサービスに `--security-settings-client-tls-policy` / `--security-settings-subject-alt-names` / AWS V4 署名関連 (`--security-settings-aws-v4-*`) フラグを追加
   - Cloud Armor セキュリティポリシーの `--enforce-on-key` に `asn` 値を追加
   - `service-attachments test-iam-permissions` コマンドを追加 (beta)
   - `--consistent-hash-http-header-name` フラグを追加
   - `--confidential-compute-type` で BMSAI をサポート
   - Backend Services の identity サポートが GA に昇格

3. **その他のサービス**
   - **Cloud Managed Kafka**: `broker-disk` 関連フラグが GA
   - **Developer Connect**: account-connectors コマンドが GA
   - **Orchestration Pipelines**: 新しい `gcloud beta orchestration-pipelines` コマンドグループを追加
   - **VMware Engine**: `gcloud vmware private-clouds migrate-management-vms` を追加
   - **Cloud Workstations**: `--pool-size` のデフォルト値が 1 に変更
   - **Firestore**: 複合インデックス検索のショートハンドを追加
   - **Cloud KMS**: 鍵バージョン更新フラグを追加
   - **Cloud Spanner**: エミュレータに `--remote_functions_host_port` を追加
   - **Cloud Composer**: Airflow 3.3.x 系 CLI コマンドに対応
   - **App Engine**: Java SDK 5.1.0、Jetty のアップグレード、Images サービスの gRPC サポート

## 技術仕様

### Cloud SQL Proxy V1 と V2 の比較

| 項目 | V1 (`cloud_sql_proxy`) | V2 (`cloud-sql-proxy`) |
|------|------------------------|------------------------|
| gcloud コンポーネントとしての提供 | **582.0.0 で削除** | 472.0.0 (2024-04-16) から提供 |
| バイナリ名 | `cloud_sql_proxy` (アンダースコア) | `cloud-sql-proxy` (ハイフン) |
| IAM データベース認証フラグ | `--enable_iam_login` | `--auto-iam-authn` |
| インストール方法 | (削除済み) | `gcloud components install cloud-sql-proxy` |
| 移行ガイド | - | [Migrating from v1 to v2](https://github.com/GoogleCloudPlatform/cloud-sql-proxy/blob/main/migration-guide.md) |

## 設定方法

### 前提条件

1. gcloud CLI がインストールされていること
2. Cloud SQL インスタンスへの接続権限 (`cloudsql.instances.connect` を含むロール、例: Cloud SQL Client) があること

### 手順

#### ステップ 1: gcloud CLI を 582.0.0 に更新

```bash
gcloud components update
gcloud version
```

gcloud CLI を最新バージョン (582.0.0 以降) に更新する。

#### ステップ 2: Cloud SQL Auth Proxy V2 コンポーネントのインストール

```bash
gcloud components install cloud-sql-proxy
```

V1 (`cloud_sql_proxy`) は削除されているため、V2 コンポーネントをインストールする。

#### ステップ 3: V1 を利用しているスクリプトの移行

```bash
# Before (V1 - 動作しなくなる)
# ./cloud_sql_proxy -instances=PROJECT:REGION:INSTANCE=tcp:5432 -enable_iam_login

# After (V2)
./cloud-sql-proxy --auto-iam-authn --port 5432 PROJECT:REGION:INSTANCE
```

CI/CD パイプラインや運用スクリプト内の `cloud_sql_proxy` の呼び出しを V2 の `cloud-sql-proxy` に置き換える。V1 と V2 ではフラグ体系が異なるため、[移行ガイド](https://github.com/GoogleCloudPlatform/cloud-sql-proxy/blob/main/migration-guide.md)を参照して書き換える。

## メリット

### ビジネス面

- **保守負荷の軽減**: 接続コンポーネントが V2 に一本化されることで、社内標準やドキュメントを 1 つに統一でき、混乱や二重管理が解消される
- **セキュリティ体制の向上**: 非推奨のレガシーコンポーネントを利用し続けるリスク (更新停止、脆弱性対応の遅れ) が構造的に排除される

### 技術面

- **改善されたプロキシ機能**: V2 は `--auto-iam-authn` による IAM データベース認証の簡素化など、V1 よりモダンなフラグ体系と機能を提供する
- **CLI コマンド体系の整理**: no-op であった MCP ポリシーコマンド群が削除され、コマンド体系がクリーンになった

## デメリット・制約事項

### 制限事項

- V1 (`cloud_sql_proxy`) を直接呼び出しているスクリプトは、gcloud CLI を 582.0.0 に更新すると動作しなくなる
- V1 と V2 ではバイナリ名 (アンダースコア → ハイフン) およびフラグ体系が異なるため、単純なバイナリ名の置換だけでは移行できないケースがある

### 考慮すべき点

- CI/CD 環境 (Cloud Build、GitHub Actions など) で gcloud CLI のバージョンが自動更新される場合、V1 依存のパイプラインが予告なく失敗する可能性があるため、早急な確認が必要
- `gcloud api-registry mcp` 系コマンドを利用していた場合は、Agent Registry への移行を検討する
- Cloud Workstations の `--pool-size` デフォルト値が 1 に変更されたため、暗黙のデフォルトに依存していた構成ではウォームプールの挙動 (起動時間・コスト) が変わる可能性がある

## ユースケース

### ユースケース 1: CI/CD パイプラインでの Cloud SQL マイグレーション実行

**シナリオ**: Cloud Build や GitHub Actions で `cloud_sql_proxy` (V1) を起動し、データベースマイグレーションを実行しているチームが、gcloud CLI の更新後にパイプラインが失敗するのを防ぎたい。

**実装例**:
```bash
# V2 コンポーネントをインストールしてバックグラウンド起動
gcloud components install cloud-sql-proxy --quiet
cloud-sql-proxy --port 5432 my-project:asia-northeast1:my-instance &
sleep 5

# マイグレーション実行
migrate -path ./migrations -database "postgres://user:pass@127.0.0.1:5432/mydb?sslmode=disable" up
```

**効果**: V1 削除の影響を受けず、V2 の改善された接続機能でパイプラインを安定稼働できる。

### ユースケース 2: IAM データベース認証への移行

**シナリオ**: V1 の `--enable_iam_login` で IAM データベース認証を利用していた環境を V2 に移行する。

**効果**: V2 の `--auto-iam-authn` フラグにより、パスワードレスの IAM 認証を引き続き利用でき、アクセストークンの管理もプロキシが自動的に行う。

## 料金

gcloud CLI および Cloud SQL Auth Proxy 自体は無料で利用できる。Cloud SQL Auth Proxy は Cloud SQL Admin API を呼び出すため、プロジェクトの API クォータを消費する (起動時が最大で、稼働中は接続インスタンスあたり毎時 2 回の API 呼び出し)。Cloud SQL インスタンス自体の料金は通常どおり発生する。

- [Cloud SQL 料金ページ](https://cloud.google.com/sql/pricing)

## 利用可能リージョン

gcloud CLI はクライアントツールのため、リージョンの制約はない。すべての環境で 582.0.0 が利用可能。

## 関連サービス・機能

- **Cloud SQL**: Cloud SQL Auth Proxy V2 が接続対象とするマネージドデータベースサービス (MySQL / PostgreSQL / SQL Server)
- **Cloud SQL Language Connectors**: プロキシを別プロセスとして起動せず、アプリケーションコードに組み込む接続ライブラリ (Java / Python / Go / Node.js)。プロキシの代替手段
- **Agent Registry**: 削除された `gcloud api-registry mcp` 系コマンドの代替として案内されている、エージェント関連機能のレジストリ
- **Cloud Run / GKE**: Cloud SQL Auth Proxy をサイドカーとして利用する代表的なワークロード実行環境

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260825-cloud-sdk-582-breaking-changes.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#August_25_2026)
- [Cloud SDK リリースノート](https://docs.cloud.google.com/sdk/docs/release-notes)
- [Cloud SQL Auth Proxy ドキュメント](https://docs.cloud.google.com/sql/docs/mysql/connect-auth-proxy)
- [Cloud SQL Proxy V1 から V2 への移行ガイド (GitHub)](https://github.com/GoogleCloudPlatform/cloud-sql-proxy/blob/main/migration-guide.md)
- [Cloud SQL 料金ページ](https://cloud.google.com/sql/pricing)

## まとめ

gcloud CLI 582.0.0 は、約 2 年半の移行期間を経て Cloud SQL Proxy V1 コンポーネントを削除する破壊的変更を含む重要なリリースである。`cloud_sql_proxy` を利用しているスクリプトや CI/CD パイプラインは、gcloud CLI の更新前に必ず Cloud SQL Auth Proxy V2 (`cloud-sql-proxy`) への移行を完了させることを強く推奨する。あわせて、Cloud Run instances の beta 昇格や Compute Engine のセキュリティ設定フラグ拡充など、新機能の活用も検討したい。

---

**タグ**: Cloud SDK, gcloud CLI, Cloud SQL, Cloud SQL Auth Proxy, Breaking Change, Cloud Run, Compute Engine, Managed Kafka, Developer Connect
