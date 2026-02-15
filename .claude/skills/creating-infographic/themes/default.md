# デフォルトテーマ（グラフィックレコーディング風）

グラフィックレコーディング風のデフォルトテーマ。手書き風の要素とカラフルな配色で、情報を視覚的に魅力的に表現する 3 カラム構成です。

## カラーパレット

```xml
<palette name="default">
  <color name='ファッション-1' rgb='593C47' r='89' g='59' b='70' description='メインテキスト、見出し' />
  <color name='ファッション-2' rgb='F2E63D' r='242' g='230' b='60' description='アクセント、強調背景' />
  <color name='ファッション-3' rgb='F2C53D' r='242' g='196' b='60' description='セカンダリアクセント' />
  <color name='ファッション-4' rgb='F25C05' r='242' g='91' b='4' description='重要な強調、アイコン' />
  <color name='ファッション-5' rgb='F24405' r='242' g='68' b='4' description='最重要強調、警告' />
</palette>
```

## デザインガイドライン

### 1. カラースキーム

デフォルトのグラフィックレコーディング風カラーパレットを使用します。

- **メインテキスト**: #593C47 (ファッション-1)
- **アクセント**: #F2E63D (ファッション-2)
- **セカンダリアクセント**: #F2C53D (ファッション-3)
- **重要な強調**: #F25C05 (ファッション-4)
- **最重要強調**: #F24405 (ファッション-5)

### 2. グラフィックレコーディング要素

- 左上から右へ、上から下へと情報を順次配置
- 日本語の手書き風フォントの使用 (Yomogi, Zen Kurenaido, Kaisei Decol)
- 手描き風の囲み線、矢印、バナー、吹き出し
- テキストと視覚要素 (アイコン、シンプルな図形) の組み合わせ
- キーワードの強調 (色付き下線、マーカー効果)
- 関連する概念を線や矢印で接続
- 絵文字やアイコンを効果的に配置 (✏️📌📝🔍📊など)

### 3. タイポグラフィ

- **タイトル**: 32px、グラデーション効果、太字
- **サブタイトル**: 16px、#475569
- **セクション見出し**: 18px、#1e40af、アイコン付き
- **本文**: 14px、#334155、行間 1.4
- **フォント指定**:

```html
<style>
@import url('https://fonts.googleapis.com/css2?family=Kaisei+Decol&family=Yomogi&family=Zen+Kurenaido&display=swap');
</style>
```

### 4. レイアウト

- **ヘッダー**: 左揃えタイトル＋右揃え日付/出典
- **3 カラム構成**: 左側 33%、中央 33%、右側 33%
- **カード型コンポーネント**: 白背景、角丸 12px、微細シャドウ
- **セクション間の適切な余白と階層構造**
- **適切にグラスモーフィズムを活用**
- **コンテンツの横幅は 100%**

## CSS テンプレート

```css
/* Default Theme Base Styles */
:root {
  --fashion-1: #593C47;
  --fashion-2: #F2E63D;
  --fashion-3: #F2C53D;
  --fashion-4: #F25C05;
  --fashion-5: #F24405;
  --text-primary: #334155;
  --text-secondary: #475569;
  --text-accent: #1e40af;
}

body {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  font-family: 'Yomogi', 'Zen Kurenaido', 'Kaisei Decol', sans-serif;
  color: var(--text-primary);
  line-height: 1.6;
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.title {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--fashion-4), var(--fashion-5));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 16px;
  color: var(--text-secondary);
}

.three-column-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

@media (max-width: 768px) {
  .three-column-grid {
    grid-template-columns: 1fr;
  }
}

.column {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 18px;
  color: var(--text-accent);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.highlight {
  background: linear-gradient(transparent 60%, var(--fashion-2) 60%);
  padding: 2px 4px;
  font-weight: 600;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin: 12px 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-left: 4px solid var(--fashion-4);
}

.icon-text {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
}

.arrow {
  color: var(--fashion-4);
  font-size: 20px;
}
```

## HTML テンプレート例

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>グラフィックレコーディング風インフォグラフィック</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Kaisei+Decol&family=Yomogi&family=Zen+Kurenaido&display=swap');
    
    /* CSS テンプレートをここに挿入 */
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 class="title">📝 タイトル</h1>
      <div class="subtitle">2026-01-08</div>
    </div>
    
    <div class="three-column-grid">
      <div class="column">
        <div class="section">
          <h2 class="section-title">✏️ セクション 1</h2>
          <p>本文テキスト。<span class="highlight">重要なポイント</span>を強調します。</p>
          
          <div class="card">
            <div class="icon-text">
              <span class="arrow">→</span>
              <span>カード内のコンテンツ</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="column">
        <div class="section">
          <h2 class="section-title">📌 セクション 2</h2>
          <p>中央カラムのコンテンツ</p>
        </div>
      </div>
      
      <div class="column">
        <div class="section">
          <h2 class="section-title">🔍 セクション 3</h2>
          <p>右カラムのコンテンツ</p>
        </div>
      </div>
    </div>
    
    <footer style="margin-top: 24px; padding-top: 16px; border-top: 1px dashed #ccc; font-size: 12px; color: #666;">
      <p>📎 出典: <a href="#" target="_blank" style="color: #1e40af;">ソース URL</a></p>
    </footer>
  </div>
</body>
</html>
```

## 適用キーワード

以下のキーワードが含まれる場合、このテーマを適用します。

- 「グラレコ」「手書き風」「カラフル」「ポップ」（デフォルト）
- 「3 カラム」「マルチカラム」（指定がない場合もこれがデフォルト）
