# Cloud Service Mesh: EnvoyFilter API サポート (TRAFFIC_DIRECTOR 実装)

**リリース日**: 2026-04-02

**サービス**: Cloud Service Mesh

**機能**: EnvoyFilter API (TRAFFIC_DIRECTOR 実装)

**ステータス**: Announcement

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260402-cloud-service-mesh-envoyfilter.html)

## 概要

Managed Cloud Service Mesh の TRAFFIC_DIRECTOR 実装において、EnvoyFilter API の限定的なサポートが追加された。これにより、他の Istio API では実現できなかったデータプレーンの拡張機能を、EnvoyFilter API を通じて利用できるようになる。

EnvoyFilter API は Envoy プロキシの設定を直接カスタマイズするための強力な API であり、HTTP フィルタチェーンへのフィルタ追加などが可能になる。特にローカルレートリミットや gRPC-Web フィルタなど、サービスメッシュのトラフィック制御における重要な拡張機能が利用可能となった。

ただし、この機能はサポートされるフィールドとエクステンションが限定されており、誤った設定がメッシュの安定性に影響を与える可能性があるため、他の Istio API で要件を満たせない場合にのみ使用することが推奨されている。

**アップデート前の課題**

- TRAFFIC_DIRECTOR 実装の Managed Cloud Service Mesh では、EnvoyFilter API によるデータプレーンのカスタマイズができなかった
- ローカルレートリミットなど、標準の Istio API では提供されない高度なトラフィック制御機能を利用できなかった
- Envoy プロキシの HTTP フィルタチェーンをカスタマイズする手段がなく、データプレーンの拡張性に制限があった

**アップデート後の改善**

- EnvoyFilter API を使用して、TRAFFIC_DIRECTOR 実装でもデータプレーンの拡張が可能になった
- ローカルレートリミット (envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit) を設定できるようになった
- gRPC-Web フィルタ (envoy.extensions.filters.http.grpc_web.v3.GrpcWeb) が利用可能になった
- HTTP フィルタチェーンへのフィルタ挿入 (INSERT_FIRST、INSERT_BEFORE) が可能になった

## アーキテクチャ図

```mermaid
flowchart TD
    User["👤 ユーザー"] --> |"kubectl apply"| EF["📝 EnvoyFilter CR"]
    EF --> |"設定伝播"| CP["☁️ TRAFFIC_DIRECTOR\nコントロールプレーン"]
    CP --> |"xDS 設定配信"| EP1["🔧 Envoy Sidecar\n(Pod A)"]
    CP --> |"xDS 設定配信"| EP2["🔧 Envoy Sidecar\n(Pod B)"]

    subgraph HTTP フィルタチェーン
        direction LR
        RL["🚦 Local Rate Limit\nフィルタ"] --> GW["🌐 gRPC-Web\nフィルタ"] --> RT["🔀 Router\nフィルタ"]
    end

    EP1 --> HTTP フィルタチェーン
    EP2 --> HTTP フィルタチェーン

    style CP fill:#4285F4,color:#fff
    style EF fill:#34A853,color:#fff
    style RL fill:#FBBC04,color:#333
    style GW fill:#FBBC04,color:#333
    style RT fill:#EA4335,color:#fff
```

EnvoyFilter CR を適用すると、TRAFFIC_DIRECTOR コントロールプレーンが xDS 経由で各 Envoy サイドカーに設定を配信し、HTTP フィルタチェーンにローカルレートリミットや gRPC-Web などのフィルタが挿入される。

## サービスアップデートの詳細

### 主要機能

1. **EnvoyFilter API の限定サポート**
   - TRAFFIC_DIRECTOR コントロールプレーン実装でのみ利用可能
   - `configPatches[].applyTo` は `HTTP_FILTER` のみサポート
   - `configPatches[].patch.operation` は `INSERT_FIRST` および `INSERT_BEFORE` (Router フィルタとの組み合わせ) のみサポート

2. **ローカルレートリミットフィルタ**
   - `envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit` エクステンションをサポート
   - トークンバケット、フィルタの有効化/強制化、レスポンスヘッダの追加、ダウンストリーム接続ごとのレート制限などの設定が可能
   - Rapid、Regular、Stable の全リリースチャンネルで利用可能

3. **gRPC-Web フィルタ**
   - `envoy.extensions.filters.http.grpc_web.v3.GrpcWeb` エクステンションをサポート
   - gRPC-Web クライアントからのリクエストを gRPC バックエンドサービスに中継可能
   - 全リリースチャンネルで利用可能

## 技術仕様

### サポートされる API フィールド

| フィールド | サポート状況 |
|------|------|
| `targetRefs` | 非サポート |
| `configPatches[].applyTo` | `HTTP_FILTER` のみ |
| `configPatches[].patch.operation` | `INSERT_FIRST`、`INSERT_BEFORE` (Router フィルタ使用時) |
| `configPatches[].patch.filterClass` | 非サポート |
| `configPatches[].match.proxy` | 非サポート |
| `configPatches[].match.routeConfiguration` | 非サポート |
| `configPatches[].match.cluster` | 非サポート |

### INSERT_BEFORE 操作でサポートされるフィールド

| フィールド | サポート値 |
|------|------|
| `configPatches[].match.listener` | `filter` のみ |
| `configPatches[].match.listener.filter.name` | `envoy.filters.network.http_connection_manager` のみ |
| `configPatches[].match.listener.filter.subFilter.name` | `envoy.filters.http.router` のみ |

### ローカルレートリミットの設定例

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: local-ratelimit
  namespace: istio-system
spec:
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      listener:
        filter:
          name: envoy.filters.network.http_connection_manager
          subFilter:
            name: envoy.filters.http.router
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.filters.http.local_ratelimit
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
          stat_prefix: http_local_rate_limiter
          token_bucket:
            max_tokens: 100
            tokens_per_fill: 100
            fill_interval: 60s
          filter_enabled:
            runtime_key: local_rate_limit_enabled
            default_value:
              numerator: 100
              denominator: HUNDRED
          filter_enforced:
            runtime_key: local_rate_limit_enforced
            default_value:
              numerator: 100
              denominator: HUNDRED
```

## 設定方法

### 前提条件

1. Cloud Service Mesh が TRAFFIC_DIRECTOR コントロールプレーン実装で有効化されていること
2. GKE クラスタに Managed Cloud Service Mesh がプロビジョニングされていること
3. `kubectl` コマンドがクラスタに接続されていること

### 手順

#### ステップ 1: コントロールプレーン実装の確認

```bash
# コントロールプレーン実装を確認
kubectl get controlplanerevision -n istio-system -o yaml
```

TRAFFIC_DIRECTOR 実装であることを確認する。ISTIOD 実装の場合、この機能は利用できない。

#### ステップ 2: EnvoyFilter の適用

```bash
# EnvoyFilter リソースを適用
kubectl apply -f envoyfilter.yaml
```

#### ステップ 3: 設定の検証

```bash
# EnvoyFilter CR のステータスを確認
kubectl get envoyfilter <NAME> -n <NAMESPACE> -o yaml

# Envoy のコンフィグダンプで設定の伝播を確認
gcloud beta container fleet mesh debug proxy-config <POD_NAME>.<NAMESPACE> \
  --type=listener \
  --membership=<MEMBERSHIP_ID> \
  --location=<MEMBERSHIP_LOCATION> \
  --project=<PROJECT_ID> \
  --output=yaml | grep envoy.filters.http.local_ratelimit -C 5
```

## メリット

### ビジネス面

- **トラフィック制御の強化**: ローカルレートリミットにより、サービスの過負荷を防止し、安定したサービス提供が可能になる
- **マネージドサービスでの拡張性**: マネージドコントロールプレーンを利用しながらも、高度なデータプレーンカスタマイズが可能になった

### 技術面

- **Envoy ネイティブの拡張機能**: Istio API の範囲を超えた Envoy の機能を直接利用できる
- **ローカルレートリミット**: 外部のレートリミットサービスを必要とせず、各 Envoy プロキシでローカルにレート制限を実施可能
- **gRPC-Web 対応**: ブラウザベースの gRPC-Web クライアントからのリクエストをメッシュ内でシームレスに処理可能

## デメリット・制約事項

### 制限事項

- TRAFFIC_DIRECTOR コントロールプレーン実装でのみサポートされ、ISTIOD 実装では利用不可
- `applyTo` は `HTTP_FILTER` のみに限定されており、ネットワークフィルタやクラスタ設定の変更はできない
- `patch.operation` は `INSERT_FIRST` と `INSERT_BEFORE` のみで、`MERGE` や `REMOVE` は非サポート
- サポートされるエクステンションはローカルレートリミットと gRPC-Web の 2 種類のみ
- Google のサポート範囲は、ユーザー提供の設定を Envoy サイドカーへ伝播することに限定され、各エクステンション API の設定の正確性については対象外

### 考慮すべき点

- EnvoyFilter API は Envoy の内部実装に依存しており、誤った設定がメッシュ全体の安定性に影響する可能性がある
- 他の Istio API (VirtualService、DestinationRule など) で要件を満たせる場合は、そちらを優先して使用すべき
- EnvoyFilter の設定変更は、コントロールプレーンの 2 パス設定コミットにより反映までに時間がかかる場合がある

## ユースケース

### ユースケース 1: マイクロサービスのローカルレートリミット

**シナリオ**: 特定のマイクロサービスに対するリクエストが急増した場合に、サービスの過負荷を防ぐためにローカルレートリミットを設定する。

**実装例**:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: payment-service-ratelimit
  namespace: payment
spec:
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      listener:
        filter:
          name: envoy.filters.network.http_connection_manager
          subFilter:
            name: envoy.filters.http.router
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.filters.http.local_ratelimit
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
          stat_prefix: payment_rate_limiter
          token_bucket:
            max_tokens: 50
            tokens_per_fill: 50
            fill_interval: 60s
          filter_enabled:
            default_value:
              numerator: 100
              denominator: HUNDRED
          filter_enforced:
            default_value:
              numerator: 100
              denominator: HUNDRED
          status:
            code: 429
```

**効果**: 外部のレートリミットサービスを構築することなく、各 Envoy サイドカーレベルで 1 分あたり 50 リクエストの制限を適用し、決済サービスの安定性を確保できる。

### ユースケース 2: gRPC-Web クライアントのサポート

**シナリオ**: ブラウザベースの gRPC-Web クライアントから gRPC バックエンドサービスへのリクエストを、サービスメッシュ内で透過的に処理する。

**効果**: gRPC-Web プロトコル変換がメッシュ内の Envoy サイドカーで自動的に処理され、バックエンドサービスの変更なしに Web クライアントからの gRPC 通信が可能になる。

## 料金

Cloud Service Mesh の料金は、マネージドコントロールプレーンの利用に基づく。EnvoyFilter API の利用自体に追加料金は発生しない。詳細は公式の料金ページを参照のこと。

- [Cloud Service Mesh 料金ページ](https://cloud.google.com/service-mesh/pricing)

## 関連サービス・機能

- **Cloud Armor**: サービスメッシュでのサーバーサイドグローバルレートリミットを提供。EnvoyFilter のローカルレートリミットとは異なり、集中管理型のレート制限を実施可能
- **Cloud Monitoring**: Envoy エクステンションが出力する統計情報を Cloud Monitoring で可視化し、フィルタの動作状態を監視可能
- **GKE (Google Kubernetes Engine)**: Cloud Service Mesh のデータプレーンが動作する基盤。マネージドデータプレーンにより Envoy サイドカーの自動アップグレードが可能
- **Istio API (VirtualService, DestinationRule)**: EnvoyFilter を使用する前に、まずこれらの標準 Istio API で要件を満たせないか検討すべき

## 参考リンク

- [このアップデートのインフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260402-cloud-service-mesh-envoyfilter.html)
- [公式リリースノート](https://cloud.google.com/release-notes#April_02_2026)
- [Data plane extensibility with EnvoyFilter](https://cloud.google.com/service-mesh/docs/data-plane-extensibility)
- [Resolving data plane extensibility issues](https://cloud.google.com/service-mesh/docs/troubleshooting/troubleshoot-data-plane-extensibility)
- [Supported features using Istio APIs (managed control plane)](https://cloud.google.com/service-mesh/docs/supported-features-managed)
- [Cloud Service Mesh 料金ページ](https://cloud.google.com/service-mesh/pricing)

## まとめ

Cloud Service Mesh の TRAFFIC_DIRECTOR 実装における EnvoyFilter API サポートは、マネージドサービスメッシュ環境でのデータプレーン拡張性を大幅に向上させるアップデートである。特にローカルレートリミット機能は、外部依存なしにサービスの過負荷保護を実現できる点で実用性が高い。ただし、サポートされるフィールドとエクステンションが限定されているため、まず標準の Istio API で要件を満たせないか確認し、本当に必要な場合にのみ EnvoyFilter API を利用することを推奨する。

---

**タグ**: #CloudServiceMesh #EnvoyFilter #TRAFFIC_DIRECTOR #レートリミット #サービスメッシュ #Envoy #gRPC-Web #データプレーン
