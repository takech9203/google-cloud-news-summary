# CI/CD セットアップガイド

このドキュメントでは、Google Cloud News Summary を GitHub Actions で自動実行するための設定手順を説明します。

## 前提条件

以下の環境が必要です。

- AWS アカウント (Amazon Bedrock へのアクセス用)
- GitHub リポジトリ
- AWS CLI がインストールされていること

## セットアップ手順

### 1. AWS IAM ロールの作成

Amazon Bedrock にアクセスするための IAM ロールを作成します。

**必要な権限:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/global.anthropic.claude-*",
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-*",
        "arn:aws:bedrock:::foundation-model/anthropic.claude-*"
      ]
    }
  ]
}
```

### 2. OIDC プロバイダーの設定

GitHub Actions 用の OIDC プロバイダーを設定します。

1. AWS IAM コンソールで OIDC プロバイダーを作成
   - プロバイダー URL: `https://token.actions.githubusercontent.com`
   - オーディエンス: `sts.amazonaws.com`

2. IAM ロールの信頼ポリシーを設定

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_ORG/YOUR_REPO:*"
        }
      }
    }
  ]
}
```

### 3. GitHub Actions 変数の設定

リポジトリの Settings > Secrets and variables > Actions > Variables で以下を設定します。

- `AWS_ROLE_ARN`: IAM ロールの ARN
- `AWS_REGION`: AWS リージョン (例: `us-east-1`)
- `INFOGRAPHIC_BASE_URL`: インフォグラフィックの公開 URL (例: `https://your-user.github.io/your-repo`)

リポジトリの Settings > Secrets and variables > Actions > Secrets で以下を設定します。

- `GCP_DEVELOPER_KNOWLEDGE_API_KEY`: Google Developer Knowledge API キー

<details>
<summary>API キーの取得手順</summary>

API キーの作成は Google Cloud コンソールまたは gcloud CLI で行えます。

**Step 1: Developer Knowledge API の有効化**

[Developer Knowledge API](https://console.cloud.google.com/apis/library/developerknowledge.googleapis.com) を開き、「有効にする」をクリックします。

または gcloud CLI で有効化します。

```bash
gcloud services enable developerknowledge.googleapis.com --project=YOUR_PROJECT_ID
```

**Step 2: API キーの作成**

Google Cloud コンソールの場合:

1. プロジェクトレベルの [認証情報ページ](https://console.cloud.google.com/apis/credentials) を開く (API の詳細ページ内の「認証情報」タブではなく、左メニューの「認証情報」から開く)
2. 「認証情報を作成」→「API キー」を選択
3. API キーが作成されるので、文字列を控える

> API の詳細ページ内の「認証情報」タブからは API キーを作成できません。必ずプロジェクトレベルの認証情報ページから作成してください。

gcloud CLI の場合:

```bash
gcloud services api-keys create --project=YOUR_PROJECT_ID --display-name="DK API Key"
```

**Step 3: API キーの制限 (推奨)**

セキュリティのため、作成した API キーを Developer Knowledge API のみに制限します。

1. 認証情報ページで作成した API キーの「API キーを編集」をクリック
2. 「API の制限」で「キーを制限」を選択
3. 「Select APIs」リストから「Developer Knowledge API」を選択して「OK」
4. 「保存」をクリック

> API を有効化した直後は「Select APIs」リストに Developer Knowledge API が表示されるまで数分かかる場合があります。

**Step 4: MCP server の有効化**

gcloud CLI の beta コンポーネントが必要です。

```bash
# beta コンポーネントの更新
gcloud components update

# MCP server の有効化
gcloud beta services mcp enable developerknowledge.googleapis.com --project=YOUR_PROJECT_ID
```

> `gcloud beta services mcp` コマンドが見つからない場合は、`gcloud components update` で gcloud CLI を最新版に更新してください。

参考: [Developer Knowledge MCP server ドキュメント](https://developers.google.com/knowledge/mcp)

</details>

### 4. パイプラインの有効化

`.github/workflows/google-cloud-news-summary.yml` がすでに有効になっています。

### 5. 動作確認

以下の手順で動作を確認します。

1. 手動でワークフローを実行
2. ログを確認して正常に動作することを確認
3. `reports/` と `infographic/` ディレクトリにファイルが生成されることを確認

## トラブルシューティング

### AWS 認証エラー

以下を確認してください。

- IAM ロールの ARN が正しいか
- 信頼ポリシーのリポジトリパスが正しいか
- OIDC プロバイダーが正しく設定されているか

### Bedrock アクセスエラー

以下を確認してください。

- IAM ロールに Bedrock の権限があるか
- リージョンで Bedrock が利用可能か

### Git push エラー

以下を確認してください。

- GitHub Actions のトークンに write 権限があるか
- ブランチ保護ルールの設定

## 参考資料

- [GitHub Actions: AWS での OpenID Connect の設定](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [Amazon Bedrock ドキュメント](https://docs.aws.amazon.com/bedrock/)
