# Bigtable: CLUSTER_ATTRIBUTE() フィルタによる継続的マテリアライズドビューのクラスタ分離 (GA)

**リリース日**: 2026-08-12

**サービス**: Bigtable

**機能**: CLUSTER_ATTRIBUTE() フィルタによる継続的マテリアライズドビューのクラスタ分離

**ステータス**: 一般提供 (GA)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260812-bigtable-cluster-attribute-materialized-views.html)

## 概要

Bigtable の継続的マテリアライズドビュー (continuous materialized view) で、`CLUSTER_ATTRIBUTE()` フィルタを使用してビューの処理を特定のクラスタに制限できる機能が一般提供 (GA) になりました。この関数を使うと、インスタンス内でビューを分離できます。

`CLUSTER_ATTRIBUTE()` は、継続的マテリアライズドビューのクエリを実行している Bigtable クラスタのメタデータにプログラムからアクセスできる非決定的 (non-deterministic) SQL 関数です。`cluster_id` 属性を指定すると、ビューを処理しているクラスタの文字列識別子が返されます。この値を SQL クエリの `WHERE` 句で定数と比較することで、指定したクラスタ (たとえば分析・レポーティング専用クラスタ) 上でのみビューの計算とストレージを行い、他のクラスタでは処理をスキップさせることができます。

レプリケーションを使用する Bigtable インスタンスで、サービング用クラスタと分析用クラスタのワークロードを分離しつつ、事前集計されたビューを分析用クラスタだけに維持したいユーザーに有用なアップデートです。

**アップデート前の課題**

- 継続的マテリアライズドビューは各クラスタが独立して処理する仕組みのため、レプリケーションを使用するインスタンスではすべてのクラスタでビューの計算と、ビューデータおよび中間ストレージの保持が発生していた
- ビューの処理対象を特定のクラスタに制限する手段がなく、インスタンス内でビューを分離できなかった
- 継続的マテリアライズドビューは全クラスタで一貫した結果を保証するため、デフォルトでは決定的 (deterministic) 関数のみをサポートしており、非決定的関数は使用できなかった

**アップデート後の改善**

- `CLUSTER_ATTRIBUTE('cluster_id')` を `WHERE` 句で使用することで、継続的マテリアライズドビューの処理を特定のクラスタに制限できるようになった
- 指定クラスタ以外のクラスタではビューの行を計算・保存しないため、コンピュートとストレージのリソースを節約できるようになった
- ソーステーブルの行に書き込んだクラスタ情報 (例: `origin_cluster` 列) と処理クラスタを照合し、データの発生元クラスタごとにビューをフィルタリングすることも可能になった

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Instance["🏢 Bigtable インスタンス (レプリケーション構成)"]
        subgraph ClusterA["🖥️ クラスタ A (サービング用)"]
            TableA[("📋 ソーステーブル<br/>レプリカ")]
            SkipA["⏭️ CMV 処理スキップ<br/>WHERE 条件 = false<br/>(計算・保存なし)"]
        end
        subgraph ClusterB["📊 クラスタ B (分析用: analytics-cluster)"]
            TableB[("📋 ソーステーブル<br/>レプリカ")]
            CMV[("📈 継続的マテリアライズドビュー<br/>WHERE CLUSTER_ATTRIBUTE('cluster_id')<br/>= 'analytics-cluster'")]
        end
    end
    App(["👤 アプリケーション"]) -->|書き込み| TableA
    TableA -.->|レプリケーション| TableB
    TableA --> SkipA
    TableB -->|バックグラウンド処理<br/>(クラスタ B のみ)| CMV
    Analyst(["👤 分析ユーザー"]) -->|シングルクラスタルーティングの<br/>アプリプロファイルで読み取り| CMV
```

`CLUSTER_ATTRIBUTE('cluster_id')` を定数と比較するフィルタにより、`WHERE` 条件が true になる分析用クラスタ B だけがビューを計算・保存し、サービング用クラスタ A はビュー処理を行わないためリソースを節約できます。

## サービスアップデートの詳細

### 主要機能

1. **CLUSTER_ATTRIBUTE() 関数 (GA)**
   - 継続的マテリアライズドビューのクエリを実行する Bigtable クラスタのメタデータにアクセスできる非決定的 SQL 関数
   - `cluster_id` 属性は、ビューを処理するクラスタの文字列識別子を返す
   - `CLUSTER_ATTRIBUTE` は「処理クラスタ」のプロパティであり、ソーステーブルに保存されたデータのプロパティではない。継続的マテリアライズドビューの処理はインスタンス内の各クラスタで独立して実行されるため、`CLUSTER_ATTRIBUTE('cluster_id')` はローカルのビュー維持処理中にそのクラスタの識別子として評価される

2. **単一クラスタへのビュー分離**
   - `CLUSTER_ATTRIBUTE('cluster_id')` をクラスタ識別子の定数文字列リテラルと比較することで、ビューの計算とストレージを単一クラスタ (専用の分析・レポーティングクラスタなど) に分離できる
   - 指定クラスタでは `WHERE` 条件が true と評価され、どのクラスタで取り込み・レプリケーションされたかに関わらずソーステーブルの全データが集計され、そのクラスタのビューのコピーにマテリアライズされる
   - 他のクラスタでは `CLUSTER_ATTRIBUTE('cluster_id')` がそれぞれのクラスタ ID として評価されるため `WHERE` 条件が false となり、ビューの行を計算も保存もしない。これによりコンピュートとストレージのリソースが節約される

3. **データの発生元クラスタによるフィルタリング**
   - アプリケーションがクラスタのメタデータをソーステーブルの行 (例: `origin_cluster` 列) に書き込んでいる場合、行の発生元クラスタと処理クラスタを照合できる
   - 各クラスタのビューのレプリカは、保存された `origin_cluster` がそのクラスタの ID と一致する行のみを集計する
   - 発生元クラスタが未指定の行がある場合は、`IF_NULL` でフォールバック用クラスタを割り当てられる

## 技術仕様

### CLUSTER_ATTRIBUTE() の主な仕様

| 項目 | 詳細 |
|------|------|
| 関数の種類 | 非決定的 (non-deterministic) SQL 関数 |
| 属性 | `cluster_id`: ビューを処理するクラスタの文字列識別子を返す |
| 作成時の要件 | ビュー作成時に `--ignore-warnings` フラグ (gcloud CLI) で意味論的差異の可能性を承認する必要がある。省略するとクエリ検証が失敗する |
| 作成方法 | 非決定的関数を使用するビューの作成は gcloud CLI を使用 (Google Cloud コンソールでは不可) |
| ビューの読み取り | シングルクラスタルーティングのアプリプロファイルを使用 (マルチクラスタルーティングは非サポート) |
| GROUP BY 列の扱い | `GROUP BY` 句の列は継続的マテリアライズドビューの行キーの一部になる |

### 単一クラスタへ分離するクエリ例

```sql
SELECT
  metrics['sensor_id'] AS sensor_id,
  COUNT(1) AS reading_count
FROM `TABLE_ID`
WHERE CLUSTER_ATTRIBUTE('cluster_id') = 'CLUSTER_ID'
GROUP BY 1
```

- `TABLE_ID`: Bigtable テーブルの一意の識別子
- `CLUSTER_ID`: ビューをマテリアライズするクラスタの識別子

## 設定方法

### 前提条件

1. ソーステーブルと同じインスタンス内に継続的マテリアライズドビューを作成すること
2. ビューの処理と同期、追加のストレージ使用に対応できるよう、クラスタに十分なノードがあること (オートスケーリングの有効化がベストプラクティス)
3. ソーステーブルの読み取り権限があること
4. 継続的マテリアライズドビューのクエリ要件 (SELECT 文、GROUP BY 句または ORDER BY 句、サポート対象の集計関数など) を満たす SQL クエリを準備すること

### 手順

#### ステップ 1: CLUSTER_ATTRIBUTE() フィルタ付きのビューを作成する

```bash
gcloud bigtable materialized-views create VIEW \
  --instance=INSTANCE \
  --query="SELECT metrics['sensor_id'] AS sensor_id, COUNT(1) AS reading_count FROM \`TABLE_ID\` WHERE CLUSTER_ATTRIBUTE('cluster_id') = 'CLUSTER_ID' GROUP BY 1" \
  --ignore-warnings
```

非決定的関数を使用する SQL クエリの場合、`--ignore-warnings` フラグが必須です。このフラグは、非決定的関数によって同じビューでもクラスタごとに異なる結果が生成される可能性があることを承認するものです。フラグを省略するとクエリ検証が失敗します。なお、非決定的関数を使用するビューはコンソールでは作成できず、gcloud CLI を使用します。

#### ステップ 2: シングルクラスタルーティングのアプリプロファイルでビューを読み取る

`CLUSTER_ATTRIBUTE` を使用するビューをクエリする際は、シングルクラスタルーティングを構成したアプリプロファイルを使用します。ビューを特定のクラスタに分離した場合は、アプリプロファイルをそのクラスタに直接向けます。ビューが作成されてからアクティブになりクエリ可能になるまで数分かかることがあります。

## メリット

### ビジネス面

- **リソースコストの削減**: 指定クラスタ以外ではビューの行を計算・保存しないため、レプリケーション構成のインスタンスにおけるコンピュートとストレージの消費を抑えられる
- **ワークロード分離による安定運用**: 分析・レポーティング用の事前集計処理を専用クラスタに閉じ込めることで、サービング用クラスタへの影響を抑えたアーキテクチャを構成できる

### 技術面

- **インスタンス内でのビュー分離**: これまで全クラスタで独立に処理されていた継続的マテリアライズドビューを、SQL の `WHERE` 句だけで特定クラスタに限定できる
- **発生元クラスタ単位の集計**: 行に記録した発生元クラスタ情報と処理クラスタを照合し、クラスタごとに異なる内容のビューレプリカを維持するといった柔軟な設計が可能
- **フルマネージド**: 継続的マテリアライズドビューは低優先度のバックグラウンドジョブとして増分更新されるため、フィルタ適用後も追加の ETL ジョブや運用作業は不要

## デメリット・制約事項

### 制限事項

- **マルチクラスタルーティング非サポート**: 関数の出力は実行する物理クラスタに依存するため、マルチクラスタルーティングでは非決定的な結果となる。`CLUSTER_ATTRIBUTE` を使用するビューのクエリにはシングルクラスタルーティングのアプリプロファイルが必要
- **指定クラスタ以外への問い合わせは空の結果**: ビューを特定クラスタに分離した場合、他のクラスタにはビューが作成されないため、他のクラスタへのクエリは空の結果を返す
- **クエリの更新は不可**: 継続的マテリアライズドビューの SQL クエリは変更できない。変更が必要な場合はビューを削除して再作成する必要がある

### 考慮すべき点

- ビュー作成時に `--ignore-warnings` フラグで「クラスタごとに異なる結果が生成される可能性」を明示的に承認する必要がある
- `CLUSTER_ATTRIBUTE` は処理クラスタのプロパティであり、データのプロパティではないという意味論を理解して設計する必要がある
- ビューを分離したクラスタが利用できない場合の可用性設計 (フェイルオーバー時の挙動) を考慮する必要がある
- 継続的マテリアライズドビューはインスタンスあたり 1,000 テーブルの上限にカウントされる

## ユースケース

### ユースケース 1: 分析専用クラスタへのビュー分離

**シナリオ**: レプリケーション構成の Bigtable インスタンスで、IoT センサーデータをサービング用クラスタで取り込みつつ、ダッシュボード向けの事前集計は分析専用クラスタでのみ実施したい。

**実装例**:
```sql
SELECT
  metrics['sensor_id'] AS sensor_id,
  COUNT(1) AS reading_count
FROM `sensor_table`
WHERE CLUSTER_ATTRIBUTE('cluster_id') = 'analytics-cluster'
GROUP BY 1
```

**効果**: 分析用クラスタだけが全データを集計・保存し、サービング用クラスタではビューの計算もストレージ消費も発生しない。集計ワークロードとサービングワークロードをインスタンス内で分離できる。

### ユースケース 2: 発生元クラスタごとの集計ビュー

**シナリオ**: 複数リージョンのクラスタでそれぞれデータを取り込んでおり、各クラスタで「そのクラスタが発生元のデータ」だけを集計したビューを保持したい。

**実装例**:
```sql
SELECT
  metrics['sensor_id'] AS sensor_id,
  COUNT(1) AS reading_count
FROM `sensor_table`
WHERE metrics['origin_cluster'] = CLUSTER_ATTRIBUTE('cluster_id')
GROUP BY 1
```

**効果**: 各クラスタのビューレプリカは、行に記録された `origin_cluster` が自クラスタ ID と一致する行のみを集計する。発生元が未指定の行には `IF_NULL(metrics['origin_cluster'], 'DEFAULT_CLUSTER_ID')` でフォールバッククラスタを割り当てられる。

## 料金

継続的マテリアライズドビュー自体にリソース単位の追加料金はありません。ただし、ビューの作成と同期には処理とストレージが必要で、標準レートで課金されます。

- **ストレージ**: ビュー内のデータと中間ストレージ (intermediate storage) の保存に対して課金される
- **コンピュート**: ソーステーブルとビューの継続的な同期に CPU 処理が必要で、バックグラウンド処理のために追加ノードが必要になる場合がある

`CLUSTER_ATTRIBUTE()` でビューを単一クラスタに分離した場合、他のクラスタではビューの行を計算・保存しないため、その分のコンピュートとストレージのリソースを節約できます。詳細は [Bigtable の料金ページ](https://cloud.google.com/bigtable/pricing) を参照してください。

## 関連サービス・機能

- **継続的マテリアライズドビュー (Continuous materialized views)**: 本機能の対象。ソーステーブルの変更を増分反映するフルマネージドの事前計算テーブルで、データの事前集計、ラムダ/カッパアーキテクチャの自動化、非同期セカンダリインデックスの作成などに使用される
- **アプリプロファイル / ルーティングポリシー**: `CLUSTER_ATTRIBUTE` を使用するビューの読み取りにはシングルクラスタルーティングのアプリプロファイルが必要
- **レプリケーション**: 継続的マテリアライズドビューは通常のテーブルと異なり、各クラスタが自身のソーステーブルのコピーを使って独立して処理する。本機能はこの動作を制御するもの
- **GoogleSQL for Bigtable**: 継続的マテリアライズドビューの定義に使用する SQL。`CLUSTER_ATTRIBUTE()` は GoogleSQL クエリの `WHERE` 句で使用する
- **オートスケーリング**: ビューの処理オーバーヘッドとストレージ需要に応じてノードを自動調整するため、ビューを含むインスタンスのクラスタでの有効化が推奨される
- **Cloud Logging / メトリクス**: `materialized_view/max_delay`、`materialized_view/storage`、`materialized_view/intermediate_storage`、`materialized_view/user_errors` などのメトリクスでビューの状態を監視できる

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260812-bigtable-cluster-attribute-materialized-views.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#August_12_2026)
- [ドキュメント: Non-deterministic SQL functions (継続的マテリアライズドビュー概要)](https://docs.cloud.google.com/bigtable/docs/continuous-materialized-views#non-deterministic-functions)
- [ドキュメント: Non-deterministic queries (CLUSTER_ATTRIBUTE の詳細)](https://docs.cloud.google.com/bigtable/docs/continuous-materialized-view-queries#non-deterministic-queries)
- [ドキュメント: 継続的マテリアライズドビューの作成と管理](https://docs.cloud.google.com/bigtable/docs/manage-continuous-materialized-views)
- [料金ページ](https://cloud.google.com/bigtable/pricing)

## まとめ

`CLUSTER_ATTRIBUTE()` フィルタの GA により、Bigtable の継続的マテリアライズドビューを特定のクラスタに分離し、レプリケーション構成のインスタンスでコンピュートとストレージを節約しながら分析ワークロードとサービングワークロードを分離できるようになりました。レプリケーションを使用しつつ継続的マテリアライズドビューを運用しているチームは、分析専用クラスタへのビュー分離を検討し、ビュー作成時の `--ignore-warnings` フラグとシングルクラスタルーティングの要件を確認することを推奨します。

---

**タグ**: Bigtable, 継続的マテリアライズドビュー, CLUSTER_ATTRIBUTE, クラスタ分離, レプリケーション, GoogleSQL, GA
