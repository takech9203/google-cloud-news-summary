# Resource Manager (Essential Contacts): 書き込みオペレーションが Admin Activity 監査ログを生成するように変更

**リリース日**: 2026-11-13

**サービス**: Resource Manager (Essential Contacts)

**機能**: Essential Contacts v1 API 書き込みオペレーションの Admin Activity 監査ログ (ADMIN_WRITE) 生成

**ステータス**: Changed (仕様変更)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261113-resource-manager-essential-contacts-audit-logs.html)

## 概要

Essential Contacts の v1 API における書き込みオペレーション (`CreateContact`、`UpdateContact`、`DeleteContact`、`SendTestMessage`) が、従来の Data Access 監査ログ (DATA_WRITE) に加えて、Admin Activity 監査ログ (ADMIN_WRITE) も生成するようになりました。

Essential Contacts は、Google Cloud からの重要な通知 (課金、法務、セキュリティ、停止、技術情報など) を組織・フォルダ・プロジェクト単位で適切な担当チームに届けるための連絡先ディレクトリです。セキュリティ通知や停止通知の宛先となる連絡先の作成・変更・削除は、組織のガバナンス上重要な管理操作であり、今回の変更によりこれらの操作が常時記録される Admin Activity 監査ログで追跡可能になります。

Data Access 監査ログを Essential Contacts に対して有効化している環境では、これらの書き込みオペレーションの実行時に Admin Activity ログエントリと Data Access ログエントリの両方が生成される点に注意が必要です。

**アップデート前の課題**

- Essential Contacts の書き込みオペレーションは DATA_WRITE 権限タイプに紐づく Data Access 監査ログのみを生成していた
- Data Access 監査ログはデフォルトで無効のため、明示的に有効化していない環境では連絡先の作成・変更・削除・テストメッセージ送信の操作履歴が記録されなかった
- 重要通知の宛先という管理メタデータの変更を監査するには、Data Access 監査ログの有効化 (および追加のログ使用量の課金) が必要だった

**アップデート後の改善**

- 書き込みオペレーションが Admin Activity 監査ログ (ADMIN_WRITE) を生成するようになり、Admin Activity ログは常に書き込まれ、構成・除外・無効化ができないため、設定なしで操作履歴が確実に記録される
- 連絡先の変更操作を他の管理操作と同様に Admin Activity ログで一元的に監査できるようになった
- Data Access 監査ログを有効化している場合は、Admin Activity と Data Access の両方のログエントリが生成され、監査証跡がより網羅的になった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Before["変更前"]
        U1([👤 管理者]) -->|CreateContact / UpdateContact / DeleteContact / SendTestMessage| EC1["📇 Essential Contacts v1 API"]
        EC1 -->|DATA_WRITE<br>(Data Access 有効時のみ)| DA1[("📘 Data Access 監査ログ")]
    end

    subgraph After["変更後"]
        U2([👤 管理者]) -->|CreateContact / UpdateContact / DeleteContact / SendTestMessage| EC2["📇 Essential Contacts v1 API"]
        EC2 -->|ADMIN_WRITE<br>(常時記録)| AA2[("📕 Admin Activity 監査ログ")]
        EC2 -->|DATA_WRITE<br>(Data Access 有効時のみ)| DA2[("📘 Data Access 監査ログ")]
    end
```

変更前は Data Access 監査ログを有効化した場合にのみ書き込み操作が記録されていましたが、変更後は常時記録される Admin Activity 監査ログにも書き込まれ、Data Access 監査ログ有効時には両方のログエントリが生成されます。

## サービスアップデートの詳細

### 主要機能

1. **書き込みオペレーションの Admin Activity 監査ログ生成**
   - v1 API の `CreateContact`、`UpdateContact`、`DeleteContact`、`SendTestMessage` が ADMIN_WRITE タイプの Admin Activity 監査ログを生成
   - Admin Activity 監査ログは常に書き込まれ、構成・除外・無効化は不可 (Cloud Logging API を無効化しても生成される)

2. **Data Access 監査ログとの併存**
   - Essential Contacts の Data Access 監査ログを有効化している場合、対象の書き込みオペレーションは Admin Activity ログエントリと Data Access ログエントリの両方を生成
   - 読み取り系オペレーション (`GetContact`、`ListContacts`、`ComputeContacts`) は従来どおり DATA_READ として Data Access 監査ログのみを生成

### ログの確認方法

Logs Explorer で以下のクエリを実行することで、Essential Contacts の監査ログを確認できます。

```
protoPayload.serviceName="essentialcontacts.googleapis.com"
```

特定のメソッドに絞り込む場合:

```
protoPayload.serviceName="essentialcontacts.googleapis.com"
protoPayload.methodName="google.cloud.essentialcontacts.v1.EssentialContactsService.CreateContact"
```

## 技術仕様

### 対象オペレーションと監査ログの種類

| メソッド (v1) | 必要な権限 | 権限タイプ | 生成される監査ログ (変更後) |
|------|------|------|------|
| `CreateContact` | `essentialcontacts.contacts.create` | DATA_WRITE | Admin Activity + Data Access (有効時) |
| `UpdateContact` | `essentialcontacts.contacts.update` | DATA_WRITE | Admin Activity + Data Access (有効時) |
| `DeleteContact` | `essentialcontacts.contacts.delete` | DATA_WRITE | Admin Activity + Data Access (有効時) |
| `SendTestMessage` | `essentialcontacts.contacts.send` | DATA_WRITE | Admin Activity + Data Access (有効時) |
| `GetContact` | `essentialcontacts.contacts.get` | DATA_READ | Data Access (有効時) |
| `ListContacts` | `essentialcontacts.contacts.list` | DATA_READ | Data Access (有効時) |
| `ComputeContacts` | `essentialcontacts.contacts.get` / `list` | DATA_READ | Data Access (有効時) |

### 監査ログの種類の比較

| 項目 | Admin Activity 監査ログ | Data Access 監査ログ |
|------|------|------|
| 記録対象 | リソースの構成やメタデータを変更する操作 | リソースの構成・メタデータの読み取り、ユーザー提供データの読み書き |
| デフォルト | 常に有効 (無効化不可) | デフォルト無効 (BigQuery を除く)。明示的な有効化が必要 |
| 課金への影響 | — | 有効化によりログ使用量の追加課金が発生する可能性あり |

## メリット

### ビジネス面

- **コンプライアンス対応の強化**: 重要通知の宛先 (セキュリティ、課金、法務、停止など) の変更操作が常時記録されるため、監査要件への対応が容易になる
- **インシデント調査の確実性**: Data Access 監査ログの有効化を忘れていた場合でも、「いつ・誰が・どの連絡先を変更したか」を Admin Activity ログから遡って確認できる

### 技術面

- **設定不要の監査証跡**: Admin Activity 監査ログは構成なしで常に書き込まれるため、追加設定なく書き込み操作を追跡できる
- **他の管理操作との一元的な監視**: 他サービスの ADMIN_WRITE 操作と同じ Admin Activity ログで扱えるため、ログシンクやアラートの既存の仕組みに統合しやすい

## デメリット・制約事項

### 考慮すべき点

- Essential Contacts の Data Access 監査ログを有効化している環境では、1 回の書き込みオペレーションで Admin Activity と Data Access の 2 つのログエントリが生成される。ログ件数を前提としたアラートや集計 (操作回数のカウントなど) を構築している場合は、二重カウントにならないかの確認が必要
- 対象は v1 API の書き込みオペレーション。読み取り系オペレーションの監査ログの扱いに変更はない

## ユースケース

### ユースケース 1: セキュリティ連絡先の変更監視

**シナリオ**: セキュリティ通知の宛先が不正に変更・削除されると重要なアラートを見逃すリスクがあるため、連絡先の変更を検知してセキュリティチームに通知したい。

**実装例** (ログベースのアラート用クエリ):
```
logName:"cloudaudit.googleapis.com%2Factivity"
protoPayload.serviceName="essentialcontacts.googleapis.com"
protoPayload.methodName=~"(CreateContact|UpdateContact|DeleteContact)"
```

**効果**: Data Access 監査ログを有効化していなくても、Admin Activity ログに常時記録されるため、連絡先変更の検知漏れを防止できる。

### ユースケース 2: 監査対応での操作履歴の提示

**シナリオ**: 内部監査や外部監査で、重要通知の宛先設定 (Essential Contacts) の変更履歴の提示を求められた。

**効果**: Admin Activity 監査ログから変更操作の実行者・日時・内容を遡って提示できる。従来は Data Access 監査ログの事前有効化が前提だったが、今回の変更以降の操作は常時記録される。

## 料金

Essential Contacts 自体の料金に変更はありません。監査ログに関しては以下のとおりです。

- Admin Activity 監査ログは常に書き込まれます。Data Access 監査ログを有効化すると、ログ使用量の追加課金が発生する可能性があります
- 詳細は [Cloud Logging の料金](https://docs.cloud.google.com/stackdriver/pricing#logs-pricing-summary) を参照してください

## 関連サービス・機能

- **Cloud Audit Logs / Cloud Logging**: 今回の変更で生成される Admin Activity・Data Access 監査ログの保存・検索・ルーティングを担う。Logs Explorer でのクエリやログシンクによる長期保管と組み合わせて利用する
- **Resource Manager (リソース階層)**: Essential Contacts は組織・フォルダ・プロジェクトの各階層に設定でき、階層を通じて継承される。監査ログも対象リソースの階層で記録される
- **Advisory Notifications**: Essential Contacts の連絡先情報を参照して、セキュリティ・プライバシー関連の重要通知を Google Cloud コンソールに表示するサービス

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261113-resource-manager-essential-contacts-audit-logs.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#November_13_2026)
- [Essential Contacts の監査ロギング (Admin Activity 書き込みログ)](https://docs.cloud.google.com/resource-manager/docs/essential-contacts-audit-logging#admin-activity-write-logs)
- [Cloud Audit Logs の概要 (Admin Activity 監査ログ)](https://docs.cloud.google.com/logging/docs/audit#admin-activity)
- [Essential Contacts の概要](https://docs.cloud.google.com/resource-manager/docs/managing-notification-contacts)
- [Data Access 監査ログの有効化](https://docs.cloud.google.com/logging/docs/audit/configure-data-access)
- [Cloud Logging の料金](https://docs.cloud.google.com/stackdriver/pricing#logs-pricing-summary)

## まとめ

Essential Contacts の連絡先に対する書き込みオペレーションが、設定不要で常時記録される Admin Activity 監査ログ (ADMIN_WRITE) を生成するようになり、重要通知の宛先変更に対する監査証跡が強化されました。Data Access 監査ログを有効化している環境では同一操作で 2 つのログエントリが生成されるため、ログ件数に依存するアラートや集計ロジックの見直しを推奨します。

---

**タグ**: #ResourceManager #EssentialContacts #CloudAuditLogs #AdminActivity #CloudLogging #セキュリティ #監査
