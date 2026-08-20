# Google SecOps: Cases の Alerts & Detections タブに Side-by-side ビューが登場 (Public Preview)

**リリース日**: 2026-08-20

**サービス**: Google SecOps (Security Operations)

**機能**: Alerts & Detections タブの Side-by-side ビュー

**ステータス**: Public Preview

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260820-google-secops-alerts-side-by-side-view.html)

## 概要

Google SecOps の刷新された Investigation Management (調査管理) エクスペリエンスにおいて、Cases ページの Alerts & Detections タブが新しい **Side-by-side ビュー** レイアウトをサポートしました。本機能は Public Preview として提供されます。

これまでのデフォルトである List ビュー (一覧表示) に加えて、Side-by-side ビューへ切り替えることで、アラートや検出 (Detection) の詳細メタデータ、ステータス、優先度、作成日、そして Gemini による調査インサイトを、メインの一覧から離れることなく隣接するサイドペインで確認できるようになります。

SOC (Security Operations Center) のアナリストは、日々大量のアラートと検出をトリアージする必要があります。一覧性を保ちながら個別のアイテムの詳細を素早く確認できる Side-by-side ビューは、トリアージと調査のコンテキストスイッチを減らし、調査効率の向上に直結するアップデートです。

**アップデート前の課題**

- Alerts & Detections タブはデフォルトの List ビューのみで、アラートや検出の詳細を確認するには個別のアイテムを開く操作が必要だった
- 詳細確認のたびにメインの一覧から画面遷移 (ナビゲーション) が発生し、複数のアラートを連続で確認する際にコンテキストが失われやすかった
- 一覧と詳細 (メタデータ、ステータス、優先度、Gemini インサイトなど) を同時に見比べながらトリアージすることが難しかった

**アップデート後の改善**

- List ビューと Side-by-side ビューをワンクリックで切り替えられるようになった
- メインの一覧を表示したまま、隣接するサイドペインでアラート・検出の詳細メタデータ、ステータス、優先度、作成日、Gemini 調査インサイトを確認できるようになった
- 画面遷移なしで一覧内のアイテムを次々に確認でき、トリアージのスピードとコンテキスト維持が向上した

## サービスアップデートの詳細

### 主要機能

1. **Side-by-side ビューレイアウト**
   - Cases の Alerts & Detections タブで、一覧と詳細ペインを左右に並べて表示するレイアウト
   - メインの一覧から離れることなく、選択したアラート・検出の詳細を隣接ペインで確認可能

2. **List ビューとの切り替え**
   - デフォルトの List ビューと Side-by-side ビューを自由に切り替え可能
   - トリアージのフェーズや好みに応じて最適なレイアウトを選択できる

3. **サイドペインで確認できる情報**
   - 詳細メタデータ
   - ステータス
   - 優先度 (Priority)
   - 作成日 (Creation date)
   - Gemini による調査インサイト (Gemini investigation insights)

### Investigation Management における位置づけ

本機能は、刷新された Investigation Management エクスペリエンスの一部です。公式ドキュメントでは、調査管理における主要な用語と操作が以下のように整理されています。

| 用語 | 説明 |
|------|------|
| Investigation Management | トリアージ・調査・管理を行うエンドツーエンドのアナリスト体験 |
| List view | ケーストリアージに使うデフォルトのテーブルレイアウト |
| Case Queue | 割り当てられたアクティブなケースの一覧。List ビューと Side-by-side ビューの両方で表示可能 |
| Finding | 調査対象となるセキュリティアイテムの総称 (アラートと非アラート検出を含む) |
| Alert | アラート有効 (Alerting=ON) のルールが生成する、トリアージが必要なシグナル |
| Detection | アラート無効 (Alerting=OFF) のルールが生成するシグナル。ノイズの多いルールやテスト中のルールで利用 |

## メリット

### ビジネス面

- **トリアージ効率の向上**: 画面遷移が減ることで、アナリストが単位時間あたりに処理できるアラート・検出の件数が増え、MTTR (平均対応時間) の短縮に寄与
- **アナリスト体験の改善**: コンテキストスイッチの削減により、調査中の集中力とコンテキスト維持が容易になる

### 技術面

- **一覧と詳細の同時表示**: 一覧のソート・フィルタ状態を保ったまま個別アイテムの詳細を確認できる
- **Gemini インサイトへの素早いアクセス**: AI による調査インサイトをサイドペインで即座に参照でき、深掘り調査 (Events Viewer や専用ページ) へ進むかどうかの判断が速くなる
- **柔軟なレイアウト選択**: List ビューと Side-by-side ビューをユースケースに応じて使い分けられる

## デメリット・制約事項

### 制限事項

- Public Preview 段階の機能であり、Google SecOps の Pre-GA Offerings Terms が適用される (サポートが限定される場合や、後方互換性のない変更が入る可能性がある)
- 刷新された Investigation Management エクスペリエンス上の機能であり、従来の Cases 画面では利用できない

### 考慮すべき点

- Preview 機能のため、本番 SOC 運用のワークフローに組み込む際は、GA までの仕様変更の可能性を考慮する
- サイドペインを併用するレイアウトのため、画面幅の狭い環境では一覧の表示領域が狭くなる点に留意する

## ユースケース

### ユースケース 1: 朝のアラートトリアージ

**シナリオ**: SOC アナリストが夜間に蓄積したアラートと検出を毎朝トリアージする。従来は 1 件ずつ開いて詳細を確認し、一覧へ戻る操作を繰り返していた。

**効果**: Side-by-side ビューに切り替えることで、一覧上でアイテムを選択するだけでサイドペインに詳細と Gemini インサイトが表示され、画面遷移なしに優先度判断と割り当てを連続して実施できる。

### ユースケース 2: ノイズの多い検出ルールのチューニング確認

**シナリオ**: アラート無効 (Alerting=OFF) でテスト運用中のルールが生成する検出を、検知エンジニアがまとめてレビューし、ルールの精度を評価する。

**効果**: 検出の一覧を保持したままサイドペインで各検出のメタデータを次々に確認でき、誤検知パターンの特定とルールチューニングの判断が効率化される。

## 料金

本機能は Google SecOps の UI 機能であり、追加料金に関する記載はありません。Google SecOps 自体はサブスクリプションベースのパッケージ (Standard / Enterprise / Enterprise Plus) で提供されます。詳細は料金ページを参照してください。

- [Google SecOps 料金](https://cloud.google.com/security/products/security-operations)

## 関連サービス・機能

- **Gemini in Google SecOps**: サイドペインに表示される調査インサイトを生成。ケースサマリー、検索クエリ生成、Triage and Investigation Agent などの AI 支援機能を提供
- **Events Viewer**: 検出をトリガーした UDM イベントや生ログを深掘りするためのインタラクティブなサイドパネル。Side-by-side ビューでの一次確認から深掘り調査へ進む際に利用
- **Case Overview タブ**: アラート一覧、エンティティグラフ、Gemini Summary ウィジェットなど、ケース全体を俯瞰するカスタマイズ可能なビュー
- **Detection Engine (YARA-L ルール)**: 本ビューで確認するアラート・検出を生成する検知エンジン

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260820-google-secops-alerts-side-by-side-view.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#August_20_2026)
- [Investigation and case management overview](https://cloud.google.com/chronicle/docs/secops/investigate/investigation-management/investigation-management-overview)
- [Use the Events Viewer](https://docs.cloud.google.com/chronicle/docs/secops/investigate/investigation-management/use-events-viewer)
- [Gemini in Google SecOps](https://docs.cloud.google.com/chronicle/docs/secops/gemini-secops)

## まとめ

Google SecOps の Alerts & Detections タブに Side-by-side ビューが Public Preview で追加され、一覧から離れることなくアラート・検出の詳細と Gemini インサイトを確認できるようになりました。SOC のトリアージ効率とアナリスト体験を直接改善するアップデートであり、刷新された Investigation Management エクスペリエンスを利用しているチームは、日次トリアージのワークフローで積極的に試す価値があります。Preview 段階のため、GA までの仕様変更の可能性には留意してください。

---

**タグ**: Google SecOps, Chronicle, Investigation Management, Cases, アラート, 検出, Side-by-side ビュー, Gemini, SOC, Public Preview
