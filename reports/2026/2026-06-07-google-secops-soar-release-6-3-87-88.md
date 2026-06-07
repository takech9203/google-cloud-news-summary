# Google SecOps SOAR: Release 6.3.87 / 6.3.88

**リリース日**: 2026-06-06 / 2026-06-07
**サービス**: Google SecOps SOAR (Security Orchestration, Automation, and Response)
**機能**: メンテナンスリリース 6.3.87 / 6.3.88
**ステータス**: 6.3.87 全リージョン提供開始 / 6.3.88 第1フェーズ展開中

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260607-google-secops-soar-release-6-3-87-88.html)

## 概要

Google SecOps SOAR (Security Orchestration, Automation, and Response) の連続メンテナンスリリースが発表された。Release 6.3.87 は 2026 年 6 月 6 日に全リージョンで利用可能となり、Release 6.3.88 は 2026 年 6 月 7 日より第 1 フェーズのリージョンへの展開が開始された。

いずれのリリースも内部バグ修正および顧客報告のバグ修正を含むメンテナンスリリースであり、新機能の追加は含まれていない。Google SecOps SOAR のリリースは段階的なリージョン展開プロセスに従い、まず第 1 フェーズのリージョン (日本、インド、オーストラリア、カナダ、ドイツ、スイス) に展開された後、約 1 週間後に第 2 フェーズのリージョン (シンガポール、カタール、サウジアラビア、イスラエル、英国、イタリア、EU マルチリージョン、US マルチリージョン) に展開される。

Google SecOps SOAR は、セキュリティオーケストレーション、自動化、レスポンスを統合したプラットフォームであり、脅威の検出・調査・対応の迅速化を目的としている。今回のリリースはプラットフォームの安定性と信頼性を維持するための定期的なメンテナンスサイクルの一環であり、Google SecOps SOAR を利用する全てのセキュリティチームに影響する。

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Release["Google SecOps SOAR リリースプロセス"]
        direction TB
        NEW["🔧 新リリース作成<br/>内部・顧客バグ修正"]
        PHASE1["🌏 第1フェーズ展開<br/>日本 / インド / オーストラリア<br/>カナダ / ドイツ / スイス"]
        WAIT["⏳ 約1週間の監視期間"]
        PHASE2["🌍 第2フェーズ展開<br/>シンガポール / カタール / サウジアラビア<br/>イスラエル / 英国 / イタリア<br/>EU マルチリージョン / US マルチリージョン"]
        GA["✅ 全リージョン提供完了"]
    end

    NEW --> PHASE1
    PHASE1 --> WAIT
    WAIT --> PHASE2
    PHASE2 --> GA

    subgraph Status["現在のステータス (2026-06-07)"]
        S87["Release 6.3.87: 全リージョン提供中"]
        S88["Release 6.3.88: 第1フェーズ展開中"]
    end

    GA -.->|"6.3.87"| S87
    PHASE1 -.->|"6.3.88"| S88
```

Google SecOps SOAR のリリースは 2 段階のリージョン展開プロセスに従い、第 1 フェーズのリージョンで問題がないことを確認した後、第 2 フェーズのリージョンに展開される。リリースは通常日曜日に実施される。

## サービスアップデートの詳細

### Release 6.3.87 (2026-06-06 全リージョン提供開始)

- **ステータス**: 全リージョンで利用可能
- **内容**: 内部バグ修正および顧客報告のバグ修正
- **展開状況**: 2026 年 5 月 31 日に第 1 フェーズのリージョンへ展開が開始され、6 月 6 日に全リージョンへの展開が完了

### Release 6.3.88 (2026-06-07 第1フェーズ展開開始)

- **ステータス**: 第 1 フェーズのリージョンへ展開中
- **内容**: 内部バグ修正および顧客報告のバグ修正
- **展開状況**: 第 1 フェーズのリージョン (日本、インド、オーストラリア、カナダ、ドイツ、スイス) への展開が開始。第 2 フェーズのリージョンへの展開は約 1 週間後を予定

### リリースの連続性

直近のリリース履歴を見ると、Google SecOps SOAR は概ね週次でメンテナンスリリースを行っている。

| リリース | 第1フェーズ展開 | 全リージョン展開 |
|---------|----------------|----------------|
| 6.3.85 | 2026-05-17 | 2026-05-23 |
| 6.3.86 | 2026-05-24 | 2026-05-30 |
| 6.3.87 | 2026-05-31 | 2026-06-06 |
| 6.3.88 | 2026-06-07 | 2026-06-14 (予定) |

## 利用可能リージョン

Google SecOps SOAR のリリースは以下の 2 段階で展開される。リリースは通常日曜日に実施され、第 2 フェーズは第 1 フェーズの約 1 週間後にアップグレードされる。

### 第 1 フェーズ (先行展開)

- 日本
- インド
- オーストラリア
- カナダ
- ドイツ
- スイス

### 第 2 フェーズ (後続展開)

- シンガポール
- カタール
- サウジアラビア
- イスラエル
- 英国 (ロンドン)
- イタリア
- EU (マルチリージョン)
- US (マルチリージョン)

自身のインスタンスがどのリージョンに割り当てられているか不明な場合は、Google SecOps の担当者に問い合わせが必要である。

## デメリット・制約事項

### 段階的展開に伴う留意点

- 第 1 フェーズと第 2 フェーズの間で約 1 週間のバージョン差が生じるため、複数リージョンにまたがる運用を行っている場合はバージョンの不一致に注意が必要
- メンテナンスリリースのため、具体的なバグ修正内容の詳細は公開されていない。個別の修正内容については Google SecOps の担当者に確認が必要

## 関連サービス・機能

- **Google SecOps SIEM**: SOAR と同時にリリースされる SIEM (Security Information and Event Management) コンポーネント。同一のリリース番号体系と段階的展開プロセスに従う
- **Google SecOps Response Integrations**: サードパーティ製品との連携を提供するマーケットプレイス統合機能。SOAR プラットフォームのリリースとは別のリリースサイクルで更新される
- **Chronicle API (統合版)**: 2026 年 5 月 28 日に GA となった統合 Chronicle API。SOAR の Case、Alert、Playbook などのリソースを REST API 経由で操作可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260607-google-secops-soar-release-6-3-87-88.html)
- [Google Cloud Release Notes](https://cloud.google.com/release-notes#June_07_2026)
- [Google SecOps SOAR リリースノート](https://docs.cloud.google.com/chronicle/docs/soar/release-notes)
- [Google SecOps リリース展開計画](https://docs.cloud.google.com/chronicle/docs/soar/overview-and-introduction/soar-gradual-release)
- [Google SecOps SOAR 概要ドキュメント](https://docs.cloud.google.com/chronicle/docs/soar/overview-and-introduction/soar-overview)
- [Google SecOps ステータスダッシュボード](https://status.cloud.google.com/security/)
- [Google SecOps 料金に関する問い合わせ](https://chronicle.security/contact)

## まとめ

Google SecOps SOAR の Release 6.3.87 および 6.3.88 は、プラットフォームの安定性向上を目的とした定期的なメンテナンスリリースである。新機能の追加は含まれていないが、内部および顧客報告のバグ修正が含まれており、セキュリティオーケストレーション・自動化・レスポンス基盤の信頼性維持に寄与する。日本リージョンは第 1 フェーズに含まれるため、Release 6.3.88 は既に展開が開始されている。特別な対応は不要だが、展開後にプラットフォームの動作 (Playbook の実行、コネクタの動作、ケース管理など) に問題がないことを確認することを推奨する。

---

**タグ**: Google SecOps, SOAR, Security, Chronicle, メンテナンスリリース, バグ修正, 段階的展開, セキュリティオーケストレーション
