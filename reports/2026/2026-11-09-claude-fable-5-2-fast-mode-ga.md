# Gemini Enterprise Agent Platform: Claude Fable 5.2 GA と Claude モデル向け Fast モード GA

**リリース日**: 2026-11-09

**サービス**: Gemini Enterprise Agent Platform (Model Garden / Anthropic Claude パートナーモデル)

**機能**: Claude Fable 5.2 (claude-fable-5-2) の GA 提供、および対応 Claude モデル向け Fast モード (`"speed": "fast"`) の GA 提供

**ステータス**: GA (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261109-claude-fable-5-2-fast-mode-ga.html)

## 概要

Gemini Enterprise Agent Platform の Model Garden で、Anthropic の最新モデル **Claude Fable 5.2** (`claude-fable-5-2`) が一般提供 (GA) になりました。Claude Fable 5.2 はコーディングや金融を含む技術・科学分野の作業向けに設計されたモデルで、曖昧な問題に長時間取り組み、自身の成果を検証し、サブエージェントをオーケストレーションする能力を備えています。最大入力 100 万トークン・最大出力 12.8 万トークンに対応し、テキスト・画像・PDF を入力として受け付けます。

あわせて、対応する Claude モデル (第一弾は Claude Fable 5.2) 向けの **Fast モード**が GA になりました。オンラインの従量課金 (pay-as-you-go) 予測リクエストのボディに `"speed": "fast"` を指定するだけで、出力トークンの生成を高速化できます。ベースモデルの知能と安全性を維持したまま高速なサービング構成を使用するため、対話型のエージェント的コーディング、ライブプランニング、インシデント対応など、トークン生成の待ち時間が開発者やユーザーの作業フローを妨げるレイテンシ重視のワークロードに適しています。

対象ユーザーは、Google Cloud 上で Claude モデルを使ったエージェントアプリケーションを構築する開発者や、人間参加型 (human-in-the-loop) の対話的ワークフローで応答速度を重視するチームです。

**アップデート前の課題**

- Claude モデルの出力トークン生成速度は標準のサービング構成のみで、レイテンシ重視の対話型エージェントワークロードでも生成速度を選択できなかった
- 対話型のコーディング反復やインシデント対応など、応答待ちがユーザーのフローを中断するユースケースでは、より小型のモデルに切り替えるなどの妥協が必要だった
- 技術・科学分野の最高難度のタスクに対応する Fable 系の最新モデルは Claude Fable 5.1 までだった

**アップデート後の改善**

- リクエストボディに `"speed": "fast"` を追加するだけで、同一モデル・同一エンドポイントのまま出力トークン生成を高速化できるようになった (ベータヘッダーや別モデルカードの有効化は不要)
- Fast モードは標準速度とは独立した専用クォータ (`anthropic-claude-fable-fast`) を使用するため、高速トラフィックと標準トラフィックが互いのレート制限を奪い合わない
- Claude Fable 5.2 が GA となり、Fast モード、Computer use、Web search、バッチ予測、プロンプトキャッシュ、Function calling、Memory tool などをサポートする最新の Fable 系モデルを本番環境で利用できるようになった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Client["🧑‍💻 クライアント / エージェント"]
        APP([エージェントアプリケーション])
    end

    subgraph GEAP["☁️ Gemini Enterprise Agent Platform"]
        EP["🌐 公開エンドポイント<br/>publishers/anthropic/models/claude-fable-5-2"]
        SPEED{"speed パラメータ"}
        FAST["⚡ Fast モード サービング<br/>(専用クォータ: anthropic-claude-fable-fast)<br/>PayGo のみ / 料金 2x"]
        STD["🐢 標準速度 サービング<br/>(標準クォータ: anthropic-claude-fable)<br/>PayGo / Provisioned Throughput"]
    end

    MON["📈 Cloud Monitoring<br/>model_user_id=claude-fable-5-2-fast"]

    APP -- "rawPredict リクエスト" --> EP
    EP --> SPEED
    SPEED -- "\"speed\": \"fast\"" --> FAST
    SPEED -- "省略 / \"standard\"" --> STD
    FAST -- "usage.speed=fast" --> APP
    STD --> APP
    FAST -.-> MON
```

同一の公開モデルエンドポイント (`claude-fable-5-2`) に対して、リクエストボディの `"speed"` パラメータの有無で標準速度と Fast モードのサービング経路が切り替わり、それぞれ独立したクォータと料金体系で処理されます。

## サービスアップデートの詳細

### 主要機能

1. **Claude Fable 5.2 (`claude-fable-5-2`) の GA 提供**
   - 技術・科学分野 (コーディング、金融など) の作業向けに設計された Anthropic の最新 GA モデル
   - 曖昧な問題への長時間の取り組み、自己検証、サブエージェントのオーケストレーションに対応
   - 入力はテキスト・画像・PDF、出力はテキスト。最大入力 1,000,000 トークン / 最大出力 128,000 トークン
   - Fast モード、Computer use、Web search、バッチ予測、プロンプトキャッシュ、Function calling、トークンカウント、Memory tool をサポート
   - リリース日は 2026 年 11 月 9 日、廃止日は 2027 年 11 月 9 日より前にならない

2. **Fast モード (`"speed": "fast"`) の GA 提供**
   - オンライン従量課金予測リクエストのトップレベルに `"speed": "fast"` を設定することで出力トークン生成を高速化
   - ベースモデルの知能・安全性を維持する高速サービング構成を使用。`anthropic-beta` ヘッダーや別モデルカードの有効化は不要
   - 応答の `usage.speed` フィールド (ストリーミングの場合は `message_start` / `message_delta` イベント) で実際に使用された速度を確認可能
   - サポートロケーションは `global`、`us` (米国マルチリージョン)、`eu` (欧州マルチリージョン)。リージョナルエンドポイントは非対応

3. **Fast モードのライフサイクルポリシー**
   - Fast モードは対応モデルファミリーの最新バージョンで提供され、新バージョン公開後は旧バージョンで 30 日間の移行期間が設けられる
   - 移行期間終了後、旧バージョンへの `"speed": "fast"` リクエストは HTTP 400 (`INVALID_ARGUMENT`) を返す (標準速度のリクエストは引き続き動作)

## 技術仕様

### Claude Fable 5.2 モデル仕様

| 項目 | 詳細 |
|------|------|
| モデル ID | `claude-fable-5-2` |
| ステータス | GA |
| 入力 | テキスト、画像、PDF |
| 出力 | テキスト |
| 最大入力トークン | 1,000,000 |
| 最大出力トークン | 128,000 |
| 利用可能エンドポイント | `global`、`us` (米国マルチリージョン)、`eu` (欧州マルチリージョン) |
| ML 処理 | 米国マルチリージョン、欧州マルチリージョン |
| クォータ | モデル有効化時に付与 (Shared lineage quotas)、Provisioned Throughput は非対応 |
| 廃止日 | 2027 年 11 月 9 日より前にならない |

### Fast モード仕様

| 項目 | 詳細 |
|------|------|
| 有効化方法 | リクエストボディに `"speed": "fast"` を設定 |
| 対応モデル | Claude Fable 5.2 (`claude-fable-5-2`) ※対応ファミリーの最新バージョンに提供 |
| 対応ロケーション | `global` / `us` / `eu` (リージョナルエンドポイントは非対応、HTTP 400 `FAILED_PRECONDITION`) |
| 課金 | 従量課金 (PayGo) のみ。Provisioned Throughput 非対応 |
| クォータ | 専用の Shared lineage quota (`anthropic-claude-fable-fast`)。標準速度クォータとは分離 |
| モニタリング | Cloud Monitoring で `model_user_id="claude-fable-5-2-fast"` としてレポート |
| 必要な IAM ロール | Agent Platform User (`roles/aiplatform.user`) |
| 組織ポリシー | ベースモデルの `publishers/anthropic/models/claude-fable-5-2:predict` の許可/拒否に従う |

### リクエスト例 (REST)

```json
{
  "anthropic_version": "vertex-2023-10-16",
  "speed": "fast",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "Analyze the root cause of an HTTP 502 spike on an upstream GKE ingress controller and list three immediate mitigation steps."
    }
  ]
}
```

Fast モードで処理された応答では、`usage` オブジェクトに `"speed": "fast"` が含まれます。

## 設定方法

### 前提条件

1. Model Garden で Claude Fable 5.2 のモデルカードから「Enable」をクリックし、Anthropic および Marketplace の利用規約に同意する (Advanced AI Safety Addendum への同意がプロジェクトごとに 1 回必要)
2. Anthropic の Service Specific Terms (Section F) に基づき、モデルロケーションごとにプロンプト・レスポンス共有を有効化する
3. リクエストを送信するプリンシパルに Agent Platform User ロール (`roles/aiplatform.user`) を付与する

### 手順

#### ステップ 1: Fast モードで予測リクエストを送信する (REST)

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @request.json \
  "https://aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/global/publishers/anthropic/models/claude-fable-5-2:rawPredict"
```

`request.json` に `"speed": "fast"` を含むリクエストボディ (前述の例) を保存して実行します。エンドポイント URL には必ずベースモデル ID (`claude-fable-5-2`) を指定します (`claude-fable-5-2-fast` を URL に指定すると HTTP 404 になります)。

#### ステップ 2: Python (Anthropic Vertex SDK) から Fast モードを使用する

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(project_id="PROJECT_ID", region="global")
message = client.messages.create(
    model="claude-fable-5-2",
    max_tokens=1024,
    extra_body={"speed": "fast"},
    messages=[{"role": "user", "content": "..."}],
)
```

`anthropic[vertex]` SDK では `extra_body={"speed": "fast"}` を渡します。応答の `usage.speed` で実際の速度を検証できます。

#### ステップ 3: Fast モードが利用できない場合のフォールバックを実装する

Agent Platform は Fast モードリクエストを暗黙的に標準速度へダウングレードしないため、`BadRequestError` のエラーメッセージを判定して標準速度で再試行する、または次のモデルバージョンの Fast モードへ切り替えるフォールバックをアプリケーション側で実装することが推奨されます。

## メリット

### ビジネス面

- **対話型エージェント体験の向上**: トークン生成の待ち時間が短縮され、人間参加型のコーディング反復やライブプランニングでコンテキストスイッチを減らせる
- **段階的な導入が容易**: リクエストパラメータ 1 つで有効化でき、既存のモデル有効化・IAM・組織ポリシー設定をそのまま利用できるため導入コストが低い
- **最新 Fable モデルの本番利用**: GA ステータスにより、技術・科学分野の高度なタスクに Claude Fable 5.2 を本番ワークロードで利用できる

### 技術面

- **クォータの分離**: Fast モードは専用の `anthropic-claude-fable-fast` クォータを使用するため、高速トラフィックが標準トラフィックのレート制限を圧迫しない (逆も同様)
- **可観測性**: Cloud Monitoring で `model_user_id="claude-fable-5-2-fast"` によって Fast モードのリクエスト数・トークン使用量・レイテンシを標準速度と分けて監視できる
- **モデル品質の維持**: Fast モードはベースモデルの知能と安全性を維持する高速サービング構成であり、モデルを変えずに速度だけを選択できる

## デメリット・制約事項

### 制限事項

- Fast モードは Provisioned Throughput に非対応。常に従量課金 (PayGo) となり、ベースモデルの Provisioned Throughput 注文があっても消費・スピルオーバーしない
- Fast モードのロケーションは `global` / `us` / `eu` のみ。リージョナルエンドポイントへの `"speed": "fast"` リクエストは HTTP 400 (`FAILED_PRECONDITION`) を返す
- `X-Vertex-AI-LLM-Request-Type: dedicated` ヘッダー付きの Fast モードリクエストは HTTP 429 (`RESOURCE_EXHAUSTED`) でスロットルされる (ヘッダーを省略するか `shared` を指定)
- Claude Fable 5.2 自体も Provisioned Throughput は非対応 (Shared Model Lineage Quota のみ)
- Fast モードのトークン料金は標準速度の 2 倍 (全トークンタイプ)

### 考慮すべき点

- 新バージョンのモデル公開後、旧バージョンの Fast モードは 30 日で廃止される。廃止後は HTTP 400 となるため、標準速度へのフォールバックまたは次バージョンへの移行処理を実装しておく必要がある
- Fast モードリクエストは暗黙にダウングレードされないため、可用性エラーのハンドリングはアプリケーション側の責務となる
- Claude Fable 5.2 は Advanced AI Safety Addendum の対象であり、不正利用監視の目的で全プロンプト・レスポンスが最大 30 日間保存される
- `claude-fable-5-2-fast` はモニタリング用のメトリクスラベルであり、呼び出し可能なモデル ID ではない点に注意

## ユースケース

### ユースケース 1: 対話型エージェントコーディング

**シナリオ**: 開発者が human-in-the-loop のコーディングエージェントで、複数ステップのリファクタリングやデバッグを反復する。応答待ちが長いとコンテキストスイッチが発生し生産性が落ちる。

**実装例**:
```python
message = client.messages.create(
    model="claude-fable-5-2",
    max_tokens=4096,
    extra_body={"speed": "fast"},
    messages=[{"role": "user", "content": "このモジュールをリファクタリングして..."}],
)
```

**効果**: 出力トークン生成が高速化され、開発者が対話のテンポを維持したまま反復作業を進められる。

### ユースケース 2: インシデント対応の高速トリアージ

**シナリオ**: 本番アラートの発生時に、エージェントがアラート内容と運用コンテキストを集約し、根本原因の分析と緩和手順を生成する。推論のターンアラウンドタイムが対応速度に直結する。

**効果**: Fast モードによりトリアージと修復手順の生成が高速化され、MTTR (平均復旧時間) の短縮に寄与する。レイテンシ非依存のバッチ分析は標準速度 (1x 料金) に振り分けることでコストも最適化できる。

### ユースケース 3: 技術・科学分野の高度なエージェントワークロード

**シナリオ**: 複雑なコーディング、数学、金融分析などの長時間タスクを、サブエージェントのオーケストレーションと自己検証を活用して自律的に処理する。

**効果**: GA となった Claude Fable 5.2 の 100 万トークン入力と Memory tool・Computer use などの機能により、大規模コードベースや長大なドキュメントを扱う本番エージェントを構築できる。

## 料金

Claude Fable 5.2 は従量課金 (pay-as-you-go) で、トークン数に基づいて課金されます。Fast モードの料金は以下のとおりです。

- **トークン**: 標準速度のトークン料金の **2 倍** (入力、出力、5 分 / 1 時間キャッシュ書き込み、キャッシュヒットの全トークンタイプに適用)
- **Web search**: Web search ツール呼び出しは標準 (1x) 料金で課金
- 課金はベースモデルの Google Cloud SKU に Fast モードのラベル付きで計上される
- Fast モードは常に PayGo であり、Provisioned Throughput では利用不可

具体的なトークン単価は [Agent Platform の料金ページ](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing#partner-models) を参照してください。

## 利用可能リージョン

| 機能 | 利用可能ロケーション |
|------|---------------------|
| Claude Fable 5.2 (標準速度) | `global` (グローバルエンドポイント)、`us` (米国マルチリージョン)、`eu` (欧州マルチリージョン) |
| Fast モード | `global`、`us`、`eu` (リージョナルエンドポイントは非対応) |
| ML 処理 | 米国マルチリージョン、欧州マルチリージョン |

## 関連サービス・機能

- **Model Garden**: Claude Fable 5.2 のモデルカードから有効化・利用規約への同意を行う。組織ポリシー `constraints/vertexai.allowedModels` でアクセス制御が可能
- **Cloud Monitoring**: `model_user_id="claude-fable-5-2-fast"` で Fast モードのトラフィックを標準速度と分離して監視
- **プロンプトキャッシュ**: Claude モデルのキャッシュ機能と併用可能 (Fast モードではキャッシュ関連トークンも 2x 料金)
- **Provisioned Throughput**: 標準速度の Claude モデル向け固定スループット購入オプション (Fast モードおよび Claude Fable 5.2 は非対応)
- **バッチ予測 / Web search / Computer use / Memory tool**: Claude Fable 5.2 がサポートする関連機能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261109-claude-fable-5-2-fast-mode-ga.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#November_09_2026)
- [Fast mode with Anthropic Claude models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/fast-mode)
- [Anthropic's Claude Fable 5.2 モデルドキュメント](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/fable-5-2)
- [Quotas for Anthropic Claude models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/quotas)
- [料金ページ](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing#partner-models)

## まとめ

Claude Fable 5.2 の GA と Fast モードの GA により、Google Cloud 上で最新の Fable 系モデルを本番利用しつつ、`"speed": "fast"` パラメータ 1 つでレイテンシ重視のエージェントワークロードを高速化できるようになりました。Fast モードは料金が標準の 2 倍かつ PayGo 限定のため、対話型・時間クリティカルな処理に限定して適用し、バッチ処理は標準速度と使い分けるのが効果的です。導入時は、モデルバージョン更新に伴う 30 日の Fast モード廃止ウィンドウを踏まえたフォールバック実装を推奨します。

---

**タグ**: Gemini Enterprise Agent Platform, Model Garden, Anthropic, Claude Fable 5.2, Fast mode, 生成 AI, エージェント, GA
