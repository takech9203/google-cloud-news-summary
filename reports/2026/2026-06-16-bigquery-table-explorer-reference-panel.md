# BigQuery: Table Explorer の Reference パネルへの統合

**リリース日**: 2026-06-16

**サービス**: BigQuery

**機能**: Table Explorer から Reference パネルへの移行

**ステータス**: Announcement (2026年7月以降に移行予定)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260616-bigquery-table-explorer-reference-panel.html)

## 概要

BigQuery の Table Explorer 機能が Reference パネルに統合されることが発表された。この移行は 2026年7月以降に実施される予定であり、ユーザーがテーブルデータを探索しクエリを作成するワークフローが、よりクエリエディタに統合された形で提供されることになる。

Table Explorer はテーブルフィールドを選択して視覚的にデータを探索し、その選択に基づいてクエリを自動生成する機能であった。一方、Reference パネルはクエリエディタ内でテーブル、スナップショット、ビュー、マテリアライズドビューのコンテキスト情報を動的に表示し、クエリスニペットやフィールド名を直接挿入できる機能である。今回の統合により、データ探索からクエリ作成までのワークフローがクエリエディタ内で完結するようになる。

**アップデート前の課題**

- Table Explorer とクエリエディタが分離しており、データ探索とクエリ作成を別々のインターフェースで行う必要があった
- Table Explorer で生成したクエリをクエリエディタにコピーする追加手順が必要であった
- テーブル情報の参照とクエリ編集を並行して行う際にコンテキストスイッチが発生していた

**アップデート後の改善**

- Reference パネルにより、クエリエディタ内でテーブルスキーマの確認とクエリ構築が一体化される
- フィールド名のクリックだけでクエリに直接挿入可能になり、操作ステップが削減される
- Gemini Cloud Assist との連携により、AI を活用したデータインサイトやコード支援も利用可能になる

## サービスアップデートの詳細

### 主要機能

1. **Table Explorer (移行元)**
   - テーブルフィールドを最大 10 個選択してデータを視覚的に探索
   - 各フィールドの上位 10 件の値をインタラクティブカードとして表示
   - 選択に基づいたデータ探索クエリの自動生成
   - パーティションフィルタのサポート
   - BigQuery テーブル、BigLake テーブル、外部テーブル、ビューに対応

2. **Reference パネル (移行先)**
   - クエリエディタ内でテーブル・ビューのスキーマ情報を動的に表示
   - 最近使用したテーブルやスター付きテーブルへのクイックアクセス
   - クエリスニペットの挿入機能
   - フィールド名のクリックによるクエリへの直接挿入
   - テーブルの検索機能

3. **Gemini Cloud Assist との連携**
   - データに関するより深いインサイトの取得
   - SQL クエリの AI 支援による生成・補完・説明
   - Table Explorer の基本的なクエリ生成を超えた高度な分析支援

## 技術仕様

### 機能比較

| 項目 | Table Explorer | Reference パネル |
|------|---------------|-----------------|
| データ探索 | フィールド選択によるカード表示 | スキーマプレビュー |
| クエリ生成 | 選択に基づく自動生成 | スニペット挿入 + フィールド名挿入 |
| 対応リソース | テーブル、ビュー | テーブル、スナップショット、ビュー、マテリアライズドビュー |
| AI 支援 | なし | Gemini Cloud Assist 連携 |
| 配置場所 | 独立タブ | クエリエディタ内サイドパネル |
| 複数テーブル | 非対応 | 検索・切り替え可能 |

### 権限要件

Table Explorer と同様に、テーブルデータの参照には対象テーブルへの読み取り権限が必要である。列レベルのアクセス制御 (ACL) が設定されている場合は、選択したフィールドすべてに対する読み取りアクセスが必要となる。

## メリット

### ビジネス面

- **ワークフローの効率化**: データ探索からクエリ作成までをクエリエディタ内で一貫して行えるようになり、分析者の生産性が向上する
- **AI 支援の活用**: Gemini Cloud Assist との統合により、より高度なデータ分析やクエリ最適化が可能になる

### 技術面

- **コンテキスト保持**: クエリエディタとデータ参照を同一画面で行えるため、コンテキストスイッチが不要になる
- **対応リソースの拡大**: スナップショットやマテリアライズドビューなど、Table Explorer では対応していなかったリソースタイプの情報も参照可能になる

## デメリット・制約事項

### 考慮すべき点

- Table Explorer の「フィールド値の出現頻度をカード表示する」機能が Reference パネルでどのように代替されるかは現時点で詳細が未発表
- 既存の Table Explorer を活用したワークフローやトレーニング資料の更新が必要になる可能性がある
- 移行時期は「2026年7月以降」とされており、具体的な日付は未定

## 料金

Table Explorer は選択したフィールドと値に基づいてクエリを実行するため、BigQuery のコンピュート料金が発生する。Reference パネルへの移行後も、クエリの実行にはコンピュート料金が適用される。料金体系自体に変更はないと見られる。

詳細は [BigQuery 料金ページ](https://cloud.google.com/bigquery/pricing) を参照。

## 関連サービス・機能

- **Gemini Cloud Assist**: データインサイトの取得やクエリ作成の AI 支援を提供。Table Explorer の移行に伴い、より深い分析には Gemini Cloud Assist の利用が推奨される
- **BigQuery Studio**: Table Explorer および Reference パネルが統合されている統合開発環境
- **Data Canvas**: 自然言語によるクエリ結果の反復的な探索を提供する関連機能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260616-bigquery-table-explorer-reference-panel.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#June_16_2026)
- [Table Explorer ドキュメント](https://docs.cloud.google.com/bigquery/docs/table-explorer)
- [Reference パネル (クエリの実行)](https://docs.cloud.google.com/bigquery/docs/running-queries#use-reference-panel)
- [Gemini Cloud Assist の利用](https://docs.cloud.google.com/bigquery/docs/use-cloud-assist)
- [料金ページ](https://cloud.google.com/bigquery/pricing)

## まとめ

BigQuery の Table Explorer が Reference パネルに統合されることで、データ探索とクエリ作成のワークフローがクエリエディタ内で一体化される。2026年7月以降の移行に備え、現在 Table Explorer を利用しているユーザーは Reference パネルの操作方法に慣れておくことが推奨される。また、より高度なデータ探索が必要な場合は Gemini Cloud Assist の活用を検討すべきである。フィードバックは bigquery-explorer-feedback@google.com へ送信可能。

---

**タグ**: #BigQuery #TableExplorer #ReferencePanel #UI変更 #GeminiCloudAssist
