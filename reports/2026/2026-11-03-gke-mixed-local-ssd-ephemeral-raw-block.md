# Google Kubernetes Engine: Local SSD のエフェメラルストレージと raw ブロックストレージの混在構成 (Mixed Local SSD)

**リリース日**: 2026-11-03

**サービス**: Google Kubernetes Engine (GKE)

**機能**: Local SSD のエフェメラルストレージ / raw ブロックストレージ分割 (Mixed Local SSD)

**ステータス**: Feature (GKE Standard クラスタ)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261103-gke-mixed-local-ssd-ephemeral-raw-block.html)

## 概要

GKE バージョン 1.37.0-gke.3570000 以降で、ノードに接続された各 Local SSD の容量を「エフェメラルストレージ」と「raw ブロックストレージ」に分割して利用できるようになりました。クラスタまたはノードプールの作成時に `--ephemeral-storage-local-ssd` フラグの `capacity` プロパティを指定すると、GKE はその容量だけを エフェメラルストレージとしてフォーマットし、残りの容量は未フォーマットのまま raw ブロックデバイスとしてノードに提供します。

エフェメラル部分は各 Local SSD に均等に分割されたうえで RAID-0 アレイとして結合され、標準の `emptyDir` ボリュームとして利用できます。raw ブロック部分は、データベースやキャッシュのようにディスクへの直接アクセスで性能を最大化したいワークロードが、local PersistentVolume を通じて利用できます。

この機能により、サイドカーやログ、コンテナキャッシュ用のファイルストレージと、高性能なダイレクトディスクアクセスの両方を同一ノードで両立でき、ハードウェア使用率の最大化とクラスタ管理オーバーヘッドの削減が可能になります。本機能は GKE Standard クラスタで利用できます。

**アップデート前の課題**

- 以前は Local SSD を「全量エフェメラルストレージ」(`--ephemeral-storage-local-ssd`) か「全量 raw ブロックストレージ」(`--local-nvme-ssd-block`) のどちらか一方の構成でしか使用できなかった
- raw ブロックストレージが必要なワークロードと、通常のエフェメラルファイルストレージが必要なワークロードを同居させるには、ノードやディスクを用途別に分ける必要があり、ハードウェア使用率が低下していた
- raw ブロック専用のノードプールを別途運用することで、クラスタ管理のオーバーヘッドが増加していた

**アップデート後の改善**

- 1 台のノード上で、同じ Local SSD をエフェメラルストレージと raw ブロックストレージに分割して併用できるようになった
- データベースやキャッシュなどの高性能ワークロードが raw ブロックを使いながら、同一ノードのサイドカーやログは標準の `emptyDir` を利用できるようになった
- raw ブロック専用のノードやディスクを用意する必要がなくなり、ハードウェア使用率の最大化と管理負荷の軽減が実現した

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Node["🖥️ GKE ノード (1.37.0-gke.3570000+)"]
        subgraph SSD1[("💽 Local SSD #1")]
            E1["📁 エフェメラル領域<br/>(フォーマット済み)"]
            B1["🧱 raw ブロック領域<br/>(未フォーマット)"]
        end
        subgraph SSD2[("💽 Local SSD #2")]
            E2["📁 エフェメラル領域<br/>(フォーマット済み)"]
            B2["🧱 raw ブロック領域<br/>(未フォーマット)"]
        end
        RAID["🔗 RAID-0 アレイ<br/>(エフェメラルストレージ)"]
        E1 --> RAID
        E2 --> RAID
    end
    Flag["⚙️ --ephemeral-storage-local-ssd<br/>count=N,capacity=XXX GB"] --> Node
    RAID --> EmptyDir["📦 Pod: emptyDir ボリューム<br/>(ログ / キャッシュ / サイドカー)"]
    B1 --> PV["🗄️ local PersistentVolume<br/>(StorageClass: WaitForFirstConsumer)"]
    B2 --> PV
    PV --> DB["🐘 Pod: データベース / キャッシュ<br/>(ダイレクトディスクアクセス)"]
```

`capacity` で指定した容量が各 Local SSD に均等に割り当てられて RAID-0 のエフェメラルストレージとなり、残りの容量は各ディスクごとに未フォーマットの raw ブロックデバイスとして提供されます。

## サービスアップデートの詳細

### 主要機能

1. **`capacity` プロパティによる容量分割**
   - `--ephemeral-storage-local-ssd` フラグに `capacity` サブフィールドを指定し、エフェメラルストレージとしてフォーマットする容量を設定する
   - 指定値は 0 より大きく、物理 Local SSD 総容量 (ディスク数 × ディスクあたり容量) 未満である必要がある
   - Local SSD 数が構成可能なマシンタイプでは `count` サブフィールドも指定する。`-lssd` タイプなど固定数のマシンタイプでは `count` を省略でき、GKE が VM シェイプから自動計算する

2. **エフェメラルストレージ部分 (RAID-0)**
   - 指定容量が各 Local SSD に均等に分割され、RAID-0 アレイとして結合される
   - 標準の `emptyDir` ボリュームとして、通常の GKE エフェメラルボリュームと同じ方法でアクセスできる
   - GKE がシステム用に一部を予約するため、割り当て可能なエフェメラルストレージは `capacity` 指定値より少なくなる

3. **raw ブロックストレージ部分**
   - 各ディスクの残容量が、未フォーマットの個別 raw ブロックデバイスとしてノードに提供される
   - GKE はフォーマットもマウントも行わないため、ユーザーがデバイスを手動構成し、StorageClass + local PersistentVolume + PersistentVolumeClaim で利用する
   - データベースやキャッシュなど、直接ディスクアクセスによる高性能が必要なワークロードに適する

4. **ノードラベルによる識別**
   - 混在構成のノードには `cloud.google.com/gke-ephemeral-storage-local-ssd: "true"` と `cloud.google.com/gke-local-nvme-ssd-partition: "true"` の両方のラベルが付与される
   - `gke-local-nvme-ssd-partition` ラベルは、全量 raw ブロック構成で使われる `gke-local-nvme-ssd=true` ラベルとは別物である点に注意

## 技術仕様

### 混在構成の仕様

| 項目 | 詳細 |
|------|------|
| 必要バージョン | GKE 1.37.0-gke.3570000 以降 (それ以前の場合は `--cluster-version` / `--node-version` 指定、または `--release-channel=rapid`) |
| 対象クラスタ | GKE Standard クラスタのみ (Autopilot 非対応) |
| 設定フラグ | `--ephemeral-storage-local-ssd count=N,capacity=XXX` |
| `capacity` の制約 | 0 より大きく、物理総容量 (ディスク数 × ディスクサイズ) 未満。作成後の変更は不可 |
| エフェメラル部分 | 各ディスクに均等分割 + RAID-0 結合、`emptyDir` でアクセス |
| raw ブロック部分 | ディスクごとに未フォーマットのブロックデバイスとして提供 |
| 対応 OS | Linux ノードイメージのみ (Container-Optimized OS、Ubuntu)。Windows Server は非対応 |
| ノードラベル | `cloud.google.com/gke-ephemeral-storage-local-ssd: "true"`、`cloud.google.com/gke-local-nvme-ssd-partition: "true"` |
| マシンタイプ | Local SSD 対応マシンタイプが必要 (共有コアタイプの e2-medium などは不可) |

### raw ブロック用 StorageClass の例

PersistentVolume のバインドを Pod スケジューリングまで遅延させるため、`volumeBindingMode: WaitForFirstConsumer` の StorageClass を作成することが推奨されています。

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: "local-storage"
provisioner: "kubernetes.io/no-provisioner"
volumeBindingMode: "WaitForFirstConsumer"
```

## 設定方法

### 前提条件

1. GKE Standard クラスタであること (Autopilot は非対応)
2. クラスタ / ノードプールのバージョンが 1.37.0-gke.3570000 以降であること (それ未満の場合はバージョンフラグで明示指定)
3. Local SSD をサポートするマシンタイプを使用すること (リージョンとマシンタイプにより接続可能なディスク数が異なる)

### 手順

#### ステップ 1: 混在構成のクラスタを作成

```bash
# Local SSD 数が構成可能なマシンタイプの場合
gcloud container clusters create CLUSTER_NAME \
    --machine-type=MACHINE_TYPE \
    --ephemeral-storage-local-ssd count=NUMBER_OF_DISKS,capacity=CAPACITY

# Local SSD 数が固定のマシンタイプ (-lssd タイプなど) の場合
gcloud container clusters create CLUSTER_NAME \
    --machine-type=MACHINE_TYPE \
    --ephemeral-storage-local-ssd capacity=CAPACITY
```

`CAPACITY` にはエフェメラルストレージとしてフォーマットする総容量 (例: `200GB`) を指定します。この設定はデフォルトノードプールにのみ適用されます。

#### ステップ 2: 既存クラスタにノードプールを追加

```bash
gcloud container node-pools create POOL_NAME \
    --cluster=CLUSTER_NAME \
    --machine-type=MACHINE_TYPE \
    --ephemeral-storage-local-ssd count=NUMBER_OF_DISKS,capacity=CAPACITY
```

#### ステップ 3: ノードラベルの確認

```bash
kubectl describe node NODE_NAME
```

出力に `cloud.google.com/gke-ephemeral-storage-local-ssd: "true"` と `cloud.google.com/gke-local-nvme-ssd-partition: "true"` の両方のラベルが含まれていることを確認します。

#### ステップ 4: raw ブロック容量の利用

`WaitForFirstConsumer` の StorageClass を作成し、local PersistentVolume をプロビジョニングして PersistentVolumeClaim で要求します。エフェメラル容量は通常の `emptyDir` ボリュームとしてそのまま利用できます。

## メリット

### ビジネス面

- **ハードウェア使用率の最大化**: raw ブロック用に専用ノードやディスク全体を割り当てる必要がなくなり、購入済みの Local SSD 容量を無駄なく活用できる
- **運用コストの削減**: 用途別に分かれていたノードプールを統合でき、クラスタ管理のオーバーヘッドが減少する

### 技術面

- **性能と利便性の両立**: データベースやキャッシュはダイレクトディスクアクセスで低レイテンシ・高 IOPS を得つつ、同一ノードのサイドカーやログは標準のエフェメラルファイルストレージを利用できる
- **標準 API での利用**: エフェメラル部分は `emptyDir`、raw ブロック部分は local PersistentVolume という Kubernetes 標準の仕組みで利用でき、Pod スケジューリングとの統合も可能

## デメリット・制約事項

### 制限事項

- GKE Autopilot クラスタでは混在構成を利用できない (Standard クラスタのみ)
- カスタム ComputeClass は混在 Local SSD 構成をサポートしない
- Linux ノードイメージ (Container-Optimized OS、Ubuntu) のみ対応。Windows Server ノードプールは非対応
- `capacity` の値はクラスタ / ノードプール作成後に変更できない
- GKE がシステム用に容量の一部を予約するため、実際に割り当て可能なエフェメラルストレージは `capacity` 指定値より少なくなる
- ノードメモリスワップとの併用では、dedicated Local SSD プロファイルは非対応 (ブートディスクまたはエフェメラル Local SSD プロファイルは併用可能)

### 考慮すべき点

- **共有 I/O**: エフェメラルの RAID-0 アレイと raw ブロックパーティションは同じ物理 SSD を共有するため、一方での高負荷な I/O が他方のスループットに影響する可能性がある
- **メンテナンスイベント**: ストレージ最適化の Z3 / Z4D VM では、メンテナンスイベント時にデータが保持されない可能性があるため、raw ブロックストレージとしての利用は推奨されない
- **手動構成が必要**: raw ブロック部分は GKE がフォーマット・マウントを行わないため、デバイスの構成、ノード容量の管理、同居ワークロードによる中断への対処はユーザーの責任となる
- **RAID DaemonSet の禁止**: 全量 raw ブロック構成で使われるコミュニティの RAID DaemonSet (`gke-daemonset-raid-disks.yaml`) を混在構成ノードで実行してはならない。GKE が管理するエフェメラル容量が破壊される
- 永続性や特殊な性能要件がないワークロードには、従来どおり全量エフェメラル構成が推奨される

## ユースケース

### ユースケース 1: 高性能データベースとサイドカーの同居

**シナリオ**: 低レイテンシ・高 IOPS が必要なセルフマネージドのデータベース (例: 分散 KVS や検索エンジン) を GKE 上で運用しており、同じ Pod やノードでログ収集サイドカーやコンテナキャッシュも動かしたい。

**実装例**:
```bash
gcloud container node-pools create db-pool \
    --cluster=my-cluster \
    --machine-type=n2-standard-32 \
    --ephemeral-storage-local-ssd count=4,capacity=400GB
```

raw ブロック部分 (残容量) を local PersistentVolume としてデータベースに割り当て、エフェメラル部分 (400GB から予約分を除いた容量) をログやキャッシュ用の `emptyDir` として利用する。

**効果**: データベースはダイレクトディスクアクセスによる最大性能を得ながら、専用ノードを分離することなくサイドカー用のファイルストレージも確保でき、ノード数とコストを削減できる。

### ユースケース 2: キャッシュ層のハードウェア使用率最適化

**シナリオ**: Local SSD を raw ブロックで使うインメモリキャッシュ (永続化オフロード付き) を運用しているが、ディスク全体をキャッシュに割り当てると容量が余り、エフェメラルストレージ不足で別のディスクが必要になっていた。

**効果**: 1 枚の Local SSD をキャッシュ用 raw ブロックとエフェメラルストレージに分割できるため、余剰容量を無駄にせず、ノードあたりのディスク枚数を削減できる。

## 料金

混在構成で Local SSD 容量を分割しても、料金はエフェメラル / raw ブロックの割り当て比率に関係なく、ノードに接続された**物理 Local SSD の総容量**に対して課金されます。Local SSD は GB あたり月額の従量課金で、Spot VM 向けの割引価格や、リソースベースの確約利用割引 (CUD) も利用できます。

最新の単価は公式料金ページを参照してください。

- [Local SSD の料金](https://cloud.google.com/compute/disks-image-pricing#localssdpricing)
- [ストレージ最適化 VM の料金 (Titanium SSD)](https://cloud.google.com/products/compute/pricing/storage-optimized)

## 利用可能リージョン

Local SSD を利用できるリージョン / ゾーンおよびマシンタイプごとの接続可能ディスク数に依存します。詳細は [Local SSD のドキュメント](https://docs.cloud.google.com/compute/docs/disks/local-ssd#choose_number_local_ssds) を参照してください。

## 関連サービス・機能

- **Compute Engine Local SSD**: 本機能の基盤となる物理接続型の高性能一時ストレージ。IOPS とレイテンシの特性、マシンシリーズ対応状況は Compute Engine 側の仕様に準拠する
- **GKE Local SSD エフェメラルストレージ (全量構成)**: 永続性や特殊な性能要件がない場合に推奨される従来構成。`emptyDir` によるアクセス方法は共通
- **GKE Local SSD raw ブロックストレージ (全量構成)**: ディスク全体を raw ブロックとして使う既存機能。混在構成とはノードラベルや RAID DaemonSet の扱いが異なる
- **GKE ノードメモリスワップ**: ブートディスクプロファイルまたはエフェメラル Local SSD プロファイルで混在構成と併用可能
- **local PersistentVolume / StorageClass**: raw ブロック部分を Pod スケジューリングと統合して利用するための Kubernetes 標準機能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261103-gke-mixed-local-ssd-ephemeral-raw-block.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#November_03_2026)
- [ドキュメント: Provision and use mixed Local SSDs for raw block and ephemeral storage](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/mixed-local-ssd)
- [ドキュメント: Local SSD-backed raw block storage](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/local-ssd-raw)
- [ドキュメント: Compute Engine Local SSD](https://docs.cloud.google.com/compute/docs/disks/local-ssd)
- [料金ページ: Local SSD](https://cloud.google.com/compute/disks-image-pricing#localssdpricing)

## まとめ

GKE 1.37.0-gke.3570000 以降の Standard クラスタで、Local SSD をエフェメラルストレージと raw ブロックストレージに分割して併用できるようになり、高性能データベース・キャッシュと通常のファイルストレージ需要を同一ノードで両立できるようになりました。raw ブロック専用のノードプールを分けて運用しているチームは、本機能によるノード統合とハードウェア使用率改善を検討する価値があります。導入時は `capacity` が作成後に変更できない点と、共有 I/O による性能影響を考慮したサイジングを行ってください。

---

**タグ**: #GKE #LocalSSD #Storage #Kubernetes #RawBlock #EphemeralStorage #PersistentVolume
