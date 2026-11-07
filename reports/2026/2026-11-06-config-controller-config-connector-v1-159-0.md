# Config Controller: 同梱される Config Connector が v1.159.0 に更新

**リリース日**: 2026-11-06

**サービス**: Config Controller

**機能**: Config Connector v1.159.0 への更新

**ステータス**: GA (バージョン更新)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261106-config-controller-config-connector-v1-159-0.html)

## 概要

Config Controller に同梱される Config Connector が v1.159.0 に更新されました。Config Controller は、Kubernetes スタイルの宣言的な構成 (KRM: Kubernetes Resource Model) で Google Cloud リソースをプロビジョニング・管理できるマネージドサービスで、Config Connector と Config Sync をホストするマネージドコントロールプレーンを提供します。

Config Controller が同梱する Config Connector は、前回のバージョン更新 (2026 年 9 月 18 日) 時点では v1.156.0 でした。今回の更新により v1.157.0、v1.158.0 を経て v1.159.0 (2026 年 10 月 13 日リリース) までの機能強化・バグ修正が Config Controller ユーザーにも提供されます。

v1.159.0 では、Eventarc パイプラインや Live Stream チャンネルなどの新しい Alpha リソース、Cloud SQL Enterprise Plus エディションのディザスタリカバリ (DR) ペア設定のサポート、GKE Autopilot クラスタの特権アドミッション設定などが追加されています。Config Controller で IaC (Infrastructure as Code) を運用しているプラットフォームチームにとって、管理対象リソースの範囲と運用性が向上するアップデートです。

**アップデート前の課題**

- Config Controller に同梱される Config Connector は v1.156.0 ベースであり、v1.157.0 以降で追加されたリソースやフィールドを利用できなかった
- Cloud SQL Enterprise Plus エディションの DR ペア構成を Config Connector の管理下に置くと、DR 関連の設定がドリフトとして検出される課題があった
- BigQueryDataset のアクセスエントリで誤検知の差分が発生し、リソースが最新状態でも冗長な PATCH リクエストが送られることがあった

**アップデート後の改善**

- Config Controller 上で Config Connector v1.159.0 の新リソース・新フィールド (Eventarc Pipeline、ContainerCluster の `spec.privilegedAdmissionConfig` など) が利用可能になった
- `cnrm.cloud.google.com/sqlinstance-advanced-dr: "enabled"` アノテーションにより、Cloud SQL Enterprise Plus の DR ペア設定とドリフト抑制がサポートされた
- BigQueryDataset、ComputeRouterNAT、MonitoringDashboard の調整 (reconciliation) に関するバグが修正され、安定性が向上した

## アーキテクチャ図

```mermaid
flowchart TD
    User([👤 プラットフォームチーム]) -->|KRM マニフェスト適用| CC

    subgraph CC["☁️ Config Controller (マネージドインスタンス)"]
        KCC["⚙️ Config Connector<br/>v1.156.0 → v1.159.0 に更新"]
        CS["🔄 Config Sync"]
    end

    Git[("📦 Git リポジトリ")] -->|構成を同期| CS
    CS --> KCC

    KCC -->|調整 (Reconcile)| GCP["🌐 Google Cloud API"]
    GCP --> R1["🗄️ Cloud SQL<br/>(Enterprise Plus DR ペア対応)"]
    GCP --> R2["🚢 GKE Autopilot<br/>(privilegedAdmissionConfig)"]
    GCP --> R3["📨 Eventarc Pipeline など<br/>(新規 Alpha リソース)"]
```

Config Controller は Config Connector と Config Sync をホストするマネージドコントロールプレーンであり、今回の更新で Config Connector が v1.159.0 となり、管理できるリソースとフィールドが拡充されます。

## サービスアップデートの詳細

### 主要機能 (Config Connector v1.159.0 の変更点)

1. **新しい Alpha リソース (Direct Reconciler)**
   - `AIPlatformReasoningEngine`: Gemini Enterprise Agent Platform の推論エンジンを管理
   - `CloudDeployCustomTargetType`: Cloud Deploy のカスタムターゲットタイプを管理
   - `EventarcPipeline`: Google Cloud サービス間でイベントを変換・ルーティングするパイプラインを管理
   - `LiveStreamChannel` / `LiveStreamInput`: ライブ動画の取り込み・エンコード・配信チャンネルと入力エンドポイントを管理
   - `MapManagementStyleConfig`: Map Management API のカスタムマップスタイルを管理
   - `NetworkSecurityDNSThreatDetector`: DNS ベースの脅威を監視・軽減する検出器を管理

2. **既存リソースへの新フィールド追加**
   - `ArtifactRegistryRepository`: `spec.remoteRepositoryConfig.commonRepository` をサポート
   - `ComposerEnvironment`: Cloud Composer 3 環境での `spec.config.workloadsConfig.dagProcessor` の更新をサポート
   - `ContainerCluster`: Autopilot クラスタの特権アドミッションを構成する `spec.privilegedAdmissionConfig` をサポート
   - `SQLInstance`: DR 関連の観測フィールド (`status.observedState.replicationCluster` 配下の `failoverDRReplicaName`、`drReplica`、`psaWriteEndpoint` と `status.observedState.masterInstanceName`) を追加

3. **新機能**
   - `cnrm.cloud.google.com/sqlinstance-advanced-dr: "enabled"` アノテーションによる Cloud SQL Enterprise Plus エディションの DR ペア設定とドリフト抑制のサポート
   - オペレーター構成の `resourceSettings` 変更時に Manager Pod が自動的に再起動するように改善
   - Argo CD などの GitOps ツールで Config Connector を管理するためのガイドを追加

4. **バグ修正**
   - `BigQueryDataset`: アクセスエントリの誤検知差分と、最新状態のリソースへの冗長な PATCH リクエストを修正
   - `ComputeRouterNAT`: Direct コントローラー移行時の誤ったドリフト検出と定常状態の調整の問題を修正
   - `MonitoringDashboard`: 未認識の enum 値による調整エラーを、Direct コントローラーの Google REST クライアント移行により修正

## 技術仕様

### Config Controller に同梱されるコンポーネント

| 項目 | 詳細 |
|------|------|
| 同梱 Config Connector バージョン | v1.159.0 (2026 年 10 月 13 日リリース) |
| 前回の同梱バージョン | v1.156.0 (2026 年 9 月 18 日の Config Controller 更新時点) |
| Config Controller の位置付け | GKE 標準機能の一部として利用可能 (2025 年 9 月以降、GKE Enterprise 不要) |
| 更新の適用 | Config Controller はマネージドサービスのため、同梱バージョンは Google 側で更新される |

### Cloud SQL DR ペア設定の例 (v1.159.0 の新機能)

```yaml
apiVersion: sql.cnrm.cloud.google.com/v1beta1
kind: SQLInstance
metadata:
  name: primary-instance
  annotations:
    cnrm.cloud.google.com/sqlinstance-advanced-dr: "enabled"
spec:
  # Enterprise Plus エディションの DR ペア構成で
  # DR 関連設定のドリフトが抑制される
```

## メリット

### ビジネス面

- **IaC カバレッジの拡大**: Eventarc、Live Stream、Cloud Deploy カスタムターゲットなど、より多くの Google Cloud リソースを宣言的に管理でき、手動運用の削減につながる
- **DR 運用の信頼性向上**: Cloud SQL Enterprise Plus の DR ペアを Config Connector 管理下に置いても意図しないドリフト検出が発生せず、GitOps フローと DR 構成を両立できる

### 技術面

- **調整処理の安定化**: BigQueryDataset の冗長な PATCH リクエスト抑制や ComputeRouterNAT の誤ドリフト修正により、コントローラーの動作が安定し API クォータの浪費も減る
- **GitOps 連携の明確化**: Argo CD などの GitOps ツールで Config Connector を管理する公式ガイドが追加され、運用設計の指針が得られる

## デメリット・制約事項

### 考慮すべき点

- 今回追加された新リソースは Alpha ステータスの Direct Reconciler ベースであり、本番利用の前にステータスと挙動の確認が必要
- Config Controller はマネージドサービスのため、同梱される Config Connector のバージョンはユーザーが個別に固定・選択できない
- セルフマネージドで Config Connector を利用している場合は、別途自身で v1.159.0 へのアップグレードが必要

## ユースケース

### ユースケース 1: Cloud SQL Enterprise Plus の DR 構成を GitOps で管理

**シナリオ**: ミッションクリティカルなデータベースを Enterprise Plus エディションの DR ペアで運用しており、構成は Git リポジトリ + Config Controller で宣言的に管理したい。

**実装例**:
```yaml
metadata:
  annotations:
    cnrm.cloud.google.com/sqlinstance-advanced-dr: "enabled"
```

**効果**: DR ペア設定が Config Connector のドリフト検出と競合せず、DR 構成と GitOps 運用を安全に両立できる。また `status.observedState.replicationCluster` で DR レプリカの状態を KRM 経由で観測できる。

### ユースケース 2: イベント駆動アーキテクチャの宣言的管理

**シナリオ**: Eventarc を使ったイベント駆動アーキテクチャを構築しており、パイプラインの構成も他のリソースと同じ KRM マニフェストで管理したい。

**効果**: `EventarcPipeline` (Alpha) により、イベントの変換・ルーティング構成を Git 管理下に置き、環境間で再現可能なイベント基盤を構築できる。

## 料金

今回のアップデートはバージョン更新であり、料金体系の変更は発表されていません。Config Controller の料金は公式料金ページを参照してください。

- [Config Controller の料金](https://cloud.google.com/kubernetes-engine/config-controller/docs/pricing)

## 関連サービス・機能

- **Config Connector**: Kubernetes 経由で Google Cloud リソースを管理するアドオン。本更新の中心コンポーネント
- **Config Sync**: Git リポジトリから Kubernetes クラスタへ構成を同期する GitOps ツール。Config Controller に同梱される
- **GKE (Google Kubernetes Engine)**: Config Controller は GKE 標準機能の一部として提供される
- **Cloud SQL**: v1.159.0 で Enterprise Plus エディションの DR ペア設定サポートが追加された
- **Eventarc / Cloud Deploy / Live Stream API**: v1.159.0 で新たに Alpha リソースとして管理可能になったサービス群

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261106-config-controller-config-connector-v1-159-0.html)
- [公式リリースノート (Google Cloud Release Notes)](https://docs.cloud.google.com/release-notes#November_06_2026)
- [Config Controller リリースノート](https://docs.cloud.google.com/kubernetes-engine/config-controller/docs/release-notes)
- [Config Connector リリースノート (v1.159.0: October 13, 2026)](https://docs.cloud.google.com/config-connector/docs/release-notes#October_13_2026)
- [Config Controller 概要](https://docs.cloud.google.com/anthos-config-management/docs/concepts/config-controller-overview)

## まとめ

Config Controller に同梱される Config Connector が v1.159.0 に更新され、Eventarc Pipeline などの新リソース、Cloud SQL Enterprise Plus の DR ペア対応、複数の調整処理のバグ修正が利用可能になりました。Config Controller で IaC を運用しているチームは、v1.157.0〜v1.159.0 の変更点 (特に利用中リソースのフィールド追加とバグ修正) を確認し、新機能の活用を検討することを推奨します。

---

**タグ**: #ConfigController #ConfigConnector #GKE #IaC #GitOps #Kubernetes #KRM
