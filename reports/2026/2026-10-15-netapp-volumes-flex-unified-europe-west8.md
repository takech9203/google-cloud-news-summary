# Google Cloud NetApp Volumes: Flex Unified サービスレベルが europe-west8 (ミラノ) で利用可能に

**リリース日**: 2026-10-15

**サービス**: Google Cloud NetApp Volumes

**機能**: Flex Unified サービスレベル (カスタムパフォーマンス含む) の europe-west8 リージョン対応

**ステータス**: Announcement (リージョン拡大)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261015-netapp-volumes-flex-unified-europe-west8.html)

## 概要

Google Cloud NetApp Volumes の Flex Unified サービスレベルが、カスタムパフォーマンス機能を含めて europe-west8 (ミラノ、イタリア) リージョンで利用可能になりました。

Flex Unified は、NetApp Volumes の中で最も柔軟性の高いサービスレベルで、容量とパフォーマンスを独立してプロビジョニングできる「カスタムパフォーマンス」をサポートします。小規模な 1 GiB のボリュームから大容量プールまで幅広く対応し、Default モードと ONTAP モードの 2 つの動作モードを提供します。なお、2026 年 9 月 15 日以降、従来の Flex File ストレージプールの新規作成は不可となっており、Flex Unified が後継の位置付けです。

今回のリージョン拡大により、イタリア国内にワークロードやデータを配置する必要があるユーザー (データレジデンシー要件のある企業など) が、ミラノリージョンで Flex Unified の機能をフル活用できるようになりました。

**アップデート前の課題**

- europe-west8 (ミラノ) では Flex Unified サービスレベルを利用できず、同リージョンにデータを置きたい場合は他のサービスレベルを選択するか、別リージョン (europe-west1、europe-west3 など) を利用する必要があった
- イタリア国内のデータレジデンシー要件を満たしつつ、容量とパフォーマンスを独立して設定できるストレージ構成を取ることが難しかった

**アップデート後の改善**

- europe-west8 で Flex Unified ストレージプールを作成できるようになった
- カスタムパフォーマンス機能も同時にサポートされ、容量とは独立してスループット・IOPS をプロビジョニングできるようになった
- ミラノリージョンで低レイテンシーなファイルストレージ (NFS/SMB など) を Flex Unified で構成可能になった

## サービスアップデートの詳細

### Flex Unified サービスレベルの主な特徴

1. **柔軟な容量設定**
   - ストレージプール: 1 TiB 〜 425 TiB (1 GiB 単位で増加可能)
   - ボリューム: 1 GiB 〜 300 TiB (1 GiB 単位で増減可能)

2. **カスタムパフォーマンス**
   - プールのパフォーマンスを容量とは独立して設定可能
   - デフォルト: プールあたり 64 MiBps / 1,024 IOPS
   - スループットは 1 MiBps 単位で最大 5 GiBps まで引き上げ可能 (1 MiBps ごとに 16 IOPS が付与)
   - IOPS はプールあたり最大 160,000 IOPS までプロビジョニング可能
   - プール内の全ボリュームでパフォーマンスを共有 (小さいボリュームが余剰パフォーマンスを利用可能)

3. **2 つの動作モード**
   - Default モードと ONTAP モードを選択可能
   - 手動 QoS、オートティアリング (ホットティア自動拡張付き)、ゾーン/リージョナルの高可用性構成に対応

## 技術仕様

| 項目 | 詳細 |
|------|------|
| 対象リージョン | europe-west8 (ミラノ、イタリア) |
| サービスレベル | Flex Unified (カスタムパフォーマンス含む) |
| プール容量 | 1 TiB 〜 425 TiB |
| プールあたり最大パフォーマンス | 5 GiBps スループット / 160,000 IOPS |
| 高可用性 | ゾーン / リージョナル |

## メリット

### ビジネス面

- **データレジデンシー対応**: イタリア国内 (ミラノ) にデータを保持する要件を満たしながら、Flex Unified の柔軟なストレージ構成を利用できる
- **コスト最適化**: 容量とパフォーマンスを独立してプロビジョニングできるため、ワークロードに合わせた無駄のないサイジングが可能

### 技術面

- **低レイテンシー**: イタリア周辺のコンピュートワークロードから近接したファイルストレージへアクセス可能
- **柔軟なスケーリング**: 1 GiB 単位の細かい容量調整と、1 MiBps 単位のスループット調整が可能

## 利用可能リージョン

今回 europe-west8 (ミラノ) が追加されました。Flex Unified および各サービスレベルの対応リージョンの全一覧は、公式ドキュメントの [Supported regions](https://docs.cloud.google.com/netapp/volumes/docs/discover/service-levels#supported_regions) を参照してください。

## 関連サービス・機能

- **Compute Engine / GKE**: NetApp Volumes は NFS/SMB ファイルストレージとして VM や GKE ワークロードから利用される
- **Flex File サービスレベル**: 2026 年 9 月 15 日以降は新規プール作成が不可となっており、Flex Unified への移行が推奨されている
- **バックアップ / ボリュームレプリケーション**: Flex Unified は通常プール間でのゾーン間・リージョン間レプリケーションやバックアップボールトに対応

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261015-netapp-volumes-flex-unified-europe-west8.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#October_15_2026)
- [サービスレベルのドキュメント](https://docs.cloud.google.com/netapp/volumes/docs/discover/service-levels)
- [ボリュームパフォーマンスのサイジング](https://docs.cloud.google.com/netapp/volumes/docs/plan-and-prepare/volume-performance-sizing)
- [料金ページ](https://cloud.google.com/netapp/volumes/pricing)

## まとめ

Flex Unified サービスレベル (カスタムパフォーマンス含む) が europe-west8 (ミラノ) に拡大され、イタリア国内でのデータレジデンシー要件を満たしつつ、容量とパフォーマンスを独立してプロビジョニングできる柔軟なファイルストレージが利用可能になりました。ミラノリージョンでファイルストレージを検討している場合は、Flex Unified の採用を検討してください。

---

**タグ**: NetApp Volumes, Flex Unified, リージョン拡大, europe-west8, ストレージ
