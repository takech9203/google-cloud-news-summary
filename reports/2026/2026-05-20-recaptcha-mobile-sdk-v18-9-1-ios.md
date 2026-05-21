# reCAPTCHA: Mobile SDK v18.9.1 for iOS - シンボル衝突の修正

**リリース日**: 2026-05-20

**サービス**: reCAPTCHA

**機能**: Mobile SDK v18.9.1 for iOS

**ステータス**: Change

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260520-recaptcha-mobile-sdk-v18-9-1-ios.html)

## 概要

reCAPTCHA Mobile SDK v18.9.1 が iOS 向けにリリースされました。本バージョンは、Objective-C Protocol Buffers (protos) を使用する他のライブラリとのシンボル衝突 (symbol collision) を修正するバグフィックスリリースです。

シンボル衝突は、同一プロジェクト内で複数のライブラリが同じシンボル名を定義している場合に発生するリンカエラーです。reCAPTCHA SDK が内部的に使用していた Objective-C proto 生成コードのシンボルが、他のライブラリ（Firebase、gRPC、その他 Google 系 SDK など）で使用される同名のシンボルと衝突していた問題が解消されました。

このアップデートは、reCAPTCHA SDK を他の Objective-C proto を使用するライブラリと併用している iOS アプリ開発者に影響します。

**アップデート前の課題**

- reCAPTCHA SDK と他の Objective-C proto を使用するライブラリを同時に導入すると、リンカがシンボルの重複を検出しビルドエラーが発生する場合があった
- 「duplicate symbol」エラーにより、アプリのビルドが失敗する、または実行時に予期しない動作が発生する可能性があった
- 回避策として、ライブラリのバージョンを固定したり、リンカフラグを調整するなどの対応が必要だった

**アップデート後の改善**

- Objective-C proto を使用する他のライブラリとのシンボル衝突が解消された
- Firebase SDK、gRPC、その他 Google 系ライブラリとの共存が安定した
- ビルド時のリンカエラーが発生しなくなり、開発者の生産性が向上した

## 技術仕様

### SDK バージョン情報

| 項目 | 詳細 |
|------|------|
| SDK バージョン | v18.9.1 |
| プラットフォーム | iOS |
| 最小サポート OS | iOS 15 |
| 修正内容 | Objective-C proto 使用ライブラリとのシンボル衝突修正 |
| 前バージョン | v18.8.0 (2025年9月15日リリース) |

### 導入方法

#### CocoaPods

```ruby
source "https://github.com/CocoaPods/Specs.git"

target 'AppTarget' do
  use_frameworks!
  pod "RecaptchaEnterprise", "18.9.1"
end
```

#### Swift Package Manager

Xcode で File > Add Packages を選択し、以下の URL を入力:

```
https://github.com/GoogleCloudPlatform/recaptcha-enterprise-mobile-sdk
```

#### 直接ダウンロード

xcframework 形式での直接ダウンロードも利用可能です。全てのバイナリを static xcframework として追加してください。

## 設定方法

### 前提条件

1. iOS 15 以上をターゲットとするプロジェクト
2. Xcode の最新バージョン（Xcode 26.0 推奨）

### 手順

#### ステップ 1: SDK のアップデート

```bash
# CocoaPods を使用している場合
pod update RecaptchaEnterprise
```

#### ステップ 2: ビルド確認

```bash
# プロジェクトをクリーンビルド
xcodebuild clean build -workspace YourApp.xcworkspace -scheme YourApp
```

シンボル衝突エラーが解消されていることを確認してください。

## メリット

### 技術面

- **ビルド安定性の向上**: Objective-C proto を使用する複数のライブラリとの共存が可能になり、ビルドの信頼性が向上
- **依存関係管理の簡素化**: リンカフラグの手動調整やバージョン固定といった回避策が不要に
- **開発効率の改善**: シンボル衝突のデバッグに費やす時間を削減

## 関連サービス・機能

- **Firebase Authentication**: reCAPTCHA と Firebase の統合において RecaptchaInterop を使用するクライアントに影響
- **Cloud Armor**: reCAPTCHA スコアに基づく WAF ルールとの連携
- **Identity Platform**: モバイルアプリでの不正アクセス防止

## 参考リンク

- [このアップデートのインフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260520-recaptcha-mobile-sdk-v18-9-1-ios.html)
- [公式リリースノート](https://cloud.google.com/release-notes#May_20_2026)
- [reCAPTCHA iOS SDK ドキュメント](https://cloud.google.com/recaptcha/docs/instrument-ios-apps)
- [reCAPTCHA Mobile SDK 非推奨・廃止ポリシー](https://cloud.google.com/recaptcha/docs/deprecation-policy-mobile)
- [reCAPTCHA Mobile SDK GitHub リポジトリ](https://github.com/GoogleCloudPlatform/recaptcha-enterprise-mobile-sdk)

## まとめ

reCAPTCHA Mobile SDK v18.9.1 は、iOS アプリで Objective-C proto を使用する他のライブラリとのシンボル衝突を修正するバグフィックスリリースです。該当する問題が発生しているプロジェクトでは速やかなアップデートを推奨します。reCAPTCHA SDK の非推奨・廃止ポリシーに基づき、常に最新バージョンを使用することで最適な保護とパフォーマンスを維持できます。

---

**タグ**: #reCAPTCHA #iOS #MobileSDK #BugFix #SymbolCollision #ObjectiveC #Protobuf
