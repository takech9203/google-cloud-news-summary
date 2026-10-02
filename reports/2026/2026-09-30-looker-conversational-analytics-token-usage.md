# Looker: Conversational Analytics System Activity の Token usage 可観測性メトリクス強化

**リリース日**: 2026-09-30

**サービス**: Looker

**機能**: Conversational Analytics System Activity ダッシュボードのトークン使用量可観測性メトリクス強化

**ステータス**: GA (Looker (original) 26.16 以降) / Preview (Looker (Google Cloud core))

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260930-looker-conversational-analytics-token-usage.html)

## 概要

Looker の Conversational Analytics System Activity ダッシュボードの **Token usage タブ** で、ユーザーエンゲージメントと推定トークン使用量データを含む可観測性メトリクスが強化され、**Looker 26.16 以降の Looker (original) インスタンスで一般提供 (GA)** となった。今回のリリースでは、新たに **Daily Token Utilization (日次トークン使用率) の可視化** が追加されたほか、**Gemini Enterprise に公開された Conversational Analytics データエージェントのトークン使用量の可観測性** にも対応した。

Conversational Analytics の使用量は「データトークン」(LLM が処理するテキストとデータの基本単位) で測定される。質問文、会話履歴、メタデータやエージェント指示などのコンテキストが入力データトークンとして、自然言語の回答、生成された API 呼び出しや SQL クエリ、可視化などが出力データトークンとして計測される。Looker 管理者は System Activity からインスタンス全体のトークン消費を把握し、コスト管理やガバナンスに活用できる。

なお、**Looker (Google Cloud core) インスタンスでは、「Conversational Analytics Agent Token usage」Preview 機能を有効化した場合に利用でき、トークン使用量の可観測性は引き続き Preview** である。

**アップデート前の課題**

- トークン使用量の可観測性は Preview 機能であり、Looker (original) インスタンスでも GA としての利用はできなかった
- 日次のトークン使用率 (Daily Token Utilization) を示す可視化がなく、使用率の推移を直接確認できなかった
- Conversational Analytics ダッシュボードは Gemini Enterprise 上で行われた会話の可観測性を提供しておらず、Gemini Enterprise に公開したデータエージェントのトークン消費を把握できなかった

**アップデート後の改善**

- Looker 26.16 以降の Looker (original) インスタンスで、ユーザーエンゲージメントと推定トークン使用量を含む強化された可観測性メトリクスが GA となった
- Daily Token Utilization の可視化が追加され、日次の推定トークン使用率の推移を確認できるようになった
- Gemini Enterprise に公開された Conversational Analytics データエージェントのトークン使用量も観測対象となり、Top Agents by Token Usage の Conversation Surface に「Gemini Enterprise」が表示されるようになった (Looker (original) インスタンスのみ)

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph Surfaces["会話サーフェス"]
        U([👤 ユーザー]) --> CA["💬 Conversational Analytics<br>(Explore / API / Embed)"]
        U --> DA["📊 Dashboard Agents<br>(通常 / Embed)"]
        U --> GE["🤖 Gemini Enterprise<br>(公開済みデータエージェント)"]
    end
    CA --> TK["🪙 データトークン計測<br>(入力 / 出力)"]
    DA --> TK
    GE --> TK
    TK -->|同期 (レイテンシ約 6 時間)| SA["📈 System Activity<br>Conversational Analytics ダッシュボード"]
    SA --> TAB["🗂️ Token usage タブ<br>Daily Token Utilization など"]
    TAB --> ADM([🛡️ Looker 管理者])
```

各会話サーフェス (Explore、ダッシュボードエージェント、Gemini Enterprise に公開されたエージェントなど) でのやり取りがデータトークンとして計測され、System Activity の Token usage タブで管理者が確認できる。

## サービスアップデートの詳細

### 主要機能

1. **強化された可観測性メトリクスの GA (Looker (original))**
   - ユーザーエンゲージメントと推定トークン使用量データを含む可観測性メトリクスが、Looker 26.16 以降の Looker (original) インスタンスで一般提供 (GA) になった
   - Looker (Google Cloud core) インスタンスでは「Conversational Analytics Agent Token usage」Preview 機能を有効化した場合に利用可能で、引き続き Preview 扱い

2. **Daily Token Utilization の可視化を追加**
   - 日次の推定トークン使用率の推移を示す可視化が Token usage タブに追加された
   - 既存の Daily Estimated Token Usage (日次の入力・出力トークンの推定使用量) と併せて、使用傾向をより詳細に把握できる

3. **Gemini Enterprise に公開されたデータエージェントのトークン可観測性**
   - Gemini Enterprise に公開された Conversational Analytics データエージェントのトークン使用量が観測対象になった
   - Top Agents by Token Usage の Conversation Surface 列に「Gemini Enterprise」が表示される (Looker (original) インスタンスのみ)

### Token usage タブで確認できるデータ

| メトリクス | 内容 |
|------|------|
| Total Estimated Input Tokens | Conversational Analytics で使用されたと推定される入力データトークンの合計 |
| Total Estimated Output Tokens | 推定される出力データトークンの合計 |
| Daily Estimated Token Usage | 日次の入力・出力トークンの推定使用量の推移 |
| Daily Token Utilization | 日次の推定トークン使用率の推移 (今回追加) |
| Top Agents by Token Usage | エージェントごとの入力・出力トークン量。Conversation Surface 列でエージェント種別を表示 |
| Top Users by Token Usage | トークン使用量の多いユーザーの一覧 |
| Top Conversations by Token Usage | トークン使用量の多い会話の一覧 |

### Conversation Surface (会話サーフェス) の種類

| サーフェス | 説明 |
|------|------|
| Conversational Analytics | 1 つ以上の Looker Explore にクエリするデータエージェント |
| Conversational Analytics API | Looker API の ConversationalAnalytics メソッドで作成されたデータエージェント |
| Conversational Analytics Embed | 埋め込まれた Looker Explore にクエリするデータエージェント |
| Dashboard Agents | Looker ダッシュボードにクエリするデータエージェント |
| Dashboard Agents Embed | 埋め込まれた Looker ダッシュボードにクエリするデータエージェント |
| Explore Insight Assistant | Insight Assistant エージェント |
| Gemini Enterprise | Gemini Enterprise に公開されたデータエージェント (Looker (original) インスタンスのみ表示) |

## 技術仕様

### データトークンの計測対象

| 種別 | 含まれる内容 |
|------|------|
| 入力データトークン | チャットに入力された質問、セッションの会話履歴、メタデータやエージェント指示などのデータコンテキスト |
| 出力データトークン | 質問への自然言語の回答、データ取得のために生成された API 呼び出しや SQL クエリ、モデルが生成したその他のテキスト、モデルが作成した可視化 |

### フィルタリング

Token usage タブでは、以下の属性によるページレベルフィルタが利用できる。

- Created Date (作成日)
- Agent ID (エージェント ID)
- Conversation Surface (会話サーフェス)
- User ID (ユーザー ID)
- Conversation ID (会話 ID)

## 設定方法

### 前提条件

1. Looker (original) インスタンスの場合: Looker 26.16 以降であること (GA として利用可能)
2. Looker (Google Cloud core) インスタンスの場合: Looker 管理者が Admin パネルの Preview 機能「Conversational Analytics Agent Token usage」を有効化すること (デフォルトでは無効。有効化後も Preview 扱い)
3. System Activity ダッシュボードへのアクセス権限があること

### 手順

#### ステップ 1: (Looker (Google Cloud core) のみ) Preview 機能の有効化

Looker 管理者が Admin パネルの Preview Features ページで「Conversational Analytics Agent Token usage」を有効にする。有効化すると、Conversational Analytics System Activity ダッシュボードでエンゲージメントとトークン使用量データを含む強化された可観測性メトリクスが利用可能になる。

#### ステップ 2: Token usage タブの確認

Admin パネルの System Activity セクションから Conversational Analytics ダッシュボードを開き、Token usage タブで推定トークン使用量、Daily Token Utilization、Top Agents / Users / Conversations by Token Usage などを確認する。必要に応じて Created Date、Agent ID、Conversation Surface などのフィルタで絞り込む。

## メリット

### ビジネス面

- **コストの透明性向上**: Conversational Analytics の料金はトークン使用量に基づくため、推定トークン使用量と日次使用率を可視化することで、コストの把握と予測がしやすくなる
- **AI 活用のガバナンス強化**: どのエージェント・ユーザー・会話がトークンを多く消費しているかを特定でき、利用ポリシーの整備や最適化に役立つ

### 技術面

- **GA による本番利用の安心感**: Looker (original) インスタンスでは GA となり、本番運用での利用に適したサポートレベルで可観測性メトリクスを活用できる
- **Gemini Enterprise まで含めた一元監視**: Looker 内の会話に加え、Gemini Enterprise に公開したデータエージェントのトークン使用量も同じダッシュボードで観測できる
- **多角的な分析**: Conversation Surface、Agent ID、User ID などのフィルタにより、サーフェス別・エージェント別・ユーザー別の詳細な分析が可能

## デメリット・制約事項

### 制限事項

- Looker (Google Cloud core) インスタンスでは、トークン使用量の可観測性は引き続き Preview であり、「Conversational Analytics Agent Token usage」Preview 機能の有効化が必要 (デフォルトは無効)
- GA は Looker 26.16 以降の Looker (original) インスタンスが対象
- トークン使用量データの同期には約 6 時間のレイテンシがある
- 会話サーフェスのタグ付けは Looker 26.14 でタグ付け機能が有効化されて以降の使用分に適用され、過去の使用分には遡及されない (Looker 26.12 や、機能有効化前の 26.14 での使用分にはサーフェスのタグが付かない)
- 会話サーフェスと関連する会話は、実際の会話が完了した後にダッシュボードに表示される

### 考慮すべき点

- 表示されるトークン数は「推定値 (Estimated)」である
- Top Users / Top Conversations にはユーザー単位の使用状況が表示されるため、社内での利用目的・運用ルールを整理しておくとよい

## ユースケース

### ユースケース 1: Conversational Analytics のコスト監視と予算管理

**シナリオ**: 全社で Conversational Analytics の利用を拡大しているが、トークンベースの課金のため消費量を継続的に監視したい。

**効果**: Token usage タブの Total Estimated Input/Output Tokens と Daily Token Utilization により、日次のトークン消費傾向を把握し、想定を超える使用の早期検知や予算計画に活用できる。

### ユースケース 2: Gemini Enterprise 公開エージェントの利用状況把握

**シナリオ**: Looker の Explore データエージェントを Gemini Enterprise に公開し、BI ツール外からも自然言語でデータに質問できるようにしている。公開後の利用実態を把握したい。

**効果**: Top Agents by Token Usage の Conversation Surface で「Gemini Enterprise」として区別して表示されるため、Looker 内の会話と Gemini Enterprise 経由の会話のトークン消費を切り分けて分析できる。

## 料金

Conversational Analytics のトークン使用量に基づく料金の詳細は、Looker の料金ページを参照。

- [Looker 料金ページ](https://cloud.google.com/looker/pricing)

## 関連サービス・機能

- **Conversational Analytics (Gemini in Looker)**: 自然言語で Looker Explore やダッシュボードにクエリできる機能。本アップデートの可観測性の対象
- **Gemini Enterprise**: Looker のデータエージェントを公開できる基盤。公開されたエージェントのトークン使用量が今回新たに観測対象になった
- **Looker System Activity**: インスタンスの利用状況を可視化する管理者向けダッシュボード群。Conversational Analytics ダッシュボードもここに含まれる
- **End User Conversational Analytics (CA) Query Review (Preview)**: ユーザーの同意に基づき Conversational Analytics のクエリと評価を Responses & feedback タブで確認できる別の Preview 機能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260930-looker-conversational-analytics-token-usage.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#September_30_2026)
- [System Activity ダッシュボード: Conversational Analytics token usage](https://cloud.google.com/looker/docs/system-activity-dashboards#ca-sa-token-usage)
- [Admin パネル Preview 機能: Conversational Analytics Agent Token usage](https://cloud.google.com/looker/docs/admin-panel-general-preview-features#ca-agent-token-usage)
- [データエージェントの Gemini Enterprise への公開](https://cloud.google.com/looker/docs/conversational-analytics-looker-data-agents#publish-data-agents)
- [Conversational Analytics の概要](https://cloud.google.com/looker/docs/conversational-analytics-overview)
- [料金ページ](https://cloud.google.com/looker/pricing)

## まとめ

Looker の Conversational Analytics に対するトークン使用量の可観測性が Looker (original) インスタンスで GA となり、Daily Token Utilization の可視化や Gemini Enterprise 公開エージェントの観測にも対応した。トークンベースの課金を採用する Conversational Analytics のコスト管理・ガバナンスに直結する機能強化であり、Looker (original) 利用者は 26.16 以降へのアップデートを、Looker (Google Cloud core) 利用者は Preview 機能の有効化を検討するとよい。

---

**タグ**: Looker, Conversational Analytics, System Activity, Token Usage, 可観測性, Gemini Enterprise, GA, Preview, BI, 生成 AI
