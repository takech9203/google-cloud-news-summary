# Confidential Space: 新イメージ 261000 リリース

**リリース日**: 2026-10-19

**サービス**: Confidential Space

**機能**: Confidential Space イメージ 261000

**ステータス**: Announcement

📊 [このアップデートのインフォグラフィックを見る](https://takech9203.github.io/google-cloud-news-summary/20261019-confidential-space-image-261000.html)

## 概要

Confidential Space の新しいイメージ (バージョン 261000) が利用可能になりました。Confidential Space イメージは、Confidential VM 上で動作する単一目的のミニマル OS で、Container-Optimized OS (COS) をベースに、暗号化・完全性保護されたディスクパーティション、認証付き暗号化ネットワーク接続、ブート測定、リモートアクセスの無効化などのセキュリティ強化が施されています。

今回のリリースノートでは、イメージ 261000 で追加された個別の機能や修正内容は公表されていません。Confidential Space イメージは定期的 (概ね毎月) に更新されており、新しいイメージの公開に伴い、既存イメージのサポート属性 (LATEST / STABLE / USABLE) が順次移行します。アテステーションポリシーで `LATEST` 属性を要求している環境では、イメージの更新タイミングに注意が必要です。

## アーキテクチャ図

```mermaid
flowchart TD
    A[📦 Confidential Space イメージファミリー<br>confidential-space / confidential-space-debug] -->|最新版 261000 を提供| B[🖥️ Confidential VM インスタンス]
    B --> C[🐳 ワークロードコンテナ]
    B --> D[🔏 アテステーショントークン生成]
    D --> E{🔍 データコラボレーターの<br>アテステーションポリシー検証}
    E -->|support_attributes: LATEST / STABLE| F[✅ 機密データへのアクセス許可]
    E -->|古いイメージ (USABLE のみ)| G[❌ アクセス拒否の可能性]
```

イメージファミリーから Confidential VM を新規作成すると最新イメージ (261000) が使用され、アテステーション検証でイメージのサポート属性が確認されるフローを示しています。

## サービスアップデートの詳細

### 主要なポイント

1. **新イメージ 261000 の提供開始**
   - 2026 年 10 月 19 日付の Google Cloud Release Notes で発表
   - イメージファミリー (`confidential-space` / `confidential-space-debug`) から VM を新規作成すると自動的に最新イメージが使用される
   - 今回のリリースノートには個別の変更内容 (機能追加・修正) の記載はない

2. **サポート属性の移行**
   - 新イメージの公開により、261000 が `LATEST` (および `STABLE`、`USABLE`) 属性を持つイメージとなる
   - 旧イメージの `LATEST` 属性は約 1 か月で外れ、`STABLE` 属性は約 6 か月間維持される

## 技術仕様

### イメージのサポート属性

| サポート属性 | 内容 |
|------|------|
| LATEST | 最新イメージ。有効期間は約 1 か月。脆弱性の監視・サポート対象 |
| STABLE | 有効期間は約 6 か月。脆弱性の監視・サポート対象。アテステーションポリシーには STABLE の使用が推奨される |
| USABLE | 6 か月超の非推奨 (deprecated) イメージ。利用は可能だがサポート対象外 |
| EXPERIMENTAL | プレビュー機能を含むテスト専用イメージ。本番利用不可 |

### イメージの確認方法

```bash
# 利用可能な Confidential Space イメージの一覧 (本番イメージ)
gcloud compute images list \
  --project=confidential-space-images \
  --no-standard-images \
  --filter="family~'confidential-space$'"

# イメージの詳細 (サポート属性・非推奨予定日など) の確認
gcloud compute images describe confidential-space-261000 \
  --format=json \
  --project=confidential-space-images
```

## デメリット・制約事項

### 考慮すべき点

- 今回のリリースノートでは 261000 の変更内容が公表されていないため、動作差分を確認したい場合は公式ドキュメントの Confidential Space リリースノートを継続的に確認する必要がある
- アテステーションポリシーで `LATEST` を要求している場合、新イメージ公開に伴い旧イメージの `LATEST` 属性が外れ、実行中のワークロードがトークン更新時にアテステーションに失敗する可能性がある。長時間実行ワークロードには `STABLE` 属性ベースのポリシーが推奨される
- `LATEST` 要求のポリシーでは最低でも毎月、`STABLE` 要求のポリシーでは最低でも 6 か月ごとにイメージの更新 (VM の再作成) が必要
- VM の再作成を容易にするため、インスタンステンプレート、自動修復付きマネージドインスタンスグループ (MIG)、OS イメージの一括アップグレードの活用が推奨される

## 関連サービス・機能

- **Confidential VM**: Confidential Space イメージが動作する基盤。AMD SEV、Intel TDX (C3)、H100 GPU (a3-highgpu-1g) などに対応
- **Confidential Computing API (アテステーション)**: ワークロードの構成とイメージバージョン (`swversion`、`support_attributes` アサーション) を検証
- **Container-Optimized OS**: Confidential Space イメージのベース OS
- **Cloud Logging / Cloud Monitoring**: 非推奨イメージ検出のログベースアラート設定に利用可能

## 参考リンク

- 📊 [インフォグラフィック](https://takech9203.github.io/google-cloud-news-summary/20261019-confidential-space-image-261000.html)
- [公式リリースノート](https://docs.cloud.google.com/release-notes#October_19_2026)
- [Confidential Space リリースノート](https://docs.cloud.google.com/confidential-computing/confidential-space/docs/release-notes)
- [Confidential Space イメージ (ライフサイクル・サポート属性)](https://docs.cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-images)
- [アテステーションアサーション リファレンス](https://docs.cloud.google.com/confidential-computing/confidential-space/docs/reference/attestation-assertions)

## まとめ

Confidential Space の新イメージ 261000 がリリースされました。変更内容の詳細は公表されていませんが、イメージの公開に伴いサポート属性が移行するため、アテステーションポリシーで `LATEST` を要求している環境では早期のイメージ更新 (VM 再作成) を推奨します。長時間実行ワークロードでは `STABLE` 属性ベースのポリシー設計と、MIG などを活用した定期的なイメージ更新の仕組み化を検討してください。

---

**タグ**: #ConfidentialSpace #ConfidentialComputing #セキュリティ #イメージ更新 #アテステーション
