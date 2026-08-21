# Container-Optimized OS: cos-125-19216-532-123 イメージリリース

**リリース日**: 2026-08-20

**サービス**: Container-Optimized OS

**機能**: COS 125 LTS イメージ更新 (cos-125-19216-532-123)

**ステータス**: リリース済み (LTS チャネル)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260820-container-optimized-os-image-updates.html)

## 概要

Container-Optimized OS (COS) の 125 LTS マイルストーンに新しいイメージ `cos-125-19216-532-123` がリリースされました。COS は Google が Compute Engine および GKE 向けに提供するコンテナ実行に最適化されたセキュアな OS イメージで、COS 125 LTS は 2028 年 2 月までサポートされる長期サポート版です。

今回のリリースは定常的なセキュリティ・バージョン更新であり、コンテナランタイムである containerd の v2.2.7 へのアップデートと、Linux カーネルの脆弱性 CVE-2026-68329 の修正が含まれます。COS 125 LTS (イメージファミリー `cos-125-lts` / `cos-arm64-125-lts`) を利用中の GKE ノードや Compute Engine インスタンスの運用者が対象です。

**アップデート前の課題**

- 従来の COS 125 イメージの Linux カーネルには CVE-2026-68329 の脆弱性が存在していた
- containerd が旧バージョン (v2.2.7 未満) のままだった

**アップデート後の改善**

- Linux カーネル (COS-6.12.94) で CVE-2026-68329 が修正され、セキュリティリスクが低減された
- containerd が v2.2.7 に更新され、最新の修正が反映された

## サービスアップデートの詳細

### 主要コンポーネントのバージョン

| コンポーネント | バージョン |
|------|------|
| イメージ名 | cos-125-19216-532-123 |
| Kernel | COS-6.12.94 |
| Docker | v27.5.1 |
| Containerd | v2.2.7 |

### 変更内容

1. **containerd の更新**
   - containerd を v2.2.7 に更新

2. **セキュリティ修正**
   - Linux カーネルの CVE-2026-68329 を修正

## 技術仕様

### COS 125 LTS マイルストーン

| 項目 | 詳細 |
|------|------|
| イメージプロジェクト | cos-cloud |
| x86 イメージファミリー | cos-125-lts |
| Arm イメージファミリー | cos-arm64-125-lts |
| サポート終了 | 2028 年 2 月 |

## 設定方法

### 最新イメージの確認と適用

```bash
# cos-125-lts ファミリーの最新イメージを確認
gcloud compute images describe-from-family cos-125-lts \
    --project=cos-cloud

# 新しいイメージで Compute Engine インスタンスを作成
gcloud compute instances create my-cos-instance \
    --image-family=cos-125-lts \
    --image-project=cos-cloud \
    --zone=asia-northeast1-a
```

GKE でノードイメージに COS を使用している場合は、ノードの自動アップグレードにより新イメージが順次適用されます。

## メリット

### ビジネス面

- **セキュリティリスクの低減**: カーネル脆弱性の修正により、コンテナワークロード基盤の安全性が維持される

### 技術面

- **最新ランタイムの適用**: containerd v2.2.7 への更新により、ランタイムの修正が取り込まれる
- **LTS の安定性**: COS 125 LTS は 2028 年 2 月までサポートされ、長期運用に適する

## 考慮すべき点

- 自動更新を無効化している環境では、脆弱性修正を反映するために手動でのイメージ更新 (インスタンス再作成またはノードアップグレード) が必要
- GKE のノードイメージバージョンはクラスタのリリースチャネルに依存するため、反映タイミングはチャネルにより異なる

## 料金

Container-Optimized OS 自体に追加料金はありません。Compute Engine / GKE の通常料金が適用されます。

## 関連サービス・機能

- **Google Kubernetes Engine (GKE)**: COS はデフォルトのノードイメージとして使用される
- **Compute Engine**: cos-cloud プロジェクトのイメージファミリーから COS インスタンスを起動できる

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260820-container-optimized-os-image-updates.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#August_20_2026)
- [COS 125 LTS リリースノート](https://docs.cloud.google.com/container-optimized-os/docs/release-notes/m125)
- [Container-Optimized OS ドキュメント](https://docs.cloud.google.com/container-optimized-os/docs)

## まとめ

COS 125 LTS の定常的なセキュリティ・バージョン更新であり、カーネル脆弱性 CVE-2026-68329 の修正と containerd v2.2.7 への更新が含まれます。COS 125 LTS を利用している環境では、自動更新の適用状況を確認し、無効化している場合は速やかに最新イメージへの更新を推奨します。

---

**タグ**: Container-Optimized OS, COS, セキュリティ, CVE, containerd, GKE, Compute Engine
