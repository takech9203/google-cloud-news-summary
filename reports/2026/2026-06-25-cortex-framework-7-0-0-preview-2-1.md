# Cortex Framework: Release 7.0.0-preview.2.1 tableSettings パス解決の修正

**リリース日**: 2026-06-25

**サービス**: Google Cloud Cortex Framework

**機能**: tableSettings パス解決の不具合修正

**ステータス**: Public Preview

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260625-cortex-framework-7-0-0-preview-2-1.html)

## 概要

Google Cloud Cortex Framework 7.0.0-preview.2.1 がリリースされた。これは 2026-06-24 にリリースされた 7.0.0-preview.2 に対するマイナーバグフィックスリリースであり、設定ファイル (`config/config.yaml`) 内の `tableSettings` プロパティにおけるパス解決の不具合が修正された。

`tableSettings` は、Data Foundation モジュールおよび Data Product モジュールのテーブル構成 (マテリアライゼーション方式、パーティショニング、クラスタリングなど) を定義する `table_settings.yaml` ファイルへのパスを指定するプロパティである。今回の修正により、カスタムパスを指定した際のパス解決が正しく動作するようになった。

**アップデート前の課題**

- `config/config.yaml` の `tableSettings` プロパティでカスタムパスを指定した場合に、パス解決が正しく行われないケースがあった
- カスタムの `table_settings.yaml` を使用するマルチインスタンスデプロイや拡張構成で、設定ファイルが正しく読み込まれない可能性があった

**アップデート後の改善**

- `tableSettings` のパス解決ロジックが修正され、カスタムパスの指定が期待通りに動作するようになった
- カスタム構成ディレクトリに配置した `table_settings.yaml` が正しく参照されるようになった

## サービスアップデートの詳細

### 主要機能

1. **tableSettings パス解決の修正**
   - `config/config.yaml` 内の `tableSettings` プロパティで指定するファイルパスの解決ロジックを修正
   - Data Foundation モジュールおよび Data Product モジュールの両方に適用
   - デフォルトパス (`definitions/data_foundation/{namespace}/table_settings.default.yaml` など) へのフォールバック動作には影響なし

## 技術仕様

### tableSettings の構成

`tableSettings` は `config/config.yaml` 内で以下のように使用される。

```yaml
data:
  modules:
    foundation:
      - moduleId: erp
        type: cortex.sap
        tableSettings: "config/cortex/data_foundation/sap/table_settings.yaml"

    product:
      - moduleId: accounts_payable
        type: cortex.accounts_payable
        tableSettings: "config/cortex/data_product/accounts_payable/table_settings.yaml"
```

| 項目 | 詳細 |
|------|------|
| 影響を受けるプロパティ | `tableSettings` (foundation / product モジュール) |
| パスの基準 | `config/config.yaml` からの相対パス |
| デフォルト動作 | `tableSettings` 省略時は `table_settings.default.yaml` にフォールバック |
| 修正対象バージョン | 7.0.0-preview.2 |

## 設定方法

### 対応手順

1. Cortex Framework リポジトリを最新 (7.0.0-preview.2.1) に更新する
2. カスタム `tableSettings` パスを使用している場合は、設定ファイルが正しく読み込まれることを確認する

```bash
# リポジトリの更新
git pull origin main

# ビルド・デプロイの再実行
uv run cortex-build-and-deploy
```

## メリット

### 技術面

- **カスタム構成の安定性向上**: カスタムパスの `table_settings.yaml` が確実に読み込まれるようになり、マルチインスタンスデプロイの信頼性が向上
- **拡張性ガイドとの整合性**: preview.2 で公開された拡張性ガイドのカスタムネームスペース構成が意図通りに動作するようになった

## デメリット・制約事項

### 制限事項

- 引き続き Public Preview 段階であり、本番環境での利用は推奨されていない
- GitHub リポジトリへのアクセスにはリクエスト申請が必要

## 関連サービス・機能

- **BigQuery**: Cortex Framework のデータ処理・ストレージ基盤
- **Dataform**: `table_settings.yaml` の設定に基づき、BigQuery テーブルのマテリアライゼーション (ビュー、テーブル、インクリメンタルテーブル) を制御
- **Cortex Framework 7.0.0-preview.2**: 本リリースの親バージョン。SAP ERP データプロダクト拡充と拡張性ガイドが含まれる

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260625-cortex-framework-7-0-0-preview-2-1.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#June_25_2026)
- [Cortex Framework リリースノート](https://docs.cloud.google.com/cortex/docs/release-notes)
- [Deployment Configuration (tableSettings)](https://docs.cloud.google.com/cortex/docs/deployment-configuration)
- [Cortex Framework 技術ドキュメント](https://docs.cloud.google.com/cortex/docs)

## まとめ

Cortex Framework 7.0.0-preview.2.1 は、前日リリースの preview.2 に対するマイナーバグフィックスである。`tableSettings` のパス解決に問題があったユーザーは、最新バージョンへの更新により解消される。カスタム `table_settings.yaml` を使用してマルチインスタンスデプロイや独自の拡張構成を行っている場合は、更新後にデプロイが正常に完了することを確認することを推奨する。

---

**タグ**: #CortexFramework #BigQuery #Dataform #Bugfix #PublicPreview #Configuration
