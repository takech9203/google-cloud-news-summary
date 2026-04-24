# Google Distributed Cloud (software only): バージョン 1.32.1100-gke.84 リリース (VMware / bare metal)

**リリース日**: 2026-04-23

**サービス**: Google Distributed Cloud (software only) for VMware / for bare metal

**機能**: セキュリティ修正、アップグレード安定性向上、Stale Mount ヘルスチェック追加

**ステータス**: Available

[このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20260423-google-distributed-cloud-1-32-1100.html)

## 概要

Google Distributed Cloud (software only) for VMware および for bare metal のバージョン 1.32.1100-gke.84 がダウンロード可能になりました。本バージョンは Kubernetes v1.32.13-gke.100 上で動作します。今回のリリースでは、両プラットフォーム共通のセキュリティ脆弱性修正に加え、VMware 版では非アドバンスドクラスタからアドバンスドクラスタへのアップグレードが停止する問題の修正、bare metal 版では Secret/ConfigMap の Stale Mount を検出する定期ヘルスチェック機能の追加やノードアップグレード時のハング問題の修正が含まれています。

bare metal 版で追加された Stale Mount ヘルスチェックは、Secret ローテーション後にノードが古いシークレットデータを配信し続けるというまれなシナリオを検出するための機能です。現在は GKE Identity Service Pod で有効化されており、各ノード上でローカルキャッシュされたボリュームの内容と API サーバーのライブデータを比較し、5 分間の猶予期間後にミスマッチを報告します。

VMware 版では、非アドバンスドクラスタからアドバンスドクラスタへの移行時に Hub メンバーシップの不変フィールドを更新しようとしてアップグレードがスタックする問題が修正されました。これは 1.32 から 1.33 へのアップグレード時に自動的にアドバンスドクラスタへ変換される際に発生する可能性があった重要な問題です。

**アップデート前の課題**

- VMware 版: 非アドバンスドクラスタからアドバンスドクラスタへのアップグレード時に、Hub メンバーシップの不変フィールドを上書きしようとしてアップグレードがスタックする場合があった
- bare metal 版: Secret ローテーション後に、ノードが古いシークレットデータを配信し続けるケースを検出する仕組みがなく、認証失敗が発生する可能性があった
- bare metal 版: Terminating 状態の Namespace 内に完了済み Pod が存在する場合、Kubernetes Eviction API が操作を拒否し、ノードアップグレードが無期限にハングして 20 分のメンテナンスタイムアウトをバイパスする問題があった
- bare metal 版: etcd-events Pod がマシン初期化フェーズで古いデータディレクトリを読み込み、古いメンバー ID でクラスタへの再参加を試みて無限リトライループに陥る問題があった
- bare metal 版: containerd の再起動時に同一ノード上の並行タスクが失敗する問題があった

**アップデート後の改善**

- VMware 版: クラスタオペレーターがアップグレードプロセス中にオリジナルのメンバーシップフィールドを保持するようになり、アドバンスドクラスタへの移行が正常に完了するようになった
- bare metal 版: GKE Identity Service Pod に対する定期ヘルスチェックにより、Stale Mount を自動検出できるようになった
- bare metal 版: ドレインプロセスがターミナルフェーズの Pod に対する Eviction をスキップするようになり、アップグレードが正常に進行するようになった
- bare metal 版: etcd-events の /var/lib/etcd-events ディレクトリが失敗時にクリアされ、kubeadm-reset にリトライロジックが追加された
- bare metal 版: 同一ノード上のタスクがロックされ順次実行されるようになり、containerd 再起動時の並行タスク失敗が解消された

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph HealthCheck["Stale Mount ヘルスチェック (bare metal)"]
        A["HealthCheck Agent\n(各ノードで実行)"] -->|"定期チェック"| B["ローカルキャッシュ\n(Secret/ConfigMap ボリューム)"]
        A -->|"データ取得"| C["API Server\n(ライブデータ)"]
        B --> D{"データ比較"}
        C --> D
        D -->|"一致"| E["正常"]
        D -->|"不一致"| F{"5分間\n猶予期間"}
        F -->|"猶予期間内に解消"| E
        F -->|"猶予期間超過"| G["ミスマッチ報告"]
    end

    subgraph DrainFix["ノードドレイン改善 (bare metal)"]
        H["ノードアップグレード開始"] --> I["Pod ドレイン処理"]
        I --> J{"Pod の状態確認"}
        J -->|"実行中 Pod"| K["Eviction API で退避"]
        J -->|"完了済み Pod\n(Terminating NS)"] -->|"スキップ"| L["次の Pod へ"]
        K --> L
        L --> M["ドレイン完了\n(20分タイムアウト内)"]
    end

    subgraph VMwareFix["Hub メンバーシップ修正 (VMware)"]
        N["非アドバンスド → アドバンスド\nアップグレード開始"] --> O["Hub メンバーシップ確認"]
        O --> P["オリジナルフィールド保持\n(不変フィールドを上書きしない)"]
        P --> Q["アドバンスドクラスタ\nへの移行完了"]
    end
```

上図は今回のリリースに含まれる 3 つの主要な改善を示しています。上段は bare metal 版で追加された Stale Mount ヘルスチェックのフロー、中段はノードドレインプロセスの改善 (完了済み Pod のスキップ)、下段は VMware 版の Hub メンバーシップフィールド保持による安定したアップグレードフローです。

## サービスアップデートの詳細

### 主要機能

1. **Stale Mount 定期ヘルスチェック (bare metal - 新機能)**
   - Secret および ConfigMap のマウントが古くなっていないかを定期的にチェックする機能が追加
   - 各ノード上でローカルキャッシュされたボリュームの内容と API サーバーのライブデータを比較
   - 通常の更新遅延を考慮した 5 分間の猶予期間が設定されており、猶予期間後にミスマッチを報告
   - 現在は GKE Identity Service Pod で有効化されており、Secret ローテーション後の認証失敗を早期に検出可能
   - Kubernetes の kubelet が Secret/ConfigMap の更新をボリュームに反映するまでのタイムラグに起因するまれな問題に対応

2. **Hub メンバーシップ不変フィールドの保持 (VMware - 修正)**
   - 非アドバンスドクラスタからアドバンスドクラスタへのアップグレード時に、Hub メンバーシップの不変フィールドを更新しようとしてスタックする問題を修正
   - クラスタオペレーターがアップグレード中にオリジナルのメンバーシップフィールドを保持するよう変更
   - バージョン 1.32 から 1.33 へのアップグレード時に自動的にアドバンスドクラスタへ変換されるワークフローに影響する重要な修正

3. **ノードアップグレードハング問題の修正 (bare metal - 修正)**
   - Terminating 状態の Namespace 内に完了済み Pod が存在する場合にノードアップグレードが無期限にハングする問題を修正
   - Kubernetes Eviction API が Terminating 状態の Namespace での操作を拒否するため、クラスタコントローラーが無限リトライループに入っていた
   - ドレインプロセスがターミナルフェーズの Pod に対する Eviction をスキップするよう更新

4. **セキュリティ脆弱性修正 (VMware / bare metal 共通)**
   - 両プラットフォームで脆弱性修正が適用
   - 詳細は各プラットフォームの Vulnerability fixes ページを参照

5. **etcd-events Pod の初期化問題修正 (bare metal - 修正)**
   - マシン初期化フェーズで etcd-events Pod が古いデータディレクトリを読み込み、古いメンバー ID でクラスタへの再参加を試みて無限リトライループに陥る問題を修正
   - /var/lib/etcd-events ディレクトリが失敗時にクリアされるようになり、kubeadm-reset にリトライロジックが追加

6. **containerd 再起動時の並行タスク問題修正 (bare metal - 修正)**
   - 同一ノード上で containerd が再起動した際に並行タスクが失敗する問題を修正
   - タスクがロックされ順次実行されるようになり、各タスクは最大 20 分間または成功/失敗まで保持
   - 並行実行が必要な場合はアノテーション `baremetal.cluster.gke.io/concurrent-machine-update: "true"` で設定可能

## 技術仕様

### バージョン情報

| 項目 | 詳細 |
|------|------|
| GDC バージョン | 1.32.1100-gke.84 |
| Kubernetes バージョン | v1.32.13-gke.100 |
| 対象プラットフォーム | VMware / bare metal |
| GKE On-Prem API 利用可能時期 | リリースから約 7-14 日後 |

### Stale Mount ヘルスチェック仕様 (bare metal)

| 項目 | 詳細 |
|------|------|
| チェック対象 | Secret / ConfigMap のボリュームマウント |
| 有効化対象 | GKE Identity Service Pod |
| 比較方法 | ローカルキャッシュ vs API サーバーのライブデータ |
| 猶予期間 | 5 分間 |
| 実行場所 | 各ノード |

### ノードドレイン改善仕様 (bare metal)

| 項目 | 詳細 |
|------|------|
| メンテナンスタイムアウト | 20 分 |
| ドレイン方式 | Eviction API ベース (v1.28 以降) |
| 修正内容 | ターミナルフェーズ Pod の Eviction スキップ |
| 影響条件 | Terminating Namespace 内の完了済み Pod |

## 設定方法

### 前提条件

1. 現在のクラスタバージョンが 1.32.x 系であること
2. サードパーティストレージベンダーを使用している場合、Google Distributed Cloud-ready ストレージパートナードキュメントで当該バージョンの認定を確認済みであること
3. アップグレード前にクラスタのバックアップを取得済みであること

### 手順

#### ステップ 1: バージョンの確認とダウンロード (VMware)

```bash
# 管理ワークステーションの gkectl バージョンを確認
gkectl version

# アップグレードの事前チェック
gkectl upgrade admin --kubeconfig ADMIN_KUBECONFIG --config ADMIN_CONFIG --dry-run
```

アドバンスドクラスタへの移行を含むアップグレードの場合、gkectl のバージョンはターゲットバージョンと一致する必要があります。

#### ステップ 2: クラスタのアップグレード (VMware)

```bash
# Admin クラスタのアップグレード
gkectl upgrade admin --kubeconfig ADMIN_KUBECONFIG --config ADMIN_CONFIG

# User クラスタのアップグレード
gkectl upgrade cluster --kubeconfig ADMIN_KUBECONFIG --config USER_CLUSTER_CONFIG
```

#### ステップ 3: クラスタのアップグレード (bare metal)

```bash
# bmctl を使用したアップグレード
bmctl upgrade cluster --kubeconfig ADMIN_KUBECONFIG --cluster CLUSTER_NAME

# アップグレード状態の確認
kubectl get baremetalmachines --namespace CLUSTER_NAMESPACE --kubeconfig ADMIN_KUBECONFIG
```

#### ステップ 4: Stale Mount ヘルスチェックの確認 (bare metal)

```bash
# GKE Identity Service Pod のステータス確認
kubectl get pods -l k8s-app=ais -n anthos-identity-service

# ヘルスチェックのログ確認
kubectl logs -l k8s-app=ais -n anthos-identity-service --tail=50
```

Stale Mount ヘルスチェックはアップグレード後に自動的に有効化されるため、追加の設定は不要です。

## メリット

### ビジネス面

- **アップグレードの信頼性向上**: VMware / bare metal 両方でアップグレードプロセスのスタックやハングを引き起こす複数の問題が修正され、計画的なメンテナンスウィンドウ内でのアップグレード完了がより確実になった
- **セキュリティ体制の強化**: 脆弱性修正の適用に加え、Stale Mount ヘルスチェックにより Secret ローテーション後の認証失敗リスクが低減

### 技術面

- **Stale Mount の早期検出**: Secret/ConfigMap の更新が正しく反映されていないケースを自動検出することで、デバッグに要する時間を大幅に削減
- **ドレインプロセスの堅牢化**: Terminating Namespace 内の完了済み Pod に起因する無限リトライループの解消により、ノードアップグレードの 20 分タイムアウトが正しく機能するようになった
- **etcd 初期化の安定性向上**: etcd-events のデータディレクトリクリアとリトライロジックの追加により、マシン初期化の信頼性が向上

## デメリット・制約事項

### 制限事項

- GKE On-Prem API クライアント (Google Cloud コンソール、gcloud CLI、Terraform) での利用はリリースから約 7-14 日後に可能
- Stale Mount ヘルスチェックは現在 GKE Identity Service Pod のみに限定されており、他のワークロードの Pod には適用されない
- サードパーティストレージベンダーを使用している場合、当該バージョンでの認定がパートナーから取得されるまで待つ必要がある

### 考慮すべき点

- VMware 版で非アドバンスドクラスタからアドバンスドクラスタへの移行を計画している場合、1.32 から 1.33 への移行パスにおける制約 (gkectl バージョン一致要件、コントロールプレーンとノードプールの同時アップグレード要件) を事前に確認すること
- bare metal 版で containerd 再起動時の並行タスクロック機能を無効化するアノテーション (`baremetal.cluster.gke.io/concurrent-machine-update: "true"`) は、安全メカニズムをバイパスするものであり、使用には注意が必要
- アドバンスドクラスタに移行する場合、cert-manager が自動的にインストールされ、既存の cert-manager がオーバーライドされるため、カスタム設定がないことを事前に確認すること

## ユースケース

### ユースケース 1: アドバンスドクラスタへの安全な移行 (VMware)

**シナリオ**: VMware 環境で運用中の非アドバンスドクラスタを 1.33 へアップグレードし、アドバンスドクラスタへ移行する計画がある場合。

**実装例**:
```bash
# まず 1.32.1100-gke.84 にパッチアップグレードして Hub メンバーシップの修正を適用
gkectl upgrade admin --kubeconfig ADMIN_KUBECONFIG --config ADMIN_CONFIG

# 次に 1.33 への移行を実行 (アドバンスドクラスタへの自動変換)
gkectl upgrade admin --kubeconfig ADMIN_KUBECONFIG --config ADMIN_CONFIG
```

**効果**: Hub メンバーシップの不変フィールド問題が修正されたバージョンで移行準備を行うことで、アドバンスドクラスタへのスムーズな移行が可能になる。

### ユースケース 2: Secret ローテーション運用の信頼性向上 (bare metal)

**シナリオ**: bare metal 環境で定期的な Secret ローテーションを実施しており、GKE Identity Service を認証基盤として使用している場合。

**効果**: Stale Mount ヘルスチェックにより、Secret ローテーション後にノード上の Pod が古い認証情報を使用し続けるケースを 5 分の猶予期間後に自動検出できる。これにより、ローテーション後の認証エラーの原因特定が迅速化される。

### ユースケース 3: 大規模ノードプールのアップグレード安定化 (bare metal)

**シナリオ**: 多数のノードを持つ bare metal クラスタで、一部のノードに Terminating 状態の Namespace や完了済み Pod が残存している環境でのアップグレード。

**効果**: ドレインプロセスの改善により、これらの Pod がアップグレードをブロックしなくなり、20 分のメンテナンスタイムアウト内でノードアップグレードが確実に完了する。

## 料金

Google Distributed Cloud (software only) はサブスクリプションベースの料金体系です。今回のパッチリリースによる追加料金は発生しません。

詳細な料金情報については以下のページをご参照ください:
- [Google Distributed Cloud pricing](https://cloud.google.com/distributed-cloud/pricing)

## 利用可能リージョン

Google Distributed Cloud (software only) はオンプレミスまたはエッジ環境にデプロイされるソフトウェアであり、特定のクラウドリージョンに依存しません。ただし、GKE On-Prem API を通じた管理には、サポートされている Google Cloud リージョンへの接続が必要です。

## 関連サービス・機能

- **GKE (Google Kubernetes Engine)**: Google Distributed Cloud はクラウド上の GKE と同じ Kubernetes API および管理ツールを使用し、ハイブリッド/マルチクラウド環境を構築
- **GKE Identity Service**: 今回の Stale Mount ヘルスチェックの対象となる認証サービス。OIDC、LDAP、SAML による認証をサポート
- **Connect Gateway**: オンプレミスクラスタを Google Cloud コンソールから管理するためのゲートウェイ。Hub メンバーシップと連携
- **Config Sync / Policy Controller**: クラスタ構成の一貫性管理とポリシー適用。アドバンスドクラスタでも引き続き利用可能
- **Cloud Monitoring / Cloud Logging**: クラスタのメトリクスやログを Google Cloud に統合し、Stale Mount の検出結果を含む運用状況を可視化

## 参考リンク

- [このアップデートのインフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20260423-google-distributed-cloud-1-32-1100.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#April_23_2026)
- [GDC for VMware リリースノート](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/vmware/docs/release-notes)
- [GDC for bare metal リリースノート](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/release-notes)
- [GDC for VMware アップグレード手順](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/vmware/docs/how-to/upgrading)
- [GDC for bare metal アップグレード手順](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/how-to/upgrade)
- [アドバンスドクラスタの概要](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/vmware/docs/concepts/advanced-clusters)
- [VMware 版 脆弱性修正](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/vmware/docs/vulnerabilities)
- [bare metal 版 脆弱性修正](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/vulnerabilities)
- [メンテナンスモード (bare metal)](https://docs.cloud.google.com/kubernetes-engine/distributed-cloud/bare-metal/docs/how-to/maintenance-mode)

## まとめ

Google Distributed Cloud 1.32.1100-gke.84 は、VMware 版と bare metal 版の両方でアップグレードの安定性とセキュリティを大幅に改善するパッチリリースです。特に、VMware 版のアドバンスドクラスタ移行時のスタック問題の修正と、bare metal 版の Stale Mount ヘルスチェック機能の追加は、運用信頼性を向上させる重要な変更です。1.32 系を使用しているクラスタ管理者は、セキュリティ脆弱性修正を含む本バージョンへの早期アップグレードを推奨します。

---

**タグ**: #GoogleDistributedCloud #GDC #VMware #BareMetal #Kubernetes #GKE #セキュリティ修正 #アップグレード #ヘルスチェック #StaleMountDetection #アドバンスドクラスタ
