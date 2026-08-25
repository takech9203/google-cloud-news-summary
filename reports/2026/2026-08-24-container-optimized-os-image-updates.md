# Container-Optimized OS: 4 つの新イメージリリース (セキュリティ修正)

**リリース日**: 2026-08-24

**サービス**: Container-Optimized OS

**機能**: COS 117 / 121 / 125 / 129 イメージ更新 (セキュリティ修正含む)

**ステータス**: リリース済み

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260824-container-optimized-os-image-updates.html)

## 概要

Container-Optimized OS (COS) の 4 つのマイルストーン (117 / 121 / 125 / 129) に対して、新しいイメージがリリースされました。COS は Google が Compute Engine および GKE 向けに提供するコンテナ実行に最適化されたセキュアな OS イメージです。

今回のリリースは定常的なセキュリティ更新であり、各マイルストーンで Linux カーネルの複数の CVE 修正と KCTF-0650f1c の修正が含まれます。また、COS 121 では lustre-client-drivers v2.14.0_p259 のサポート追加と各種パッケージの更新、COS 125 / 129 では cos-gpu-installer v2.7.7 への更新が含まれます。COS をノードイメージとして利用する GKE クラスタや、COS ベースの Compute Engine インスタンスの運用者が対象です。

**アップデート前の課題**

- 従来の各イメージの Linux カーネルには CVE-2026-68096、CVE-2026-68129 をはじめとする複数の脆弱性が存在していた
- KCTF-0650f1c で報告されたカーネルの問題が未修正だった
- COS 121 では lustre-client-drivers の新バージョン (v2.14.0_p259) が利用できなかった

**アップデート後の改善**

- 全 4 マイルストーンで Linux カーネルの複数の CVE と KCTF-0650f1c が修正され、セキュリティリスクが低減された
- COS 121 で lustre-client-drivers v2.14.0_p259 がサポートされ、zstd (1.5.7-r1) や expat (2.8.3) などのパッケージが更新された
- COS 125 / 129 で cos-gpu-installer が v2.7.7 に更新された

## サービスアップデートの詳細

### リリースされたイメージ

| イメージ名 | マイルストーン | Kernel | Docker | Containerd |
|------|------|------|------|------|
| cos-121-18867-528-78 | COS 121 | COS-6.6.143 | v27.5.1 | v2.0.10 |
| cos-117-18613-675-64 | COS 117 | COS-6.6.143 | v24.0.9 | v1.7.34 |
| cos-129-19506-299-161 | COS 129 | COS-6.12.94 | v27.5.1 | v2.2.6 |
| cos-125-19216-532-135 | COS 125 | COS-6.12.94 | v27.5.1 | v2.2.7 |

### セキュリティ修正 (CVE / KCTF)

| イメージ | 修正された脆弱性 |
|------|------|
| cos-121-18867-528-78 | CVE-2026-68096, CVE-2026-68129, CVE-2026-68146, CVE-2026-68149, CVE-2026-68171, CVE-2026-68299, CVE-2026-68329, KCTF-0650f1c |
| cos-117-18613-675-64 | CVE-2026-68096, CVE-2026-68116, CVE-2026-68129, CVE-2026-68146, CVE-2026-68147, CVE-2026-68149, CVE-2026-68171, CVE-2026-68325, CVE-2026-68386, CVE-2026-68428, KCTF-0650f1c |
| cos-129-19506-299-161 | CVE-2026-68096, CVE-2026-68129, CVE-2026-68146, CVE-2026-68325, CVE-2026-68338, CVE-2026-68422, KCTF-0650f1c |
| cos-125-19216-532-135 | CVE-2026-68093, CVE-2026-68096, CVE-2026-68129, CVE-2026-68296, CVE-2026-68386, KCTF-0650f1c |

CVE-2026-68096、CVE-2026-68129 は全 4 マイルストーン共通で修正されており、KCTF-0650f1c も全イメージで修正されています。

### その他の変更

1. **COS 121: lustre-client-drivers サポートと各種パッケージ更新**
   - lustre-client-drivers v2.14.0_p259 のサポートを追加
   - zstd を 1.5.7-r1 に、expat を 2.8.3 に更新するなど、各種パッケージをアップグレード

2. **COS 125 / 129: cos-gpu-installer の更新**
   - cos-gpu-installer を v2.7.7 に更新

3. **ランタイム sysctl の変更**
   - `net.ipv4.udp_mem` のデフォルト値を `188034 250715 376068` から `188034 250714 376068` に変更

## 技術仕様

### 対象イメージファミリー

| マイルストーン | イメージプロジェクト | x86 イメージファミリー | Arm イメージファミリー |
|------|------|------|------|
| COS 117 | cos-cloud | cos-117-lts | cos-arm64-117-lts |
| COS 121 | cos-cloud | cos-121-lts | cos-arm64-121-lts |
| COS 125 | cos-cloud | cos-125-lts | cos-arm64-125-lts |
| COS 129 | cos-cloud | cos-129-lts | cos-arm64-129-lts |

## 設定方法

### 最新イメージの確認と適用

```bash
# 各 LTS ファミリーの最新イメージを確認 (例: cos-121-lts)
gcloud compute images describe-from-family cos-121-lts \
    --project=cos-cloud

# 新しいイメージで Compute Engine インスタンスを作成
gcloud compute instances create my-cos-instance \
    --image-family=cos-121-lts \
    --image-project=cos-cloud \
    --zone=asia-northeast1-a
```

GKE でノードイメージに COS を使用している場合は、ノードの自動アップグレードにより新イメージが順次適用されます。

## メリット

### ビジネス面

- **セキュリティリスクの低減**: 複数のカーネル脆弱性の修正により、コンテナワークロード基盤の安全性が維持される
- **全マイルストーンの同時更新**: 利用中の COS バージョンに関わらず、共通の脆弱性 (CVE-2026-68096 など) への修正が提供される

### 技術面

- **最新パッケージの適用**: COS 121 での zstd / expat などのパッケージ更新、COS 125 / 129 での cos-gpu-installer v2.7.7 更新により最新の修正が取り込まれる
- **Lustre ファイルシステム対応の更新**: COS 121 で lustre-client-drivers v2.14.0_p259 が利用可能になり、Managed Lustre などの並列ファイルシステム利用環境で最新ドライバを利用できる

## 考慮すべき点

- 自動更新を無効化している環境では、脆弱性修正を反映するために手動でのイメージ更新 (インスタンス再作成またはノードアップグレード) が必要
- GKE のノードイメージバージョンはクラスタのリリースチャネルに依存するため、反映タイミングはチャネルにより異なる
- `net.ipv4.udp_mem` のデフォルト値がわずかに変更されているため、この sysctl を前提にチューニングしている環境では値を確認すること

## 料金

Container-Optimized OS 自体に追加料金はありません。Compute Engine / GKE の通常料金が適用されます。

## 関連サービス・機能

- **Google Kubernetes Engine (GKE)**: COS はデフォルトのノードイメージとして使用される
- **Compute Engine**: cos-cloud プロジェクトのイメージファミリーから COS インスタンスを起動できる
- **Managed Lustre**: COS 121 の lustre-client-drivers 更新により、Lustre クライアントとしての利用環境が更新される

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260824-container-optimized-os-image-updates.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#August_24_2026)
- [COS 117 リリースノート](https://docs.cloud.google.com/container-optimized-os/docs/release-notes/m117)
- [COS 121 リリースノート](https://docs.cloud.google.com/container-optimized-os/docs/release-notes/m121)
- [COS 125 リリースノート](https://docs.cloud.google.com/container-optimized-os/docs/release-notes/m125)
- [COS 129 リリースノート](https://docs.cloud.google.com/container-optimized-os/docs/release-notes/m129)
- [Container-Optimized OS ドキュメント](https://docs.cloud.google.com/container-optimized-os/docs)

## まとめ

COS 117 / 121 / 125 / 129 の 4 マイルストーンに対する定常的なセキュリティ更新であり、複数のカーネル CVE と KCTF-0650f1c の修正が含まれます。COS を利用している環境では、自動更新の適用状況を確認し、無効化している場合は速やかに最新イメージへの更新を推奨します。

---

**タグ**: Container-Optimized OS, COS, セキュリティ, CVE, containerd, Docker, GKE, Compute Engine
