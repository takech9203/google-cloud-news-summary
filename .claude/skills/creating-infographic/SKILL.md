---
name: creating-infographic
description: グラフィックレコーディング風の HTML インフォグラフィックを生成するスキル。手書き風のビジュアル要素、日本語フォント、カラフルな配色を使用して、テキストコンテンツを視覚的に魅力的なインフォグラフィックに変換します。ユーザーが「グラフィックレコーディング」「インフォグラフィック作成」「視覚化」「ビジュアル化」「手書き風デザイン」などと言った場合、または記事やテキストを視覚的に表現したい場合に使用します。
---

# グラフィックレコーディング風インフォグラフィック変換

## 目的

テキストコンテンツを、超一流デザイナーが作成したような日本語グラフィックレコーディング風 HTML インフォグラフィックに変換します。情報設計とビジュアルデザインの両面で最高水準を目指し、手書き風の図形やアイコンを活用して内容を視覚的に表現します。

## テーマ一覧

ユーザーの要望に応じて、以下のテーマから選択してください。指定がない場合は「デフォルト」テーマを使用します。

| テーマ | ファイル | 説明 | 適用キーワード |
|--------|----------|------|----------------|
| デフォルト | #[[file:themes/default.md]] | グラフィックレコーディング風 3 カラム | 「グラレコ」「手書き風」「カラフル」「ポップ」または指定なし |
| デフォルト (シンプル) | #[[file:themes/default-simple.md]] | グラフィックレコーディング風 1 カラム | 「1 カラム」「シンプル」「読みやすい」「モバイル対応」 |
| Google Cloud ライト | #[[file:themes/google-cloud-light.md]] | Google Cloud プレゼンテーション風ライトテーマ | 「Google Cloud」「ライト」「白背景」「ドキュメント」「印刷」 |
| Google Cloud News | #[[file:themes/google-cloud-news.md]] | Google Cloud ニュースレポート専用テーマ | 「Google Cloud ニュース」「レポート」「アップデート」 |

各テーマファイルには、カラーパレット、CSS テンプレート、HTML テンプレート例が含まれています。テーマを適用する際は、該当ファイルを参照してください。

## グラフィックレコーディング表現技法

インフォグラフィック生成時に適用する表現技法です。

- テキストと視覚要素のバランスを重視
- キーワードを囲み線や色で強調
- 簡易的なアイコンや図形で概念を視覚化
- 数値データは簡潔なグラフや図表で表現
- 接続線や矢印で情報間の関係性を明示
- 余白を効果的に活用して視認性を確保
- 絵文字やアイコンを効果的に配置 (✏️📌📝🔍📊など)

## アーキテクチャ図・シーケンス図の活用

インフォグラフィックには、可能な限りアーキテクチャ図やシーケンス図などのビジュアルを含めること。これにより、複雑な概念やシステム構成の理解が促進されます。

### 図を含めるべきケース

以下のようなコンテンツでは、積極的に図を作成すること。

- **システムアーキテクチャ**: Google Cloud サービス間の連携、データフロー、ネットワーク構成
- **処理フロー**: リクエスト/レスポンスの流れ、イベント駆動処理、ワークフロー
- **Before/After 比較**: アップデート前後の構成変更、改善点の視覚化
- **コンポーネント関係**: サービス間の依存関係、レプリケーション構成
- **シーケンス**: API 呼び出し順序、認証フロー、マルチステップ処理

### ソースに Mermaid 図がある場合

**必須**: ソース (レポート、記事など) に Mermaid 図 (` ```mermaid ` ブロック) が含まれている場合は、**必ず** Mermaid.js で HTML に埋め込むこと。HTML/CSS で独自に図を再作成してはならない。

**手順:**
1. ソースから Mermaid コードブロックをそのままコピー
2. `<pre class="mermaid">` タグ内に配置
3. Mermaid.js を読み込み、初期化設定を適用

さらに、内容の理解を深めるために有用であれば、追加の図 (シーケンス図、Before/After 比較など) を作成して補完する。

### 図の実装方法の選択

図の複雑さに応じて、適切な実装方法を選択すること。

| 複雑さ | 実装方法 | 適用ケース |
|--------|----------|------------|
| シンプル | HTML/CSS | 3〜4 ステップの線形フロー、単純な Before/After、単方向の関係 |
| 複雑 | Mermaid | 下記「Mermaid を使用すべきケース」に該当する場合 |

### Mermaid を使用すべきケース

以下の条件に 1 つでも該当する場合は、Mermaid を使用すること。

**構造的な複雑さ**

- **コンポーネント数**: 5 つ以上のコンポーネントを含む構成
- **階層構造**: サブグラフやグループ化が必要な構成 (リージョン、プロジェクト、VPC など)
- **双方向の関係**: 相互通信、レプリケーション、同期処理

**フローの複雑さ**

- **分岐処理**: 条件分岐、エラーハンドリング、複数パスのフロー
- **並列処理**: 同時実行、ファンアウト/ファンイン、非同期処理
- **ループ/再帰**: 繰り返し処理、リトライロジック

**図の種類**

- **シーケンス図**: API 呼び出し順序、認証フロー、リクエスト/レスポンスの流れ、マルチステップ処理
- **状態遷移図**: ライフサイクル管理、ステートマシン
- **ER 図**: データモデル、エンティティ間の関係

**ドメイン固有の複雑さ**

- **マルチリージョン構成**: 複数リージョン間のレプリケーション、フェイルオーバー
- **マルチプロジェクト構成**: クロスプロジェクトアクセス、組織構造
- **ネットワーク構成**: VPC ピアリング、Shared VPC、複数サブネット

### HTML/CSS で十分なケース

以下の条件をすべて満たす場合は、HTML/CSS で実装すること。

- コンポーネント数が 4 つ以下
- 単方向の線形フロー (A → B → C → D)
- 分岐や並列処理がない
- サブグラフやグループ化が不要

### Mermaid の実装方法

Mermaid 図のスタイルガイドラインは `#[[file:../../../CLAUDE.md]]` の「Architecture Diagram Guidelines」セクションを参照すること。

**重要な参照ポイント:**

- **Mermaid (Default)**: 基本的な構文、レイアウト、接続線のルール
- **Template**: flowchart のテンプレートと classDef の定義
- **Color Palette**: 色の意味と使用ケース
- **Shape Semantics**: 形状の使い分け
- **Diagram Type Selection**: 図の種類の選択基準
- **Sequence Diagram**: シーケンス図のテンプレート
- **Mermaid Diagram Styling Restrictions**: スタイリングの制限事項
- **Mermaid Sequence Diagram Special Character Restrictions**: 特殊文字の制限
- **Mermaid Flowchart Special Character Restrictions**: フローチャートの特殊文字制限

**HTML への埋め込み方法:**

**重要**: Mermaid 図の背景は必ず白にすること。`theme: 'dark'` は使用禁止。

```html
<!-- Mermaid.js の読み込み (head または body 末尾) -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
    mermaid.initialize({
        startOnLoad: true,
        theme: 'base',
        themeVariables: {
            primaryColor: '#4285F4',
            primaryTextColor: '#202124',
            primaryBorderColor: '#4285F4',
            lineColor: '#4285F4',
            secondaryColor: '#F1F3F4',
            tertiaryColor: '#FAFAFA',
            background: '#FFFFFF',
            mainBkg: '#E8F0FE',
            nodeBorder: '#4285F4',
            clusterBkg: '#E8F0FE',
            clusterBorder: '#4285F4',
            edgeLabelBackground: '#FFFFFF',
            textColor: '#202124'
        }
    });
</script>

<!-- Mermaid 図の定義 -->
<div class="mermaid-container">
    <pre class="mermaid">
    <!-- CLAUDE.md のテンプレートを参照して図を作成 -->
    </pre>
</div>
```

### Mermaid コンテナのスタイリング

```css
.mermaid-container {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 24px;
    margin: 20px 0;
    border: 2px solid rgba(66, 133, 244, 0.3);
    overflow-x: auto;
}
.mermaid {
    display: flex;
    justify-content: center;
}
```

### シンプルな図: HTML/CSS での実装

3〜5 ステップの線形フローなど、シンプルな図は HTML/CSS で実装すること。

```html
<!-- フローダイアグラム例 -->
<div class="flow-diagram">
    <div class="flow-step">📱 ユーザー<br/>リクエスト</div>
    <span class="flow-arrow">→</span>
    <div class="flow-step">🔐 認証<br/>処理</div>
    <span class="flow-arrow">→</span>
    <div class="flow-step">⚡ Cloud Run<br/>実行</div>
    <span class="flow-arrow">→</span>
    <div class="flow-step">🗄️ データ<br/>保存</div>
</div>

<!-- アーキテクチャ図例 (グリッドレイアウト) -->
<div class="architecture-grid">
    <div class="arch-component primary">🌐 Cloud CDN</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-component">🔌 Cloud Load Balancing</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-component">⚡ Cloud Run</div>
    <div class="arch-arrow-group">
        <span>↙</span><span>↘</span>
    </div>
    <div class="arch-row">
        <div class="arch-component storage">🗄️ Cloud SQL</div>
        <div class="arch-component storage">🪣 Cloud Storage</div>
    </div>
</div>
```

### HTML/CSS 図のスタイリング

```css
.flow-diagram {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin: 24px 0;
}
.flow-step {
    background: var(--gc-surface-container-low);
    border: 2px solid var(--gc-blue-600);
    border-radius: 8px;
    padding: 12px 20px;
    text-align: center;
    min-width: 100px;
}
.flow-arrow {
    color: var(--gc-blue-600);
    font-size: 24px;
    font-weight: bold;
}
.architecture-grid {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    margin: 24px 0;
}
.arch-component {
    background: rgba(66, 133, 244, 0.15);
    border: 2px solid var(--gc-blue-600);
    border-radius: 8px;
    padding: 12px 24px;
    text-align: center;
}
.arch-row {
    display: flex;
    gap: 24px;
}
```

## コードサンプルの活用

技術的なコンテンツでは、実装例やコードサンプルを含めることを推奨します。

### コードサンプルを含めるべきケース

- **API の使用方法**: SDK の呼び出し例、リクエスト/レスポンス形式
- **設定例**: Terraform、gcloud CLI コマンド、Cloud Deploy 設定
- **実装パターン**: Cloud Run サービス、Cloud Functions ハンドラー、イベント処理、エラーハンドリング
- **JSON/YAML 構造**: ポリシー定義、設定ファイル、イベントペイロード

### コードブロックのスタイリング (highlight.js シンタックスハイライト)

コードブロックには highlight.js を使用してシンタックスハイライトを適用すること。これは全テーマ共通のルールである。

**highlight.js の読み込み (head または body 末尾に追加):**

```html
<!-- highlight.js の読み込み (ダーク背景用テーマ) -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/vs2015.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
```

**注意**: コードブロックはダーク背景 (`#1E1E1E`) で統一するため、highlight.js テーマは `vs2015` を使用すること。`atom-one-light` などのライト系テーマは使用しない。

**コードブロックの HTML 構造:**

```html
<div class="code-block">
    <div class="code-header">
        <span class="code-lang">Python</span>
        <span class="code-title">Cloud Functions ハンドラー例</span>
    </div>
    <pre><code class="language-python">import functions_framework

@functions_framework.http
def handle_request(request):
    # リクエスト処理
    return json.dumps({'message': 'Success'}), 200</code></pre>
</div>
```

**重要**: `<code>` タグには必ず `class="language-xxx"` を指定すること (例: `language-python`, `language-json`, `language-yaml`, `language-bash`, `language-javascript`, `language-typescript`, `language-html`, `language-css`, `language-hcl`)。これにより highlight.js が正しく言語を認識してハイライトする。

```css
.code-block {
    background: #1E1E1E;
    border-radius: 8px;
    overflow: hidden;
    margin: 16px 0;
}
.code-header {
    background: #2D2D2D;
    padding: 8px 16px;
    display: flex;
    justify-content: space-between;
    font-size: 12px;
}
.code-lang {
    color: #9CDCFE;
    font-weight: bold;
}
.code-title {
    color: #AAAAAA;
}
.code-block pre {
    margin: 0;
    padding: 0;
    overflow-x: auto;
}
.code-block code {
    font-family: 'Roboto Mono', 'Source Code Pro', 'Courier New', monospace;
    font-size: 15px;
    line-height: 1.6;
    padding: 16px !important;
}
```

**重要: `pre` タグと Mermaid 図の競合を防ぐ**

コードブロック用に `pre` タグにダーク背景を指定する場合、必ず `pre:not(.mermaid)` を使用すること。Mermaid 図は `<pre class="mermaid">` で定義されるため、`pre` に直接スタイルを指定すると Mermaid 図も黒背景になってしまう。

```css
/* ✅ 正しい: Mermaid の pre を除外 */
.code-block,
pre:not(.mermaid) {
    background: #1E1E1E;
    /* ... */
}

/* ❌ 間違い: Mermaid 図も黒背景になる */
.code-block,
pre {
    background: #1E1E1E;
    /* ... */
}
```

### コードサンプルのベストプラクティス

- **簡潔に**: 核心部分のみを抽出し、冗長なコードは省略
- **コメント付き**: 重要な行にはコメントを追加
- **実行可能**: そのままコピーして使用できる形式を心がける
- **言語明示**: コードブロックには言語を明示

## 全体的な指針

生成時に守るべき指針です。

- 読み手が自然に視線を移動できる配置
- 情報の階層と関連性を視覚的に明確化
- 手書き風の要素で親しみやすさを演出
- 視覚的な記憶に残るデザイン
- フッターに出典情報を明記
- 生成した HTML は単一ファイルで完結し、外部依存なしでブラウザで開けるようにすること (ただし Mermaid.js と highlight.js の CDN 読み込みは許可)

### ストーリー構成

コンテンツは自然な流れで構成すること。

1. **導入**: 何についての話か、なぜ重要かを簡潔に
2. **本題**: 核心となる情報を論理的な順序で展開
3. **まとめ**: 要点の整理、次のアクションや展望

情報の順序は「背景 → 課題 → 解決策 → 効果」や「What → Why → How」など、読み手が理解しやすい流れを選択すること。

### マルチカラムレイアウトの調整

3 カラム構成でコンテンツを配置する際は、以下の原則に従うこと。

**基本原則: 構成・流れを最優先**

- カラム間の配置バランスではなく、コンテンツの構成・流れを重視する
- 配置のバランスを取るために、コンテンツの順序を変更してはならない
- 読み手が自然に情報を追える論理的な流れを維持すること

**カラムバランスの調整方法**

カラム間の長さに偏りがある場合は、以下の手順で調整する。

1. **左カラムが長い場合**: 左カラムの最後のセクションを、中央カラムの最初に移動
2. **中央カラムが溢れた場合**: 中央カラムの最後のセクションを、右カラムの最初に移動
3. **右カラムが溢れた場合**: 同様に次のカラムへシフト

```
調整前:
左カラム: [A] [B] [C] [D] [E]  ← 長い
中央カラム: [F] [G]
右カラム: [H]

調整後:
左カラム: [A] [B] [C] [D]
中央カラム: [E] [F] [G]  ← E を移動
右カラム: [H]
```

**禁止事項**

- 視覚的なバランスのためだけにセクションの順序を入れ替えない
- 関連するセクション群を分断しない (例: 「概念説明」→「具体例」の流れを崩さない)
- 空白を埋めるために無関係なセクションを移動しない

### コードブロックの表示

YAML やコードブロックを表示する際は、必ず `<code>` タグに `class="language-xxx"` を指定して highlight.js によるシンタックスハイライトを適用すること。YAML フロントマター (`---` で囲まれた部分) を HTML 内に表示する場合も同様。

```html
<div class="code-block">
    <div class="code-header">
        <span class="code-lang">YAML</span>
    </div>
    <pre><code class="language-yaml">---
name: your-skill-name
description: Brief description
---</code></pre>
</div>
```

## 出典 URL の表示

元記事や参照元の URL がある場合は、必ず HTML 内に出典として含めること。

- フッター部分に「出典」または「Source」セクションを設ける
- クリック可能なリンクとして表示
- URL が長い場合は `word-break: break-all` を適用して折り返し表示
- 複数の出典がある場合はリスト形式で表示
- 出典がない場合は「出典: ユーザー提供コンテンツ」と記載

```html
<footer style="margin-top: 24px; padding-top: 16px; border-top: 1px dashed #ccc; font-size: 12px; color: #666;">
  <p>📎 出典: <a href="https://example.com/original-article" target="_blank" rel="noopener noreferrer" style="color: #1e40af; text-decoration: underline;">https://example.com/original-article</a></p>
</footer>
```

## ソースコンテンツの完全性

**重要**: インフォグラフィックは、ソース (レポート、記事など) の内容を視覚的に表現したものである。ソースの情報を省略せず、全ての内容を含めること。

### 必須ルール

1. **ソースの全セクションを含める**: ソースに含まれるセクションは、原則として全てインフォグラフィックに含める
2. **情報を省略しない**: 視覚的なバランスのために情報を削除してはならない
3. **Mermaid 図はそのまま使用**: ソースに Mermaid 図がある場合は、HTML/CSS で再作成せず、Mermaid.js でそのまま埋め込む

### ソースに含まれる場合に必須で含めるセクション

以下のセクションがソースに含まれている場合は、必ずインフォグラフィックにも含めること。

| セクション | 説明 |
|------------|------|
| 概要 | Before/After 比較、課題と解決策 |
| アーキテクチャ図 | Mermaid 図、シーケンス図、フロー図 |
| 主要機能 | 機能一覧、特徴 |
| 技術仕様・技術詳細 | API 変更、パラメータ、制限事項 |
| 設定方法・コードサンプル | CLI コマンド、SDK 例、設定ファイル |
| メリット・デメリット | 利点、制約事項、考慮点 |
| ユースケース | 具体的な使用例、シナリオ |
| 料金情報 | 料金体系、料金例 |
| 利用可能リージョン | 対応リージョン一覧 |
| 参考リンク | 公式ドキュメント、関連記事 |

### 禁止事項

- ソースに含まれる Mermaid 図を HTML/CSS で独自に再作成すること
- 視覚的なバランスのためにセクションを省略すること
- ソースの情報を要約しすぎて重要な詳細を失うこと

## 使用方法

### ファイル名規則

生成する HTML ファイルには、必ず日付をプレフィックスとして付与すること。

- **形式**: `YYYYMMDD-<descriptive-name>.html`
- **例**: `20260108-google-cloud-architecture-overview.html`, `20260108-meeting-summary.html`
- 日付は生成日を使用
- ファイル名の説明部分は英語の小文字とハイフンを使用
- 内容を端的に表す名前を付ける
### 入力形式

以下の形式での入力に対応すること。

1. **テキスト直接入力**: ユーザーが文章をそのまま貼り付けた場合
2. **URL 入力**: ユーザーが記事の URL を提供した場合
   - Web フェッチツールを使用して記事内容を取得
   - 取得した URL は必ず出典として HTML に含める

### URL 入力時の処理フロー

```
1. URL を受け取る
2. Web フェッチツールで記事内容を取得
3. 記事内容をインフォグラフィックに変換
4. 元の URL を出典としてフッターに表示
```
