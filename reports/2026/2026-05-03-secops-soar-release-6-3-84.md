# Google SecOps SOAR: Release 6.3.84

**リリース日**: 2026-05-03
**サービス**: Google SecOps SOAR
**機能**: Release 6.3.84
**ステータス**: 第1フェーズのリージョンにロールアウト中

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260503-secops-soar-release-6-3-84.html)

## 概要

Google SecOps SOAR の Release 6.3.84 が第1フェーズのリージョンへのロールアウトを開始しました。本リリースには内部バグ修正およびカスタマーバグ修正が含まれています。また、プレイブックの多肢選択質問フローにおける「応答時間」オプションの機能強化も含まれています。

## サービスアップデートの詳細

### リリースロールアウト

Release 6.3.84 は段階的リリースプロセスに従い、第1フェーズとして以下のリージョンに展開されます:

- 日本
- インド
- オーストラリア
- カナダ
- ドイツ
- スイス

残りのリージョン（シンガポール、カタール、サウジアラビア、イスラエル、UK、イタリア、EU マルチリージョン、US マルチリージョン）には第2フェーズで展開される予定です。

### バグ修正

本リリースには内部およびカスタマー向けのバグ修正が含まれています。具体的な修正内容は公開されていません。

### 機能強化: 多肢選択質問の「応答時間」オプション改善

本リリースと同時に、プレイブックの MultiChoiceQuestion ステップにおける「応答時間(time to respond)」超過時の動作について、より細かな制御が可能になりました。多肢選択質問を設定する際に、事前定義された回答ブランチのいずれかに進むか、専用のブランチを作成してこのシナリオに対応するかを選択できるようになっています。

## 関連サービス・機能

- **Google SecOps SOAR プレイブック**: ワークフローの自動化とインシデント対応の効率化を実現するオーケストレーション機能
- **段階的リリースプロセス**: 2025年3月から導入されたリージョンごとの段階的ロールアウト方式
- **Google SecOps SIEM**: SOAR と連携するセキュリティ情報イベント管理サービス

## 参考リンク

- [Google SecOps SOAR リリースノート](https://docs.cloud.google.com/chronicle/docs/soar/release-notes)
- [SOAR 段階的リリース情報](https://docs.cloud.google.com/chronicle/docs/soar/overview-and-introduction/soar-gradual-release)
- [プレイブックでの多肢選択フローの使用](https://docs.cloud.google.com/chronicle/docs/soar/respond/working-with-playbooks/using-flows-in-playbooks#multi-choice)
- [Google Cloud リリースノート (2026年5月3日)](https://docs.cloud.google.com/release-notes#May_03_2026)

## まとめ

Google SecOps SOAR Release 6.3.84 は、内部およびカスタマー向けバグ修正を中心としたメンテナンスリリースです。加えて、プレイブックの多肢選択質問フローにおける応答時間超過時の挙動をより柔軟に制御できる機能強化が含まれています。第1フェーズのリージョンから順次展開され、その後残りのリージョンへのロールアウトが行われます。

---

**タグ**: #GoogleSecOps #SOAR #Release6.3.84 #BugFix #PlaybookEnhancement #SecurityOperations #段階的リリース
