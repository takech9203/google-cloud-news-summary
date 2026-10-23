# Google Cloud Contact Center as a Service (CCAI Platform): 高度なレポートダッシュボード プレリリースノート 6.24

**リリース日**: 2026-10-22

**サービス**: Google Cloud Contact Center as a Service (CCAI Platform)

**機能**: 高度なレポートダッシュボード (Advanced Reporting Dashboards) プレリリースノート 6.24

**ステータス**: アナウンス (プレリリースノート) / 修正 (Fixed)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261022-ccaas-advanced-reporting-dashboards-6-24.html)

## 概要

Google Cloud Contact Center as a Service (CCAI Platform) の高度なレポートダッシュボード (Advanced Reporting Dashboards) について、バージョン 6.24 のプレリリースノートが公開されました。プレリリースノートは、今後リリースされるアップデートの内容を事前に知らせるもので、リリース時には記載どおりの機能・修正が提供される見込みです。なお、公式リリースノートには「実際にリリースされる次のバージョンは 6.24 より大きい番号になる可能性がある」と明記されています。

今回のバージョン 6.24 は新機能の追加ではなく、レポーティング機能の不具合修正 (Fixed) が中心です。ダッシュボードの表示崩れ、ダウンロードレポートにおけるデータ欠落、多言語環境 (フランス語・スペイン語・カナダフランス語) でのキュー名や指標名の翻訳不備、長期間の日付範囲指定時の通話ディスポジション (対応結果) フィールドの空白表示など、コンタクトセンターの運用レポートの正確性に直結する 7 件の問題が修正されます。

コンタクトセンターの KPI 管理やエージェントパフォーマンス評価にレポートを利用している管理者・スーパーバイザーにとって、これまで集計から漏れていた「エージェントに割り当てられなかった通話・チャット (放棄、デフレクト、期限切れ)」や「キューなしの発信通話」がレポートに正しく含まれるようになる点は、レポート値の解釈に影響し得る重要な変更です。

**アップデート前の課題**

このアップデート以前には、以下の問題が存在していました。

- ワイドスクリーンディスプレイで、Dashboard Reports のセレクタ内の通話タイプ・チャットタイプ名が途中で切れて表示されていた
- 全エージェント対象で Individual Call History / Individual Chat History レポートを実行した際、選択期間中にアクティビティのあったエージェントが 1 名以下の場合、エージェントに一度も割り当てられなかった通話・チャット (放棄、デフレクト、期限切れなど) がレポートから欠落していた
- 全エージェント対象で Interactions Detail by Agent レポートを生成すると、キューを経由せずに発信されたアウトバウンド通話が欠落していた
- Real-time Queue Monitoring および Campaign ダッシュボードで、フランス語・スペイン語のインタラクションに対して英語のキュー名が誤って表示されていた
- 高度なレポートの「ラップアップ (wrap-up)」「保留 (hold)」指標のカナダフランス語 (fr_CA) 翻訳に一貫性がなく、不正確だった
- Real-time Queue Monitoring と高度なレポートダッシュボードで、スペイン語チャットキューに英語の名前が誤って表示されていた
- 46 日から 365 日の間の日付範囲を表示すると、ダッシュボードの通話ディスポジションフィールドが空白になっていた

**アップデート後の改善**

バージョン 6.24 のリリースにより、以下が改善される見込みです。

- ワイドスクリーンでも Dashboard Reports セレクタの通話・チャットタイプ名が切れずに表示される
- 全エージェント対象の Individual Call/Chat History レポートで、All Call History / All Chat History ファイルが常に含まれるようになり、未割り当ての通話・チャットが漏れなく出力される
- Interactions Detail by Agent レポートに、キューなしのアウトバウンド通話が含まれるようになる
- フランス語・スペイン語環境でキュー名がローカライズされた名前で正しく表示される
- fr_CA のラップアップ・保留指標の翻訳が統一され、正確になる
- 46〜365 日の日付範囲でも通話ディスポジションフィールドが正しく表示される

## サービスアップデートの詳細

### 修正内容 (Fixed)

今回のプレリリースノートに含まれる修正は以下のとおりです。

1. **Dashboard Reports セレクタの表示崩れ修正**
   - ワイドスクリーンディスプレイで、通話タイプ・チャットタイプ名がセレクタ内で途切れて表示される問題を修正

2. **Individual Call/Chat History レポートのデータ欠落修正**
   - 全エージェント対象で実行した際、選択期間にアクティビティのあったエージェントが 1 名または 0 名の場合に、エージェント未割り当ての通話・チャット (放棄、デフレクト、期限切れなど) が欠落する問題を修正
   - 修正後は All Call History / All Chat History ファイルが常にレポートに含まれる

3. **Interactions Detail by Agent レポートの欠落修正**
   - 全エージェント対象で生成した際に、キューを経由せず発信されたアウトバウンド通話が欠落する問題を修正

4. **多言語環境でのキュー名表示の修正**
   - Real-time Queue Monitoring および Campaign ダッシュボードで、フランス語・スペイン語のインタラクションに英語のキュー名が表示される問題を修正
   - Real-time Queue Monitoring と高度なレポートダッシュボードで、スペイン語チャットキューに英語名が表示される問題を修正

5. **カナダフランス語 (fr_CA) 翻訳の修正**
   - 高度なレポートにおける「wrap-up」「hold」指標の翻訳が一貫せず不正確だった問題を修正

6. **長期間の日付範囲でのディスポジション表示の修正**
   - 46 日〜365 日の日付範囲を指定すると、通話ディスポジションフィールドが空白になる問題を修正

## 技術仕様

### 影響を受けるレポート・ダッシュボード

| レポート / ダッシュボード | 修正内容 |
|------|------|
| Dashboard Reports セレクタ | ワイドスクリーンでのタイプ名の表示切れを修正 |
| Individual Call History / Individual Chat History レポート | 未割り当て通話・チャットの欠落を修正 (All Call/Chat History ファイルを常に含める) |
| Interactions Detail by Agent レポート | キューなしのアウトバウンド通話の欠落を修正 |
| Real-time Queue Monitoring ダッシュボード | フランス語・スペイン語キュー名のローカライズ表示を修正 |
| Campaign ダッシュボード | フランス語・スペイン語キュー名のローカライズ表示を修正 |
| 高度なレポート全般 | fr_CA のラップアップ・保留指標翻訳の統一、スペイン語チャットキュー名の修正 |
| ダッシュボード全般 (ディスポジション) | 46〜365 日の日付範囲での通話ディスポジション空白表示を修正 |

### 高度なレポートダッシュボードの前提

公式ドキュメントによると、高度なレポートダッシュボードは以下の前提で利用します。

| 項目 | 詳細 |
|------|------|
| 有効化 | Google Cloud コンソールの CCAI Platform インスタンス設定で「Advanced reporting」拡張機能を有効化 |
| 注意点 | 有効化すると従来 (レガシー) の CCAI Platform ダッシュボードは利用不可。カスタムロールの権限設定に影響する場合あり |
| 閲覧権限 | Admin (閲覧・編集可)、Manager Admin / Manager 系ロール (閲覧のみ)、Agent (閲覧不可) |
| アクセス方法 | CCAI Platform ポータルの Dashboard メニュー、または Advanced Reporting Landing Page |

## メリット

### ビジネス面

- **レポートの網羅性向上**: 放棄・デフレクト・期限切れなど、エージェントに割り当てられなかったインタラクションが履歴レポートに確実に含まれるため、応答率や放棄率の分析の正確性が向上する
- **多言語コンタクトセンターの運用品質向上**: フランス語・スペイン語環境でのキュー名や指標名の誤表示が解消され、グローバル・多言語チームのスーパーバイザーがダッシュボードを正しく読み取れるようになる

### 技術面

- **長期間レポートの信頼性向上**: 46〜365 日の日付範囲でディスポジションデータが欠落する問題が解消され、四半期・年次レベルの分析が可能になる
- **アウトバウンド業務の可視化改善**: キューを経由しない発信通話が Interactions Detail by Agent レポートに反映され、エージェントの発信業務を正確に把握できる

## デメリット・制約事項

### 制限事項

- 本リリースノートはプレリリースノートであり、実際のリリース時のバージョン番号は 6.24 より大きくなる可能性がある (公式リリースノートに明記)
- 高度なレポートダッシュボードは利用可能なリージョンが限定されており、対象リージョン外のインスタンスでは拡張機能を有効化できない

### 考慮すべき点

- Individual Call/Chat History レポートの集計対象が変わる (未割り当てインタラクションが常に含まれる) ため、過去のレポート値と比較する際は数値の増加が不具合修正によるものである点に留意が必要
- リリース時期は各インスタンスへのデプロイスケジュールに依存するため、適用タイミングは自社インスタンスの設定を確認すること

## 利用可能リージョン

公式ドキュメントによると、高度なレポートダッシュボードは以下のリージョンでのみ利用可能です。

- us-east1、us-central1、us-west1
- europe-west2
- asia-northeast1
- northamerica-northeast1
- australia-southeast1
- southamerica-east1

## 関連サービス・機能

- **高度なレポートダッシュボード (Advanced Reporting Dashboards)**: Looker ベースのダッシュボード群。Real-time Queue Monitoring、Campaign、Agent Performance などのダッシュボードを提供し、カスタムダッシュボードや Looks の作成も可能
- **標準レポート (Standard Reports)**: Report Builder から CSV 形式でダウンロードするレポート機能。今回修正対象の Individual Call/Chat History レポートはこの機能に含まれる
- **アウトバウンドキャンペーン (Campaigns)**: Campaign ダッシュボードで通話結果やキャンペーンボリュームを監視する機能。今回の多言語キュー名表示の修正対象

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261022-ccaas-advanced-reporting-dashboards-6-24.html)
- [公式リリースノート (Google Cloud Release Notes)](https://docs.cloud.google.com/release-notes#October_22_2026)
- [CCAI Platform リリースノート](https://docs.cloud.google.com/contact-center/ccai-platform/docs/release-notes)
- [高度なレポートダッシュボードの概要](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-overview)
- [標準レポート (Individual Call History レポートなど)](https://docs.cloud.google.com/contact-center/ccai-platform/docs/standard-reports)
- [キュー監視ダッシュボード](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-real-time-queue-monitor)

## まとめ

CCAI Platform の高度なレポートダッシュボード 6.24 のプレリリースノートは、履歴レポートのデータ欠落、多言語環境でのキュー名・指標名の誤表示、長期間指定時のディスポジション空白表示といった、レポートの正確性に関わる 7 件の修正を予告するものです。特に Individual Call/Chat History レポートに未割り当てインタラクションが常に含まれるようになる変更は集計値に影響するため、KPI レポートを定期運用している管理者はリリース適用後の数値変化を事前に把握しておくことを推奨します。

---

**タグ**: #CCAIPlatform #CCaaS #ContactCenter #AdvancedReporting #Dashboards #BugFix #Localization
