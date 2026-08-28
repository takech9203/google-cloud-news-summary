# Cloud Trace: Datastream のリモート MCP サーバーが tools/call のトレーススパンを自動生成

**リリース日**: 2026-08-27

**サービス**: Cloud Trace

**機能**: リモート MCP サーバーによる `tools/call` トレーススパンの自動生成 (Datastream の追加)

**ステータス**: Feature

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260827-cloud-trace-datastream-mcp-spans.html)

## 概要

Google Cloud のリモート MCP (Model Context Protocol) サーバーのうち、**Datastream** の MCP サーバーが、`tools/call` オペレーションに対してトレーススパンを自動生成するようになりました。生成されたスパンは Cloud Trace に保存され、AI エージェント (エージェンティックアプリケーション) が Datastream のツールを呼び出した際の挙動やレイテンシを可視化できます。

Datastream はサーバーレスの変更データキャプチャ (CDC) / レプリケーションサービスであり、そのリモート MCP サーバー (`https://datastream.googleapis.com/mcp`) を利用すると、AI エージェントはストリームの一覧取得・詳細確認・実行・削除、接続プロファイルの一覧取得などを標準化されたツールとして呼び出せます。今回のアップデートにより、エージェントがこれらの Datastream 操作を実行した場合でも、その呼び出しがエンドツーエンドのトレースの一部として記録されるようになります。

対象ユーザーは、ADK (Agent Development Kit) などのフレームワークで AI エージェントを構築し、Datastream のリモート MCP サーバーを組み込んでいるデータエンジニア・開発者・SRE です。なお、2026-08-24 には Policy Troubleshooter と Managed Service for Apache Airflow の MCP サーバーが同機能に対応しており、今回はその対応プロダクトの拡大にあたります。

**アップデート前の課題**

- Datastream のリモート MCP サーバーは `tools/call` に対するトレーススパンを生成しておらず、エージェントからのツール呼び出し (ストリーム操作など) がトレース上で可視化されなかった
- エージェントのエンドツーエンドのトレースにおいて、Datastream MCP サーバー呼び出し部分のステータスやレイテンシがブラックボックスになっていた

**アップデート後の改善**

- Datastream のリモート MCP サーバーが `tools/call` オペレーションのトレーススパンを自動生成するようになった
- クライアント側から W3C Trace Context (`traceparent`) を `_meta` フィールドで伝播させることで、エージェントのトレースにサーバー側スパンが結合され、呼び出しの挙動とレイテンシを Trace Explorer で分析できるようになった
- トレーススパン生成に対応するリモート MCP サーバーは、Cloud Logging、BigQuery、Cloud SQL、Policy Troubleshooter などに続き計 16 プロダクトに拡大した

## アーキテクチャ図

```mermaid
sequenceDiagram
    participant User as 🧑 ユーザー
    participant Agent as 🤖 AI エージェント<br/>(ADK など)
    participant MCP as 🔌 Datastream<br/>リモート MCP サーバー
    participant DS as 🔄 Datastream API
    participant Trace as 📊 Cloud Trace

    User->>Agent: プロンプト入力
    Agent->>MCP: tools/call (例: list_streams)<br/>_meta: traceparent (W3C Trace Context)
    Note over MCP: 認証・認可チェック後<br/>スパンを自動生成
    MCP->>DS: API メソッド呼び出し
    DS-->>MCP: レスポンス
    MCP-->>Trace: スパン送信<br/>(名前: "tools/call NAME")
    MCP-->>Agent: ツール実行結果
    Agent-->>User: 回答
    User->>Trace: Trace Explorer で<br/>スパンを確認
```

AI エージェントが `_meta` フィールドでトレースコンテキストを渡して Datastream MCP サーバーの `tools/call` を実行すると、サーバーがスパンを自動生成して Cloud Trace に記録し、エージェントのトレースに結合されます。

## サービスアップデートの詳細

### 主要機能

1. **Datastream MCP サーバーによる `tools/call` スパンの自動生成**
   - Datastream のリモート MCP サーバーが、ツール呼び出しを受信するとトレーススパンを生成する
   - スパンには呼び出しのステータスとレイテンシ情報が記録され、エージェントのエンドツーエンドのトレースの一部として分析できる

2. **W3C Trace Context によるトレースコンテキストの伝播**
   - MCP 標準の `_meta` フィールドに `traceparent` (および任意で `tracestate`) を含めることで、クライアント側スパンとサーバー側スパンが同一トレースに紐付く
   - OpenTelemetry Semantic Conventions for MCP に対応するフレームワーク・SDK (ADK など) がこの伝播をサポートする

3. **Trace Explorer でのスパン検索**
   - スパン名は OpenTelemetry Semantic Conventions for MCP に従い `tools/call NAME` (NAME は呼び出したツール名。例: `list_streams`) の形式で記録される
   - Trace Explorer のフィルタバーで属性 `mcp.method.name` = `tools/call` を指定して、MCP サーバーが生成したスパンを絞り込める

### スパン生成の対象となる Datastream MCP ツール

Datastream のリモート MCP サーバーは以下のツールを提供しており、これらへの `tools/call` がスパン生成の対象になります。

| ツール | 説明 |
|------|------|
| `list_streams` / `get_stream` | ストリームの一覧取得・詳細取得 |
| `run_stream` / `delete_stream` | ストリームの実行・削除 (長時間実行オペレーションを返す) |
| `get_operation` | 長時間実行オペレーションのステータス取得 |
| `list_stream_objects` / `get_stream_object` / `lookup_stream_object` | ストリームオブジェクトの一覧・詳細・ルックアップ |
| `list_connection_profiles` | 接続プロファイルの一覧取得 |
| `list_static_ips` | 静的 IP 接続方式で許可リストに登録する IP アドレスの一覧取得 |

### 対応プロダクト一覧 (トレーススパン生成に対応するリモート MCP サーバー)

| プロダクト | 備考 |
|------|------|
| **Datastream** | 今回追加 |
| Policy Troubleshooter / Managed Service for Apache Airflow | 2026-08-24 に追加 |
| Cloud Logging / Cloud Monitoring | 対応済み |
| GKE / Cloud Run / Compute Engine | 対応済み |
| BigQuery / Cloud SQL / AlloyDB for PostgreSQL | 対応済み |
| Google Security Operations / Agent Search / Personalized Service Health / Cloud Billing / Maps Grounding Lite | 対応済み |

## 技術仕様

### トレースコンテキストの伝播 (`_meta` フィールド)

`tools/call` リクエストの `params._meta` に W3C Trace Context を含めます。

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "list_streams",
    "arguments": {
      "parent": "projects/my-project/locations/us-central1"
    },
    "_meta": {
      "traceparent": "00-TRACE_ID-PARENT_SPAN_ID-SAMPLED_FLAG",
      "tracestate": "Vendor specific information."
    }
  },
  "id": 1
}
```

| `traceparent` の構成要素 | 説明 |
|------|------|
| `00` | traceparent 仕様のバージョン |
| `TRACE_ID` | トレースの ID |
| `PARENT_SPAN_ID` | 呼び出し元スパンの ID |
| `SAMPLED_FLAG` | サンプリングフラグ (サンプリング時は `01`、非サンプリング時は `00`) |

### Datastream MCP サーバーのエンドポイント

| 項目 | 詳細 |
|------|------|
| エンドポイント | `https://datastream.googleapis.com/mcp` |
| 事前準備 | MCP サーバーの有効化と認証の設定が必要 |

## 設定方法

### 前提条件

1. AI エージェントが Datastream のリモート MCP サーバーを利用していること (MCP サーバーの有効化と認証設定が必要)
2. トレースコンテキストを `_meta` フィールドで伝播できるフレームワーク・SDK (OpenTelemetry Semantic Conventions for MCP に対応するもの。例: ADK) を使用していること
3. リクエストが認証・認可を通過すること (スパンは認証・認可などの内部チェックを通過したリクエストに対してのみ生成される)

### 手順

#### ステップ 1: アプリケーションでトレースコンテキストを伝播する

ADK などのフレームワークを使用するか、`tools/call` リクエストの `_meta` フィールドに W3C Trace Context 形式の `traceparent` を設定します。サンプリングフラグは `1` (サンプリング有効) にする必要があります。

#### ステップ 2: Trace Explorer でスパンを確認する

Google Cloud コンソールの Trace Explorer を開き、フィルタバーで属性 `mcp.method.name` に値 `tools/call` を指定してスパンを検索します。スパン名は `tools/call NAME` (例: `tools/call list_streams`) の形式で表示されます。

## メリット

### ビジネス面

- **データパイプライン運用エージェントの信頼性向上**: エージェント経由の Datastream 操作 (ストリームの確認・実行など) を可観測にし、問題の切り分けと解決を迅速化できる
- **追加実装コストの削減**: サーバー側のスパン生成は MCP サーバー側の統合として提供されるため、サーバー側の計装を自前で行う必要がない

### 技術面

- **エンドツーエンドのトレーサビリティ**: クライアント (エージェント) 側のスパンとサーバー側のスパンが W3C Trace Context で結合され、呼び出しシーケンス全体のレイテンシを分析できる
- **標準準拠**: スパン命名やトレースコンテキストの伝播は OpenTelemetry Semantic Conventions for MCP と W3C Trace Context に準拠しており、特定ベンダーにロックインされない

## デメリット・制約事項

### 制限事項

- トレースコンテキストは W3C Trace Context 標準に従う必要があり、サンプリングフラグを `1` に設定しなければならない
- リモート Google Cloud MCP サーバーが生成するのは `tools/call` オペレーションに対する単一のスパンのみで、その他のオペレーションのスパンや `tools/call` の子スパンは生成されない
- スパンは、リクエストが認証・認可などの内部チェックを通過した場合にのみ生成される

### 考慮すべき点

- 生成されたスパンは Cloud Trace のスパン取り込みとして課金対象になるため、無料枠 (月 250 万スパン) を超える利用がある場合はサンプリングレートの調整を検討する
- `run_stream` や `delete_stream` は長時間実行オペレーションを返すため、エージェントが `get_operation` をポーリングする設計では `tools/call` スパンが複数生成される点に留意する
- セルフホストの MCP サーバーは対象外のため、OpenTelemetry による計装を自前で行う必要がある (Python の場合は `tools/call` のスパン生成に対応した計装手順が提供されている)

## ユースケース

### ユースケース 1: CDC ストリーム運用エージェントの可観測化

**シナリオ**: データ基盤の運用支援エージェントが Datastream MCP サーバーの `list_streams` / `get_stream` を呼び出してストリームの状態を診断し、必要に応じて `run_stream` で再実行している。応答が遅い・失敗するケースの原因を特定したい。

**効果**: `tools/call` スパンによりツール呼び出しのステータスとレイテンシがトレース上で可視化され、遅延がエージェント側 (モデル推論) と MCP サーバー側のどちらで発生しているかを切り分けられる。

### ユースケース 2: 長時間実行オペレーションのポーリング挙動の分析

**シナリオ**: エージェントが `run_stream` の実行後に `get_operation` で完了をポーリングするワークフローを構築しており、ポーリングの回数や間隔が適切かを確認したい。

**効果**: Trace Explorer で `mcp.method.name = tools/call` のフィルタを使い、`tools/call get_operation` スパンの回数・間隔・レイテンシをトレース単位で分析し、過剰なポーリングを検出できる。

## 料金

MCP サーバーが生成するスパンは Cloud Trace のスパン取り込みとして課金されます。

| 項目 | 料金 | 無料枠 (月あたり) |
|--------|-----------------|-----------------|
| Trace スパン取り込み | $0.20 / 100 万スパン | 最初の 250 万スパン |

詳細は [Google Cloud Observability の料金ページ](https://cloud.google.com/products/observability/pricing) を参照してください。

## 関連サービス・機能

- **Datastream**: サーバーレスの CDC / レプリケーションサービス。今回そのリモート MCP サーバーがスパン生成に対応した
- **Cloud Trace / Trace Explorer**: スパンの保存・分析基盤。`mcp.method.name` 属性でのフィルタリングにより MCP スパンを検索できる
- **Agent Development Kit (ADK)**: トレースコンテキストの伝播に対応したエージェント開発フレームワーク。OpenTelemetry による計装手順が提供されている
- **Cloud Monitoring**: 「Monthly trace spans ingested」指標を使ったスパン取り込み量のアラート設定により、コストを監視できる
- **Policy Troubleshooter / Managed Service for Apache Airflow**: 直前の 2026-08-24 に同機能へ対応したプロダクト。対応プロダクトは段階的に拡大している

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260827-cloud-trace-datastream-mcp-spans.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#August_27_2026)
- [ドキュメント: View calls made to remote MCP servers](https://docs.cloud.google.com/trace/docs/trace-remote-mcp-server-calls)
- [Datastream MCP リファレンス](https://docs.cloud.google.com/datastream/docs/reference/mcp)
- [Find and explore traces](https://docs.cloud.google.com/trace/docs/finding-traces)
- [Instrument a self-hosted MCP server with OpenTelemetry](https://docs.cloud.google.com/stackdriver/docs/instrumentation/self-hosted-mcp-servers)
- [料金ページ](https://cloud.google.com/products/observability/pricing)
- [関連レポート: Policy Troubleshooter / Managed Airflow の MCP スパン対応 (2026-08-24)](./2026-08-24-cloud-trace-remote-mcp-server-spans.md)

## まとめ

Datastream のリモート MCP サーバーが `tools/call` のトレーススパンを自動生成するようになり、AI エージェントから CDC / レプリケーションパイプラインを操作するワークフローの可観測性が向上しました。Datastream MCP サーバーを利用するエージェントを運用している場合は、ADK などトレースコンテキスト伝播に対応したフレームワークを採用し、Trace Explorer の `mcp.method.name` フィルタでツール呼び出しの挙動を確認することを推奨します。

---

**タグ**: #CloudTrace #MCP #ModelContextProtocol #Datastream #CDC #Observability #AIAgent #OpenTelemetry
