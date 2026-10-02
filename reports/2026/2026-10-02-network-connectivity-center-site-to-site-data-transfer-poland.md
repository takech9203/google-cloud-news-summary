# Network Connectivity Center: サイト間データ転送がポーランドをサポート

**リリース日**: 2026-10-02

**サービス**: Network Connectivity Center

**機能**: サイト間データ転送 (Site-to-site data transfer) のポーランド対応

**ステータス**: Feature (一般提供)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261002-network-connectivity-center-site-to-site-data-transfer-poland.html)

## 概要

Network Connectivity Center (NCC) のサイト間データ転送 (site-to-site data transfer) 機能が、新たにポーランドでサポートされました。これにより、ポーランドのリージョン (europe-central2 / ワルシャワ) に接続リソースを配置し、Google のグローバルネットワークを WAN バックボーンとして活用した拠点間通信が可能になります。

サイト間データ転送は、オンプレミスのデータセンターや他のクラウドにある外部サイト同士を、Google のネットワーク経由で接続する機能です。Cloud VPN (HA VPN)、Cloud Interconnect、Router appliance といった接続リソースを NCC のスポークとして中央のハブに接続することで、すべてのスポーク間にフルメッシュの接続が自動的に確立されます。

今回のアップデートの対象ユーザーは、ポーランド国内または中東欧地域に拠点を持ち、複数拠点間のネットワークを Google Cloud を介して統合したい企業です。既存の MPLS 網や専用線によるハブ & スポーク構成を、Google のバックボーンを使った構成に置き換える選択肢が広がります。

**アップデート前の課題**

- サイト間データ転送はヨーロッパではベルギー、フィンランド、フランス、ドイツ、イタリア、オランダ、スペイン、スウェーデン、スイス、英国などの国に限定されており、ポーランドのリージョンではサポートされていなかった
- ポーランドのリージョン (europe-central2) にスポークを作成しても、サイト間データ転送を有効化できず、近隣国 (ドイツなど) の対応リージョンに接続リソースを配置する必要があった
- 非対応リージョンに接続リソースを配置した場合、ルート広告の構成を工夫しないとサイト間接続が失敗するリスクがあった

**アップデート後の改善**

- ポーランドのリージョンに作成した NCC スポークでサイト間データ転送を有効化できるようになった
- ポーランド国内の拠点が最寄りの接続ポイントを利用でき、レイテンシの低減と構成の簡素化が期待できる
- 中東欧地域の拠点を含むグローバル WAN を、Google ネットワークを介して構成しやすくなった

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph PL["🇵🇱 ポーランド拠点"]
        SiteA(["🏢 ワルシャワ オフィス"])
    end
    subgraph GC["☁️ Google Cloud"]
        SpokeA["🔌 スポーク A<br/>europe-central2<br/>(HA VPN / Interconnect)"]
        Hub{{"🌐 NCC ハブ"}}
        SpokeB["🔌 スポーク B<br/>europe-west3<br/>(HA VPN / Interconnect)"]
    end
    subgraph DE["🇩🇪 ドイツ拠点"]
        SiteB(["🏢 フランクフルト オフィス"])
    end

    SiteA -->|"BGP / 暗号化トンネル"| SpokeA
    SpokeA -->|"データ転送"| Hub
    Hub -->|"データ転送"| SpokeB
    SpokeB -->|"BGP / 暗号化トンネル"| SiteB
```

ポーランドのリージョンに配置したスポークがサイト間データ転送に対応したことで、ポーランドの拠点と他国の拠点を Google のバックボーンネットワーク経由でフルメッシュ接続できます。

## サービスアップデートの詳細

### 主要機能

1. **ポーランドでのサイト間データ転送サポート**
   - ポーランドのリージョンに作成したスポークで、サイト間データ転送を有効化可能になった
   - スポーク作成時に「Site-to-site data transfer」を On にすることで利用できる

2. **サイト間データ転送 (site-to-site data transfer)**
   - Google のネットワークを WAN の一部として利用し、オンプレミス拠点や他クラウドのネットワーク同士を接続する機能
   - 各サイトを Cloud VPN (HA VPN トンネル)、Cloud Interconnect、Router appliance で Google Cloud に接続し、それぞれを NCC スポークとしてハブに登録
   - ハブに接続されたすべてのスポーク間でフルメッシュ接続が確立され、ルートが自動的に交換される

3. **ハブ & スポークによる一元管理**
   - 複数拠点の接続を 1 つのハブに集約し、ネットワーク構成を一元的に管理できる
   - Cloud Router との BGP によるダイナミックルーティングで、拠点のプレフィックスが自動的に伝播される

## 技術仕様

### サイト間データ転送の対応地域 (今回の更新後)

| 地域 | 対応国 |
|------|--------|
| アフリカ | 南アフリカ |
| APAC | オーストラリア、インド、インドネシア、日本、韓国、シンガポール、台湾 |
| ヨーロッパ | ベルギー、フィンランド、フランス、ドイツ、イタリア、オランダ、**ポーランド (新規)**、スペイン、スウェーデン、スイス、英国 |
| 中東 | イスラエル、カタール |
| 北米 | カナダ、メキシコ、米国 |
| 南米 | ブラジル、チリ |

### サイト間データ転送の要件

| 項目 | 詳細 |
|------|------|
| 対応接続リソース | Cloud VPN (HA VPN トンネル)、Cloud Interconnect (VLAN アタッチメント)、Router appliance |
| VPC ネットワーク | データ転送を有効にしたスポークの接続リソースは、すべて単一の VPC ネットワークに所属する必要がある |
| ダイナミックルーティングモード | 複数リージョンのスポーク間でルートを交換する場合、VPC の動的ルーティングモードを `global` に設定 |
| 高可用性 | スポークに関連付ける接続リソースはすべて高可用性構成が必須 |
| ASN | サイト間データ転送向けの ASN 要件に従う必要がある |
| ルート広告 | 各スポークのオンプレミスルーターは、スポークに対応する Cloud Router に同一のルートを広告する |

## 設定方法

### 前提条件

1. NCC ハブが作成済みであること
2. ポーランドのリージョンに HA VPN トンネル、VLAN アタッチメント、または Router appliance インスタンスなどの接続リソースが高可用性構成で作成済みであること
3. VPC の動的ルーティングモードが `global` に設定されていること (複数リージョン間でルートを交換する場合)

### 手順

#### ステップ 1: ハブの作成 (未作成の場合)

```bash
gcloud network-connectivity hubs create my-hub \
    --description="Global WAN hub"
```

拠点間接続の中心となる NCC ハブを作成します。

#### ステップ 2: データ転送を有効にしたスポークの作成

```bash
# 例: ポーランドのリージョンの HA VPN トンネルをスポークとして追加
gcloud network-connectivity spokes linked-vpn-tunnels create warsaw-spoke \
    --hub=my-hub \
    --region=europe-central2 \
    --vpn-tunnels=tunnel-1,tunnel-2 \
    --site-to-site-data-transfer
```

`--site-to-site-data-transfer` フラグを指定することで、サイト間データ転送が有効になります。Google Cloud コンソールの場合は、スポーク作成フォームで「Site-to-site data transfer」を **On** に設定します (非対応リージョンではこのフィールドは無効化されます)。

#### ステップ 3: 他拠点のスポークを追加

```bash
gcloud network-connectivity spokes linked-vpn-tunnels create frankfurt-spoke \
    --hub=my-hub \
    --region=europe-west3 \
    --vpn-tunnels=tunnel-3,tunnel-4 \
    --site-to-site-data-transfer
```

他拠点のスポークも同様に追加すると、ハブを介してスポーク間のフルメッシュ接続とルート交換が確立されます。

## メリット

### ビジネス面

- **WAN コストの最適化**: 専用線や MPLS 網の代わりに Google のバックボーンを利用でき、拠点間接続の調達・運用コストを削減できる可能性がある
- **中東欧拠点のカバレッジ向上**: ポーランドに拠点を持つ企業が最寄りの接続ポイントを利用でき、グローバル WAN 設計の自由度が高まる

### 技術面

- **構成の簡素化**: ポーランドの拠点を近隣国の対応リージョン経由で接続する回避策が不要になり、ルート広告の設計がシンプルになる
- **フルメッシュ接続の自動化**: ハブにスポークを追加するだけで拠点間のルート交換が自動的に行われ、拠点ごとのピア設定が不要
- **レイテンシの低減が期待できる**: ポーランド国内の拠点が地理的に近い europe-central2 に接続できる

## デメリット・制約事項

### 制限事項

- サイト間のデータ転送トラフィックはベストエフォートであり、帯域幅やレイテンシの保証はない
- データ転送を有効にしたスポークの接続リソースは、すべて単一の VPC ネットワークに属している必要がある
- Classic VPN トンネルはサポートされない (HA VPN が必要)
- Cloud Router のカスタム学習ルートは、この機能に関連する BGP セッションでは外部サイトに伝播されない

### 考慮すべき点

- 複数のスポークから同一サブネットへの重複ルート広告がある場合、リソースタイプに応じた優先度 (VLAN アタッチメント > Cloud VPN > Router appliance) で、同一タイプ間では ECMP でトラフィックが分散される
- ルーティングプレフィックスはハブの内側または外側のどちらかで排他的に広告する必要がある (混在するとスポークに関連付けられていないルートが選択される可能性がある)
- 冗長構成の一部が非対応リージョンにある場合は、ルート広告の構成に注意が必要 (混合広告の構成ガイドを参照)

## ユースケース

### ユースケース 1: ポーランドとドイツの拠点間を Google ネットワークで接続

**シナリオ**: 製造業の企業がワルシャワとフランクフルトにオフィスを持ち、専用線の代わりに Google Cloud を経由して拠点間を接続したい。

**実装例**:
```bash
# ワルシャワ拠点: europe-central2 の HA VPN スポーク
gcloud network-connectivity spokes linked-vpn-tunnels create warsaw-spoke \
    --hub=my-hub --region=europe-central2 \
    --vpn-tunnels=warsaw-tunnel-1,warsaw-tunnel-2 \
    --site-to-site-data-transfer

# フランクフルト拠点: europe-west3 の VLAN アタッチメントスポーク
gcloud network-connectivity spokes linked-vlan-attachments create frankfurt-spoke \
    --hub=my-hub --region=europe-west3 \
    --vlan-attachments=fra-attachment-1,fra-attachment-2 \
    --site-to-site-data-transfer
```

**効果**: 専用線の調達なしに、Google のバックボーンを利用した低レイテンシな拠点間接続を実現。ハブで接続を一元管理できる。

### ユースケース 2: 中東欧を含むグローバル WAN の統合

**シナリオ**: 欧州、アジア、北米に拠点を持つ多国籍企業が、ポーランドの開発拠点を既存の NCC ベースのグローバル WAN に追加したい。

**効果**: 既存ハブにポーランドのスポークを追加するだけで、全拠点とのフルメッシュ接続とルート交換が自動的に確立される。従来必要だった近隣リージョン経由の迂回構成が不要になる。

## 料金

NCC の料金は「スポーク時間課金」と「データ転送課金」で構成されます。ハブ自体は無料です。

| リソース | 料金 (USD) |
|----------|-----------|
| ハブ | 無料 |
| スポーク時間 (Cloud Interconnect / Cloud VPN / Router appliance スポーク) | $0.075 / 時間 |
| スポーク時間 (VPC スポーク / producer VPC スポーク) | $0.10 / 時間 |
| サイト間データ転送 | 送信元・宛先リージョンの組み合わせに応じた GiB 単価 |

### 料金例

| 使用量 | 月額料金 (概算) |
|--------|-----------------|
| ハイブリッドスポーク 2 個 (24 時間 x 30 日) | 2 x 720 時間 x $0.075 = $108.00 + データ転送料金 |

このほか、Cloud VPN トンネルや VLAN アタッチメント自体の料金が別途発生します。詳細は [NCC 料金ページ](https://cloud.google.com/network-connectivity/pricing#ncc-pricing) を参照してください。

## 利用可能リージョン

ポーランドの Google Cloud リージョンは europe-central2 (ワルシャワ) です。サイト間データ転送の対応地域の全リストは [NCC locations ドキュメント](https://docs.cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/locations) を参照してください。

## 関連サービス・機能

- **Cloud VPN (HA VPN)**: サイトを Google Cloud に接続する接続リソース。IPsec トンネルで暗号化された接続を提供し、NCC スポークとして登録できる
- **Cloud Interconnect**: Dedicated / Partner Interconnect の VLAN アタッチメントをスポークとして利用可能。大容量・低レイテンシの接続に適する
- **Cloud Router**: 各スポークと BGP セッションを確立し、拠点のルートを動的に交換する
- **Router appliance**: サードパーティのネットワーク仮想アプライアンスを Google Cloud 上に配置し、Cloud Router とルートを交換する NCC の機能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261002-network-connectivity-center-site-to-site-data-transfer-poland.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#October_02_2026)
- [サイト間データ転送の概要](https://docs.cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/data-transfer)
- [NCC の対応ロケーション](https://docs.cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/locations)
- [NCC の概要](https://docs.cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/overview)
- [料金ページ](https://cloud.google.com/network-connectivity/pricing#ncc-pricing)

## まとめ

ポーランドが NCC のサイト間データ転送の対応国に加わったことで、中東欧に拠点を持つ企業が Google のバックボーンを活用したグローバル WAN を構成しやすくなりました。ポーランドの拠点を持つ組織は、europe-central2 にスポークを配置した構成を検討し、既存の専用線や迂回構成からの移行可否を評価することを推奨します。

---

**タグ**: Network Connectivity Center, NCC, site-to-site data transfer, Poland, europe-central2, ネットワーク, ハイブリッド接続, WAN
