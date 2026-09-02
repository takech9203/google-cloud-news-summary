# reCAPTCHA: Fraud Defense Mobile SDK v18.9.3 (Android) リリース

**リリース日**: 2026-09-01

**サービス**: reCAPTCHA (Google Cloud Fraud Defense)

**機能**: Fraud Defense Mobile SDK v18.9.3 for Android

**ステータス**: Change (リリース済み)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260901-recaptcha-fraud-defense-mobile-sdk-18-9-3.html)

## 概要

Android 向けの Fraud Defense Mobile SDK v18.9.3 がリリースされました。このバージョンには、検出 (detection) の強化とパフォーマンスの改善が含まれています。

Fraud Defense Mobile SDK は、モバイルアプリ内のユーザー操作に関する情報を収集して reCAPTCHA に送信し、ボットや不正行為のリスク評価 (アセスメント) を行うためのネイティブ SDK です。SDK はリフレクションと動的コードを利用して、デプロイ済みアプリ内でも検出システムの修正・改善を継続的に反映できる仕組みを持っています。

今回はマイナーバージョンアップであり、API の破壊的変更のアナウンスはありません。reCAPTCHA には[モバイル SDK の非推奨化・シャットダウンポリシー](https://docs.cloud.google.com/recaptcha/docs/deprecation-policy-mobile)が定められているため、Android アプリで reCAPTCHA / Fraud Defense を利用している場合は、定期的なアップデートの一環として本バージョンへの更新を推奨します。

**アップデート後の改善**

- 不正・ボット検出 (detection) の強化
- SDK のパフォーマンス改善

## サービスアップデートの詳細

### 主要な変更点

1. **検出の強化**
   - リスク評価に用いるシグナル検出が強化され、より精度の高いアセスメントに寄与

2. **パフォーマンスの改善**
   - SDK の動作パフォーマンスが改善

リリースノートに記載されている変更点は上記のとおりで、詳細な内部変更は公開されていません。

## 技術仕様

| 項目 | 詳細 |
|------|------|
| 対象プラットフォーム | Android |
| バージョン | v18.9.3 |
| Maven アーティファクト | `com.google.android.recaptcha:recaptcha` |
| 最小 Android SDK | API 23: Android 6.0 (Marshmallow) |
| 必要な権限 | `android.permission.INTERNET` |

## 設定方法

### 手順

アプリレベルの `build.gradle` の依存関係のバージョンを更新します。

```groovy
dependencies {
    implementation 'com.google.android.recaptcha:recaptcha:18.9.3'
}
```

初回導入時の手順 (reCAPTCHA キーの作成、クライアントの初期化、`execute` によるトークン取得など) は [Android アプリへの統合ガイド](https://docs.cloud.google.com/recaptcha/docs/instrument-android-apps)を参照してください。

## メリット

- **検出精度の向上**: 検出強化により、ボット・不正行為のリスク評価の精度向上が期待できる
- **低コストでの追従**: 依存関係のバージョン更新のみで適用でき、破壊的変更のアナウンスはない
- **サポートポリシーへの準拠**: 定期的な SDK 更新により、非推奨化・シャットダウンポリシーへの対応リスクを低減

## 考慮すべき点

- リリースノートには変更点の概要のみが記載されており、検出強化の具体的な内容は公開されていない
- SDK 更新後は、アプリの回帰テスト (特に reCAPTCHA で保護しているログイン・決済などのアクション) を実施することを推奨
- 過去のバージョンで検出改善によりリスクスコアの分布が変化した例があるため、更新後はアセスメントのスコア傾向としきい値を確認するとよい

## 料金

SDK 自体の利用に追加料金はありません。reCAPTCHA のアセスメント数に応じたティア (Essentials / Standard / Enterprise) ベースの料金が適用されます。詳細は[料金ページ](https://cloud.google.com/recaptcha/pricing)を参照してください。

## 関連サービス・機能

- **reCAPTCHA アセスメント API**: SDK が取得したトークンをバックエンドから検証し、リスクスコアを取得する
- **Fraud Defense Mobile SDK for iOS**: iOS 向けには同日に v18.10.0-beta01 がリリースされている
- **アカウント防御 / SMS 防御**: モバイルアプリでのアカウント乗っ取りや SMS 不正への対策として組み合わせて利用可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260901-recaptcha-fraud-defense-mobile-sdk-18-9-3.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#September_01_2026)
- [reCAPTCHA リリースノート](https://docs.cloud.google.com/recaptcha/docs/release-notes)
- [Android アプリへの統合ガイド](https://docs.cloud.google.com/recaptcha/docs/instrument-android-apps)
- [モバイル SDK 非推奨化ポリシー](https://docs.cloud.google.com/recaptcha/docs/deprecation-policy-mobile)
- [料金ページ](https://cloud.google.com/recaptcha/pricing)

## まとめ

Android 向け Fraud Defense Mobile SDK v18.9.3 は、検出強化とパフォーマンス改善を含むメンテナンスリリースです。reCAPTCHA を Android アプリで利用している場合は、依存関係のバージョンを更新し、保護対象アクションの動作とスコア傾向を確認することを推奨します。

---

**タグ**: reCAPTCHA, Fraud Defense, Mobile SDK, Android, セキュリティ, 不正検出
