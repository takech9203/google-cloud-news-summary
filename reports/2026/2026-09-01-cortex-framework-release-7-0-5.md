# Cortex Framework: Release 7.0.5 (テストから旧式のレビュー項目チェックリストを削除)

**リリース日**: 2026-09-01

**サービス**: Cortex Framework

**機能**: Release 7.0.5 (メンテナンスリリース)

**ステータス**: Announcement / Fixed

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260901-cortex-framework-release-7-0-5.html)

## 概要

Google Cloud Cortex Framework の Release 7.0.5 が公開されました。2026 年 7 月 30 日に一般提供 (GA) となったバージョン 7 系に対するパッチリリースで、8 月 26 日の Release 7.0.4 (未使用依存関係 pandas / pytest-bigquery-mock の削除とロックファイルのクリーンアップ) に続くものです。

本リリースで公表されている変更は 1 件のみで、テストから旧式 (obsolete) のレビュー項目チェックリストが削除されました (リリースノート原文: "Removed obsolete review items checklist from tests.")。フレームワークのデータモデルやビルド・デプロイの挙動、設定モデルに影響する変更は含まれておらず、リポジトリ内部の保守・クリーンアップを目的としたメンテナンスリリースです。

対象となるのは Cortex Framework v7 を利用しているデータエンジニアリングチームですが、既存のデプロイに対する機能的な影響はありません。7.0.4 に続きコードベースの整理が中心の小規模リリースであり、緊急の対応は不要です。

**アップデート前の課題**

- リポジトリのテストに、すでに使われていない旧式のレビュー項目チェックリストが残存していた

**アップデート後の改善**

- テストから旧式のレビュー項目チェックリストが削除され、コードベースが整理された

## サービスアップデートの詳細

### 主要機能

1. **テストからの旧式レビュー項目チェックリストの削除 (Fixed)**
   - リリースノート原文: "Removed obsolete review items checklist from tests."
   - リポジトリ内部のテスト資産のクリーンアップであり、デプロイ済み環境の動作やデータモデルへの影響はない
   - 本リリースで公表されている変更はこの 1 件のみで、新機能の追加はない

### v7 系パッチリリースの経緯

| リリース | 公開日 | 主な内容 |
|------|------|------|
| 7.0 (GA) | 2026-07-30 | モジュラーデプロイアーキテクチャ、Dataform オーケストレーション、SAP BDC 連携などを含むメジャーリリース |
| 7.0.1 | 2026-08-07 | Windows での `uv run cortex-build` エラー修正、Dataform クォータ管理の改善 |
| 7.0.2 | 2026-08-11 | 推移的依存関係のセキュリティ脆弱性解消 |
| 7.0.3 | 2026-08-14 | `SapBdcProductBuilder` の `table_settings` 強制問題の修正 |
| 7.0.4 | 2026-08-26 | 未使用依存関係 (pandas、pytest-bigquery-mock) の削除、ロックファイルのクリーンアップ |
| 7.0.5 | 2026-09-01 | テストから旧式のレビュー項目チェックリストを削除 (本リリース) |

## 設定方法

### 前提条件

1. Cortex Framework v7 を利用していること
2. `uv` (Python パッケージマネージャー) がインストールされていること

### 手順

#### ステップ 1: リポジトリの更新

```bash
cd cortex-framework
git pull
uv sync
```

パッチリリースのため、リポジトリの最新化と依存関係の同期のみで適用できます。テスト資産のクリーンアップが中心のため、既存デプロイの再実行は必須ではありません。

## デメリット・制約事項

### 考慮すべき点

- 機能・挙動の変更を含まないメンテナンスリリースであり、既存環境への実質的な影響はない
- リリースノートに記載されているのは修正の事実のみで、削除されたチェックリストの具体的な内容は公表されていない
- v7 系はパッチが短い間隔で継続的に提供されているため、フォークやカスタマイズをしているチームはリリースノートの定期確認と追従が有効

## 関連サービス・機能

- **BigQuery**: Cortex Framework のデータ基盤・データプロダクトが構築されるデータウェアハウス
- **Dataform**: v7 のオーケストレーション基盤。`cortex-build` でコンパイルした成果物のデプロイ先
- **SAP ECC / S/4HANA、SAP Business Data Cloud**: Cortex Framework v7 がサポートする主要データソース

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260901-cortex-framework-release-7-0-5.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#September_01_2026)
- [Cortex Framework リリースノート](https://docs.cloud.google.com/cortex/docs/release-notes)
- [Cortex Framework 概要](https://docs.cloud.google.com/cortex/docs/overview)
- [Cortex Data Foundation (GitHub)](https://github.com/GoogleCloudPlatform/cortex-data-foundation)

## まとめ

Release 7.0.5 は、テストから旧式のレビュー項目チェックリストを削除するのみの小規模なメンテナンスリリースで、機能やデプロイ挙動への影響はありません。緊急の対応は不要ですが、Cortex Framework v7 を利用しているチームは通常の更新サイクルの中で `git pull` と `uv sync` により最新パッチへ追従しておくことを推奨します。

---

**タグ**: Cortex Framework, パッチリリース, メンテナンス, テスト, BigQuery, Dataform
