# Cloud Load Balancing: TLS ポスト量子鍵交換のロールアウトが Phase 2 (デフォルト有効化) に移行

**リリース日**: 2026-11-16

**サービス**: Cloud Load Balancing

**機能**: TLS ポスト量子鍵交換 (Post-Quantum Key Exchange) の Phase 2 ロールアウト

**ステータス**: Feature (デフォルト有効化フェーズ)

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261116-cloud-load-balancing-post-quantum-key-exchange-phase-2.html)

## 概要

Cloud Load Balancing における TLS ポスト量子鍵交換 (Post-Quantum Key Exchange) のサポートが、Application Load Balancer および外部プロキシ Network Load Balancer を対象としたロールアウトの Phase 2 に移行しました。Phase 2 (2026 年 10 月〜2027 年 10 月) では、ポスト量子鍵交換が**デフォルトで有効**になります。SSL ポリシーが未アタッチのロードバランサーや、ポスト量子鍵交換の設定を持たない SSL ポリシーを使用しているロードバランサーがこの変更の影響を受けます。

ポスト量子鍵交換は、量子コンピュータの脅威に備えた暗号技術です。Google は、研究が現在のペースで進めば、TLS で使用されている非対称暗号は**早ければ 2029 年にも量子コンピュータによって破られる可能性がある**と考えています。特に、現在暗号化された通信を記録しておき、将来量子コンピュータが実用化された時点で復号する「**Harvest Now, Decrypt Later (今収集して後で復号する) 攻撃**」への対策として、鍵交換の耐量子化は今すぐ対応すべき課題とされています。

Google Cloud のロードバランサーがサポートするポスト量子鍵交換は **X25519MLKEM768** で、古典暗号 (X25519) と NIST が標準化したポスト量子暗号 (ML-KEM-768) を組み合わせたハイブリッド方式です。クライアントが TLS 1.3 と X25519MLKEM768 のサポートを広告した場合にのみ使用されるため、未対応クライアントからの接続には影響しません。追加のテストが必要な場合や、クライアント・中間ネットワークデバイスとのネゴシエーションで問題が発生した場合は、SSL ポリシーで `DEFERRED` を設定することで 2027 年 10 月まで有効化を延期 (オプトアウト) できます。

**アップデート前の課題**

Phase 1 (2026 年 10 月まで) では、ポスト量子鍵交換はオプトイン方式でした。

- 以前はポスト量子鍵交換を利用するには、SSL ポリシーで明示的に `ENABLED` を設定する (オプトイン) 必要があった
- SSL ポリシーを設定していない大多数のロードバランサーでは、ポスト量子鍵交換が使用されず、Harvest Now, Decrypt Later 攻撃に対して無防備なままだった
- 耐量子セキュリティを組織全体に展開するには、各プロジェクト・各ロードバランサーで個別の設定作業が必要だった

**アップデート後の改善**

- Phase 2 (2026 年 10 月〜2027 年 10 月) では、SSL ポリシーの設定なしで、ポスト量子鍵交換がデフォルトで有効になった
- 対応クライアント (TLS 1.3 + X25519MLKEM768) との通信が自動的に耐量子ハイブリッド鍵交換で保護され、Harvest Now, Decrypt Later 攻撃のリスクが軽減された
- 互換性の問題がある場合は、SSL ポリシーの `post-quantum-key-exchange` を `DEFERRED` に設定することで、2027 年 10 月まで有効化を延期できる猶予が用意された

## アーキテクチャ図

```mermaid
flowchart TD
    subgraph Clients["クライアント"]
        C1([📱 TLS 1.3 + X25519MLKEM768 対応クライアント])
        C2([💻 未対応クライアント<br/>TLS 1.2 など])
    end

    subgraph GC["☁️ Google Cloud"]
        SSLP[/"📜 SSL ポリシー<br/>post-quantum-key-exchange:<br/>ENABLED / DEFAULT / DEFERRED"/]
        LB["⚖️ Application Load Balancer /<br/>外部プロキシ Network Load Balancer"]
        BE["🖥️ バックエンド"]
        SSLP -.->|アタッチ (任意)| LB
    end

    C1 -->|"🔐 ハイブリッド鍵交換<br/>X25519MLKEM768 (耐量子)"| LB
    C2 -->|"🔑 従来の鍵交換<br/>(影響なし)"| LB
    LB -->|"バックエンド側 TLS は対象外"| BE
```

Phase 2 ではフロントエンド TLS 接続においてポスト量子鍵交換がデフォルトで有効になり、対応クライアントとの間で自動的に X25519MLKEM768 ハイブリッド鍵交換が使用されます。未対応クライアントやロードバランサーとバックエンド間の接続には影響しません。

## サービスアップデートの詳細

### 主要機能

1. **ポスト量子鍵交換のデフォルト有効化 (Phase 2)**
   - 2026 年 10 月以降、SSL ポリシーが未アタッチのロードバランサー、またはポスト量子鍵交換の設定がない SSL ポリシーを使用するロードバランサーで、ポスト量子鍵交換がデフォルトで有効になる
   - クライアントが TLS 1.3 と X25519MLKEM768 のサポートを広告した場合にのみ使用されるため、未対応クライアントとの接続は従来どおり動作する

2. **ハイブリッド鍵交換方式 X25519MLKEM768**
   - 古典暗号 (X25519) と NIST 標準のポスト量子暗号 (ML-KEM-768) を組み合わせたハイブリッド方式で、どちらか一方が破られても安全性が保たれる
   - NIST が開発・検証したアルゴリズムを使用し、IETF で策定中の標準に準拠

3. **SSL ポリシーによる延期 (オプトアウト) オプション**
   - SSL ポリシーの `post-quantum-key-exchange` フィールドを `DEFERRED` に設定することで、2027 年 10 月までポスト量子鍵交換の有効化を延期可能
   - クライアントアプリケーションや中間ネットワークデバイスに互換性の問題がある場合の猶予措置として利用できる
   - Phase 3 (2027 年 10 月以降) では常時有効となり、`DEFERRED` 設定は効力を失う

### ロールアウトのタイムライン

| フェーズ | 期間 | ポスト量子鍵交換のステータス |
|---------|------|------------------------------|
| Phase 1 | 2026 年 10 月まで | SSL ポリシーによるオプトイン (`ENABLED` 設定時のみ有効) |
| **Phase 2 (現在)** | **2026 年 10 月〜2027 年 10 月** | **デフォルトで有効。`DEFERRED` 設定で延期可能** |
| Phase 3 | 2027 年 10 月以降 | 常時有効。延期オプションは効力を失う |

## 技術仕様

### 対応ロードバランサー

| ロードバランサー | ポスト量子鍵交換 |
|------------------|------------------|
| グローバル外部 Application Load Balancer | 対応 |
| クラシック Application Load Balancer | 対応 |
| リージョン外部 Application Load Balancer | 対応 |
| クロスリージョン内部 Application Load Balancer | 対応 |
| リージョン内部 Application Load Balancer | 対応 |
| グローバル外部プロキシ Network Load Balancer | 対応 |
| クラシックプロキシ Network Load Balancer | 対応 |

### ポスト量子鍵交換の動作仕様

| 項目 | 詳細 |
|------|------|
| 鍵交換アルゴリズム | X25519MLKEM768 (古典 + ポスト量子のハイブリッド) |
| 必要な TLS バージョン | TLS 1.3 (クライアント側が広告する場合のみ使用) |
| 適用範囲 | フロントエンド TLS 接続のみ (クライアント ↔ ロードバランサー間)。バックエンド側接続は対象外 |
| SSL ポリシープロファイルとの関係 | COMPATIBLE / MODERN / RESTRICTED / FIPS_202205 / CUSTOM のいずれのプロファイル、いずれの最小 TLS バージョン設定とも併用可能 |
| 対象外の暗号 | AES-128、AES-256、ChaCha20 などの対称暗号は量子コンピュータの脅威の対象外 |

### post-quantum-key-exchange のモード

| モード | 動作 |
|--------|------|
| `ENABLED` | ポスト量子鍵交換を有効化。対応クライアントとの間で X25519MLKEM768 を使用 |
| `DEFAULT` | ロードバランサーのデフォルト動作に従う (Phase 2 では有効) |
| `DEFERRED` | 2027 年 10 月までポスト量子鍵交換を一時的に無効化 (延期) |

## 設定方法

### 前提条件

1. SSL ポリシーをサポートするロードバランサー (Application Load Balancer または プロキシ Network Load Balancer) を使用していること
2. SSL ポリシーを作成・変更できる IAM 権限があること

### 手順

#### ステップ 1: 現在の SSL ポリシー構成を確認する

```bash
# グローバル・リージョンの SSL ポリシーを一覧表示
gcloud compute ssl-policies list
```

SSL ポリシーが未アタッチ、またはポスト量子鍵交換の設定がない場合、Phase 2 ではデフォルトで有効になっています。そのまま有効を維持することが推奨されます。

#### ステップ 2 (延期が必要な場合のみ): DEFERRED を設定した SSL ポリシーを作成する

```bash
# グローバル SSL ポリシーの作成例 (延期設定)
gcloud compute ssl-policies create pqc-deferred-policy \
    --profile MODERN \
    --min-tls-version 1.2 \
    --post-quantum-key-exchange DEFERRED
```

クライアントや中間ネットワークデバイスとのネゴシエーションに問題がある場合のみ、`DEFERRED` を設定します。作成したポリシーは `TargetHttpsProxy` または `TargetSslProxy` にアタッチします。

#### ステップ 3 (既存ポリシーを変更する場合): SSL ポリシーを更新する

```bash
# 既存のグローバル SSL ポリシーの更新例
gcloud compute ssl-policies update SSL_POLICY_NAME \
    --post-quantum-key-exchange DEFERRED

# リージョン SSL ポリシーの場合
gcloud compute ssl-policies update SSL_POLICY_NAME \
    --region REGION \
    --post-quantum-key-exchange DEFERRED
```

延期はあくまで一時的な猶予措置です。Phase 3 (2027 年 10 月以降) では `DEFERRED` は効力を失うため、それまでにクライアント側の互換性対応を完了させる必要があります。

## メリット

### ビジネス面

- **将来の量子脅威への先行対応**: Harvest Now, Decrypt Later 攻撃により、現在記録された通信が将来復号されるリスクを、設定作業なしで軽減できる
- **コンプライアンス・セキュリティ要件への対応**: NIST 標準のポスト量子暗号を採用しており、耐量子暗号への移行を求める規制・業界要件への対応を前倒しできる
- **移行の猶予期間**: 互換性に問題がある組織は 2027 年 10 月まで延期でき、計画的な移行が可能

### 技術面

- **ゼロコンフィグでの保護**: SSL ポリシーの設定なしでデフォルト有効になるため、大規模環境でも一括で耐量子保護が適用される
- **ハイブリッド方式による安全性**: X25519MLKEM768 は古典暗号とポスト量子暗号の両方で保護されるため、万一 ML-KEM に脆弱性が見つかっても X25519 の安全性が維持される
- **後方互換性**: TLS 1.3 と X25519MLKEM768 に対応したクライアントのみが対象で、未対応クライアントの接続には一切影響しない

## デメリット・制約事項

### 制限事項

- ポスト量子鍵交換はフロントエンド TLS 接続 (クライアント ↔ ロードバランサー間) のみが対象で、ロードバランサーとバックエンド間の接続には適用されない
- 量子コンピュータによる認証 (証明書) への攻撃は本機能の対象外 (本機能は鍵交換の保護のみ)
- `DEFERRED` による延期は 2027 年 10 月までの時限措置で、Phase 3 以降は設定しても効力を失う

### 考慮すべき点

- 正しく実装されたクライアントでは問題は発生しない想定だが、TLS 実装が古いクライアントや、TLS ハンドシェイクを検査する中間ネットワークデバイス (ファイアウォール、プロキシなど) で、大きくなった ClientHello / 鍵交換メッセージの処理に問題が発生する可能性がある
- 延期 (オプトアウト) を選択した場合でも、2027 年 10 月までにクライアントアプリケーションと中間デバイスの互換性対応を完了させる移行計画が必要
- SSL ポリシーを多数のプロジェクトで標準化したい場合は、クロスプロジェクト SSL ポリシー参照 (Preview) の活用も検討できる

## ユースケース

### ユースケース 1: 公開 Web サービスの耐量子保護 (推奨: デフォルトのまま有効)

**シナリオ**: グローバル外部 Application Load Balancer で公開している Web サービスで、長期間秘匿が必要な個人情報や金融データを扱っている。将来の量子コンピュータによる復号リスク (Harvest Now, Decrypt Later) に備えたい。

**実装例**:
```bash
# 何も設定しない (デフォルトで有効) か、明示的に ENABLED を設定
gcloud compute ssl-policies create pqc-enabled-policy \
    --profile MODERN \
    --min-tls-version 1.2 \
    --post-quantum-key-exchange ENABLED
```

**効果**: Chrome など X25519MLKEM768 対応クライアントとの通信が自動的に耐量子ハイブリッド鍵交換で保護され、記録された通信が将来復号されるリスクを軽減できる。

### ユースケース 2: レガシー環境を抱える企業での段階的移行

**シナリオ**: 社内システムのクライアントや中間ネットワーク機器 (TLS インスペクションを行うファイアウォールなど) が古く、ポスト量子鍵交換のネゴシエーションで問題が発生した。互換性対応が完了するまで有効化を延期したい。

**効果**: SSL ポリシーで `DEFERRED` を設定することで 2027 年 10 月まで有効化を延期でき、その間にクライアント・機器のアップデートを計画的に実施できる。Phase 3 の期限が明確なため、移行計画の締め切りとして活用できる。

## 料金

ポスト量子鍵交換の利用自体に追加料金に関する記載はありません。Cloud Load Balancing および SSL ポリシーの利用には通常の Cloud Load Balancing 料金が適用されます。詳細は料金ページを参照してください。

- [Cloud Load Balancing の料金](https://cloud.google.com/vpc/network-pricing#lb)

## 利用可能リージョン

SSL ポリシーをサポートするすべての対象ロードバランサー (グローバル・リージョンの Application Load Balancer、外部プロキシ Network Load Balancer) で利用できます。詳細は[ポスト量子鍵交換のドキュメント](https://docs.cloud.google.com/load-balancing/docs/post-quantum-tls)を参照してください。

## 関連サービス・機能

- **SSL ポリシー**: ポスト量子鍵交換のモード (`ENABLED` / `DEFAULT` / `DEFERRED`) を制御する設定の中核。プロファイル (COMPATIBLE / MODERN / RESTRICTED / FIPS_202205 / CUSTOM) や最小 TLS バージョンと組み合わせて利用する
- **Certificate Manager / Google マネージド SSL 証明書**: ロードバランサーのフロントエンド TLS を構成する証明書管理サービス。ポスト量子鍵交換はこれらの証明書構成と独立して動作する
- **クロスプロジェクト SSL ポリシー参照 (Preview)**: 管理プロジェクトで一元管理した SSL ポリシーを複数のサービスプロジェクトから参照でき、組織全体でポスト量子鍵交換の設定を標準化できる
- **Cloud KMS のポスト量子暗号対応**: Google Cloud は TLS 以外でも耐量子暗号への移行を進めており、組織全体の PQC 移行戦略の一部として位置づけられる

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261116-cloud-load-balancing-post-quantum-key-exchange-phase-2.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#November_16_2026)
- [ポスト量子鍵交換のドキュメント](https://docs.cloud.google.com/load-balancing/docs/post-quantum-tls)
- [SSL ポリシーの概要](https://docs.cloud.google.com/load-balancing/docs/ssl-policies-concepts)
- [SSL ポリシーの使用 (作成・更新手順)](https://docs.cloud.google.com/load-balancing/docs/use-ssl-policies)
- [Google Cloud のポスト量子暗号](https://cloud.google.com/security/resources/post-quantum-cryptography)
- [料金ページ](https://cloud.google.com/vpc/network-pricing#lb)

## まとめ

Cloud Load Balancing のポスト量子鍵交換が Phase 2 に移行し、デフォルトで有効になりました。追加設定なしで Harvest Now, Decrypt Later 攻撃への耐性が得られるため、原則としてそのまま有効を維持することが推奨されます。クライアントや中間機器で互換性の問題がある場合は SSL ポリシーの `DEFERRED` 設定で 2027 年 10 月まで延期できますが、Phase 3 以降は延期できなくなるため、今のうちに自社環境での互換性検証と移行計画の策定を進めるべきです。

---

**タグ**: Cloud Load Balancing, Post-Quantum Cryptography, TLS, SSL ポリシー, X25519MLKEM768, セキュリティ, Application Load Balancer, Network Load Balancer
