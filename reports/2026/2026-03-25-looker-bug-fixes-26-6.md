# Looker: バグ修正および Looker 26.6 リリースアナウンス

**リリース日**: 2026-03-25

**サービス**: Looker

**機能**: バグ修正および Looker 26.6 リリースアナウンス

**ステータス**: Fixed / Announcement

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260325-looker-bug-fixes-26-6.html)

## 概要

Looker (Google Cloud core) および Looker (original) に対して、複数のバグ修正がリリースされた。OAuth データベース接続における JDBC パラメータバリデーションエラー、ダッシュボードテーマのカラーコレクション適用問題、テーマピッカーの表示不具合、Extension Framework のボタン URL 問題、マージクエリビジュアライゼーションにおけるカラーピッカーのアクセシビリティ問題が修正された。

加えて、Looker 26.6 のリリースアナウンスが公開され、デプロイメントスケジュールが提示された。Looker のリリースサイクルは毎月新バージョンがリリースされる形式で、26.6 は 2026 年 3 月のリリースに相当する。

これらの修正は、Looker を利用するデータアナリスト、ダッシュボード開発者、Extension Framework を用いたカスタムアプリケーション開発者に影響する内容である。

**アップデート前の課題**

- OAuth 認証 (Snowflake/BigQuery) を使用するデータベース接続で「JDBC Parameter Validation Failed」エラーが発生し、接続に失敗するケースがあった
- テーマピッカーでテーマが選択されていない場合に「None」と表示され、デフォルトテーマの適用状態が分かりにくかった
- ダッシュボードテーマにカラーコレクションを設定しても、正しく適用されなかった
- Extension Framework のボタンが URL に不要な `/embed/` パスを追加してしまい、意図しないナビゲーションが発生していた
- マージクエリのビジュアライゼーションでフォント色・背景色のカラーピッカーにアクセスできなかった

**アップデート後の改善**

- OAuth データベース接続が JDBC パラメータバリデーションを正しく処理し、Snowflake および BigQuery への接続が安定した
- テーマピッカーでテーマ未選択時に「Default」と表示されるようになり、UI の一貫性が向上した
- ダッシュボードテーマのカラーコレクションが正しく適用されるようになった
- Extension Framework のボタンが正しい URL を生成するようになり、不要な `/embed/` パスが追加されなくなった
- マージクエリのビジュアライゼーションでフォント色・背景色のカラーピッカーが利用可能になった

## サービスアップデートの詳細

### バグ修正

1. **OAuth データベース接続の JDBC パラメータバリデーション修正**
   - Snowflake および BigQuery への OAuth 認証接続で「JDBC Parameter Validation Failed」エラーが発生する問題が修正された
   - OAuth 接続では各ユーザーが自身の OAuth アカウントでデータベースに認証するため、この修正により全ユーザーの接続安定性が改善される
   - Snowflake の OAuth 接続では、JDBC 追加パラメータ (warehouse 指定など) との組み合わせで問題が発生していた可能性がある

2. **テーマピッカーの表示修正**
   - ダッシュボードのスタイルパネルでテーマが選択されていない場合、従来の「None」表示から「Default」表示に変更された
   - テーマ未選択時にはインスタンスのデフォルトテーマが適用される仕様であるため、「Default」表示はこの動作をより正確に反映する

3. **ダッシュボードテーマのカラーコレクション適用修正**
   - ダッシュボードテーマに設定したカラーコレクションが正しくビジュアライゼーションに反映されるようになった
   - カラーコレクションは、カテゴリ別パレット、シーケンシャルパレット、ダイバージングパレットを含む色の組み合わせセットであり、テーマを通じてダッシュボード全体に統一的な配色を適用するために使用される

4. **Extension Framework ボタンの URL 修正**
   - Extension Framework 内のボタンが URL に不要な `/embed/` パスを追加する問題が修正された
   - Extension Framework は Looker の sandboxed iframe 内で動作するため、ナビゲーション URL の生成に影響が出ていた

5. **マージクエリビジュアライゼーションのカラーピッカー修正**
   - マージクエリのビジュアライゼーション設定でフォント色および背景色のカラーピッカーにアクセスできない問題が修正された
   - マージクエリは複数の Explore クエリの結果を結合する機能であり、結合結果のビジュアライゼーション設定が正しく機能するようになった

### Looker 26.6 リリースアナウンス

Looker 26.6 のリリースが発表された。Looker のリリース番号は X.Y.Z の形式で、X は年の下 2 桁、Y は月次バージョン (1 月を 0 として偶数で増加)、Z はパッチバージョンを表す。26.6 は 2026 年の 4 番目のリリースに該当する。

| 項目 | スケジュール |
|------|------------|
| リリースバージョン | Looker 26.6 |
| デプロイメント方式 | ローリングデプロイメント |

## 技術仕様

### 影響を受けるコンポーネント

| コンポーネント | 影響範囲 |
|--------------|---------|
| OAuth データベース接続 | Snowflake、BigQuery への OAuth 認証接続 |
| テーマピッカー | 内部ダッシュボードおよび埋め込みダッシュボードのスタイルパネル |
| カラーコレクション | ダッシュボードテーマのビジュアライゼーション配色 |
| Extension Framework | 拡張機能内のボタンによるナビゲーション |
| マージクエリ | マージ結果のビジュアライゼーション設定 |

### 対象プラットフォーム

| プラットフォーム | 対象 |
|----------------|------|
| Looker (Google Cloud core) | 対象 |
| Looker (original) | 対象 |

## メリット

### ビジネス面

- **ダッシュボードのブランディング品質向上**: カラーコレクションとテーマが正しく適用されることで、組織のブランドガイドラインに沿ったダッシュボード配信が確実になる
- **埋め込み分析の信頼性向上**: Extension Framework の URL 修正により、顧客向け埋め込み分析アプリケーションのナビゲーションが安定する

### 技術面

- **OAuth 接続の安定性向上**: Snowflake および BigQuery への OAuth 接続が安定し、ユーザーごとの認証フローが正しく動作する
- **ビジュアライゼーションのカスタマイズ性回復**: マージクエリのカラーピッカー修正により、複雑なデータ分析結果の表示設定が可能になった

## 関連サービス・機能

- **Snowflake**: OAuth データベース接続の修正対象。Looker は Snowflake の OAuth 統合、キーペア認証、データベースアカウント認証をサポートする
- **BigQuery**: OAuth データベース接続の修正対象。Google Cloud のデータウェアハウスサービスとして Looker と密接に連携する
- **Looker Extension Framework**: カスタム JavaScript アプリケーション開発のためのフレームワーク。sandboxed iframe 内で動作し、Looker の認証とアクセス制御を活用する
- **Looker テーマ機能**: 内部ダッシュボードおよび埋め込みダッシュボードの外観をカスタマイズする機能。カラーコレクション、フォント、背景色などを設定可能

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260325-looker-bug-fixes-26-6.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#March_25_2026)
- [Looker リリースノート](https://docs.cloud.google.com/looker/docs/release-notes)
- [Looker テーマドキュメント (内部ダッシュボード)](https://docs.cloud.google.com/looker/docs/themes-for-internal-dashboards)
- [Looker テーマドキュメント (埋め込み)](https://docs.cloud.google.com/looker/docs/themes-for-embedded-dashboards-and-explores)
- [Looker Extension Framework](https://docs.cloud.google.com/looker/docs/intro-to-extension-framework)
- [Snowflake 接続設定](https://docs.cloud.google.com/looker/docs/db-config-snowflake)
- [カラーコレクション](https://docs.cloud.google.com/looker/docs/color-collections)

## まとめ

今回のアップデートでは、Looker の OAuth データベース接続、テーマ機能、Extension Framework、マージクエリビジュアライゼーションにおける 5 件のバグが修正された。特に OAuth 接続の JDBC パラメータバリデーション修正は、Snowflake や BigQuery を OAuth 認証で利用している環境に直接影響するため、該当する構成を使用している場合はデプロイ後の接続確認を推奨する。Looker 26.6 のデプロイスケジュールも公開されており、新バージョンの適用計画を進めることが望ましい。

---

**タグ**: #Looker #BugFix #OAuth #Snowflake #BigQuery #Dashboard #Theme #ExtensionFramework #MergeQuery #Looker26.6
