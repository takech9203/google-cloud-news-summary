# Google SecOps SOAR: Release 6.3.85 全リージョン提供開始

**リリース日**: 2026-05-23

**サービス**: Google SecOps SOAR

**機能**: Release 6.3.85 全リージョン展開完了

**ステータス**: GA

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260523-google-secops-soar-release-6-3-85.html)

## 概要

Google Security Operations (SecOps) SOAR プラットフォームの Release 6.3.85 が、全リージョンで利用可能になりました。本リリースは 2026 年 5 月 17 日に第 1 段階のリージョン（日本、インド、オーストラリア、カナダ、ドイツ、スイス）に先行展開され、5 月 23 日に第 2 段階のリージョン（シンガポール、カタール、サウジアラビア、イスラエル、英国、イタリア、EU マルチリージョン、US マルチリージョン）への展開が完了しました。

本リリースには、内部バグ修正およびお客様報告のバグ修正が含まれています。Google SecOps SOAR は、セキュリティオーケストレーション・自動化・レスポンス（SOAR）プラットフォームとして、脅威の検出・調査・対応を効率化する統合セキュリティ運用環境を提供しています。

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph データ収集
        A[セキュリティテレメトリ] --> B[Google SecOps SIEM]
        C[ログソース] --> B
        D[脅威インテリジェンス] --> B
    end

    subgraph 検出・分析
        B --> E[検出エンジン]
        E --> F[アラート生成]
    end

    subgraph 対応・自動化
        F --> G[Google SecOps SOAR]
        G --> H[Playbook エンジン]
        G --> I[ケース管理]
        H --> J[自動対応アクション]
        H --> K[外部ツール連携]
        I --> L[SOC アナリスト]
    end

    style G fill:#4285F4,color:#fff
```

Google SecOps プラットフォームにおける SIEM と SOAR の連携を示す図です。SIEM がセキュリティデータの収集・検出を担い、SOAR がアラートに対する自動対応・ケース管理・ワークフローオーケストレーションを実行します。

## サービスアップデートの詳細

### リリース内容

1. **内部バグ修正**
   - Google SecOps SOAR プラットフォームの安定性向上に関する内部修正が含まれています

2. **お客様報告のバグ修正**
   - お客様から報告された問題に対する修正が含まれています

### 段階的ロールアウトプロセス

本リリースは Google SecOps SOAR の標準的な 2 段階ロールアウトプロセスに従って展開されました。

| 段階 | リージョン | 展開日 |
|------|-----------|--------|
| 第 1 段階 | 日本、インド、オーストラリア、カナダ、ドイツ、スイス | 2026-05-17 |
| 第 2 段階 | シンガポール、カタール、サウジアラビア、イスラエル、英国（ロンドン）、イタリア、EU（マルチリージョン）、US（マルチリージョン） | 2026-05-23 |

## 技術仕様

### リリース情報

| 項目 | 詳細 |
|------|------|
| バージョン | 6.3.85 |
| リリースタイプ | メンテナンスリリース（バグ修正） |
| 初回展開日 | 2026-05-17（第 1 段階リージョン） |
| 全リージョン展開日 | 2026-05-23 |
| メンテナンスウィンドウ | 毎週日曜日 11:00-15:00 UTC |

## 利用可能リージョン

Release 6.3.85 は以下の全リージョンで利用可能です。

**第 1 段階リージョン:**
- 日本
- インド
- オーストラリア
- カナダ
- ドイツ
- スイス

**第 2 段階リージョン:**
- シンガポール
- カタール
- サウジアラビア
- イスラエル
- 英国（ロンドン）
- イタリア
- EU（マルチリージョン）
- US（マルチリージョン）

## 関連サービス・機能

- **Google SecOps SIEM**: セキュリティ情報・イベント管理。SOAR と統合されたプラットフォームとして脅威検出を担当
- **Google SecOps Playbook エンジン**: セキュリティ対応の自動化ワークフローを構築・実行するエンジン
- **Google SecOps Marketplace**: 300 以上の SOAR インテグレーションを提供するマーケットプレイス
- **Gemini in Security Operations**: AI を活用した Playbook 作成、調査支援、レスポンス推奨

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260523-google-secops-soar-release-6-3-85.html)
- [公式リリースノート](https://cloud.google.com/release-notes#May_23_2026)
- [Google SecOps SOAR リリースノート](https://docs.cloud.google.com/chronicle/docs/soar/release-notes)
- [段階的リリース計画](https://docs.cloud.google.com/chronicle/docs/soar/overview-and-introduction/soar-gradual-release)
- [Google SecOps SOAR 概要](https://docs.cloud.google.com/chronicle/docs/soar/overview-and-introduction/soar-overview)

## まとめ

Google SecOps SOAR Release 6.3.85 は、内部およびお客様報告のバグ修正を含むメンテナンスリリースとして全リージョンへの展開が完了しました。セキュリティ運用の安定性維持のため、自動アップデートが適用されていることをご確認ください。詳細な修正内容については公式リリースノートを参照してください。

---

**タグ**: #GoogleSecOps #SOAR #SecurityOperations #BugFix #Release #Chronicle
