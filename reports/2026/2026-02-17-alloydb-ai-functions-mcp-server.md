# AlloyDB for PostgreSQL: パフォーマンススナップショット・AI 関数一括処理・リモート MCP サーバー

**リリース日**: 2026-02-17
**サービス**: AlloyDB for PostgreSQL
**機能**: パフォーマンススナップショット Read Pool 対応、AI 関数一括処理、リモート MCP サーバー
**ステータス**: Feature (Preview/GA mix)

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260217-alloydb-ai-functions-mcp-server.html)

## 概要

AlloyDB for PostgreSQL に対して複数の重要なアップデートが同時にリリースされた。パフォーマンススナップショットレポートが Read Pool インスタンスノードに対応し、AI 関数の配列ベース一括処理が Preview として利用可能になり、さらにリモート MCP サーバーが Preview として公開された。加えて、Model Context Protocol (MCP) を使用した生成 AI エージェントのセキュリティベストプラクティスも新たに公開されている。

これらのアップデートは、AlloyDB をデータベースとしてだけでなく、AI ワークロードの中核的なプラットフォームとして位置づける Google Cloud の戦略を反映している。AI 関数の一括処理により、大量データに対するインテリジェントな SQL クエリのスケーラビリティが向上し、リモート MCP サーバーにより LLM や AI アプリケーションから AlloyDB クラスターへの接続が標準化された。

対象ユーザーは、AlloyDB を利用するデータベース管理者、AI アプリケーション開発者、および AI エージェントを構築する Solutions Architect である。

**アップデート前の課題**

- パフォーマンススナップショットレポートはプライマリインスタンスのみに対応しており、Read Pool インスタンスノードのパフォーマンスを個別に分析できなかった
- AI 関数 (ai.if、ai.rank、ai.generate) は行ごとに逐次処理されるため、大量データに対する AI ワークロードのスケーリングに時間がかかっていた
- AlloyDB クラスターに LLM や AI アプリケーションから接続するには、MCP Toolbox for Databases をローカルにインストールして個別に設定する必要があった
- MCP を使用した AI エージェントのセキュリティに関する統一的なベストプラクティスが存在しなかった

**アップデート後の改善**

- Read Pool インスタンスノードのパフォーマンススナップショットレポートが取得可能になり、読み取り操作やレプリカ固有のパフォーマンス問題を詳細に分析できるようになった
- 配列ベースの一括処理 (array-based processing) により、AI 関数呼び出しを行単位ではなくまとめて実行でき、インテリジェントなワークフローのスケーリングが高速化された (Preview)
- AlloyDB リモート MCP サーバーにより、Gemini CLI、Claude Code、Cursor などの AI アプリケーションからマネージド HTTP エンドポイント経由で AlloyDB クラスターに接続できるようになった (Preview)
- Google Cloud データベースにおける生成 AI エージェントのセキュリティベストプラクティス (最小権限、ネイティブデータベースコントロール、セキュアなエージェント設計) が公式に文書化された

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph AI_Apps["AI アプリケーション"]
        A1(["Gemini CLI"])
        A2(["Claude Code"])
        A3(["カスタム AI エージェント"])
    end

    subgraph MCP_Layer["MCP レイヤー"]
        MCP["AlloyDB リモート\nMCP サーバー\n(Preview)"]
    end

    subgraph AlloyDB_Cluster["AlloyDB クラスター"]
        Primary[("Primary\nインスタンス")]
        ReadPool[("Read Pool\nインスタンス")]

        subgraph AI_Functions["AI 関数"]
            AIF["ai.if / ai.rank\nai.generate\n(配列ベース一括処理)"]
        end

        subgraph Observability["オブザーバビリティ"]
            PerfSnap["パフォーマンス\nスナップショット"]
        end
    end

    subgraph Vertex_AI["Vertex AI"]
        Gemini["Gemini モデル"]
    end

    A1 & A2 & A3 -->|HTTP| MCP
    MCP -->|SQL| Primary
    MCP -->|SQL| ReadPool
    AIF -->|API 呼び出し| Gemini
    PerfSnap -.->|メトリクス収集| Primary
    PerfSnap -.->|メトリクス収集\n(新規対応)| ReadPool
```

AlloyDB のアーキテクチャにおいて、AI アプリケーションがリモート MCP サーバー経由で AlloyDB クラスターに接続し、AI 関数が Vertex AI の Gemini モデルと連携して一括処理を行い、パフォーマンススナップショットが Primary と Read Pool の両方からメトリクスを収集する全体像を示している。

## サービスアップデートの詳細

### 主要機能

1. **パフォーマンススナップショットの Read Pool インスタンスノード対応**
   - パフォーマンススナップショットレポートが Read Pool インスタンスノードをサポートするようになった
   - vCPU 使用率、メモリ使用率、ディスク I/O、トランザクション数、待機イベントなどのシステムメトリクスを Read Pool ノードから収集可能
   - `perfsnap.snap()` 関数と `perfsnap.report()` 関数を Read Pool インスタンス上で実行可能
   - 自動スナップショット (デフォルト: 1 日 1 回) と手動スナップショットの両方に対応
   - 2 つのスナップショット間の差分レポートを生成し、Read Pool 固有のパフォーマンス問題を特定できる

2. **AI 関数の配列ベース一括処理 (Preview)**
   - AI 関数呼び出し (ai.if、ai.rank、ai.generate) を行ごとではなく配列ベースでまとめて実行可能
   - `google_ml_integration` エクステンション経由で Vertex AI の Gemini モデルなどと連携
   - 大量データに対するインテリジェントなフィルタリング、ランキング、テキスト生成のスケーリングが高速化
   - Gemini、OpenAI、Anthropic などのプロバイダーの登録済みモデルと連携可能
   - SQL クエリ内で自然言語を使用した AI 処理を効率的に実行

3. **AlloyDB リモート MCP サーバー (Preview)**
   - AlloyDB クラスターに LLM、AI アプリケーション、AI 対応開発プラットフォームから接続可能
   - マネージドグローバルまたはリージョナル HTTP エンドポイントを提供
   - 簡素化された集中型ディスカバリ、きめ細かな認可制御
   - Model Armor によるプロンプトおよびレスポンスのセキュリティ保護 (オプション)
   - 集中監査ログに対応
   - Gemini CLI、Claude Code、Cursor、VS Code (Copilot)、Windsurf などの AI ツールから利用可能

4. **生成 AI エージェントのセキュリティベストプラクティス**
   - MCP を使用した AI エージェントの安全な設計に関するガイダンス
   - 最小権限の原則に基づくアクセス制御
   - ネイティブデータベースコントロールの活用
   - セキュアなエージェント設計パターン

## 技術仕様

### AI 関数の仕様

| 項目 | 詳細 |
|------|------|
| 対応オペレーター | `ai.if` (フィルタ)、`ai.rank` (スコアリング)、`ai.generate` (テキスト生成) |
| 必須エクステンション | `google_ml_integration` バージョン 1.5.2 以上 |
| 対応モデルプロバイダー | Gemini、OpenAI、Anthropic |
| 処理モード | 行単位処理 (従来)、配列ベース一括処理 (新規・Preview) |
| 必須フラグ | `google_ml_integration.enable_ai_query_engine = true` |
| 必須フラグ | `google_ml_integration.enable_model_support = on` |

### パフォーマンススナップショットの仕様

| 項目 | 詳細 |
|------|------|
| 対応インスタンス | Primary インスタンス、Read Pool インスタンスノード (新規) |
| 自動スナップショット頻度 | デフォルト 1 日 1 回 (カスタマイズ可能) |
| 自動スナップショット保持期間 | 7 日間 |
| 手動スナップショット上限 | インスタンスあたり最大 2,500 |
| 手動スナップショット保持期間 | 90 日間 (自動クリーンアップ) |
| 収集メトリクス | vCPU 使用率、メモリ使用率、ディスク I/O、トランザクション数、待機イベント |
| SQL 統計対応 | `pg_stat_statements` エクステンション有効化時 |

### MCP サーバーの接続設定

```json
{
  "mcpServers": {
    "alloydb": {
      "command": "./PATH/TO/toolbox",
      "args": ["--prebuilt", "alloydb-postgres", "--stdio"],
      "env": {
        "ALLOYDB_POSTGRES_PROJECT": "PROJECT_ID",
        "ALLOYDB_POSTGRES_REGION": "REGION",
        "ALLOYDB_POSTGRES_CLUSTER": "CLUSTER_NAME",
        "ALLOYDB_POSTGRES_INSTANCE": "INSTANCE_NAME",
        "ALLOYDB_POSTGRES_DATABASE": "DATABASE_NAME",
        "ALLOYDB_POSTGRES_USER": "USERNAME",
        "ALLOYDB_POSTGRES_PASSWORD": "PASSWORD"
      }
    }
  }
}
```

## 設定方法

### 前提条件

1. AlloyDB for PostgreSQL クラスターが作成済みであること
2. Vertex AI API が有効化済みであること (AI 関数利用時)
3. `alloydbsuperuser` ロールまたは `pg_monitor` ロールが付与済みであること (パフォーマンススナップショット利用時)

### 手順

#### ステップ 1: AI 関数の有効化

```sql
-- google_ml_integration エクステンションのインストール・更新
CREATE EXTENSION IF NOT EXISTS google_ml_integration;
ALTER EXTENSION google_ml_integration UPDATE;

-- AI クエリエンジンの有効化 (セッション単位)
SET google_ml_integration.enable_ai_query_engine = true;

-- AI クエリエンジンの有効化 (データベース単位)
ALTER DATABASE my_database SET google_ml_integration.enable_ai_query_engine = 'on';
```

#### ステップ 2: AI 関数の使用例 (一括処理)

```sql
-- ai.if: 自然言語条件でフィルタリング
SELECT r.name, r.location_city
FROM restaurant_reviews r
WHERE AI.IF(
  r.location_city || ' has a population of more than 100,000 AND the following is a positive review; Review: ' || r.review
)
GROUP BY r.name, r.location_city
HAVING COUNT(*) > 500;

-- ai.generate: テキスト要約の生成
SELECT
  ai.generate(
    prompt => 'Summarize the review in 20 words or less. Review: ' || review
  ) AS review_summary
FROM user_reviews;

-- ai.rank: カスタムスコアリング
SELECT review AS top20
FROM user_reviews
ORDER BY ai.rank(
  'Score the following review: (1) 8-10 if excellent, (2) 4-7 if ok, (3) 1-3 if not good. Review:' || review
) DESC
LIMIT 20;
```

#### ステップ 3: パフォーマンススナップショットの取得 (Read Pool)

```sql
-- Read Pool インスタンスに接続後、スナップショットを取得
SELECT perfsnap.snap();

-- ワークロード実行後に 2 つ目のスナップショットを取得
SELECT perfsnap.snap();

-- 2 つのスナップショット間のレポートを生成
SELECT perfsnap.report(1, 2);

-- 既存スナップショットの一覧表示
SELECT * FROM perfsnap.g$snapshots;
```

#### ステップ 4: MCP Toolbox for Databases のインストール

```bash
# Linux/amd64 の場合
curl -O https://storage.googleapis.com/genai-toolbox/v0.15.0/linux/amd64/toolbox
chmod +x toolbox
./toolbox --version
```

## メリット

### ビジネス面

- **AI ワークロードのコスト最適化**: 一括処理により API 呼び出しのオーバーヘッドが削減され、大量データに対する AI 処理のコスト効率が向上する
- **開発者生産性の向上**: リモート MCP サーバーにより、AI 開発ツールからデータベースへのアクセスが標準化・簡素化され、AI アプリケーションの開発サイクルが短縮される
- **運用効率の改善**: Read Pool のパフォーマンス分析が可能になることで、読み取り負荷の最適化やキャパシティプランニングがより正確になる

### 技術面

- **スケーラビリティの向上**: 配列ベースの一括処理により、数万行に対する AI 関数実行のスループットが大幅に改善される
- **オブザーバビリティの強化**: Read Pool ノード個別のメトリクス (vCPU、メモリ、ディスク I/O、待機イベント) が取得可能になり、レプリケーション遅延の原因特定が容易になる
- **セキュリティの強化**: リモート MCP サーバーのきめ細かな認可制御、Model Armor によるプロンプト保護、集中監査ログにより、エンタープライズグレードの AI エージェント運用が可能

## デメリット・制約事項

### 制限事項

- AI 関数の配列ベース一括処理は Preview 段階であり、SLA の対象外。本番ワークロードでの利用には注意が必要
- リモート MCP サーバーも Preview であり、ツール名やパラメータが予告なく変更される可能性がある
- パフォーマンススナップショットの手動スナップショットはインスタンスあたり最大 2,500 個に制限されている
- AI 関数の利用には `google_ml_integration` エクステンション 1.5.2 以上が必要
- AI 関数で使用する Gemini モデルはリージョンによって利用可能なモデルが異なる

### 考慮すべき点

- AI 関数の一括処理を使用する場合、Vertex AI の API 呼び出しクォータとレート制限を事前に確認すること
- リモート MCP サーバーの利用にはプロジェクトでの有効化と適切な IAM 設定が必要
- パフォーマンススナップショットの `perfsnap.interval` フラグによる頻度のカスタマイズは、リソース使用量に影響するため適切な間隔を設定すること

## ユースケース

### ユースケース 1: 大規模レビューデータの AI 分析

**シナリオ**: EC サイトで数百万件の商品レビューに対して、センチメント分析とカテゴリ分類を SQL で一括実行する

**実装例**:
```sql
-- 一括処理による商品レビューのセンチメント分析とフィルタリング
SELECT product_id, review_text,
  ai.generate(
    prompt => 'Classify the sentiment as positive/negative/neutral. Review: ' || review_text
  ) AS sentiment
FROM product_reviews
WHERE ai.if(
  prompt => 'Is this review about product quality issues? Review: ' || review_text
);
```

**効果**: 行ごとの逐次処理と比較して、配列ベースの一括処理により処理スループットが向上し、大量データに対する AI 分析パイプラインの実行時間が短縮される

### ユースケース 2: AI エージェントからのデータベース操作

**シナリオ**: カスタマーサポート AI エージェントが、リモート MCP サーバー経由で AlloyDB に格納された顧客データや注文履歴に自然言語でアクセスする

**効果**: MCP 標準プロトコルによる接続の標準化、Model Armor によるプロンプトセキュリティ保護、IAM による細粒度のアクセス制御により、セキュアかつ効率的な AI エージェント運用が実現される

### ユースケース 3: Read Pool のパフォーマンスチューニング

**シナリオ**: 読み取り負荷の高いアプリケーションで、特定の Read Pool ノードにおけるクエリパフォーマンスの低下原因を調査する

**実装例**:
```sql
-- Read Pool ノードでベースラインスナップショットを取得
SELECT perfsnap.snap();

-- ピーク負荷時にスナップショットを取得
SELECT perfsnap.snap();

-- 差分レポートを生成して待機イベントやディスク I/O を分析
SELECT perfsnap.report(1, 2);
```

**効果**: Read Pool ノード固有の待機イベント、ディスク I/O パターン、SQL 実行統計を分析でき、レプリカ固有のパフォーマンスボトルネックを特定・解消できる

## 料金

AlloyDB for PostgreSQL は従量課金制を採用しており、料金は以下の要素で決定される。

- **インスタンスリソース**: Primary および Read Pool インスタンスのマシンタイプ (vCPU 数、RAM 量) に基づく
- **ストレージ**: クラスターのフレキシブルストレージレイヤーに保存されたデータ量
- **ネットワーク**: インスタンスからのネットワーク Egress トラフィック量

AI 関数の使用に伴う Vertex AI API 呼び出しの料金は、Vertex AI の料金体系に従って別途課金される。

詳細は [AlloyDB for PostgreSQL の料金ページ](https://cloud.google.com/alloydb/pricing) を参照。

## 利用可能リージョン

AlloyDB for PostgreSQL は複数のリージョンで利用可能である。AI 関数で使用する Gemini モデルの利用可能性はリージョンによって異なる。`gemini-2.0-flash` がサポートされていないリージョンでは、グローバルエンドポイントを使用するか、利用可能な他の Gemini モデルを `model_id` パラメータで指定する必要がある。リモート MCP サーバーはグローバルおよびリージョナルの HTTP エンドポイントを提供する。

詳細は [AlloyDB のロケーションに関するドキュメント](https://cloud.google.com/alloydb/docs/locations) を参照。

## 関連サービス・機能

- **Vertex AI**: AI 関数が Vertex AI の Gemini モデルと連携し、エンベディング生成、予測、テキスト生成を実行する基盤
- **Cloud Monitoring / Metrics Explorer**: パフォーマンススナップショットを補完するリアルタイムメトリクス監視機能
- **MCP Toolbox for Databases**: AlloyDB を含む Google Cloud データベースに AI エージェントを接続するためのオープンソース MCP サーバー
- **Model Armor**: リモート MCP サーバーのプロンプトおよびレスポンスに対するセキュリティスキャン機能
- **Cloud SQL**: 同様にリモート MCP サーバーに対応しており、MySQL / PostgreSQL / SQL Server をサポート
- **AlloyDB AI natural language**: 自然言語クエリを SQL に変換する機能 (Preview) で、AI 関数と組み合わせて利用可能

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260217-alloydb-ai-functions-mcp-server.html)
- [公式リリースノート](https://cloud.google.com/release-notes#February_17_2026)
- [AlloyDB AI 関数ドキュメント](https://cloud.google.com/alloydb/docs/ai/evaluate-semantic-queries-ai-operators)
- [AlloyDB AI 概要](https://cloud.google.com/alloydb/docs/ai)
- [AlloyDB パフォーマンススナップショット](https://cloud.google.com/alloydb/docs/optimize-database-performance-compare-snapshots)
- [AlloyDB MCP Toolbox 接続ガイド](https://cloud.google.com/alloydb/docs/connect-ide-using-mcp-toolbox)
- [Google Cloud MCP サーバー概要](https://cloud.google.com/mcp/overview)
- [料金ページ](https://cloud.google.com/alloydb/pricing)

## まとめ

今回の AlloyDB for PostgreSQL アップデートは、データベース内 AI 処理のスケーラビリティ、AI エージェントとの標準的な接続手段、Read Pool のオブザーバビリティという 3 つの重要な領域を強化するものである。特に AI 関数の配列ベース一括処理とリモート MCP サーバーは、AlloyDB を AI ネイティブなデータプラットフォームとして進化させる戦略的な機能であり、AI アプリケーション開発者は早期に Preview 機能を評価することを推奨する。パフォーマンススナップショットの Read Pool 対応については、読み取り負荷の高い本番環境での即座の活用が可能である。

---

**タグ**: #AlloyDB #PostgreSQL #AI #MCP #ModelContextProtocol #Databases #VertexAI #パフォーマンス #オブザーバビリティ #GoogleCloud
