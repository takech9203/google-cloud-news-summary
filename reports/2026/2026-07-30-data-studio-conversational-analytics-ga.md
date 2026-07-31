# Data Studio: Conversational Analytics の GA とデータエージェント共有時のメール通知

**リリース日**: 2026-07-30

**サービス**: Data Studio

**機能**: Conversational Analytics の一般提供 (GA) / データエージェント共有時のメール通知

**ステータス**: GA (一般提供) + 機能追加

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260730-data-studio-conversational-analytics-ga.html)

## 概要

Data Studio の Conversational Analytics が一般提供 (GA) になりました。Conversational Analytics は Gemini for Google Cloud を活用した「チャットでデータと対話する」機能で、BI の専門知識がないユーザーでも自然言語でデータに関する質問を行い、静的なダッシュボードを超えた分析が可能になります。GA に合わせて、データエージェントを所属する Google Cloud プロジェクトでフィルタリングする機能が追加され、追加の権限が必要なエージェントには「Unavailable」ラベルが表示されるようになりました。

同日に、Conversational Analytics データエージェントの共有時のメール通知機能も追加されました。BigQuery で作成したデータエージェントを Data Studio ユーザーと共有する際に、対象ユーザーへアクセス権が付与されたことを知らせるメールを送信するオプションを選択できます。

新しい Conversational Analytics エクスペリエンスは、BigQuery で作成・公開されたデータエージェントとの対話をすべての Data Studio ユーザーに開放するもので、データアナリストがエージェントを整備し、ビジネスユーザーがセルフサービスで分析を行う分業モデルを支えるアップデートです。

**アップデート前の課題**

- 従来 (レガシー) の Conversational Analytics は、Gemini in Data Studio を有効化した Data Studio Pro サブスクリプションのユーザーのみが利用可能だった
- 多数のエージェントが共有されている環境で、目的のエージェントを探す手段が検索バーに限られていた
- 権限が不足しているエージェントかどうかが一覧上で判別しにくかった
- BigQuery で作成したエージェントを Data Studio ユーザーに共有しても、共有されたことがユーザーに自動的に通知されず、エージェントへのリンクを別途伝える必要があった

**アップデート後の改善**

- 新しい Conversational Analytics エクスペリエンスが GA となり、すべての Data Studio ユーザーが BigQuery データエージェントとチャットできるようになった (Code Interpreter の利用には引き続き Gemini in Data Studio と Data Studio Pro が必要)
- 「Chat with your data」ページで、エージェントが作成された Google Cloud プロジェクトを選択して一覧を絞り込めるようになった
- アクセスやチャットに必要な権限が不足しているエージェントには「Unavailable」ラベルが表示され、利用可否が一目で分かるようになった
- エージェント共有時にメール通知を送信するオプションが追加され、ユーザーがアクセス権の付与にすぐ気づけるようになった

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph BQ["🗄️ BigQuery"]
        Creator([👩‍💻 エージェント作成者]) -->|作成・公開| Agent["🤖 データエージェント<br/>(メタデータ + 指示)"]
        Agent --- Table[("📊 BigQuery テーブル")]
        Creator -->|共有 + 📧 メール通知 (New)| Share["🔑 IAM ロール付与<br/>dataAgentUser"]
    end
    subgraph DS["📈 Data Studio (GA)"]
        User([👤 ビジネスユーザー]) --> Chat["💬 Chat with your data<br/>プロジェクトでフィルタ (New)<br/>Unavailable ラベル (New)"]
    end
    Share -->|📧 通知メール| User
    Chat -->|自然言語で質問| Agent
    Agent -->|Gemini による回答| Chat
```

データエージェントは BigQuery で作成・公開され、共有時にメール通知 (オプション) で Data Studio ユーザーに知らされます。ユーザーは Data Studio の「Chat with your data」ページでプロジェクト別にエージェントを絞り込み、自然言語で対話できます。

## サービスアップデートの詳細

### 主要機能

1. **Conversational Analytics の一般提供 (GA)**
   - Gemini for Google Cloud を活用し、自然言語でデータに質問できる機能が GA に到達
   - 新しいエクスペリエンスでは、BigQuery で作成・共有されたデータエージェントとの対話がすべての Data Studio ユーザーに提供される (レガシーは Data Studio Pro + Gemini in Data Studio が必要だった)
   - エージェントは BigQuery で作成・編集し、Data Studio の「Chat with your data」ページに自動的に表示される

2. **Google Cloud プロジェクトによるエージェントのフィルタリング**
   - 検索バー横のドロップダウンメニューから Google Cloud プロジェクトを選択可能
   - プロジェクトを選択すると、そのプロジェクトで (BigQuery 上で) 作成されたエージェントのみが表示される

3. **「Unavailable」ラベルの表示**
   - エージェントへのアクセスやチャットに必要な権限が不足している場合、そのエージェントに「Unavailable」ラベルが表示される
   - 権限不足による利用不可を一覧画面で事前に把握できる

4. **共有時のメール通知 (新機能)**
   - BigQuery で作成したデータエージェントを Data Studio ユーザーと共有する際、アクセス権付与を知らせるメールの送信を選択できる
   - 共有されたエージェントは対象ユーザーの「Chat with your data」ページに自動表示されるほか、エージェントへの直接リンク (Data Studio 用 URL) のコピーも可能

## 技術仕様

### レガシーと新しいエクスペリエンスの比較

| 項目 | レガシー Conversational Analytics | 新しい Conversational Analytics |
|------|----------------------------------|--------------------------------|
| 対応データソース | CSV、Sheets、Looker、BigQuery のデータソースまたはエージェント | BigQuery データエージェント |
| 利用可能なユーザー | Data Studio Pro サブスクリプション + Gemini in Data Studio 有効化が必要 | すべての Data Studio ユーザー (Code Interpreter は引き続き Gemini in Data Studio + Data Studio Pro が必要) |
| エージェント | Data Studio 内で作成 (新エクスペリエンスへの移行は不可) | BigQuery で作成し Data Studio に共有 (Data Studio 内では作成不可) |

### エージェント利用に必要な権限と API

Data Studio 経由で BigQuery データエージェントを利用するエンドユーザーには、以下の設定が必要です。

| 種別 | 内容 |
|------|------|
| 有効化が必要な API | BigQuery API、Cloud AI Companion API、Gemini Data Analytics API |
| エージェントに対するロール | Gemini Data Analytics Data Agent User (`roles/geminidataanalytics.dataAgentUser`) |
| プロジェクトレベルのロール | BigQuery Data Viewer (`roles/bigquery.dataViewer`)、BigQuery Job User (`roles/bigquery.jobUser`)、Gemini for Google Cloud User (`roles/cloudaicompanion.user`) または BigQuery Studio User (`roles/bigquery.studioUser`) |

エージェントの共有時に選択できる主なロールは以下のとおりです。

| ロール | 権限 |
|--------|------|
| Gemini Data Analytics Data Agent User (`roles/geminidataanalytics.dataAgentUser`) | エージェントとのチャット |
| Gemini Data Analytics Data Agent Editor (`roles/geminidataanalytics.dataAgentEditor`) | エージェントの編集 |
| Gemini Data Analytics Data Agent Viewer (`roles/geminidataanalytics.dataAgentViewer`) | エージェントの閲覧 |

**注意**: エージェントはユーザーの権限で動作します。エージェントへのアクセス権を付与しても、基盤となるデータソースへのアクセス権は付与されないため、データ側の権限も別途確認が必要です。

## 設定方法

### 前提条件

1. Google Cloud プロジェクトで課金が有効化されていること
2. BigQuery、Gemini Data Analytics、Gemini for Google Cloud、Knowledge Catalog の各 API が有効化されていること
3. エージェント作成者に Gemini Data Analytics Data Agent Creator (`roles/geminidataanalytics.dataAgentCreator`) が付与されていること

### 手順

#### ステップ 1: BigQuery でデータエージェントを作成・公開する

1. BigQuery の **Agents** ページで **Agent Catalog** タブを選択
2. エージェントを作成し、テーブル・ビュー・UDF などのナレッジソースと指示 (instructions) を設定
3. **Publish** で公開する (下書き状態のエージェントは共有不可)

#### ステップ 2: Data Studio ユーザーにエージェントを共有する (メール通知)

1. エージェントカードの **Open actions > Edit** からエージェントエディタを開く
2. **Share** を選択し、**Add principal** でユーザーまたはグループを追加
3. ロール (例: Gemini Data Analytics Data Agent User) を選択して保存
4. 共有時にメール通知の送信を選択すると、対象ユーザーにアクセス権付与を知らせるメールが届く

#### ステップ 3: Data Studio でエージェントとチャットする

1. Data Studio のナビゲーションから **Conversational Analytics** を選択して「Chat with your data」ページを開く
2. 検索バー横のドロップダウンで Google Cloud プロジェクトを選択してエージェントを絞り込む (権限が不足しているエージェントには「Unavailable」ラベルが表示される)
3. エージェントを選択し、自然言語で質問を入力して会話を開始する

## メリット

### ビジネス面

- **セルフサービス分析の民主化**: 新しいエクスペリエンスはすべての Data Studio ユーザーが利用できるため、BI の専門知識がないビジネスユーザーも自然言語でデータ分析ができる
- **GA によるプロダクション利用の安心感**: 一般提供となったことで、本番のワークフローに組み込みやすくなった
- **共有の摩擦を低減**: メール通知により、エージェントを共有された側がすぐに利用を開始でき、リンクを別途連絡する手間が減る

### 技術面

- **一元的なエージェント管理**: エージェントの作成・編集・権限管理は BigQuery 側に集約され、Data Studio はチャットの利用体験に専念する構成
- **プロジェクト単位のガバナンス**: プロジェクトフィルタにより、大量のエージェントが存在する組織でも目的のエージェントを効率的に発見できる
- **権限状態の可視化**: 「Unavailable」ラベルにより権限不足を事前に把握でき、問い合わせやトラブルシューティングの手間を削減できる

## デメリット・制約事項

### 制限事項

- 新しいエクスペリエンスでは Data Studio 内でデータエージェントを作成できない (BigQuery での作成が必須)
- 新しいエクスペリエンスの対応データソースは BigQuery データエージェントのみ (レガシーの CSV、Sheets、Looker データソースは対象外)
- レガシーの会話やエージェントを新しいエクスペリエンスへ移行することはできない
- Code Interpreter (Python による高度な分析) の利用には、引き続き Data Studio Pro サブスクリプションと Gemini in Data Studio の有効化が必要
- 下書き (draft) 状態のエージェントは共有できない

### 考慮すべき点

- エージェントの共有はデータソースへのアクセス権付与を含まないため、BigQuery 側の IAM (Data Viewer、Job User など) を別途整備する必要がある
- Gemini for Google Cloud は妥当に見えても事実と異なる出力を生成する可能性があるため、出力の検証が推奨される
- Data Agent User ロールのみのユーザーには Data Studio の「Manage Agent」ページにエージェントが表示されない場合があり、その際は直接リンクの共有が回避策となる
- `cloudaicompanion.topics.create` 権限の不足によるエラーが発生した場合は、Cloud AI Companion API の有効化と `roles/cloudaicompanion.user` または `roles/bigquery.studioUser` の付与を確認する

## ユースケース

### ユースケース 1: 全社向けセルフサービス分析ポータル

**シナリオ**: データチームが BigQuery で売上データ用のデータエージェントを作成し、「"ロイヤル顧客" は注文数 5 件超のユーザーを指す」などのビジネス用語の定義を指示として設定。営業部門全体に共有する。

**実装例**:
```
1. BigQuery で売上テーブルをナレッジソースとするエージェントを作成・公開
2. 営業部門の Google グループに roles/geminidataanalytics.dataAgentUser を付与して共有
   (メール通知オプションを有効化)
3. 営業メンバーは通知メールから Data Studio を開き、
   「今四半期のロイヤル顧客の売上推移は?」と自然言語で質問
```

**効果**: SQL やダッシュボード作成のスキルがなくても、統一されたビジネス定義に基づく正確な分析を各自が実行できる。

### ユースケース 2: マルチプロジェクト環境でのエージェント整理

**シナリオ**: 部門ごとに Google Cloud プロジェクトを分けている企業で、ユーザーに多数のエージェントが共有されている。

**効果**: プロジェクトフィルタで自部門のプロジェクトのエージェントだけを表示でき、「Unavailable」ラベルにより権限申請が必要なエージェントを事前に識別できる。

## 料金

このアップデートに関する個別の料金情報は Release Notes には記載されていません。Code Interpreter の利用には Data Studio Pro サブスクリプションが必要です。詳細は以下を参照してください。

- [Looker Studio Pro (Data Studio Pro) の料金](https://cloud.google.com/looker-studio/pricing)
- [BigQuery の料金](https://cloud.google.com/bigquery/pricing)

## 関連サービス・機能

- **BigQuery**: データエージェントの作成・編集・公開・共有を行う場所。エージェントのナレッジソース (テーブル、ビュー、UDF) も BigQuery 上のデータ
- **Gemini for Google Cloud**: Conversational Analytics の自然言語処理を支える基盤。データガバナンスと責任ある AI のドキュメントを確認のこと
- **Gemini Data Analytics API (Conversational Analytics API)**: エージェントの権限管理 (Data Agent User / Editor / Viewer ロール) を提供
- **Code Interpreter**: 自然言語の質問を Python コードに変換・実行し、SQL ベースより高度な分析と可視化を実現 (Data Studio Pro + Gemini in Data Studio が必要)

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260730-data-studio-conversational-analytics-ga.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#July_30_2026)
- [Conversational Analytics の概要](https://docs.cloud.google.com/data-studio/conversational-analytics-overview)
- [Conversational Analytics のセットアップ](https://docs.cloud.google.com/data-studio/conversational-analytics-setup)
- [Data Studio のデータエージェント](https://docs.cloud.google.com/data-studio/conversational-analytics-data-agents)
- [BigQuery でのデータエージェント作成](https://docs.cloud.google.com/bigquery/docs/create-data-agents)

## まとめ

Data Studio の Conversational Analytics が GA となり、BigQuery で作成したデータエージェントとの自然言語チャットがすべての Data Studio ユーザーに開放されました。プロジェクトフィルタ、「Unavailable」ラベル、共有時のメール通知により、組織的なエージェント運用の実用性が大きく向上しています。BigQuery にデータ資産を持つ組織は、データエージェントを整備してビジネスユーザー向けのセルフサービス分析を展開する好機です。

---

**タグ**: Data Studio, Conversational Analytics, BigQuery, データエージェント, Gemini, GA, 自然言語分析, BI
