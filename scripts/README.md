# IAM Setup Scripts

このディレクトリには、Google Cloud News Summary CI/CD 用の AWS IAM リソースをデプロイするスクリプトとテンプレートが含まれています。

## ファイル構成

- `deploy-iam.sh`: IAM ロールと OIDC プロバイダーをデプロイするメインスクリプト
- `cfn-github-oidc-iam.yaml`: GitHub Actions 用の CloudFormation テンプレート

## 前提条件

- AWS CLI がインストールされ、適切な権限で設定されていること
- 以下の権限が必要:
  - CloudFormation スタックの作成・更新
  - IAM ロール・ポリシーの作成
  - IAM OIDC プロバイダーの作成

## 使用方法

### 基本的な使用方法

```bash
./scripts/deploy-iam.sh -o <GitHub組織名> -r google-cloud-news-summary
```

### 使用例

```bash
# 基本的な使用方法（既存の OIDC プロバイダーを自動検出）
./scripts/deploy-iam.sh -o myorg -r google-cloud-news-summary

# カスタムロール名とリージョンを指定
./scripts/deploy-iam.sh -o myorg -r google-cloud-news-summary \
  -n MyCustomRole -R us-west-2

# 明示的に OIDC プロバイダー ARN を指定（自動検出をオーバーライド）
./scripts/deploy-iam.sh -o myorg -r google-cloud-news-summary \
  -p arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com
```

**自動検出機能**: スクリプトは自動的に既存の GitHub Actions OIDC プロバイダー (`token.actions.githubusercontent.com`) を検出します。既存のプロバイダーが見つかった場合は、それを使用します。見つからない場合は、新しいプロバイダーを作成します。

**デプロイされるリソース**:

- IAM OIDC プロバイダー: `https://token.actions.githubusercontent.com`
- IAM ロール: `GitHubActions-GoogleCloudNewsSummary` (デフォルト)
- マネージドポリシー: `GitHubActions-GoogleCloudNewsSummary-BedrockInvoke`
- CloudFormation スタック: `google-cloud-news-summary-github-iam`

## オプション

| オプション | 説明 | デフォルト |
|----------|------|----------|
| `-o, --org` | GitHub 組織名 | (必須) |
| `-r, --repo` | リポジトリ名 | (必須) |
| `-n, --role-name` | IAM ロール名 | `GitHubActions-GoogleCloudNewsSummary` |
| `-s, --stack-name` | CloudFormation スタック名 | `google-cloud-news-summary-github-iam` |
| `-R, --region` | AWS リージョン | `us-east-1` |
| `-p, --oidc-provider-arn` | 既存の OIDC プロバイダー ARN (自動検出をオーバーライド) | 自動検出 |
| `-h, --help` | ヘルプを表示 | - |

## デプロイ後の設定

1. スクリプト実行後に出力される `RoleArn` をコピー
2. GitHub リポジトリの Settings > Secrets and variables > Actions に移動
3. 新しい変数 `AWS_ROLE_ARN` を作成し、コピーした ARN を設定

## IAM 権限

デプロイされる IAM ロールには以下の権限が付与されます。

### Bedrock Invoke

Anthropic Claude モデルを呼び出すための権限:

- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`

**リソース**:

- `arn:aws:bedrock:*:*:inference-profile/global.anthropic.claude-*`
- `arn:aws:bedrock:*::foundation-model/anthropic.claude-*`
- `arn:aws:bedrock:*::foundation-model/us.anthropic.claude-*`

## OIDC プロバイダーの自動検出

スクリプトは実行時に以下の動作を行います。

1. 既存の GitHub Actions OIDC プロバイダー (`token.actions.githubusercontent.com`) を自動検出
2. 既存のプロバイダーが見つかった場合は、それを使用（新規作成をスキップ）
3. 見つからない場合は、新しいプロバイダーを作成

**手動で OIDC プロバイダーを確認する場合**:

```bash
aws iam list-open-id-connect-providers
```

**明示的に ARN を指定する場合** (`-p` オプション):

```bash
./scripts/deploy-iam.sh -o myorg -r google-cloud-news-summary \
  -p arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com
```

自動検出をオーバーライドして、特定の OIDC プロバイダーを使用できます。

## トラブルシューティング

### OIDC プロバイダーが既に存在する

エラーメッセージ: `OIDCProvider already exists`

**対処法 1: 既存のプロバイダーを使用する (推奨)**

上記の「既存の OIDC プロバイダーを使用する場合」を参照して、`-p` オプションで既存のプロバイダー ARN を指定してください。

**対処法 2: 既存のプロバイダーを削除して再作成**

```bash
# 既存の OIDC プロバイダーを確認
aws iam list-open-id-connect-providers

# 削除 (必要な場合)
aws iam delete-open-id-connect-provider --open-id-connect-provider-arn <ARN>
```

**注意**: 既存のプロバイダーを削除すると、そのプロバイダーに依存している他の IAM ロールが機能しなくなる可能性があります。

### スタックが既に存在する

エラーメッセージ: `Stack already exists`

**対処法**: 既存のスタックを更新するか、削除してから再実行してください。

```bash
# スタックの削除
aws cloudformation delete-stack --stack-name google-cloud-news-summary-github-iam

# 削除完了を待機
aws cloudformation wait stack-delete-complete --stack-name google-cloud-news-summary-github-iam
```

### 権限エラー

エラーメッセージ: `User is not authorized to perform: iam:CreateRole`

**対処法**: AWS CLI を実行しているユーザーに適切な IAM 権限が付与されているか確認してください。

## スタックの削除

不要になった場合は、以下のコマンドでスタックを削除できます。

```bash
aws cloudformation delete-stack \
  --stack-name google-cloud-news-summary-github-iam \
  --region us-east-1
```

**注意**: OIDC プロバイダーが他のスタックで使用されている場合、手動で削除する必要があります。

## 参考資料

- [Configuring OpenID Connect in Amazon Web Services](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [AWS CloudFormation: AWS::IAM::OIDCProvider](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html)
