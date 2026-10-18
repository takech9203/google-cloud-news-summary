# Google Cloud Contact Center as a Service: Advanced Reporting ダッシュボード 6.16 プレリリースノート

**リリース日**: 2026-10-16 (プレリリースノート公開日)

**サービス**: Google Cloud Contact Center as a Service (CCAI Platform)

**機能**: Advanced reporting dashboards プレリリースノート 6.16 (フィルター動作の統一、Channel 値の補完、Actor 値の標準化など多数の修正)

**ステータス**: プレリリース (次期バージョンの事前公開情報)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261016-ccaas-6-16-advanced-reporting-prerelease.html)

## 概要

CCAI Platform の advanced reporting dashboards およびその他のレポーティング機能に関するプレリリースノート 6.16 が公開されました。**これは正式リリース前の事前公開情報であり、Google は「これらのアップデートをリリースする際、新しい機能はここに示すとおりになる見込み」としています。また、リリース時の advanced reporting dashboards のバージョンは 6.16 より大きくなる可能性があります。**

本リリースは新機能の追加ではなく、ダッシュボードの修正 (Fixed) に特化した内容です。中心となるのは advanced reporting のフィルタープロンプトの大規模な改善で、全ダッシュボードで一貫した動作となり、Agent Name や Location、Disposition Codes など多くのドロップダウンが設定済みの値の完全なリストを表示するようになります。加えて、Real-time Agent Monitoring ダッシュボードでの冗長なデータベースクエリの修正、ライブ/履歴ダッシュボードで空白だった Channel 値の補完、Agent Audit ダッシュボードのタイムスタンプ列の表示・ソート修正などが含まれます。

一方で、既存の運用に影響する変更も含まれます。インタラクションの応答・終了・切断を示す Actor 値が Human Agent / Virtual Agent / End User / System に標準化されるため、**旧表記を使用していた保存済みフィルター、Look、スケジュールは再選択が必要**です。また、消費者電話番号フィルターが単一値のみを受け付けるようになり、Missed Interactions ダッシュボードの Activity Status 列・フィルターは Projection Result に名称変更されます。レポーティングを運用するスーパーバイザーや管理者は、正式リリース前に影響範囲を確認しておくことが推奨されます。

**アップデート前の課題**

- フィルタープロンプトの動作がダッシュボードごとに不統一で、Agent Name、Agent Email、Agent Custom ID、Agent Teams、Location、Language、Answered By、Projection Result などのドロップダウンが空または部分的なリストしか返さないことがあった
- Disposition Codes / Disposition List フィルターにインスタンスへ設定したコードが表示されず、Call Status / Deflection Type フィルターにはデータ上存在する値がリストから欠落していた
- Queue Group、Queue、Agent Team、Disposition Code、Location、Role、Skill の名前変更がフィルタードロップダウンに反映されるまで最大 6 時間かかっていた
- internal、API-initiated、campaign、UCaaS、callback、extension calls といったインタラクションタイプで、ライブの Voice / Chat ダッシュボードおよび履歴 Chat ダッシュボードの Channel が空白のまま表示されていた
- Real-time Agent Monitoring ダッシュボードの Agent Performance タイルが、自動更新のたびに冗長なデータベースクエリを実行していた
- Agent Audit ダッシュボードの Change Details テーブルでタイムスタンプ列が表示されず、正しくソートできなかった
- インタラクションの応答・終了・切断を示す Actor 値の表記が標準化されておらず、ライブ Queued ダッシュボードの Projecting フィルターはクリアできなかった

**アップデート後の改善**

- フィルタープロンプトが全ダッシュボードで一貫した動作になり、リストベースのフィルターは初回クリックで検索可能なリストを直接開き、各ドロップダウンが設定済みの値の完全なリストを表示する
- 設定の名前変更がフィルタードロップダウンに最大 6 時間ではなく 30 分以内に反映される
- Channel が、以前空白だったインタラクションタイプについてもライブの Voice / Chat ダッシュボードと履歴 Chat ダッシュボードで値を報告する
- Agent Performance タイルの冗長なデータベースクエリが解消され、Agent Audit ダッシュボードの Change Details テーブルがタイムスタンプ列を表示して正しくソートする
- Actor 値が Human Agent / Virtual Agent / End User / System に標準化され、Missed Interactions ダッシュボードの Activity Status が Projection Result に名称変更されて用語が整理される

## サービスアップデートの詳細

### 主要な修正内容

1. **パフォーマンスの修正**
   - Real-time Agent Monitoring ダッシュボードの Agent Performance タイルが、自動更新時に冗長なデータベースクエリを実行していた問題を修正

2. **フィルタープロンプトの一貫性向上と完全なリスト表示**
   - リストベースのフィルターが初回クリックで検索可能なリストを直接開くように変更
   - 以前は空または部分的なリストを返していた以下のドロップダウンが、設定済みの値の完全なリストを表示: Agent Name、Agent Email、Agent Custom ID、Agent Teams、Location、Language、Answered By、Projection Result
   - Disposition Codes / Disposition List フィルターが、インスタンスに設定されたコードを表示
   - Agent Teams / Team Name フィルターが、エージェントに割り当てられたいずれかのチームでマッチするように変更
   - 設定の名前変更 (Queue Group、Queue、Agent Team、Disposition Code、Location、Role、Skill) が、フィルタードロップダウンに最大 6 時間ではなく 30 分以内に反映
   - ライブ Queued ダッシュボードの Projecting フィルターがクリア可能になり、すべてのキュー内インタラクションの表示にリセットできる (選択肢は Yes のみ提供)
   - 定義済み値リストのないフィールド (消費者電話番号、ID フィールドなど) は、演算子付きのプレーンテキストボックスを表示し、値を直接入力できる
   - Call Status / Deflection Type フィルターが、データに存在するものの以前はリストから欠落していた値を表示

3. **データ表示の修正**
   - Channel が、以前空白だったインタラクションタイプ (internal、API-initiated、campaign、UCaaS、callback、extension calls) について、ライブの Voice / Chat ダッシュボードおよび履歴 Chat ダッシュボードで値を報告
   - Agent Audit ダッシュボードの Change Details テーブルがタイムスタンプ列を表示し、正しくソート

4. **仕様変更 (既存運用に影響する可能性あり)**
   - 消費者電話番号フィルターが複数値ではなく単一値を受け付けるように変更。複数の番号を渡す保存済みフィルターやリンクは 1 つの番号のみ適用される
   - Missed Interactions ダッシュボードで、Activity Status 列・フィルターを Projection Result に名称変更
   - インタラクションの応答・終了・切断を示す Actor 値を Human Agent、Virtual Agent、End User、System に標準化。旧表記を使用していた保存済みフィルター、Look、スケジュールは再選択が必要

## 技術仕様

### フィルター動作の Before / After

| 項目 | 変更前 | 変更後 |
|------|--------|--------|
| リストベースのフィルター | - | 初回クリックで検索可能なリストを直接開く |
| Agent Name / Agent Email / Agent Custom ID / Agent Teams / Location / Language / Answered By / Projection Result | 空または部分的なリストを返すことがあった | 設定済みの値の完全なリストを表示 |
| Disposition Codes / Disposition List | 設定済みコードが表示されないことがあった | インスタンスに設定されたコードを表示 |
| Agent Teams / Team Name | - | 割り当てられたいずれかのチームでエージェントにマッチ |
| 設定の名前変更の反映時間 | 最大 6 時間 | 30 分以内 |
| ライブ Queued の Projecting フィルター | クリア不可 | クリア可能 (選択肢は Yes のみ) |
| 定義済みリストのないフィールド (電話番号、ID など) | - | 演算子付きプレーンテキストボックスで直接入力 |
| Call Status / Deflection Type | データに存在する値がリストから欠落 | 欠落していた値を表示 |
| 消費者電話番号フィルター | 複数値を受け付け | 単一値のみ受け付け |

### 名称・値の標準化

| 項目 | 変更前 | 変更後 |
|------|--------|--------|
| Missed Interactions の列・フィルター名 | Activity Status | Projection Result |
| Actor 値 (応答・終了・切断の主体) | 標準化されていない旧表記 | Human Agent / Virtual Agent / End User / System |
| Channel 値 (internal、API-initiated、campaign、UCaaS、callback、extension calls) | 空白 | ライブ Voice / Chat および履歴 Chat ダッシュボードで値を報告 |

## メリット

### ビジネス面

- **レポート作成の効率化**: フィルターが設定済みの値の完全なリストを表示するため、スーパーバイザーや管理者が目的のエージェント・チーム・ディスポジションコードを確実に絞り込め、分析作業の手戻りが減る
- **運用変更の反映が迅速に**: キューやチーム名などの構成変更が 30 分以内にフィルターへ反映されるため、組織変更直後でも最新の構成でレポートを作成できる

### 技術面

- **ダッシュボードの負荷軽減**: Agent Performance タイルの冗長なデータベースクエリが解消され、Real-time Agent Monitoring の自動更新が効率化される
- **データの網羅性・一貫性向上**: 空白だった Channel 値の補完、リストから欠落していたフィルター値の表示、Actor 値の標準化により、ダッシュボード間でのデータの突き合わせや集計の信頼性が高まる

## デメリット・制約事項

### 制限事項

- **プレリリースノートである点に注意**: 本内容は次期アップデートの予定であり、正式リリース時に変更される可能性がある。また、リリース時のバージョンは 6.16 より大きくなる可能性がある
- 消費者電話番号フィルターは単一値のみを受け付けるようになる。複数の番号を渡していた保存済みフィルターやリンクは 1 つの番号のみ適用される
- ライブ Queued ダッシュボードの Projecting フィルターの選択肢は Yes のみ

### 考慮すべき点

- **Actor 値の標準化は破壊的変更**: 旧表記の Actor 値を使用していた保存済みフィルター、Look、スケジュールは、リリース後に再選択 (再設定) が必要
- Missed Interactions ダッシュボードの Activity Status を参照していた運用手順やドキュメントは、Projection Result への名称変更に合わせた更新が必要
- Channel 値が新たに報告されるインタラクションタイプ (internal、API-initiated、campaign など) により、Channel ベースの集計値が従来と変わる可能性があるため、既存レポートとの比較時に注意が必要

## ユースケース

### ユースケース 1: 組織変更直後のチーム別パフォーマンス分析

**シナリオ**: コンタクトセンターの組織再編でエージェントチーム名やキューグループ名を変更した直後に、スーパーバイザーが新しいチーム名でダッシュボードをフィルタリングして当日のパフォーマンスを確認する。

**効果**: 従来は名前変更の反映に最大 6 時間かかっていたが、30 分以内にフィルタードロップダウンへ反映されるため、組織変更当日から新体制でのモニタリングを開始できる。複数チームに所属するエージェントも、いずれかの所属チームでマッチするため漏れなく抽出できる。

### ユースケース 2: 保存済みフィルター・Look の棚卸しと移行準備

**シナリオ**: レポーティング管理者が、正式リリースに先立ち、旧表記の Actor 値や Activity Status、複数の消費者電話番号を使用している保存済みフィルター・Look・スケジュール済みレポートを棚卸しする。

**効果**: Actor 値の標準化 (Human Agent / Virtual Agent / End User / System) と Projection Result への名称変更の影響を受ける資産を事前に特定でき、リリース後のレポート欠落や誤ったフィルタリングを防止できる。

## 料金

本プレリリースノートに料金に関する記載はありません。CCAI Platform の料金については公式ドキュメントを参照してください。

- [CCAI Platform ドキュメント](https://docs.cloud.google.com/contact-center/ccai-platform/docs)

## 利用可能リージョン

Advanced reporting dashboards は以下のリージョンでのみ利用可能です (インスタンスがこれらのリージョンにない場合、advanced reporting 拡張機能は有効化できません)。

- us-east1、us-central1、us-west1、europe-west2、asia-northeast1、northamerica-northeast1、australia-southeast1、southamerica-east1

## 関連サービス・機能

- **Advanced Reporting Landing Page**: タイルからのカスタムダッシュボード作成、Look の作成・リンク、ダッシュボード編集などの高度な機能を提供する入口。今回修正される Look やスケジュールはこの機能群の一部
- **Real-time Agent Monitoring / Missed Interactions / Agent Audit (Audit Log) ダッシュボード**: 今回の修正対象となる個別ダッシュボード。エージェントのリアルタイム監視、ミスしたインタラクションの分析、インスタンス設定変更の監査にそれぞれ使用する
- **バーチャルエージェント (Virtual Agent)**: Actor 値の標準化で Human Agent と並ぶ応答主体として明示される。人間と仮想エージェントの対応切り分け分析に関連する

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261016-ccaas-6-16-advanced-reporting-prerelease.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#October_16_2026)
- [CCAI Platform リリースノート](https://docs.cloud.google.com/contact-center/ccai-platform/docs/release-notes)
- [Advanced reporting ダッシュボードの概要](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-overview)
- [Advanced reporting の高度な機能](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-advanced-capabilities)
- [Missed Interactions ダッシュボード](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-missed-interactions)
- [Audit Log ダッシュボード](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-audit-log)

## まとめ

CCAI Platform の advanced reporting dashboards 6.16 プレリリースノートは、新機能ではなくフィルター動作の統一、空白データの補完、パフォーマンス改善を中心とした修正リリースの予告です。多くはレポート作成体験を改善するものですが、Actor 値の標準化、消費者電話番号フィルターの単一値化、Activity Status の名称変更は既存の保存済みフィルター・Look・スケジュールに影響します。レポーティングを運用するチームは、正式リリース前に影響を受ける資産を棚卸しし、リリース後に速やかに再設定できるよう準備しておくことを推奨します。

---

**タグ**: #CCaaS #ContactCenter #CCAIPlatform #AdvancedReporting #Dashboard #プレリリース
