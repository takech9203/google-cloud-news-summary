# Google Kubernetes Engine (GKE): バージョンアップデート 2026-R38

**リリース日**: 2026-09-08

**サービス**: Google Kubernetes Engine (GKE)

**機能**: クラスタバージョンの更新とセキュリティアップデート (2026-R38)

**ステータス**: Change + Security (Version Update / Security Update)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260908-gke-2026-r38-version-updates.html)

## 概要

Google Kubernetes Engine (GKE) の全リリースチャネル (Rapid, Regular, Stable, Extended, No channel) において、クラスタバージョンが更新された。今回の 2026-R38 アップデートでは、Rapid チャネルのデフォルトバージョンが 1.36.4-gke.1082000 に更新され、Rapid チャネルの新規クラスタが 1.36.4 系で作成されるようになった。Regular / Extended / No channel のデフォルトバージョンは 1.35.7-gke.1222000 に更新されている。Rapid チャネルには 1.34.11 / 1.35.8 / 1.36.4 / 1.37.0 系の新パッチ (1.34.11-gke.1056000, 1.35.8-gke.1380000, 1.36.4-gke.1247000, 1.37.0-gke.3165000) が追加され、Regular / Extended チャネルには前回まで Rapid で提供されていた 1.34.10-gke.1328000 / 1.35.8-gke.1036000 / 1.36.3-gke.1767000 が昇格して追加された。

セキュリティアップデート (2026-R38) として、更新された Container-Optimized OS イメージを使用する新しい GKE バージョンもリリースされた。これらのイメージは前回の GKE リリース以降に公開されたすべての Container-Optimized OS のセキュリティ修正を累積的に含んでおり、今回は cos-117 / cos-129 のイメージが 1.31.14 / 1.36.4 / 1.37.0 系の新バージョンに適用されている。このアップデートは、GKE クラスタを運用するすべてのプラットフォーム管理者およびインフラエンジニアに影響する。

**アップデート前の課題**

- 前回 (2026-R37) までのバージョンには、直近の Container-Optimized OS セキュリティ修正が含まれていなかった
- Rapid チャネルのデフォルトは 1.36.3-gke.1767000 のままであり、1.36.4 系の新パッチが新規クラスタに標準適用されていなかった
- Regular / Extended / No channel のデフォルトは旧パッチ (1.35.7-gke.1150000 / 1.35.7-gke.1027000 など) のままだった
- 1.35.8 / 1.36.3 系の新パッチは Rapid チャネル限定で、Regular / Extended チャネルでは利用できなかった

**アップデート後の改善**

- Rapid チャネルのデフォルトが 1.36.4-gke.1082000 に更新され、新規クラスタに 1.36.4 系が標準適用されるようになった
- Regular / Extended / No channel のデフォルトが 1.35.7-gke.1222000 に更新された
- 1.34.10-gke.1328000 / 1.35.8-gke.1036000 / 1.36.3-gke.1767000 が Regular / Extended チャネルに昇格し、より広い環境で利用可能になった
- 累積的なセキュリティ修正を含む Container-Optimized OS イメージ (cos-117 / cos-129) が新バージョンに適用され、ノード OS の脆弱性リスクが低減された

## アーキテクチャ図

```mermaid
flowchart LR
    subgraph Rapid["🚀 Rapid チャネル"]
        R_Default["新デフォルト<br/>1.36.4-gke.1082000"]
        R_New["新パッチ<br/>1.34.11 / 1.35.8 / 1.36.4 / 1.37.0"]
    end

    subgraph Regular["⚖️ Regular チャネル"]
        Reg_Default["新デフォルト<br/>1.35.7-gke.1222000"]
        Reg_New["昇格バージョン<br/>1.34.10 / 1.35.8 / 1.36.3"]
    end

    subgraph Stable["🛡️ Stable チャネル"]
        S_New["新バージョン<br/>1.34.10-gke.1106000"]
    end

    subgraph Extended["⏳ Extended チャネル"]
        E_Default["新デフォルト<br/>1.35.7-gke.1222000"]
    end

    COS["💿 Container-Optimized OS<br/>cos-117 / cos-129<br/>(累積セキュリティ修正)"]

    Rapid -->|"検証完了後"| Regular
    Regular -->|"追加検証後"| Stable
    Regular -->|"同期"| Extended
    COS -.->|"ノードイメージ更新"| Rapid
```

GKE のリリースチャネルは、Rapid で導入されたバージョンが検証を経て Regular、Stable へと段階的に展開されるパイプラインとして機能する。今回は Rapid チャネルのデフォルトが 1.36.4-gke.1082000 に引き上げられ、前回まで Rapid で提供されていた 1.34.10 / 1.35.8 / 1.36.3 系のパッチが Regular / Extended チャネルへ昇格した。あわせて新しい Container-Optimized OS イメージによるセキュリティ修正が各バージョンに組み込まれている。

## サービスアップデートの詳細

### チャネル別バージョン一覧

| チャネル | デフォルトバージョン | 新規追加バージョン | 非推奨バージョン (90 日以内に削除) |
|---------|---------------------|-------------------|-----------------|
| Rapid | 1.36.4-gke.1082000 (新デフォルト) | 1.34.11-gke.1056000, 1.35.8-gke.1380000, 1.36.4-gke.1247000, 1.37.0-gke.3165000 | なし (1.34.10-gke.1328000, 1.35.8-gke.1036000, 1.36.3-gke.1767000, 1.37.0-gke.2155000 は Rapid では提供終了) |
| Regular | 1.35.7-gke.1222000 (新デフォルト) | 1.34.10-gke.1328000, 1.35.8-gke.1036000, 1.36.3-gke.1767000 | 1.36.3-gke.1537000 (1.34.10-gke.1106000, 1.35.7-gke.1150000 は提供終了) |
| Stable | 変更なし | 1.34.10-gke.1106000 | 1.34.10-gke.1079000 |
| Extended | 1.35.7-gke.1222000 (新デフォルト) | 1.31.14-gke.2689000, 1.32.13-gke.2411000, 1.33.13-gke.1636000, 1.34.10-gke.1328000, 1.35.8-gke.1036000, 1.36.3-gke.1767000 | 1.31.14-gke.2667000, 1.32.13-gke.2393000, 1.33.13-gke.1613000, 1.36.3-gke.1537000 (1.34.10-gke.1106000, 1.35.7-gke.1150000 は提供終了) |
| No channel (非推奨) | 1.35.7-gke.1222000 (新デフォルト) | 1.34.11-gke.1056000, 1.35.8-gke.1380000, 1.36.4-gke.1247000 (ノード版はさらに 1.31.14-gke.2689000, 1.32.13-gke.2411000, 1.33.13-gke.1636000) | 1.34.10-gke.1079000, 1.35.7-gke.1027000, 1.36.3-gke.1537000 |

### 自動アップグレードターゲット

各チャネルで、対象マイナーバージョンのクラスタに新しい自動アップグレードターゲットが設定された。

**Rapid チャネル (マイナーバージョンアップグレード)**

| 現在のマイナーバージョン | アップグレード先 |
|------------------------|------------------|
| 1.33 | 1.34.11-gke.1044000 |
| 1.34 | 1.35.8-gke.1225000 |
| 1.35 | 1.36.4-gke.1082000 |

**Regular チャネル (マイナーバージョンアップグレード)**

| 現在のマイナーバージョン | アップグレード先 |
|------------------------|------------------|
| 1.33 | 1.34.10-gke.1236000 |
| 1.34 | 1.35.7-gke.1222000 |

メンテナンス除外や非推奨 API の使用などマイナーアップグレードを妨げる要因がある場合は、同一マイナーバージョン内の新パッチへ自動アップグレードされる (例: Rapid チャネルは 1.34 系が 1.34.11-gke.1044000、1.35 系が 1.35.8-gke.1225000、1.36 系が 1.36.4-gke.1082000、1.37 系が 1.37.0-gke.2941000 へ。Regular / Extended チャネルは 1.34 系が 1.34.10-gke.1236000、1.35 系が 1.35.7-gke.1222000、1.36 系が 1.36.3-gke.1640000 へ。No channel は 1.35 系が 1.35.7-gke.1222000、1.36 系が 1.36.3-gke.1640000 へ)。

なお、今回のリリースでは Stable / Extended / No channel の新しいマイナーバージョンアップグレードターゲットは設定されていない。

### セキュリティアップデート (2026-R38)

新しい GKE バージョンでは、更新された Container-Optimized OS イメージが使用される。これらのイメージは前回の GKE リリース以降のセキュリティ修正を累積的に含む。

| GKE バージョン | Container-Optimized OS バージョン |
|---------------|----------------------------------|
| 1.31.14-gke.2689000 | cos-117-18613-731-2 |
| 1.36.4-gke.1247000 | cos-129-19506-448-8 |
| 1.37.0-gke.3165000 | cos-129-19506-299-82 |

解決された個別の脆弱性は、各 Container-Optimized OS イメージのセキュリティリリースノートで確認できる。

### 主要な変更点

1. **Rapid チャネルのデフォルトが 1.36.4-gke.1082000 に更新**
   - 前回 (2026-R37) で追加された 1.36.4 系パッチが Rapid チャネルの標準バージョンに昇格
   - 新パッチ 1.34.11-gke.1056000 / 1.35.8-gke.1380000 / 1.36.4-gke.1247000 / 1.37.0-gke.3165000 が追加され、旧パッチ (1.34.10-gke.1328000, 1.35.8-gke.1036000, 1.36.3-gke.1767000, 1.37.0-gke.2155000) は Rapid では提供終了

2. **Regular / Extended / No channel のデフォルトが 1.35.7-gke.1222000 に更新**
   - 前回デフォルトの 1.35.7-gke.1150000 は Regular / Extended で提供終了
   - Regular / Extended で 1.36.3-gke.1537000 が非推奨化

3. **1.34.10 / 1.35.8 / 1.36.3 系パッチが Regular / Extended チャネルへ昇格**
   - 前回 Rapid で提供されていた 1.34.10-gke.1328000 / 1.35.8-gke.1036000 / 1.36.3-gke.1767000 が Regular / Extended チャネルで利用可能に

4. **Stable チャネルに 1.34.10-gke.1106000 を追加、1.34.10-gke.1079000 が非推奨化**
   - 非推奨バージョンは 90 日後、またはサポート終了時のいずれか早い時点で削除される

5. **Container-Optimized OS のセキュリティ修正を累積適用**
   - cos-117 (M117) / cos-129 (M129) のイメージを更新
   - 1.31 / 1.36 / 1.37 系の新バージョンにそれぞれ適用

## 技術仕様

### バージョンロールアウトの注意点

- リリースノート公開時点でロールアウトは進行中であり、全ゾーンへの展開完了まで数日を要する場合がある
- 非推奨バージョンは 90 日後、またはサポート終了時のいずれか早い時点で削除される
- Rapid チャネルのバージョンは GKE SLA の対象外
- No channel (リリースチャネル未登録) 構成は非推奨

## 設定方法

### 前提条件

1. Google Cloud プロジェクトで GKE API が有効であること
2. `gcloud` CLI がインストール・認証済みであること
3. クラスタに対する適切な IAM 権限 (`container.admin` ロールなど) を保持していること

### 手順

#### ステップ 1: 現在のクラスタバージョンとチャネルを確認

```bash
gcloud container clusters list \
  --format="table(name,location,currentMasterVersion,releaseChannel.channel)"
```

#### ステップ 2: 利用可能なバージョンを確認

```bash
gcloud container get-server-config \
  --flatten="channels" \
  --filter="channels.channel=REGULAR" \
  --format="yaml(channels.channel,channels.defaultVersion,channels.validVersions)" \
  --location=asia-northeast1
```

#### ステップ 3: 手動アップグレード (必要な場合)

```bash
# コントロールプレーンのアップグレード
gcloud container clusters upgrade CLUSTER_NAME \
  --master \
  --cluster-version=1.35.7-gke.1222000 \
  --location=LOCATION

# ノードプールのアップグレード
gcloud container clusters upgrade CLUSTER_NAME \
  --node-pool=NODE_POOL_NAME \
  --cluster-version=1.35.7-gke.1222000 \
  --location=LOCATION
```

## メリット

### ビジネス面

- **セキュリティリスクの低減**: 累積的なセキュリティ修正を含む Container-Optimized OS イメージへの更新により、ノード OS の脆弱性露出時間を短縮
- **運用コストの削減**: 自動アップグレードにより、手動でのバージョン管理・パッチ適用作業が不要

### 技術面

- **1.36.4 系の標準適用**: Rapid チャネルのデフォルトが 1.36.4-gke.1082000 に更新され、新規クラスタに最新パッチが標準適用
- **Regular チャネルでの新パッチ利用**: 1.34.10 / 1.35.8 / 1.36.3 系の新パッチが Regular / Extended チャネルに昇格し、SLA 対象の環境でも利用可能に
- **累積的なセキュリティ修正**: COS イメージは前回リリース以降の修正をすべて含むため、途中のパッチをスキップしても最新のセキュリティ状態に到達可能

## デメリット・制約事項

### 制限事項

- ロールアウトは段階的に行われるため、一部のゾーンでは新バージョンがまだ利用できない場合がある
- コントロールプレーンのマイナーバージョンのスキップアップグレードは不可 (1 バージョンずつ順次アップグレードが必要)
- Rapid チャネルの最新バージョンは GKE SLA の対象外であり、既知の回避策がない問題を含む可能性がある
- Extended チャネルの拡張サポート期間中はセキュリティパッチのみ提供 (新機能追加なし)

### 考慮すべき点

- Stable チャネルで非推奨となった 1.34.10-gke.1079000 を使用中の場合、90 日以内に削除されるため移行計画を早期に策定すること
- Regular / Extended チャネルで 1.36.3-gke.1537000 が非推奨化されており、対象クラスタは後継パッチ (1.36.3-gke.1640000 以降) への移行が必要
- Extended チャネルでは 1.31.14-gke.2667000 / 1.32.13-gke.2393000 / 1.33.13-gke.1613000 が非推奨化されており、対象クラスタは新パッチ (1.31.14-gke.2689000 / 1.32.13-gke.2411000 / 1.33.13-gke.1636000) への移行が必要
- Rapid チャネルの 1.35 系クラスタは 1.36.4-gke.1082000 への自動アップグレード対象となるため、Kubernetes 1.36 の非推奨 API への対応状況を事前に確認すること
- ノードのバージョンスキューポリシー (コントロールプレーンとノードの差は最大 2 マイナーバージョン) に注意

## ユースケース

### ユースケース 1: セキュリティ修正の迅速な適用

**シナリオ**: セキュリティポリシーにより、ノード OS の脆弱性修正を速やかに適用する必要があるプロダクションクラスタを運用している。

**実装例**:
```bash
# 該当ノードプールを COS 更新済みバージョンへ手動アップグレード (Rapid チャネルの例)
gcloud container clusters upgrade my-prod-cluster \
  --node-pool=default-pool \
  --cluster-version=1.36.4-gke.1247000 \
  --location=asia-northeast1
```

**効果**: cos-129-19506-448-8 の累積セキュリティ修正が適用されたノードイメージに更新され、脆弱性の露出時間を最小化できる。

### ユースケース 2: Regular チャネルでの最新パッチ検証

**シナリオ**: SLA 対象の Regular チャネルを利用しつつ、1.36 系への移行前に新パッチ 1.36.3-gke.1767000 でワークロードの互換性を確認したい。

**実装例**:
```bash
# Regular チャネルで 1.36.3 の新パッチを指定してテストクラスタを作成
gcloud container clusters create test-136-cluster \
  --release-channel=regular \
  --cluster-version=1.36.3-gke.1767000 \
  --location=us-central1
```

**効果**: Rapid チャネルから昇格した 1.36.3 系の新パッチを SLA 対象のチャネルで検証でき、本番クラスタの 1.36 系へのアップグレード計画を安心して策定できる。

### ユースケース 3: 非推奨バージョンからの計画的移行

**シナリオ**: Stable チャネルで 1.34.10-gke.1079000 を使用しており、90 日以内の削除に備えて移行が必要。

**実装例**:
```bash
# Stable チャネルの後継パッチへアップグレード
gcloud container clusters upgrade my-cluster \
  --master \
  --cluster-version=1.34.10-gke.1106000 \
  --location=us-central1
```

**効果**: 削除期限前に計画的にアップグレードすることで、強制アップグレードによる予期しない業務影響を回避できる。

## 料金

GKE のバージョンアップデート自体には追加料金は発生しない。

| 項目 | 料金 |
|------|------|
| GKE クラスタ管理費 (Standard) | $0.10 / クラスタ / 時間 |
| GKE クラスタ管理費 (Autopilot) | 管理費無料 (Pod リソース課金) |
| Extended サポート追加料金 | 拡張サポート期間に入ったクラスタに追加費用が発生 |
| ノードのコンピューティング費用 | 通常の Compute Engine 料金 |

詳細は [GKE 料金ページ](https://cloud.google.com/kubernetes-engine/pricing) を参照。

## 利用可能リージョン

GKE バージョンアップデートは全リージョンで利用可能。ただし、新バージョンのロールアウトはゾーンごとに段階的に行われ、完了まで数日を要する場合がある。

```bash
gcloud container get-server-config --location=LOCATION
```

## 関連サービス・機能

- **Container-Optimized OS**: GKE ノードの OS イメージ。今回のセキュリティアップデートの中核であり、GKE バージョンと連動して更新される
- **Cloud Monitoring / Cloud Logging**: クラスタのアップグレード状態やイベントの監視・記録
- **GKE Security Posture**: クラスタのセキュリティ状態の継続的評価とバージョン推奨
- **GKE Rollout Sequencing**: 複数クラスタ間でのバージョンロールアウトの順序制御
- **メンテナンスウィンドウ / メンテナンス除外**: 自動アップグレードのタイミング制御に利用

## 参考リンク

- 📊 [このアップデートのインフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260908-gke-2026-r38-version-updates.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#September_08_2026)
- [GKE リリースノート](https://docs.cloud.google.com/kubernetes-engine/docs/release-notes)
- [GKE バージョニングとサポート](https://docs.cloud.google.com/kubernetes-engine/versioning)
- [リリースチャネルの概要](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/release-channels)
- [クラスタアップグレードのベストプラクティス](https://docs.cloud.google.com/kubernetes-engine/docs/best-practices/upgrading-clusters)
- [Container-Optimized OS リリースノート (M129)](https://docs.cloud.google.com/container-optimized-os/docs/release-notes/m129)
- [料金ページ](https://cloud.google.com/kubernetes-engine/pricing)

## まとめ

GKE 2026-R38 アップデートにより、Rapid チャネルのデフォルトバージョンが 1.36.4-gke.1082000 に、Regular / Extended / No channel のデフォルトが 1.35.7-gke.1222000 に更新され、Rapid チャネルには 1.34.11 / 1.35.8 / 1.36.4 / 1.37.0 系の新パッチが、Regular / Extended チャネルには Rapid から昇格した 1.34.10 / 1.35.8 / 1.36.3 系のパッチが追加された。あわせて累積的なセキュリティ修正を含む Container-Optimized OS イメージ (cos-117 / cos-129) が 1.31.14 / 1.36.4 / 1.37.0 系の新バージョンに適用されている。クラスタ管理者は、Stable チャネルで非推奨となった 1.34.10-gke.1079000 や Regular / Extended チャネルで非推奨化された 1.36.3-gke.1537000 などからの移行計画を早期に策定し、メンテナンスウィンドウの設定を確認したうえで、セキュリティ修正済みバージョンへの計画的なアップグレードを推奨する。

---

**タグ**: #GKE #Kubernetes #VersionUpdate #SecurityUpdate #ReleaseChannel #ContainerOptimizedOS #2026-R38
