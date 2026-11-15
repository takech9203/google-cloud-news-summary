# Google SecOps Marketplace: 統合 (Integration) アップデートと 25 統合のソースコード GitHub 公開

**リリース日**: 2026-11-13

**サービス**: Google SecOps Marketplace (Response Integrations)

**機能**: 統合のソースコード GitHub 公開 + 5 つの統合の修正・改善

**ステータス**: GA (Generally Available)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261113-google-secops-marketplace-integration-updates.html)

## 概要

2026 年 11 月 13 日、Google SecOps Marketplace (Response Integrations) に関する 6 件のアップデートが発表されました。最も注目すべきは、**Apache Kafka、Azure Active Directory、ElasticSearch、Mandiant、Microsoft 365 Defender、VMware Carbon Black Cloud など 25 の統合のソースコードが GitHub ([chronicle/content-hub](https://github.com/chronicle/content-hub) リポジトリ) で一般公開された**ことです。Google SecOps はソースコードの公開を段階的に進めており、今回のバッチで対象統合がさらに拡大しました。SOC エンジニアや SOAR プレイブック開発者は、統合の内部実装 (コネクタ、アクション、ジョブのロジック) を直接確認できるようになります。

あわせて、Microsoft Graph Mail / Microsoft Graph Mail Delegated、Palo Alto Cortex XDR、Microsoft 365 Defender、Zscaler の 5 つの統合で、メールヘッダー解析、アーカイブ展開、アラート同期、ドメイン正規化に関する修正・改善がリリースされました。いずれも SOAR のコネクタやプレイブックアクションの信頼性に直結する修正であり、該当統合を利用中の環境では Content Hub からのアップデートを推奨します。

Google SecOps の Response Integrations は、Content Hub からインストール可能なパッケージとして提供され、サードパーティ製品との連携 (アラート取り込み用のコネクタ、プレイブックアクション、スケジュールジョブ) を実現するコンポーネントです。

**アップデート前の課題**

- 今回公開された 25 統合のソースコードは一般公開されておらず、統合の内部ロジック (API 呼び出し、データ変換、エラーハンドリング) をコードレベルで確認できなかった
- Microsoft Graph Mail / Delegated 統合では、複数行にまたがるメールヘッダー (folded header) が展開されず、抽出したヘッダー値に生の改行文字 (`\r\n`) が残ることがあった
- Palo Alto Cortex XDR 統合の Download File アクションで、外側のアーカイブにディレクトリエントリが含まれる場合に内側のアーカイブファイルの展開が失敗していた
- Microsoft 365 Defender 統合で、アンダースコア (`_`) を含むカスタム検出アラート ID が同期・重複排除処理中に切り詰められ、アラートの取りこぼしや重複が発生する可能性があった
- Zscaler 統合で、ワイルドカードドメインの先頭のドット (`.`) が URL・ドメイン正規化処理で保持されず、ブロックリスト/許可リスト操作が意図通りに動作しないことがあった

**アップデート後の改善**

- 25 統合のソースコードが GitHub で公開され、実装の透明性が向上。挙動の調査やトラブルシューティング、カスタム統合開発時の参考としてコードを直接参照できるようになった
- Microsoft Graph Mail v51.0 / Microsoft Graph Mail Delegated v28.0 で、複数行メールヘッダーの展開 (unfold) と `\r\n` の除去が行われ、ヘッダー値を正しく抽出できるようになった
- Palo Alto Cortex XDR v35.0 で、ディレクトリエントリを含むネストされたアーカイブの展開が正しく動作するようになった
- Microsoft 365 Defender v35.0 で、アンダースコアを含むアラート ID が正しく処理され、アラートの欠落・重複が防止されるようになった
- Zscaler v17.0 で、ワイルドカードドメインの先頭ドットが保持され、ブロックリスト/許可リスト関連アクションが正確に動作するようになった

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph GS["🛡️ Google SecOps"]
        CH["🧰 Content Hub /<br>Marketplace"]
        INT["🔌 Response Integrations<br>(コネクタ / アクション / ジョブ)"]
        PB["📘 プレイブック"]
    end

    subgraph TP["🌐 サードパーティ製品"]
        M365["📧 Microsoft Graph Mail /<br>365 Defender"]
        PAN["🔥 Palo Alto Cortex XDR"]
        ZS["🚧 Zscaler"]
    end

    GH["🐙 GitHub<br>chronicle/content-hub<br>(25 統合のソース公開)"]

    CH -->|インストール / 更新| INT
    INT --> PB
    INT <-->|API 連携| M365
    INT <-->|API 連携| PAN
    INT <-->|API 連携| ZS
    GH -.->|ソースコード公開<br>(透明性・参照)| INT
```

Google SecOps の Response Integrations は Content Hub からインストールされ、サードパーティ製品と API 連携します。今回、25 統合のソースコードが GitHub で公開され、統合の内部実装を直接確認できるようになりました。

## サービスアップデートの詳細

### 主要アップデート: 25 統合のソースコードを GitHub で公開

以下の 25 統合のソースコードが [chronicle/content-hub](https://github.com/chronicle/content-hub) リポジトリで一般公開されました。

| カテゴリ | 統合 (バージョン) |
|---------|------------------|
| メッセージング / データ基盤 | Apache Kafka v4.0、ElasticSearch v45.0、ElasticSearchV7 v23.0、CSV v43.0、HTTP V2 v16.0 |
| Microsoft / Azure | Azure Active Directory v31.0、Azure AD Identity Protection v11.0、Azure API v5.0、Microsoft 365 Defender v35.0、Microsoft Defender ATP v35.0、Microsoft Graph Security v30.0 |
| 脅威インテリジェンス | Mandiant v12.0、Mandiant Digital Threat Monitoring v8.0、Mandiant Threat Intelligence v19.0、ThreatQ v21.0、ReversingLabs Titanium v14.0、UrlScan.io v32.0 |
| エンドポイント / スキャン | VMware Carbon Black Cloud v40.0、Trend Micro DDAN v8.0、NessusScanner v14.0、Nmap v6.0、Sysdig Secure v4.0 |
| その他 | Atlassian Confluence Server v7.0、CyberArk Credential Provider v6.0、PhishRod v7.0 |

Google SecOps はこれまでも段階的に統合のソースコード公開を進めており (例: 2026 年 4 月 29 日にも 13 統合を公開)、今回のバッチで公開範囲がさらに拡大しました。

### 統合の修正・改善 (5 件)

| 統合 | バージョン | 変更内容 | 影響するコンポーネント |
|------|-----------|---------|----------------------|
| Microsoft Graph Mail | 51.0 | 複数行メールヘッダーの展開 (unfold) と抽出ヘッダー値からの `\r\n` 除去 | 統合全体 (メール解析ロジック) |
| Microsoft Graph Mail Delegated | 28.0 | 同上 | 統合全体 (メール解析ロジック) |
| Palo Alto Cortex XDR | 35.0 | 外側アーカイブにディレクトリエントリが含まれる場合に内側アーカイブの展開が失敗する問題を修正 | アクション: Download File |
| Microsoft 365 Defender | 35.0 | アンダースコア (`_`) を含むカスタム検出アラート ID が同期・重複排除で切り詰められる問題を修正 (アラートの欠落・重複を防止) | コネクタ: Microsoft 365 Defender - Incidents Connector、ジョブ: Sync Alerts |
| Zscaler | 17.0 | ワイルドカードドメインの先頭ドット (`.`) を保持するよう URL・ドメイン正規化ロジックを更新 | アクション: Add To Blacklist、Add To Whitelist、Lookup Entity、Remove From Blacklist、Remove From Whitelist |

## 技術仕様

### Response Integrations の構成要素

| コンポーネント | 役割 |
|---------------|------|
| コネクタ (Connectors) | 外部ソースからアラート・イベントを Google SecOps に取り込む |
| アクション (Actions) | データのエンリッチメントや、IP ブロック・メール送信などのタスクを実行 (プレイブックで使用) |
| ジョブスケジューラ (Jobs) | サードパーティ製品に対するスケジュールタスクを Google SecOps から直接実行 |

### 統合の更新とロールバック

- 統合は Content Hub の「Integrations」(統合) タブから検索してインストール・更新できます
- 統合のインストール・アップグレード時には、オントロジーマッピングの「Override (置換)」または「Retain (既存を維持)」を選択できます。カスタムマッピングを加えている場合は事前にエクスポートしてバックアップすることが推奨されています
- 更新により問題が発生した場合は、以前にインストールしたバージョンへの[ロールバック](https://docs.cloud.google.com/chronicle/docs/soar/respond/integrations-setup/version-rollback)が可能です

## メリット

### ビジネス面

- **透明性と監査性の向上**: 統合のソースコードを直接確認できるため、セキュリティ製品との連携ロジックに対する監査・レビューが容易になり、コンプライアンス要件への対応がしやすくなる
- **アラート処理の信頼性向上**: Microsoft 365 Defender のアラート ID 切り詰め修正により、アラートの取りこぼしや重複によるインシデント対応の抜け漏れリスクが低減する

### 技術面

- **トラブルシューティングの効率化**: 統合の挙動が想定と異なる場合に、GitHub 上のソースコードを参照して原因をコードレベルで特定できる
- **カスタム統合開発の参考**: IDE でカスタム統合を開発する際、公開された Google 製統合の実装パターン (API 呼び出し、ページネーション、エラーハンドリング) を参考にできる
- **メール解析の精度向上**: Microsoft Graph Mail / Delegated のヘッダー unfold 対応により、フィッシング調査プレイブックなどでヘッダー値 (Received、Authentication-Results など) を正しく抽出・評価できる
- **ワイルドカードドメインの正確な制御**: Zscaler のブロックリスト/許可リスト操作で `.example.com` のようなワイルドカード指定が意図通りに反映される

## デメリット・制約事項

### 考慮すべき点

- 統合のアップデート時にオントロジーマッピングの Override を選択すると、既存のカスタムマッピングが削除される。カスタマイズしている場合は Retain を選択するか、事前にマッピングをエクスポートしておく
- Microsoft 365 Defender v35.0 の修正効果 (アラート欠落・重複の防止) を得るには、コネクタと Sync Alerts ジョブが新バージョンで動作している必要がある
- GitHub でのソースコード公開は参照用であり、統合の導入・更新は従来通り Content Hub (Marketplace) 経由で行う

## ユースケース

### ユースケース 1: フィッシングメール調査プレイブックの精度向上

**シナリオ**: Microsoft Graph Mail コネクタで取り込んだ不審メールのヘッダー (Received チェーン、Authentication-Results など) をプレイブックで解析し、送信元の正当性を判定している。従来は複数行ヘッダーに `\r\n` が残り、正規表現での抽出や比較が失敗することがあった。

**効果**: v51.0 (Delegated は v28.0) へ更新することで、ヘッダーが正しく unfold されて抽出されるため、ヘッダーベースの判定ロジックの誤動作を防止できる。

### ユースケース 2: 統合アップデート前のコードレベル事前レビュー

**シナリオ**: 変更管理プロセスが厳格な SOC で、統合の新バージョン適用前に変更内容の影響を評価したい。

**実装例**:
```
1. GitHub の chronicle/content-hub リポジトリで対象統合のコードを確認
2. 変更されたアクション・コネクタのロジックをレビュー
3. 問題がなければ Content Hub から統合を更新
4. 問題が発生した場合はバージョンロールバック機能で旧バージョンへ復帰
```

**効果**: リリースノートの記述だけでなく実装レベルで変更を把握でき、本番 SOAR 環境への影響を事前に評価できる。

## 関連サービス・機能

- **Google SecOps SOAR**: 本アップデートの対象である Response Integrations は、SOAR のプレイブック・コネクタ・ジョブの基盤となるコンポーネント
- **Content Hub**: 統合・ユースケース・Power Ups を検索・インストール・更新する入口。統合のリリースノート確認やバージョンロールバックもここから行う
- **Google SecOps SIEM**: コネクタで取り込んだアラート・イベントは SIEM の検索・検出機能と組み合わせて調査に活用できる

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261113-google-secops-marketplace-integration-updates.html)
- [公式リリースノート (Google Cloud Release Notes)](https://docs.cloud.google.com/release-notes#November_13_2026)
- [Google SecOps Marketplace Release Notes](https://docs.cloud.google.com/chronicle/docs/soar/marketplace-integrations/release-notes)
- [Response Integrations ドキュメント](https://docs.cloud.google.com/chronicle/docs/soar/marketplace-integrations)
- [Configure response integrations](https://docs.cloud.google.com/chronicle/docs/soar/respond/integrations-setup/configure-integrations)
- [Content Hub overview](https://docs.cloud.google.com/chronicle/docs/secops/content_hub)
- [GitHub: chronicle/content-hub](https://github.com/chronicle/content-hub)

## まとめ

今回のアップデートの目玉は、25 統合のソースコードが GitHub で公開され、Google SecOps の統合エコシステムの透明性が大きく向上した点です。あわせて、Microsoft Graph Mail / Delegated、Palo Alto Cortex XDR、Microsoft 365 Defender、Zscaler の修正は、メール調査やアラート同期、ドメイン制御の信頼性に直結します。該当統合を利用中の環境では、Content Hub で新バージョンへの更新を検討し、必要に応じて GitHub 上のソースコードで変更内容を事前確認することを推奨します。

---

**タグ**: Google SecOps, SOAR, Marketplace, Response Integrations, Content Hub, GitHub, Microsoft 365 Defender, Microsoft Graph Mail, Palo Alto Cortex XDR, Zscaler, セキュリティ
