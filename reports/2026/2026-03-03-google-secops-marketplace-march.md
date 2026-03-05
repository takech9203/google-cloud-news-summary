# Google SecOps Marketplace: コネクタ一括アップデート (2026年3月)

**リリース日**: 2026-03-03

**サービス**: Google SecOps Marketplace

**機能**: Marketplace Connector Updates - March 2026

**ステータス**: GA

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260303-google-secops-marketplace-march.html)

## 概要

Google SecOps (旧 Chronicle SOAR) の Marketplace において、9 つのインテグレーション/コネクタが一斉にアップデートされた。対象は Akamai、Siemplify、Microsoft Graph Mail、Google Chronicle、Microsoft Graph Mail Delegated、AWS GuardDuty、Google Security Command Center、CrowdStrike Falcon、Splunk と多岐にわたり、セキュリティオペレーション基盤の広範な機能強化が行われている。

今回のアップデートでは、新しいアクションやジョブの追加 (Akamai、Siemplify)、フォルダ処理の改善 (Microsoft Graph Mail 系)、ログデータ処理の更新 (Google Chronicle)、重大度ハンドリングの改善 (AWS GuardDuty)、ミュート状態処理の更新 (Security Command Center)、IOC 有効期限や隠しホストのサポート (CrowdStrike Falcon)、入力処理の改善 (Splunk) など、各コネクタの実用性と信頼性が向上している。

セキュリティチームや SOC アナリストにとって、日常的なインシデント対応ワークフローの精度と効率が高まるアップデートである。

**アップデート前の課題**

- Akamai 連携でクライアントリストのアクティベーション操作を SOAR プラットフォームから直接実行できなかった
- Microsoft Graph Mail のフォルダ処理において、特定の条件下でフォルダの指定やネストされたフォルダの取り扱いに制限があった
- Google Chronicle の UDM クエリや検出詳細取得時に、生ログデータの処理が最適化されていなかった
- CrowdStrike Falcon の IOC に有効期限を設定できず、隠しホストの管理にも対応していなかった
- AWS GuardDuty の Findings Connector において重大度のハンドリングが限定的だった

**アップデート後の改善**

- Akamai v2.0 で「Activate Client List」アクションが追加され、SOAR ワークフロー内で直接クライアントリストを有効化できるようになった
- Microsoft Graph Mail v36.0 および Delegated v13.0 でフォルダ処理が改善され、Forward/Save/Send Email アクションの安定性が向上した
- Google Chronicle v78.0 で生ログデータ処理が更新され、検出詳細と UDM クエリの精度が向上した
- CrowdStrike Falcon v71.0 で IOC の有効期限設定と隠しホストのサポートが追加された
- AWS GuardDuty v9.0 で重大度ハンドリングが改善され、より正確なアラートの優先度付けが可能になった

## アーキテクチャ図

```mermaid
architecture-beta
    group soar(cloud)[Google SecOps SOAR Platform]

    service marketplace(server)[Marketplace] in soar
    service playbook(disk)[Playbook Engine] in soar
    service cases(database)[Cases DB] in soar

    group connectors(cloud)[Updated Connectors]

    service akamai(server)[Akamai v2.0] in connectors
    service msgraph(server)[MS Graph Mail v36.0] in connectors
    service chronicle(server)[Chronicle v78.0] in connectors
    service crowdstrike(server)[CrowdStrike v71.0] in connectors
    service guardduty(server)[AWS GuardDuty v9.0] in connectors
    service scc(server)[SCC v15.0] in connectors
    service splunk(server)[Splunk v61.0] in connectors
    service siemplify(server)[Siemplify v103.0] in connectors

    marketplace:R --> L:akamai
    marketplace:R --> L:msgraph
    marketplace:R --> L:chronicle
    marketplace:R --> L:crowdstrike
    marketplace:R --> L:guardduty
    marketplace:R --> L:scc
    marketplace:R --> L:splunk
    marketplace:R --> L:siemplify

    playbook:R --> L:marketplace
    cases:R --> L:playbook
```

Google SecOps SOAR プラットフォームの Marketplace を通じて、各セキュリティ製品とのインテグレーションが更新される。コネクタは外部サービスからデータを取り込み、Playbook Engine を経由してケース管理に反映される。

## サービスアップデートの詳細

### 主要機能

1. **Akamai v2.0 - Activate Client List アクション**
   - 新しい「Activate Client List」アクションが追加された
   - SOAR のプレイブック内から Akamai のクライアントリストをアクティベートできるようになり、脅威インテリジェンスに基づく自動ブロックリスト管理が可能になった

2. **Siemplify v103.0 - Response Integration & Connector Upgrade ジョブ**
   - 新しいジョブ「Response Integration & Connector Upgrade」が追加された
   - インテグレーションとコネクタのアップグレードプロセスを自動化し、運用負荷を軽減する

3. **Microsoft Graph Mail v36.0 - フォルダ処理の改善**
   - Forward Email、Save Email to File、Send Email アクションにおけるフォルダ処理が更新された
   - コネクタのフォルダハンドリングも改善され、サブフォルダを含む複雑なフォルダ構成での動作が安定化した

4. **Google Chronicle v78.0 - 生ログデータ処理の更新**
   - Get Detection Details アクションの生ログデータ処理が更新された
   - Execute UDM Query アクションの生ログデータ処理も同様に更新され、クエリ結果の正確性が向上した

5. **Microsoft Graph Mail Delegated v13.0 - フォルダ処理の改善**
   - 委任認証版の Microsoft Graph Mail コネクタでもフォルダ処理が更新された
   - v36.0 と同様の改善が適用されている

6. **AWS GuardDuty v9.0 - 重大度ハンドリングの改善**
   - Findings Connector における重大度 (severity) の処理が更新された
   - GuardDuty の重大度スコアがより正確に Google SecOps のアラート優先度にマッピングされるようになった

7. **Google Security Command Center v15.0 - ミュート状態処理の更新**
   - List Asset Vulnerabilities アクションにおけるミュート状態の処理が更新された
   - ミュートされた脆弱性の取り扱いがより正確になり、アラートノイズの削減に貢献する

8. **CrowdStrike Falcon v71.0 - IOC 有効期限と隠しホスト対応**
   - IOC (Indicator of Compromise) に有効期限を設定できるようになった
   - 隠しホスト (Hidden Hosts) のサポートが追加され、非アクティブなホストの管理が改善された

9. **Splunk v61.0 - Notable Events 入力処理の改善**
   - Update Notable Events アクションにおける入力処理が更新された
   - Splunk Enterprise Security との連携における Notable Events の更新操作がより堅牢になった

## 技術仕様

### コネクタバージョン一覧

| コネクタ | バージョン | 主な変更点 |
|----------|------------|------------|
| Akamai | v2.0 | 新アクション追加 |
| Siemplify | v103.0 | 新ジョブ追加 |
| Microsoft Graph Mail | v36.0 | フォルダ処理改善 |
| Google Chronicle | v78.0 | 生ログデータ処理更新 |
| MS Graph Mail Delegated | v13.0 | フォルダ処理改善 |
| AWS GuardDuty | v9.0 | 重大度ハンドリング改善 |
| Google SCC | v15.0 | ミュート状態処理更新 |
| CrowdStrike Falcon | v71.0 | IOC 有効期限、隠しホスト対応 |
| Splunk | v61.0 | 入力処理改善 |

### CrowdStrike Falcon の必要な権限

CrowdStrike Falcon コネクタでは、機能に応じて以下の権限が必要となる:

| コネクタ | 必要な権限 |
|----------|------------|
| CrowdStrike Detections Connector | Detection.Read |
| CrowdStrike Falcon Streaming Events Connector | Event streams.Read |
| CrowdStrike Identity Protection Detections Connector | Alerts.Read |
| CrowdStrike Incidents Connector | Incidents.Read |

## 設定方法

### 前提条件

1. Google SecOps SOAR コンソールへの管理者アクセス権
2. 各外部サービス (Akamai、CrowdStrike、AWS、Splunk など) の API 認証情報
3. Marketplace でのインテグレーションアップグレード権限

### 手順

#### ステップ 1: コネクタのアップグレード

Google SecOps SOAR コンソールで Marketplace に移動し、対象のインテグレーションを検索して「Upgrade to (バージョン番号)」をクリックする。

#### ステップ 2: コネクタの手動更新

インテグレーションにコネクタが設定されている場合、アップグレード後にコネクタの手動更新が必要となる。Settings > Ingestion > Connectors で対象コネクタを選択し「Update」をクリックする。

#### ステップ 3: 動作確認

アップグレード後、各コネクタの Ping アクションを実行して接続性を確認する。その後、実際のデータ取り込みが正常に行われているかをケース画面で確認する。

## メリット

### ビジネス面

- **セキュリティ運用の効率化**: 9 つのコネクタが同時に強化され、SOC チームの日常業務における摩擦が軽減される
- **マルチベンダー環境の管理改善**: CrowdStrike、AWS、Splunk、Microsoft など主要なセキュリティベンダーとの連携品質が向上し、統合セキュリティ運用が容易になる

### 技術面

- **データ処理の精度向上**: Google Chronicle の生ログデータ処理や AWS GuardDuty の重大度マッピングの改善により、アラートの正確性が向上する
- **自動化の範囲拡大**: Akamai のクライアントリストアクティベーションや CrowdStrike の IOC 有効期限設定により、プレイブックで自動化できる範囲が広がった
- **ステートレスアーキテクチャとの互換性**: Google SecOps のステートレスコネクタアーキテクチャに対応した更新により、スケーラビリティと信頼性が維持される

## デメリット・制約事項

### 制限事項

- コネクタのアップグレード時、コネクタの状態がファイルシステムからコネクタコンテキストに自動移行されないため、初回実行時に重複ケースが発生する可能性がある
- ステートレスコネクタのデータストレージにはデフォルトで 300 万文字の制限がある

### 考慮すべき点

- 複数のコネクタを同時にアップグレードする場合、段階的に実施してそれぞれの動作を確認することが推奨される
- CrowdStrike Falcon の一部アクションはプレミアムバージョンが必要
- アップグレード後はプレイブックのテスト実行を行い、既存のワークフローに影響がないことを確認すべきである

## ユースケース

### ユースケース 1: 脅威インテリジェンスに基づく自動ブロック

**シナリオ**: SOC チームが CrowdStrike Falcon で検出した IOC を Akamai のクライアントリストに自動登録し、有効期限付きでブロックする。

**効果**: CrowdStrike Falcon v71.0 の IOC 有効期限サポートと Akamai v2.0 の Activate Client List アクションを組み合わせることで、脅威検出からネットワークレベルでのブロックまでを自動化できる。有効期限の設定により、古い IOC が自動的に失効し、誤検知によるビジネス影響を最小限に抑える。

### ユースケース 2: メールフィッシング対応の自動化

**シナリオ**: Microsoft Graph Mail コネクタでフィッシングメールを検出し、プレイブックで自動的に特定フォルダへの移動や転送を行う。

**効果**: Microsoft Graph Mail v36.0 のフォルダ処理改善により、サブフォルダを含む複雑なメールボックス構成でもフィッシングメールの自動分類と隔離が安定して動作する。委任認証版 (v13.0) も同様に改善されているため、共有メールボックスにも対応可能。

## 料金

Google SecOps Marketplace のコネクタ更新自体に追加料金は発生しない。料金は Google SecOps (Chronicle SOAR) のライセンスに含まれる。

詳細な料金体系については Google Cloud の営業担当に問い合わせるか、以下のページを参照のこと。

## 関連サービス・機能

- **Google SecOps (Chronicle SIEM)**: ログの取り込みと検出エンジンを提供。Chronicle v78.0 の生ログデータ処理改善は SIEM 側のデータ品質にも影響する
- **Google Security Command Center**: クラウド環境の脆弱性とセキュリティ態勢管理を提供。v15.0 でミュート状態処理が改善された
- **Google SecOps Playbooks**: コネクタが取り込んだデータに基づいて自動応答を実行するエンジン。今回のアップデートにより自動化可能な範囲が拡大
- **VirusTotal**: 脅威インテリジェンスプラットフォーム。CrowdStrike Falcon の IOC データと組み合わせた脅威分析に活用できる

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260303-google-secops-marketplace-march.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#March_03_2026)
- [Google SecOps SOAR Marketplace ドキュメント](https://cloud.google.com/chronicle/docs/soar/marketplace-integrations)
- [CrowdStrike Falcon インテグレーション](https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/crowdstrike-falcon)
- [Microsoft Graph Mail インテグレーション](https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/microsoft-graph-mail)
- [ステートレスコネクタ ホワイトペーパー](https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/stateless-connectors-white-paper)
- [Security Command Center SOAR 連携](https://cloud.google.com/security-command-center/docs/how-to-configure-secops-soar)

## まとめ

今回の Google SecOps Marketplace 一括アップデートは、セキュリティ運用の中核を担う 9 つのコネクタを同時に強化するものであり、SOC チームの業務効率と検出精度の向上に直結する。特に CrowdStrike Falcon の IOC 有効期限サポートや Akamai のクライアントリスト操作は、脅威対応の自動化を大きく前進させる。Google SecOps を利用している組織は、各コネクタのアップグレードを計画的に実施し、プレイブックの動作確認を行うことを推奨する。

---

**タグ**: #GoogleSecOps #ChronicleSOAR #Marketplace #CrowdStrike #MicrosoftGraphMail #AWSGuardDuty #SecurityCommandCenter #Splunk #Akamai #コネクタ #セキュリティ運用
