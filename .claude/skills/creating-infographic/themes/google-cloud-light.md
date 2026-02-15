# Google Cloud ライトテーマ (プレゼンテーション風)

Google Cloud 公式サイト (cloud.google.com) のデザインに準拠したライトテーマ。白背景を基調とし、Google Blue をアクセントカラーとして使用。ドキュメント、ホワイトペーパー、印刷物に最適な 1 カラム構成 (最大幅 1000px) です。

## カラーパレット

Google Cloud 公式ブランドカラーと Material Design 3 のサーフェスカラーに基づいたライトテーマのカラーパレットです。

```xml
<palette name="google-cloud-light">
  <!-- Google Brand Primary Colors -->
  <color name='Google Blue' rgb='4285F4' r='66' g='133' b='244' description='ロゴ、ブランドアイデンティティ' />
  <color name='Google Red' rgb='EA4335' r='234' g='67' b='53' description='警告、エラー、Breaking Changes' />
  <color name='Google Yellow' rgb='FBBC04' r='251' g='188' b='4' description='注意、ハイライト' />
  <color name='Google Green' rgb='34A853' r='52' g='168' b='83' description='成功、GA ステータス、ポジティブ指標' />

  <!-- Google Cloud UI Blue Scale (cloud.google.com で実際に使用) -->
  <color name='Blue 900' rgb='174EA6' r='23' g='78' b='166' description='ダークブルー、ホバー状態のボタン' />
  <color name='Blue 800' rgb='185ABC' r='24' g='90' b='188' description='アクティブ状態' />
  <color name='Blue 700' rgb='1967D2' r='25' g='103' b='210' description='セカンダリボタン' />
  <color name='Blue 600' rgb='1A73E8' r='26' g='115' b='232' description='プライマリ UI カラー、リンク、CTA ボタン' />
  <color name='Blue 500' rgb='4285F4' r='66' g='133' b='244' description='ブランドブルー (ロゴ)' />
  <color name='Blue 300' rgb='669DF6' r='102' g='157' b='246' description='セカンダリアクセント' />
  <color name='Blue 200' rgb='8AB4F8' r='138' g='180' b='248' description='ライトアクセント' />
  <color name='Blue 100' rgb='AECBFA' r='174' g='203' b='250' description='薄いブルー背景' />
  <color name='Blue 50' rgb='E8F0FE' r='232' g='240' b='254' description='最も薄いブルー背景' />

  <!-- Text Colors (Material Design 3 準拠) -->
  <color name='On Surface' rgb='202124' r='32' g='33' b='36' description='メインテキスト、H1、H2' />
  <color name='On Surface Variant' rgb='5F6368' r='95' g='99' b='104' description='本文テキスト、説明文' />
  <color name='Outline' rgb='80868B' r='128' g='134' b='139' description='サブテキスト、プレースホルダー' />

  <!-- Surface Colors (Material Design 3 準拠) -->
  <color name='Surface' rgb='FFFFFF' r='255' g='255' b='255' description='メイン背景' />
  <color name='Surface Container Lowest' rgb='F8F9FA' r='248' g='249' b='250' description='最も薄いサーフェス' />
  <color name='Surface Container Low' rgb='F1F3F4' r='241' g='243' b='244' description='カード背景、セクション区切り' />
  <color name='Surface Container' rgb='E8EAED' r='232' g='234' b='237' description='ボーダー、区切り線' />
  <color name='Outline Variant' rgb='DADCE0' r='218' g='220' b='224' description='薄いボーダー' />

  <!-- Semantic Tint Backgrounds -->
  <color name='Blue Tint' rgb='E8F0FE' r='232' g='240' b='254' description='情報、ブルー系の薄い背景' />
  <color name='Green Tint' rgb='E6F4EA' r='230' g='244' b='234' description='成功、グリーン系の薄い背景' />
  <color name='Red Tint' rgb='FCE8E6' r='252' g='232' b='230' description='エラー、レッド系の薄い背景' />
  <color name='Yellow Tint' rgb='FEF7E0' r='254' g='247' b='224' description='警告、イエロー系の薄い背景' />
  <color name='Purple Tint' rgb='F3E8FD' r='243' g='232' b='253' description='AI/ML、パープル系の薄い背景' />
  <color name='Teal Tint' rgb='E0F7FA' r='224' g='247' b='250' description='ネットワーク、ティール系の薄い背景' />

  <!-- Google Cloud Service Category Colors -->
  <color name='Compute' rgb='4285F4' description='Compute Engine, GKE, Cloud Run' />
  <color name='Storage' rgb='669DF6' description='Cloud Storage, Filestore' />
  <color name='Database' rgb='F4B400' description='Cloud SQL, Spanner, Bigtable, Firestore' />
  <color name='Networking' rgb='00BCD4' description='VPC, Cloud CDN, Load Balancing' />
  <color name='AI/ML' rgb='A142F4' description='Vertex AI, Gemini, AutoML' />
  <color name='Security' rgb='EA4335' description='IAM, Security Command Center' />
  <color name='Analytics' rgb='34A853' description='BigQuery, Dataflow, Pub/Sub' />
  <color name='DevOps' rgb='FF6D00' description='Cloud Build, Artifact Registry' />
</palette>
```

## デザインガイドライン

### 1. カラースキーム

Google Cloud 公式サイトのカラー体系に準拠します。

- **背景**: 白 (#FFFFFF) をメイン背景に使用
- **プライマリ UI カラー**: Blue 600 (#1A73E8) をリンク、ボタン、アクセントに使用
- **ブランドカラー**: Google Blue (#4285F4) はロゴやブランド要素に使用
- **タイトル**: On Surface (#202124)
- **本文**: On Surface Variant (#5F6368)
- **カード**: Surface Container Low (#F1F3F4) 背景、角丸 12px、微細なシャドウ
- **ボーダー**: Outline Variant (#DADCE0)

### 2. ビジュアル表現

Google Cloud プレゼンテーション風の分かりやすいビジュアル要素を積極的に使用します。

#### アイコンと絵文字

- 絵文字やアイコンを効果的に配置 (☁️🔧⚙️🚀📊🔒✅❌⚡💡🎯など)
- 各セクションの見出しにはアイコンを必ず付ける
- 箇条書きの先頭にチェックマーク (✓) や矢印 (→) を使用

#### フロー図・プロセス図

ステップやプロセスは横並びのフロー図で表現します。

```html
<div class="flow-diagram">
  <div class="flow-step">💬 入力</div>
  <span class="flow-arrow">→</span>
  <div class="flow-step">⚙️ 処理</div>
  <span class="flow-arrow">→</span>
  <div class="flow-step">✅ 出力</div>
</div>
```

#### 強調表現

- キーワードの強調 (Blue 50 背景 + Blue 600 下線のマーカー効果)
- 重要な数値は大きなフォントで表示
- 引用や注意事項は囲み枠で区別

### 3. タイポグラフィ

テキスト階層を明確にします。

- **タイトル**: 36px, #202124, font-weight: 700
- **サブタイトル**: 16px, #80868B
- **セクション見出し**: 24px, #202124, font-weight: 600、Blue 600 のアンダーライン
- **本文**: 16px, #5F6368, line-height: 1.7
- **フォント**: Google Sans (代替: Noto Sans JP, Hiragino Kaku Gothic ProN, Hiragino Sans, Meiryo, sans-serif)

```html
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap');

body {
  font-family: 'Google Sans', 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
}
</style>
```

### 4. レイアウト

- **ヘッダー**: 左揃えタイトル＋右揃え日付/出典
- **1 カラム構成**: 中央配置、最大幅 1000px
- **カード型コンポーネント**: Surface Container Low 背景、角丸 12px、微細なシャドウ
- **セクション間の適切な余白と階層構造**
- **コンテンツの横幅は 100%**

## CSS テンプレート

```css
/* Google Cloud Light Theme Base Styles */
:root {
  /* Google Brand Colors */
  --gc-blue: #4285F4;
  --gc-red: #EA4335;
  --gc-yellow: #FBBC04;
  --gc-green: #34A853;

  /* Google Cloud UI Blue Scale */
  --gc-blue-900: #174EA6;
  --gc-blue-800: #185ABC;
  --gc-blue-700: #1967D2;
  --gc-blue-600: #1A73E8;
  --gc-blue-500: #4285F4;
  --gc-blue-300: #669DF6;
  --gc-blue-200: #8AB4F8;
  --gc-blue-100: #AECBFA;
  --gc-blue-50: #E8F0FE;

  /* Text Colors */
  --gc-on-surface: #202124;
  --gc-on-surface-variant: #5F6368;
  --gc-outline: #80868B;

  /* Surface Colors */
  --gc-surface: #FFFFFF;
  --gc-surface-container-lowest: #F8F9FA;
  --gc-surface-container-low: #F1F3F4;
  --gc-surface-container: #E8EAED;
  --gc-outline-variant: #DADCE0;

  /* Semantic Tints */
  --gc-blue-tint: #E8F0FE;
  --gc-green-tint: #E6F4EA;
  --gc-red-tint: #FCE8E6;
  --gc-yellow-tint: #FEF7E0;
  --gc-purple-tint: #F3E8FD;
  --gc-teal-tint: #E0F7FA;

  /* Extended Colors */
  --gc-purple: #A142F4;
  --gc-teal: #00BCD4;
  --gc-orange: #FF6D00;
}

body {
  background-color: var(--gc-surface);
  font-family: 'Google Sans', 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
  color: var(--gc-on-surface-variant);
  font-size: 16px;
  line-height: 1.7;
  padding: 20px;
  margin: 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  padding-bottom: 16px;
  border-bottom: 3px solid var(--gc-blue-600);
}

h1, .title {
  font-size: 36px;
  font-weight: 700;
  color: var(--gc-on-surface);
  margin: 0;
}

h2, .section-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--gc-on-surface);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--gc-blue-600);
}

.subtitle {
  font-size: 16px;
  color: var(--gc-outline);
}

.section {
  background: var(--gc-surface-container-low);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  border: 1px solid var(--gc-outline-variant);
}

.highlight {
  background-color: var(--gc-blue-50);
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
  color: var(--gc-blue-800);
  border-bottom: 2px solid var(--gc-blue-600);
}

.card {
  background: var(--gc-surface);
  border-radius: 12px;
  padding: 20px;
  margin: 12px 0;
  border-left: 4px solid var(--gc-blue-600);
  box-shadow: 0 1px 3px rgba(60, 64, 67, 0.12), 0 1px 2px rgba(60, 64, 67, 0.08);
}

.icon-text {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
  color: var(--gc-on-surface-variant);
}

.arrow {
  color: var(--gc-blue-600);
  font-size: 20px;
}

.gc-link {
  color: var(--gc-blue-600);
  text-decoration: none;
}

.gc-link:hover {
  color: var(--gc-blue-800);
  text-decoration: underline;
}

/* サービスバッジ
   重要: すべてのバッジは白文字 (#FFFFFF) を使用すること。
   背景色が濃いため、グレー文字だとコントラスト不足で読めない。
   重要: .badge-ga, .badge-preview, .badge-deprecated は
   必ず .badge と併用すること (例: class="badge badge-ga")。
   単独で使用すると共通スタイル (padding, border-radius, margin) が適用されない。 */
.badge,
.badge-ga,
.badge-preview,
.badge-deprecated {
  display: inline-block;
  color: #FFFFFF;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.25px;
  margin: 4px 8px 4px 0;
}

.badge {
  background: var(--gc-blue-600);
}

.badge-ga {
  background: var(--gc-green);
  color: #FFFFFF;
}

.badge-preview {
  background: var(--gc-orange);
  color: #FFFFFF;
}

.badge-deprecated {
  background: var(--gc-red);
  color: #FFFFFF;
}

/* フロー図スタイル */
.flow-diagram {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin: 24px 0;
}

.flow-step {
  background: var(--gc-surface);
  border: 2px solid var(--gc-blue-600);
  border-radius: 12px;
  padding: 12px 20px;
  text-align: center;
  min-width: 100px;
  color: var(--gc-on-surface);
  box-shadow: 0 1px 3px rgba(60, 64, 67, 0.12);
}

.flow-arrow {
  color: var(--gc-blue-600);
  font-size: 24px;
  font-weight: bold;
}

/* チェックリストスタイル */
.check-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 8px 0;
}

.check-icon {
  color: var(--gc-green);
  font-size: 18px;
}

.cross-icon {
  color: var(--gc-red);
  font-size: 18px;
}

/* コードブロック
   ダーク背景 (#1E1E1E) + 明るいテキストで統一。
   .code-block クラスと <pre><code> タグの両方に対応する。
   重要: pre:not(.mermaid) を使用して Mermaid 図の <pre> タグを除外すること。
   Mermaid 図は <pre class="mermaid"> で定義されるため、
   pre に直接ダーク背景を指定すると Mermaid 図も黒背景になってしまう。 */
.code-block,
pre:not(.mermaid) {
  background: #1E1E1E;
  border-radius: 8px;
  padding: 16px;
  font-family: 'Roboto Mono', 'Source Code Pro', 'Courier New', monospace;
  font-size: 15px;
  line-height: 1.6;
  overflow-x: auto;
  color: #E8E8E8;
  margin: 16px 0;
}

pre code {
  background: none;
  border: none;
  padding: 0;
  font-size: inherit;
  color: inherit;
}

/* コードブロックのラベル (言語名表示) */
.code-label {
  display: inline-block;
  background: #2D2D2D;
  color: #9CDCFE;
  padding: 4px 12px;
  border-radius: 8px 8px 0 0;
  font-size: 12px;
  font-weight: 600;
  font-family: 'Roboto Mono', 'Source Code Pro', 'Courier New', monospace;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ラベル付きコードブロック */
.code-label + pre:not(.mermaid),
.code-label + .code-block {
  border-top-left-radius: 0;
  margin-top: 0;
}

/* インラインコード */
code:not(pre code) {
  background: var(--gc-surface-container-low);
  border: 1px solid var(--gc-outline-variant);
  border-radius: 4px;
  padding: 2px 6px;
  font-family: 'Roboto Mono', 'Source Code Pro', 'Courier New', monospace;
  font-size: 0.9em;
  color: var(--gc-blue-900);
}

/* シンタックスハイライト (ダーク背景用 — VS Code 風) */
.code-block .comment, pre .comment { color: #6A9955; font-style: italic; }
.code-block .keyword, pre .keyword { color: #569CD6; font-weight: 600; }
.code-block .string, pre .string { color: #CE9178; }
.code-block .number, pre .number { color: #B5CEA8; }
.code-block .flag, pre .flag { color: #C586C0; }
.code-block .property, pre .property { color: #9CDCFE; }
.code-block .value, pre .value { color: #CE9178; }

/* テーブルスタイル */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--gc-outline-variant);
}

th {
  background: var(--gc-blue-50);
  color: var(--gc-blue-900);
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
  border-bottom: 2px solid var(--gc-blue-200);
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--gc-outline-variant);
  font-size: 14px;
}

tr:nth-child(even) {
  background: var(--gc-surface-container-lowest);
}

tr:hover {
  background: var(--gc-blue-50);
}

/* 注意・警告ボックス */
.note-box {
  background: var(--gc-blue-tint);
  border-left: 4px solid var(--gc-blue-600);
  padding: 16px 20px;
  border-radius: 0 12px 12px 0;
  margin: 16px 0;
}

.warning-box {
  background: var(--gc-yellow-tint);
  border-left: 4px solid var(--gc-yellow);
  padding: 16px 20px;
  border-radius: 0 12px 12px 0;
  margin: 16px 0;
}

.error-box {
  background: var(--gc-red-tint);
  border-left: 4px solid var(--gc-red);
  padding: 16px 20px;
  border-radius: 0 12px 12px 0;
  margin: 16px 0;
}

.ai-box {
  background: var(--gc-purple-tint);
  border-left: 4px solid var(--gc-purple);
  padding: 16px 20px;
  border-radius: 0 12px 12px 0;
  margin: 16px 0;
}

.success-box {
  background: var(--gc-green-tint);
  border-left: 4px solid var(--gc-green);
  padding: 16px 20px;
  border-radius: 0 12px 12px 0;
  margin: 16px 0;
}

/* 統計カード */
.stat-card {
  background: linear-gradient(135deg, var(--gc-blue-600), var(--gc-blue-800));
  color: var(--gc-surface);
  border-radius: 12px;
  padding: 24px;
  text-align: center;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

footer {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--gc-outline-variant);
  font-size: 12px;
  color: var(--gc-outline);
}
```

## HTML テンプレート例

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Google Cloud アーキテクチャ概要</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap');
    
    /* CSS テンプレートをここに挿入 */
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>☁️ Google Cloud アーキテクチャ概要</h1>
      <div class="subtitle">2026-02-15</div>
    </div>
    
    <div class="section">
      <h2>🔧 セクション 1</h2>
      <p>本文テキスト。<span class="highlight">重要なポイント</span>を強調します。</p>
      
      <div class="card">
        <div class="icon-text">
          <span class="arrow">→</span>
          <span>カード内のコンテンツ</span>
        </div>
      </div>
    </div>
    
    <div class="section">
      <h2>⚡ フロー図の例</h2>
      <div class="flow-diagram">
        <div class="flow-step">💬 入力</div>
        <span class="flow-arrow">→</span>
        <div class="flow-step">⚙️ 処理</div>
        <span class="flow-arrow">→</span>
        <div class="flow-step">✅ 出力</div>
      </div>
    </div>
    
    <div class="note-box">
      <strong>💡 ヒント:</strong> これは情報ボックスの例です。
    </div>
    
    <div class="warning-box">
      <strong>⚠️ 注意:</strong> これは警告ボックスの例です。
    </div>
    
    <div class="ai-box">
      <strong>🤖 AI/ML:</strong> これは AI/ML 関連の情報ボックスの例です。
    </div>
    
    <div class="success-box">
      <strong>✅ 成功:</strong> これは成功ボックスの例です。
    </div>
    
    <footer>
      <p>📎 出典: <a href="#" target="_blank" class="gc-link">ソース URL</a></p>
    </footer>
  </div>
</body>
</html>
```

## 適用キーワード

以下のキーワードが含まれる場合、このテーマを適用します。

- 「Google Cloud」「GCP」「クラウド」「アーキテクチャ」「技術資料」
- 「ライト」「ライトテーマ」「白背景」「明るい」
- 「ドキュメント」「ホワイトペーパー」「印刷」
