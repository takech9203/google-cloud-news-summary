# Google Kubernetes Engine (GKE): Cloud Storage FUSE CSI ドライバーが Google Cloud Dedicated クラスタに対応

**リリース日**: 2026-05-26

**サービス**: Google Kubernetes Engine (GKE)

**機能**: Cloud Storage FUSE CSI driver support for Google Cloud Dedicated clusters

**ステータス**: GA (一般提供)

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260526-gke-cloud-storage-fuse-dedicated.html)

## 概要

Google Kubernetes Engine (GKE) の Cloud Storage FUSE CSI ドライバーが、Google Cloud Dedicated クラスタおよびノードプールで利用可能になりました。これにより、規制要件や主権要件を満たすために専用インフラストラクチャを使用している組織が、Cloud Storage バケットをファイルシステムとして GKE Pod に直接マウントできるようになります。

Google Cloud Dedicated は、規制対象のワークロード向けに設計された分離型シングルテナントインフラストラクチャです。これまで、Dedicated 環境では Cloud Storage へのファイルシステムライクなアクセスが制限されていましたが、本アップデートにより、Dedicated クラスタのワークロードでも標準 GKE クラスタと同等の Cloud Storage FUSE 機能を利用できるようになりました。

利用するには GKE バージョン 1.36.0-gke.1266000 以上が必要であり、Dedicated 環境固有のエンドポイントに接続するために `custom-endpoint` マウントオプションの指定が必須です。

**アップデート前の課題**

- Google Cloud Dedicated クラスタでは Cloud Storage FUSE CSI ドライバーが利用できず、オブジェクトストレージへのファイルシステムライクなアクセスが困難だった
- Dedicated 環境のワークロードが Cloud Storage のデータにアクセスするには、アプリケーション側で独自の SDK 統合が必要だった
- 規制対象環境で大規模なデータ処理や ML ワークロードを実行する際、データアクセスパターンの実装が複雑だった

**アップデート後の改善**

- Dedicated クラスタの Pod から Cloud Storage バケットをローカルファイルシステムとして直接マウント可能になった
- `custom-endpoint` マウントオプションにより、Dedicated 環境専用のストレージエンドポイントに安全に接続できる
- 既存の Cloud Storage FUSE の機能 (ファイルキャッシュ、メタデータプリフェッチ、書き込みバッファリングなど) が Dedicated 環境でも利用可能になった

## アーキテクチャ図

```mermaid
architecture-beta
    group dedicated[Google Cloud Dedicated]
    group gke[GKE Cluster v1.36.0+] in dedicated
    group pod[Pod] in gke

    service app(server)[Application Container] in pod
    service sidecar(server)[FUSE Sidecar Container] in pod
    service csi(disk)[CSI Driver] in gke
    service endpoint(cloud)[Custom Endpoint] in dedicated
    service gcs(database)[Cloud Storage Bucket]

    app:R --> L:sidecar
    sidecar:B --> T:csi
    csi:R --> L:endpoint
    endpoint:R --> L:gcs
```

このアーキテクチャでは、GKE Dedicated クラスタ内の Pod にサイドカーコンテナが自動注入され、CSI ドライバーを介して custom-endpoint 経由で Cloud Storage バケットに接続します。Dedicated 環境の分離されたネットワーク内で、専用エンドポイントを通じてストレージにアクセスする構成です。

## サービスアップデートの詳細

### 主要機能

1. **Dedicated クラスタ対応**
   - Google Cloud Dedicated のクラスタとノードプールで Cloud Storage FUSE CSI ドライバーが GA として利用可能
   - シングルテナントの分離されたインフラストラクチャ上で動作
   - 既存の Cloud Storage FUSE 機能 (ephemeral volume、PersistentVolume) をサポート

2. **custom-endpoint マウントオプション**
   - Dedicated 環境の専用ストレージエンドポイントへの接続に必須
   - gcsfuse CLI のコマンドラインオプション (`--custom-endpoint`) または設定ファイル形式で指定可能
   - 標準の `storage.googleapis.com` の代わりに Dedicated 固有のエンドポイントを使用

3. **サイドカーコンテナモデル**
   - `gke-gcsfuse-sidecar` コンテナが Pod に自動注入
   - Cloud Storage FUSE のマウント処理とライフサイクル管理を担当
   - ワークロードコンテナ終了時にサイドカーも自動終了

## 技術仕様

### バージョン要件

| 項目 | 詳細 |
|------|------|
| 最小 GKE バージョン | 1.36.0-gke.1266000 |
| クラスタタイプ | Google Cloud Dedicated |
| ドライバー有効化 | `GcsFuseCsiDriver` アドオン |
| 認証方式 | Workload Identity Federation for GKE |

### custom-endpoint の設定方法

**方法 1: gcsfuse CLI オプション**

```bash
gcsfuse --custom-endpoint=DEDICATED_STORAGE_ENDPOINT BUCKET_NAME /mount/path
```

**方法 2: 設定ファイル形式 (gcsfuse.yaml)**

```yaml
storage:
  custom-endpoint: "https://DEDICATED_STORAGE_ENDPOINT"
```

### Pod マニフェスト例

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dedicated-gcsfuse-pod
  annotations:
    gke-gcsfuse/volumes: "true"
spec:
  containers:
  - name: app
    image: my-app:latest
    volumeMounts:
    - name: gcs-data
      mountPath: /data
  volumes:
  - name: gcs-data
    csi:
      driver: gcsfuse.csi.storage.gke.io
      volumeAttributes:
        bucketName: my-dedicated-bucket
        mountOptions: "custom-endpoint=DEDICATED_STORAGE_ENDPOINT"
```

## 設定方法

### 前提条件

1. Google Cloud Dedicated 環境がプロビジョニング済みであること
2. GKE クラスタが バージョン 1.36.0-gke.1266000 以上であること
3. Cloud Storage FUSE CSI ドライバーアドオンが有効であること
4. Workload Identity Federation for GKE が構成済みであること
5. Dedicated 環境の custom-endpoint URL を把握していること

### 手順

#### ステップ 1: CSI ドライバーの有効化

```bash
gcloud container clusters update CLUSTER_NAME \
  --update-addons GcsFuseCsiDriver=ENABLED \
  --location=LOCATION
```

Dedicated クラスタで Cloud Storage FUSE CSI ドライバーアドオンを有効にします。

#### ステップ 2: Cloud Storage バケットへのアクセス権限の設定

```bash
# Kubernetes サービスアカウントに Cloud Storage へのアクセス権限を付与
gcloud storage buckets add-iam-policy-binding gs://BUCKET_NAME \
  --member="principal://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/PROJECT_ID.svc.id.goog/subject/ns/NAMESPACE/sa/KSA_NAME" \
  --role="roles/storage.objectUser"
```

Workload Identity Federation を使用して、Pod のサービスアカウントにバケットへのアクセス権限を付与します。

#### ステップ 3: custom-endpoint を指定した Pod のデプロイ

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dedicated-app
  annotations:
    gke-gcsfuse/volumes: "true"
spec:
  serviceAccountName: my-ksa
  containers:
  - name: app
    image: my-app:latest
    volumeMounts:
    - name: gcs-volume
      mountPath: /data
  volumes:
  - name: gcs-volume
    csi:
      driver: gcsfuse.csi.storage.gke.io
      volumeAttributes:
        bucketName: my-bucket
        mountOptions: "custom-endpoint=DEDICATED_STORAGE_ENDPOINT,implicit-dirs"
```

`custom-endpoint` マウントオプションで Dedicated 環境のストレージエンドポイントを指定します。

## メリット

### ビジネス面

- **コンプライアンス対応**: 規制要件 (データ主権、SecNumCloud 等) を満たしながら Cloud Storage の利便性を活用可能
- **運用統合**: Dedicated 環境でも標準 GKE と同じワークフローでストレージアクセスを実現し、運用負荷を軽減
- **パートナーエコシステム**: ローカル運用パートナー (Thales/S3NS 等) が管理する環境でも Cloud Storage を活用可能

### 技術面

- **透過的なファイルアクセス**: アプリケーションコードの変更なしに Cloud Storage をファイルシステムとして利用可能
- **パフォーマンス最適化**: ファイルキャッシュ、メタデータプリフェッチ、書き込みバッファリングにより I/O パフォーマンスを最適化
- **ライフサイクル管理**: サイドカーコンテナがワークロードに連動して自動管理されるため、リソースの無駄が発生しない

## デメリット・制約事項

### 制限事項

- GKE バージョン 1.36.0-gke.1266000 以上が必須であり、それ以前のバージョンでは利用不可
- `custom-endpoint` マウントオプションの指定が必須であるため、既存のマニフェストの修正が必要
- Dedicated 環境固有のエンドポイント情報を事前に取得・管理する必要がある

### 考慮すべき点

- Cloud Storage FUSE はオブジェクトストレージ上のファイルシステムエミュレーションであり、POSIX 完全互換ではない (rename 操作のアトミック性など)
- 高頻度のランダム書き込みワークロードには Persistent Disk の方が適している場合がある
- Dedicated 環境のネットワーク構成により、スループットが標準環境と異なる可能性がある
- サイドカーコンテナのリソース消費 (デフォルト: 250m CPU、256 MiB メモリ) を考慮したキャパシティプランニングが必要

## ユースケース

### ユースケース 1: 規制対象の ML/AI トレーニング

**シナリオ**: 金融機関や政府機関が、規制要件に準拠した Dedicated 環境上で機械学習モデルのトレーニングを実行する場合。大量のトレーニングデータを Cloud Storage に格納し、GKE 上の ML ワークロードから効率的にアクセスする必要がある。

**実装例**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ml-training
  annotations:
    gke-gcsfuse/volumes: "true"
    gke-gcsfuse/memory-limit: "8Gi"
    gke-gcsfuse/cpu-limit: "4"
spec:
  serviceAccountName: ml-training-sa
  containers:
  - name: trainer
    image: ml-training:latest
    volumeMounts:
    - name: training-data
      mountPath: /data/training
      readOnly: true
    - name: model-output
      mountPath: /data/models
  volumes:
  - name: training-data
    csi:
      driver: gcsfuse.csi.storage.gke.io
      volumeAttributes:
        bucketName: regulated-training-data
        mountOptions: "custom-endpoint=DEDICATED_ENDPOINT,implicit-dirs,file-cache:max-size-mb:-1"
  - name: model-output
    csi:
      driver: gcsfuse.csi.storage.gke.io
      volumeAttributes:
        bucketName: regulated-model-output
        mountOptions: "custom-endpoint=DEDICATED_ENDPOINT,implicit-dirs"
```

**効果**: データ主権要件を維持しながら、Cloud Storage の大容量・低コストストレージを ML トレーニングデータとして活用。ファイルキャッシュにより繰り返しアクセスのパフォーマンスを向上。

### ユースケース 2: データ分析パイプライン

**シナリオ**: 欧州の規制に準拠した Dedicated 環境で、複数のバッチ処理ジョブが共有データセットにアクセスするデータ分析パイプラインを構築する場合。

**効果**: ReadWriteMany アクセスモードにより、複数の Pod から同一バケットへの同時アクセスが可能。Dedicated 環境内でデータを保持しながら、スケーラブルな並列処理を実現。

## 料金

Cloud Storage FUSE CSI ドライバー自体の追加料金は発生しません。料金は以下の要素で構成されます。

### 料金例

| 使用量 | 月額料金 (概算) |
|--------|-----------------|
| Cloud Storage Standard (100 GB) | 約 $2.30/月 |
| Cloud Storage Standard (1 TB) | 約 $23.00/月 |
| Class A オペレーション (10,000 回) | 約 $0.05 |
| Class B オペレーション (100,000 回) | 約 $0.04 |
| GKE Dedicated クラスタ | Dedicated 契約に準拠 |

注意: Google Cloud Dedicated の利用料金は個別契約となります。Cloud Storage の料金は標準料金に基づきますが、Dedicated 環境では契約形態により異なる場合があります。

## 利用可能リージョン

Google Cloud Dedicated がデプロイされているリージョンで利用可能です。現在、Dedicated は主に以下の地域で提供されています:

- 欧州 (フランス: Thales/S3NS パートナーシップによる SecNumCloud 対応)
- その他の Dedicated 契約が締結されている地域

具体的な利用可能リージョンは Google Cloud Dedicated の契約内容に依存します。

## 関連サービス・機能

- **Google Cloud Dedicated**: 規制対象ワークロード向けの分離型シングルテナントインフラストラクチャ。本アップデートの基盤環境
- **Cloud Storage**: スケーラブルなオブジェクトストレージ。FUSE を通じてファイルシステムとしてアクセス可能
- **Cloud Storage FUSE**: Cloud Storage バケットをローカルファイルシステムとしてマウントする FUSE アダプター
- **Workload Identity Federation for GKE**: GKE Pod への IAM 権限付与メカニズム。Cloud Storage アクセスの認証に使用
- **Assured Workloads**: コンプライアンス要件を満たすためのワークロード管理サービス

## 参考リンク

- [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260526-gke-cloud-storage-fuse-dedicated.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#May_26_2026)
- [Cloud Storage FUSE CSI driver for GKE ドキュメント](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/cloud-storage-fuse-csi-driver)
- [Cloud Storage FUSE CSI driver セットアップガイド](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/cloud-storage-fuse-csi-driver-setup)
- [Cloud Storage FUSE CLI オプション](https://docs.cloud.google.com/storage/docs/cloud-storage-fuse/cli-options)
- [Google Cloud Sovereign Cloud](https://cloud.google.com/sovereign-cloud)

## まとめ

Cloud Storage FUSE CSI ドライバーの Google Cloud Dedicated 対応は、規制環境で GKE を利用する組織にとって重要なアップデートです。データ主権やコンプライアンス要件を維持しながら、Cloud Storage の柔軟性とスケーラビリティを活用できるようになりました。Dedicated 環境で GKE ワークロードを運用している組織は、クラスタバージョンを 1.36.0-gke.1266000 以上にアップグレードし、`custom-endpoint` マウントオプションを使用した設定を検討することを推奨します。

---

**タグ**: #GKE #CloudStorage #FUSE #CSIDriver #GoogleCloudDedicated #SovereignCloud #Kubernetes #コンプライアンス #データ主権 #GA
