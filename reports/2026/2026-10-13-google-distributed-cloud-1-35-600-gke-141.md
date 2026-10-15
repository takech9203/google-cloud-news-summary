# Google Distributed Cloud (software only): VMware 版 / ベアメタル版 1.35.600-gke.141 リリース

**リリース日**: 2026-10-13

**サービス**: Google Distributed Cloud (software only) for VMware / for bare metal

**機能**: パッチリリース 1.35.600-gke.141 (脆弱性修正)

**ステータス**: Announcement / Fixed

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261013-google-distributed-cloud-1-35-600-gke-141.html)

## 概要

Google Distributed Cloud (software only) の VMware 版およびベアメタル版の両プラットフォームで、パッチリリース 1.35.600-gke.141 がダウンロード可能になりました。両バージョンとも Kubernetes v1.35.8-gke.100 上で動作します。リリース後、GKE On-Prem API クライアント (Google Cloud コンソール、gcloud CLI、Terraform) で利用可能になるまで約 7〜14 日かかります。

本リリースは、前日 (2026-10-12) に公開された [1.35.600-gke.140](./2026-10-12-google-distributed-cloud-1-35-600.md) に続くフォローアップのパッチリリースです。.140 がバグ修正を多く含んでいたのに対し、.141 の修正内容は「Vulnerability fixes に記載されたセキュリティ脆弱性の修正」のみで、新機能の追加や機能的なバグ修正は含まれません。1.35 系を運用するオンプレミス環境のセキュリティを最新の状態に保つためのリリースです。

**アップデート前の課題**

- 1.35.600-gke.140 以前のバージョンには、脆弱性修正一覧 (Vulnerability fixes) に記載された既知のセキュリティ脆弱性が未修正のまま残っていた

**アップデート後の改善**

- 脆弱性修正一覧に記載されたセキュリティ脆弱性が、VMware 版・ベアメタル版の両プラットフォームで修正された

## サービスアップデートの詳細

### 主要機能

1. **1.35.600-gke.141 のリリース (両プラットフォーム共通)**
   - VMware 版・ベアメタル版ともに Kubernetes v1.35.8-gke.100 上で動作 (.140 から変更なし)
   - サードパーティストレージベンダーを利用している場合は、[認定済みストレージパートナー](https://docs.cloud.google.com/kubernetes-engine/enterprise/docs/resources/partner-storage)の一覧で対応状況の確認が必要

2. **脆弱性修正**
   - 脆弱性修正一覧 ([VMware 版](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/vmware/docs/vulnerabilities) / [ベアメタル版](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/vulnerabilities)) に記載されたセキュリティ脆弱性を修正
   - 本リリースの Fixed 項目は脆弱性修正のみ。機能的なバグ修正 (audit-proxy、プリフライトチェック、CA ローテーションなど) は前リリース [1.35.600-gke.140](./2026-10-12-google-distributed-cloud-1-35-600.md) を参照

## 技術仕様

### リリース情報

| 項目 | 詳細 |
|------|------|
| GDC バージョン | 1.35.600-gke.141 (VMware 版 / ベアメタル版共通) |
| Kubernetes バージョン | v1.35.8-gke.100 |
| リリースタイプ | パッチリリース (脆弱性修正のみ) |
| 前リリース | 1.35.600-gke.140 (2026-10-12、バグ修正 + 脆弱性修正) |
| GKE On-Prem API クライアントでの利用 | リリース後約 7〜14 日で利用可能 |
| アップグレードツール | VMware 版: gkectl / ベアメタル版: bmctl (GKE On-Prem API クライアントも利用可) |

## 設定方法

アップグレード手順は 1.35.600-gke.140 と同様です。アップグレード先バージョンと同じバージョンのツール (gkectl / bmctl 1.35.600-gke.141) を使用してください。

```bash
# ベアメタル版の例: bmctl 1.35.600-gke.141 をダウンロードしてアップグレード
gcloud storage cp gs://anthos-baremetal-release/bmctl/1.35.600-gke.141/linux-amd64/bmctl ./bmctl
chmod +x ./bmctl
# クラスタ構成ファイルの anthosBareMetalVersion を 1.35.600-gke.141 に更新後
./bmctl upgrade cluster -c CLUSTER_NAME --kubeconfig ADMIN_KUBECONFIG
```

詳細な手順はプラットフォームごとのアップグレードガイド ([VMware 版](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/vmware/docs/how-to/upgrading) / [ベアメタル版](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/how-to/upgrade)) を参照してください。

## メリット

### ビジネス面

- **セキュリティリスクの低減**: 既知の脆弱性が修正され、オンプレミス環境のコンプライアンス要件への対応が容易になる

### 技術面

- **最新パッチへの集約**: .140 のバグ修正と .141 の脆弱性修正を 1 回のアップグレードでまとめて適用できる (1.35.500 以前からのアップグレードの場合)

## デメリット・制約事項

### 制限事項

- GKE On-Prem API クライアント (コンソール、gcloud CLI、Terraform) でこのバージョンが利用可能になるまで、リリース後約 7〜14 日かかる
- サードパーティストレージベンダー利用時は、本リリースに対する認定状況を事前に確認する必要がある
- クラスタのダウングレードはサポートされない

### 考慮すべき点

- .140 へのアップグレードを計画中だった場合は、脆弱性修正を含む .141 を直接適用する方が効率的
- アップグレードはメンテナンスウィンドウの計画が必要

## 料金

Google Distributed Cloud (software only) は GKE Enterprise エディションのライセンスに基づいて課金されます。本パッチリリースの適用自体に追加料金は発生しません。

詳細は [GKE の料金ページ](https://cloud.google.com/kubernetes-engine/pricing) を参照してください。

## 利用可能リージョン

オンプレミス環境 (VMware vSphere / ベアメタル) にデプロイするソフトウェアのため、リージョンの制約はありません。ダウンロードは即時可能で、GKE On-Prem API クライアント経由での利用はリリース後約 7〜14 日で可能になります。

## 関連サービス・機能

- **GKE Enterprise**: GDC (software only) はハイブリッド/マルチクラウド向けの GKE Enterprise の構成要素
- **GKE On-Prem API**: Google Cloud コンソール、gcloud CLI、Terraform からのクラスタライフサイクル管理を提供

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261013-google-distributed-cloud-1-35-600-gke-141.html)
- [公式リリースノート (Google Cloud 全体)](https://docs.cloud.google.com/release-notes#October_13_2026)
- [前リリースのレポート: 1.35.600-gke.140](./2026-10-12-google-distributed-cloud-1-35-600.md)
- [GDC (software only) for VMware リリースノート](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/vmware/docs/release-notes)
- [GDC (software only) for bare metal リリースノート](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/release-notes)
- [VMware 版 脆弱性修正一覧](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/vmware/docs/vulnerabilities)
- [ベアメタル版 脆弱性修正一覧](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/vulnerabilities)
- [VMware 版 アップグレードガイド](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/vmware/docs/how-to/upgrading)
- [ベアメタル版 アップグレードガイド](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/how-to/upgrade)
- [認定済みストレージパートナー](https://docs.cloud.google.com/kubernetes-engine/enterprise/docs/resources/partner-storage)
- [料金ページ (GKE)](https://cloud.google.com/kubernetes-engine/pricing)

## まとめ

GDC (software only) 1.35.600-gke.141 は、前日リリースの .140 に続く脆弱性修正のみのフォローアップパッチです。1.35 系へのアップグレードを計画している場合は、.140 ではなく本バージョンを直接適用することで、バグ修正と最新の脆弱性修正をまとめて取り込めます。セキュリティ要件の厳しいオンプレミス環境では早期の適用を推奨します。

---

**タグ**: Google Distributed Cloud, GDC, VMware, ベアメタル, GKE Enterprise, Kubernetes, パッチリリース, 脆弱性修正, オンプレミス, ハイブリッドクラウド
