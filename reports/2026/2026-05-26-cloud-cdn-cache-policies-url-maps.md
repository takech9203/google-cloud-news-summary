# Cloud CDN: URL マップレベルでのキャッシュポリシー設定が GA

**リリース日**: 2026-05-26

**サービス**: Cloud CDN

**機能**: URL マップの各レベルにおけるキャッシュポリシーのきめ細かな制御

**ステータス**: Generally Available (GA)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260526-cloud-cdn-cache-policies-url-maps.html)

## 概要

Google Cloud は、グローバル外部アプリケーションロードバランサー (global external Application Load Balancer) において、Cloud CDN のキャッシュポリシーを URL マップの各レベルで設定できる機能を一般提供 (GA) として発表しました。これにより、ホスト名、URL パス、HTTP ヘッダー、クエリパラメータに基づいて、より細粒度なキャッシュ制御が可能になります。

この機能は 2026 年 3 月にプレビューとして公開され、約 2 ヶ月の検証期間を経て GA に到達しました。従来はバックエンドサービスまたはバックエンドバケット単位でのみキャッシュポリシーを設定可能でしたが、今回のアップデートにより URL マップの 4 つの階層（Root、Path matchers、Path rules、Route rules）でそれぞれ独立したキャッシュポリシーを定義できるようになりました。

コンテンツの種類やアクセスパターンが異なる複数のリソースを同一バックエンドで配信しているアーキテクチャにおいて、最適なキャッシュ戦略を実現するための重要な機能です。

**アップデート前の課題**

従来の Cloud CDN キャッシュポリシー設定には以下の制限がありました。

- キャッシュポリシーはバックエンドサービスまたはバックエンドバケット単位でしか設定できず、同一バックエンドで配信する全コンテンツに同じキャッシュルールが適用されていた
- 静的画像と動的 HTML ページで異なる TTL を設定したい場合、バックエンドを分離するか、オリジンサーバー側で Cache-Control ヘッダーを適切に返す必要があった
- 特定の URL パスやホスト名に対してのみキャッシュを有効化するといった柔軟な制御ができなかった

**アップデート後の改善**

今回のアップデートにより以下が可能になりました。

- URL マップの Root、Path matchers、Path rules、Route rules の 4 つのレベルで独立したキャッシュポリシーを定義可能
- ホスト名、URL パス、HTTP ヘッダー、クエリパラメータを条件として、異なるキャッシュモードや TTL を設定可能
- バックエンドを分離せずに、パスごとに最適なキャッシュ戦略（例: /images/* は 24 時間、/pages/* は 5 分）を適用可能

## アーキテクチャ図

```mermaid
flowchart TD
    Client[クライアントリクエスト] --> ALB[グローバル外部<br/>Application Load Balancer]
    ALB --> URLMap[URL マップ評価]

    URLMap --> HostCheck{ホスト名<br/>マッチ?}

    HostCheck -->|マッチなし| Root[Root レベル<br/>defaultRouteAction.cachePolicy]
    HostCheck -->|マッチ| PathCheck{パス<br/>マッチ?}

    PathCheck -->|マッチなし| PathMatcher[Path Matchers レベル<br/>pathMatchers[].defaultRouteAction.cachePolicy]
    PathCheck -->|Path Rule マッチ| PathRule[Path Rules レベル<br/>pathMatchers[].pathRules[].routeAction.cachePolicy]
    PathCheck -->|Route Rule マッチ| RouteRule[Route Rules レベル<br/>pathMatchers[].routeRules[].routeAction.cachePolicy]

    Root --> CDN[Cloud CDN キャッシュ]
    PathMatcher --> CDN
    PathRule --> CDN
    RouteRule --> CDN

    CDN --> CacheHit{キャッシュ<br/>ヒット?}
    CacheHit -->|Yes| Response[レスポンス返却]
    CacheHit -->|No| Backend[バックエンドサービス/<br/>バックエンドバケット]
    Backend --> CDN
```

この図は、クライアントリクエストが URL マップの各レベルで評価され、該当するレベルのキャッシュポリシーが適用される流れを示しています。各レベルのキャッシュポリシーはバックエンドの cdnPolicy よりも優先されます。

## サービスアップデートの詳細

### 主要機能

1. **4 階層のキャッシュポリシー定義**
   - URL マップの Root、Path matchers、Path rules、Route rules の各レベルで独立したキャッシュポリシーを設定可能
   - `routeAction` または `defaultRouteAction` がサポートされる全ての場所で cachePolicy を定義可能

2. **条件ベースのキャッシュ制御**
   - ホスト名による分岐: 異なるドメインで異なるキャッシュ戦略を適用
   - URL パスによる分岐: コンテンツの種類に応じた TTL 設定
   - HTTP ヘッダーによる分岐: 特定ヘッダーの有無でキャッシュ動作を変更
   - クエリパラメータによる分岐: パラメータ値に基づくルーティングとキャッシュ制御

3. **優先順位とフォールバックの明確なルール**
   - URL マップレベルのキャッシュポリシーはバックエンドの cdnPolicy より優先される
   - 上位レベルへのフォールバックは行われない（マッチしたルートにキャッシュポリシーがない場合はバックエンドの cdnPolicy が適用）
   - Signed URLs や動的圧縮はバックエンド設定と組み合わせて適用

## 技術仕様

### URL マップレベルとキャッシュポリシー適用条件

| URL マップレベル | API パス | 適用条件 |
|------|------|------|
| Root | `urlMap.defaultRouteAction.cachePolicy` | リクエストのホスト名が既存のホストルールにマッチしない場合 |
| Path matchers | `urlMap.pathMatchers[].defaultRouteAction.cachePolicy` | ホスト名がホストルールにマッチするが、パスルール/ルートルールにマッチしない場合 |
| Path rules | `urlMap.pathMatchers[].pathRules[].routeAction.cachePolicy` | リクエストのパスがパスルールにマッチした場合 |
| Route rules | `urlMap.pathMatchers[].routeRules[].routeAction.cachePolicy` | パス、ヘッダー、クエリパラメータの条件にマッチした場合 |

### キャッシュポリシーで設定可能なパラメータ

| パラメータ | 説明 |
|------|------|
| `cacheMode` | キャッシュモード（CACHE_ALL_STATIC / USE_ORIGIN_HEADERS / FORCE_CACHE_ALL） |
| `defaultTtl` | デフォルト TTL（最大 31,622,400 秒 = 1 年） |
| `maxTtl` | 最大 TTL |
| `clientTtl` | クライアント TTL |
| `serveWhileStale` | 再検証中に既存キャッシュを提供する時間 |
| `negativeCaching` | ネガティブキャッシング有効/無効 |
| `negativeCachingPolicy` | ステータスコードごとのキャッシュ TTL |
| `requestCoalescing` | リクエスト統合（デフォルト有効） |
| `cacheBypassRequestHeaderNames` | キャッシュバイパスヘッダー（最大 5 つ） |
| `includeHttpHeaders` | キャッシュキーに含める HTTP ヘッダー |
| `includeNamedCookies` | キャッシュキーに含める Cookie（最大 5 つ） |

### 設定例 (YAML)

```yaml
defaultUrlRedirect: null
defaultRouteAction:
  cachePolicy:
    cacheMode: CACHE_ALL_STATIC
    defaultTtl: 3600s
    maxTtl: 86400s
hostRules:
  - hosts:
      - "example.com"
    pathMatcher: example-matcher
pathMatchers:
  - name: example-matcher
    defaultRouteAction:
      cachePolicy:
        cacheMode: USE_ORIGIN_HEADERS
    pathRules:
      - paths:
          - "/images/*"
        routeAction:
          cachePolicy:
            cacheMode: FORCE_CACHE_ALL
            defaultTtl: 86400s
            maxTtl: 604800s
      - paths:
          - "/pages/*"
        routeAction:
          cachePolicy:
            cacheMode: CACHE_ALL_STATIC
            defaultTtl: 300s
            maxTtl: 3600s
    routeRules:
      - priority: 1
        matchRules:
          - prefixMatch: "/api/"
            headerMatches:
              - headerName: "X-Cache-Enabled"
                exactMatch: "true"
        routeAction:
          cachePolicy:
            cacheMode: FORCE_CACHE_ALL
            defaultTtl: 60s
            maxTtl: 300s
```

## 設定方法

### 前提条件

1. グローバル外部アプリケーションロードバランサーが設定済みであること（クラシック Application Load Balancer では非対応）
2. Cloud CDN がバックエンドサービスまたはバックエンドバケットで有効化されていること
3. 適切な IAM 権限（`compute.urlMaps.update`）を持つアカウントであること

### 手順

#### ステップ 1: 既存の URL マップ設定をエクスポート

```bash
gcloud compute url-maps export MY_URL_MAP \
    --destination=url-map-config.yaml \
    --global
```

現在の URL マップ設定を YAML ファイルとしてエクスポートします。

#### ステップ 2: キャッシュポリシーを追加

エクスポートした YAML ファイルを編集し、目的のレベルに cachePolicy を追加します。

```yaml
# Path rules レベルでのキャッシュポリシー追加例
pathMatchers:
  - name: my-path-matcher
    pathRules:
      - paths:
          - "/static/*"
        routeAction:
          cachePolicy:
            cacheMode: FORCE_CACHE_ALL
            defaultTtl: 86400s
            maxTtl: 604800s
            serveWhileStale: 86400s
        service: projects/PROJECT_ID/global/backendServices/my-backend
```

#### ステップ 3: URL マップ設定をインポート

```bash
gcloud compute url-maps import MY_URL_MAP \
    --source=url-map-config.yaml \
    --global
```

編集した設定を URL マップに適用します。

#### ステップ 4: 設定の確認

```bash
gcloud compute url-maps describe MY_URL_MAP \
    --global \
    --format=yaml
```

適用されたキャッシュポリシーが正しいことを確認します。

## メリット

### ビジネス面

- **配信コスト最適化**: コンテンツの種類に応じた最適な TTL 設定により、オリジンへのリクエスト数を最小化し、帯域コストを削減
- **ユーザー体験の向上**: 静的コンテンツの長期キャッシュと動的コンテンツの短期キャッシュを適切に分離することで、鮮度とパフォーマンスの両立が可能
- **運用負荷の軽減**: バックエンドを分離せずにキャッシュ戦略を差別化できるため、インフラ構成の簡素化が可能

### 技術面

- **きめ細かな制御**: 4 階層の URL マップレベルで独立したキャッシュポリシーを定義し、複雑なキャッシュ要件に対応
- **ゼロダウンタイム変更**: URL マップの設定変更はグローバルに伝播し、サービス中断なしにキャッシュ戦略を更新可能
- **オリジン負荷の軽減**: リクエスト統合（Request Coalescing）との組み合わせで、キャッシュミス時のオリジンへの同時リクエストを最小化

## デメリット・制約事項

### 制限事項

- グローバル外部アプリケーションロードバランサーでのみ利用可能（クラシック Application Load Balancer では非対応）
- Signed URLs および動的圧縮はバックエンドレベルでのみ設定可能であり、URL マップレベルでは定義不可
- URL マップレベルのキャッシュポリシーは上位レベルへのフォールバックを行わない（階層継承なし）
- Cookie ベースのキャッシュキーは Backend Service にルーティングされるルートでのみ有効（Backend Bucket では不可）
- キャッシュキーに含められる HTTP ヘッダーおよび Cookie はそれぞれ最大 5 つまで

### 考慮すべき点

- キャッシュポリシーの優先順位を正しく理解する必要がある（URL マップレベル > バックエンドの cdnPolicy）
- フォールバックが行われないため、全ルートに対してキャッシュポリシーを明示的に設定するか、バックエンドの cdnPolicy をデフォルトとして適切に構成する必要がある
- 設定変更のグローバル伝播には数分かかる場合があり、即時反映を期待する場合は注意が必要

## ユースケース

### ユースケース 1: E コマースサイトのマルチコンテンツキャッシュ

**シナリオ**: 商品画像、商品ページ HTML、API レスポンスを同一バックエンドで配信する E コマースサイトで、コンテンツ種別ごとに最適なキャッシュ戦略を適用したい。

**実装例**:
```yaml
pathMatchers:
  - name: ecommerce-matcher
    pathRules:
      - paths: ["/images/*", "/assets/*"]
        routeAction:
          cachePolicy:
            cacheMode: FORCE_CACHE_ALL
            defaultTtl: 604800s  # 7日間
            maxTtl: 2592000s     # 30日間
      - paths: ["/products/*"]
        routeAction:
          cachePolicy:
            cacheMode: CACHE_ALL_STATIC
            defaultTtl: 300s     # 5分
            maxTtl: 3600s        # 1時間
    routeRules:
      - priority: 1
        matchRules:
          - prefixMatch: "/api/catalog"
        routeAction:
          cachePolicy:
            cacheMode: FORCE_CACHE_ALL
            defaultTtl: 60s      # 1分
            maxTtl: 300s         # 5分
```

**効果**: 静的アセットは長期間キャッシュされてオリジン負荷を大幅削減、商品ページは適度な鮮度を維持、API レスポンスは短期キャッシュで最新データとパフォーマンスを両立。

### ユースケース 2: マルチテナント SaaS プラットフォーム

**シナリオ**: 複数のテナント（顧客企業）がそれぞれ異なるサブドメインでアクセスする SaaS プラットフォームで、テナントごとに異なるキャッシュ戦略を適用したい。

**実装例**:
```yaml
hostRules:
  - hosts: ["tenant-a.example.com"]
    pathMatcher: tenant-a-matcher
  - hosts: ["tenant-b.example.com"]
    pathMatcher: tenant-b-matcher
pathMatchers:
  - name: tenant-a-matcher
    defaultRouteAction:
      cachePolicy:
        cacheMode: FORCE_CACHE_ALL
        defaultTtl: 3600s
  - name: tenant-b-matcher
    defaultRouteAction:
      cachePolicy:
        cacheMode: USE_ORIGIN_HEADERS
```

**効果**: テナントごとの SLA やコンテンツ特性に応じたキャッシュ戦略を、単一のロードバランサー構成で実現。インフラの共有効率を維持しつつ、個別最適化が可能。

### ユースケース 3: ヘッダーベースのキャッシュバイパス

**シナリオ**: テスト環境からのリクエストや認証が必要なリクエストに対して、キャッシュをバイパスしたい。

**実装例**:
```yaml
routeRules:
  - priority: 1
    matchRules:
      - prefixMatch: "/"
        headerMatches:
          - headerName: "X-Debug"
            exactMatch: "true"
    routeAction:
      cachePolicy:
        cacheMode: CACHE_ALL_STATIC
        cacheBypassRequestHeaderNames:
          - "X-Debug"
          - "Authorization"
```

**効果**: 開発者がデバッグ用ヘッダーを付与したリクエストはキャッシュを経由せず直接オリジンに到達するため、キャッシュの影響を受けないテストが可能。

## 料金

Cloud CDN のキャッシュポリシー設定自体に追加料金は発生しません。料金は従来通り以下の要素で決定されます。

### 料金例

| 項目 | 料金 (概算) |
|--------|-----------------|
| キャッシュ配信 (北米) | $0.02 - $0.08/GB |
| キャッシュ配信 (アジア) | $0.03 - $0.10/GB |
| キャッシュフィル (オリジンへのリクエスト) | $0.01/10,000 リクエスト |
| キャッシュ無効化リクエスト | $0.005/リクエスト |

※ 最新の料金は [Cloud CDN の料金ページ](https://cloud.google.com/cdn/pricing) を参照してください。キャッシュポリシーの最適化により、キャッシュヒット率の向上とオリジンリクエストの削減が期待でき、結果的にコスト削減につながります。

## 利用可能リージョン

Cloud CDN はグローバルサービスであり、グローバル外部アプリケーションロードバランサーと連携して動作します。URL マップレベルのキャッシュポリシー機能は、グローバル外部 Application Load Balancer が利用可能な全てのリージョンで利用できます。Cloud CDN のキャッシュノードは世界中のエッジロケーションに分散配置されています。

## 関連サービス・機能

- **Cloud Load Balancing**: URL マップはグローバル外部アプリケーションロードバランサーの構成要素であり、キャッシュポリシーの設定基盤
- **Cloud Armor**: セキュリティポリシーと組み合わせることで、キャッシュ前の DDoS 防御や WAF ルールを適用可能
- **GKE Gateway**: GKE Gateway でも Cloud CDN がサポートされており（2026 年 4 月 GA）、Gateway API 経由でキャッシュ設定が可能
- **Service Extensions**: エッジエクステンション（pre-cache）とトラフィックエクステンション（post-cache）を使用して、キャッシュ処理前後にカスタムロジックを追加可能
- **Cloud Storage**: バックエンドバケットとして使用する場合、URL マップレベルのキャッシュポリシーでパスごとの TTL を制御可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260526-cloud-cdn-cache-policies-url-maps.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#May_26_2026)
- [URL マップでのキャッシュポリシー設定ドキュメント](https://docs.cloud.google.com/load-balancing/docs/https/setting-up-global-traffic-mgmt#cdn-cache-policy)
- [Cloud CDN キャッシュの概要](https://docs.cloud.google.com/cdn/docs/caching#cache-policies-url-maps)
- [Cloud CDN 料金](https://cloud.google.com/cdn/pricing)

## まとめ

Cloud CDN の URL マップレベルでのキャッシュポリシー設定が GA になったことで、グローバル外部アプリケーションロードバランサーを使用する環境において、コンテンツの特性に応じたきめ細かなキャッシュ制御が可能になりました。バックエンドの分離やオリジン側での複雑な Cache-Control ヘッダー管理に依存せず、インフラ層でキャッシュ戦略を一元管理できるため、運用効率とパフォーマンスの大幅な改善が期待できます。既存のグローバル外部 ALB + Cloud CDN 環境を運用しているチームは、コンテンツ種別ごとの TTL 最適化を検討することを推奨します。

---

**タグ**: #CloudCDN #LoadBalancing #Caching #URLMap #Performance #GA #Networking
