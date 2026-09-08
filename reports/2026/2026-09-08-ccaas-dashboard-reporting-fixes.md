# Google Cloud Contact Center as a Service: ダッシュボード・レポーティングの不具合修正

**リリース日**: 2026-09-08

**サービス**: Google Cloud Contact Center as a Service (CCaaS)

**機能**: ダッシュボード・レポーティングの不具合修正

**ステータス**: Fixed (バグ修正)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260908-ccaas-dashboard-reporting-fixes.html)

## 概要

Google Cloud Contact Center as a Service (CCaaS) のレポーティング・ダッシュボード機能に関する複数の不具合修正がリリースされた。今回の修正は、数値フォーマットの不整合や言語切り替えの遅延といった表示上の問題から、フィルターが正しく適用されない・メトリクスが誤った値を返すといった、レポートデータの正確性に直結する問題まで、広範囲に及ぶ。

特に、Avg Queue Time が平均値ではなく合計値を表示していた問題や、リアルタイムのキュー待機メトリクスがキュー再投入後の待機時間を正しく測定していなかった問題など、コンタクトセンターの運用判断 (人員配置、ルーティング調整、SLA 監視) に影響し得るデータ精度の修正が含まれており、CCaaS のダッシュボードを KPI 管理に利用しているスーパーバイザーや管理者にとって重要なリリースである。

**アップデート前の課題**

- タイル間で数値のフォーマットが不統一だった
- 言語を切り替えても、列ヘッダー・フィルターラベル・タイルタイトルが即座に新しい言語に切り替わらなかった
- Queue Group Performance - All ダッシュボードの Productive Agents 列が、キューグループ設定に応じた適切な値を表示していなかった
- Call Queue Metrics (Historical) Explore で、Agent Name を表示列に含めずにフィルターすると 0 行が返されていた
- Custom After Hours Deflection でメッセージに転送されたサブメニューへのコールが、All Queued Interactions レポートで親メニューに誤って計上されていた
- Agent Performance、Real-time Agent Monitoring、All Interactions の各ダッシュボードで Direction フィルターが一部のテーブル・タイルに正しく反映されていなかった
- Queue Performance - Calls ダッシュボードで、期間内にショートアバンダン (短時間放棄) が存在すると、Queue Summary テーブルの Avg Queue Time 列が平均値ではなくキュー滞在時間の合計 (生の合算値) を表示していた
- Individual Call History Report / Individual Chat History Report の生成時にチームフィルターが正しく適用されず、管理対象外キューのデータが含まれていた
- Real-time Calls - Calls Queued ダッシュボードで、自動応答検出ミス後にキューへ戻された発信者が Total Queued Now に含まれず、Current Max/Avg Queue Wait Time が直近のキュー再投入時点ではなく最初のキュー投入時点から測定されていた
- 高度なレポーティングダッシュボードの下部にグレーのバーが表示され、ダッシュボード全体の表示が妨げられていた

**アップデート後の改善**

- タイル間で数値フォーマットが統一され、表示の一貫性が向上した
- 言語切り替え時に列ヘッダー・フィルターラベル・タイルタイトルが即座に反映されるようになった
- 各種フィルター (Agent Name、Direction、チームフィルター) が意図どおりに機能し、レポート結果の正確性が向上した
- Avg Queue Time やリアルタイムキュー待機メトリクスが正しい値を返すようになり、運用判断に使うデータの信頼性が向上した
- レポートの帰属 (サブメニュー転送コールの計上先) が正しくなり、メニュー別の分析精度が改善された

## サービスアップデートの詳細

### 修正内容一覧

| # | 対象 | 修正内容 |
|---|------|---------|
| 1 | 全般 (タイル表示) | 数値フォーマットがタイル間で不統一だった問題を修正 |
| 2 | 全般 (多言語対応) | 言語切り替え時に列ヘッダー・フィルターラベル・タイルタイトルが即座に切り替わらない問題を修正 |
| 3 | Queue Group Performance - All | Productive Agents 列がキューグループ設定に応じた値を表示しない問題を修正 |
| 4 | Call Queue Metrics (Historical) Explore | Agent Name を表示列に含めずフィルターすると 0 行が返る問題を修正 |
| 5 | All Queued Interactions レポート | Custom After Hours Deflection でメッセージに転送されたサブメニューへのコールが親メニューに誤計上される問題を修正 |
| 6 | Agent Performance | Agent Productivity Detailed – Calls / Chats テーブルが Direction フィルターを正しく反映するよう修正 |
| 7 | Real-time Agent Monitoring | Agent Performance テーブルと履歴メトリクスタイルが Direction フィルターを正しく反映するよう修正 |
| 8 | All Interactions – Calls / Chats | IVR Interactions (コールのみ) と Virtual Agent Interactions テーブルが Direction フィルターを正しく反映するよう修正 |
| 9 | Queue Performance - Calls | ショートアバンダンが存在する期間で、Avg Queue Time 列が平均ではなく合計値を表示する問題を修正 |
| 10 | Individual Call/Chat History Report | チームフィルターが適用されず、管理対象外キューのデータが含まれる問題を修正 |
| 11 | Real-time Calls - Calls Queued | Total Queued Now が自動応答検出ミス後にキューへ戻された発信者を含まない問題、および Current Max/Avg Queue Wait Time (H:M:S) が直近のキュー再投入時点ではなく最初の投入時点から測定される問題を修正 |
| 12 | 高度なレポーティングダッシュボード | 画面下部にグレーのバーが表示され全体が見えない問題を修正 |

### 影響を受けるダッシュボード・レポート

- Queue Group Performance - All ダッシュボード
- Call Queue Metrics (Historical) Explore
- All Queued Interactions レポート
- Agent Performance ダッシュボード
- Real-time Agent Monitoring ダッシュボード
- All Interactions – Calls / Chats ダッシュボード
- Queue Performance - Calls ダッシュボード
- Individual Call History Report / Individual Chat History Report
- Real-time Calls - Calls Queued ダッシュボード

## メリット

### ビジネス面

- **運用判断の信頼性向上**: Avg Queue Time やリアルタイム待機メトリクスの精度が改善され、人員配置やルーティング調整などの判断をより正確なデータに基づいて行えるようになった
- **レポートの正確な帰属**: サブメニュー転送コールの計上先やチームフィルターの適用が正しくなり、メニュー別・チーム別の分析結果を信頼できるようになった

### 技術面

- **フィルターの一貫した動作**: Direction フィルターや Agent Name フィルターが対象テーブル・タイル全体で一貫して機能するようになった
- **多言語環境での即時反映**: 言語切り替えが UI 全体に即座に反映され、多言語で運用するコンタクトセンターでの利便性が向上した

## 考慮すべき点

- 修正前の期間に取得・保存したレポートデータや KPI 集計値 (特に Avg Queue Time、Total Queued Now、Current Max/Avg Queue Wait Time、チームフィルター適用済みの Individual Call/Chat History Report) は、修正前の不具合の影響を受けている可能性があるため、過去データとの比較時には注意が必要
- 追加の設定作業は不要で、修正はプラットフォーム側で適用される

## 関連サービス・機能

- **Conversational Agents (Dialogflow)**: CCaaS の IVR / バーチャルエージェント連携。All Interactions ダッシュボードの Virtual Agent Interactions テーブルなどでレポートされる
- **Looker ベースの高度なレポーティング**: Call Queue Metrics (Historical) Explore など、Explore ベースのカスタム分析機能が今回の修正対象に含まれる

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260908-ccaas-dashboard-reporting-fixes.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#September_08_2026)
- [ダッシュボードの概要 (公式ドキュメント)](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-overview)
- [Queue Performance ダッシュボード](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-queue-performance)
- [Queue Group Performance ダッシュボード](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-queue-group-perf)
- [Real-time Agent Monitoring ダッシュボード](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-real-time-agent-monitoring)
- [All Interactions ダッシュボード](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-all-interactions)
- [Agent Performance ダッシュボード](https://docs.cloud.google.com/contact-center/ccai-platform/docs/dashboards-agent-performance)

## まとめ

今回のリリースは、CCaaS のレポーティング・ダッシュボードにおけるメトリクス精度とフィルター動作に関する 12 件の不具合をまとめて修正するものであり、ダッシュボードを日常の運用監視や KPI 管理に利用しているコンタクトセンターにとって重要なアップデートである。特に Avg Queue Time やリアルタイム待機メトリクスの修正はデータの意味自体が変わるため、修正前の期間のレポートと比較する際は不具合の影響を考慮することを推奨する。

---

**タグ**: #GoogleCloud #CCaaS #ContactCenter #CCAIPlatform #Dashboard #Reporting #BugFix
