# Gemini Enterprise Agent Platform: Gemini Online Inference API SLA の管理上の修正

**リリース日**: 2026-06-25

**サービス**: Gemini Enterprise Agent Platform

**機能**: Gemini Online Inference API SLA 修正

**ステータス**: 管理上の修正 (Administrative Correction)

## 概要

Google Cloud は、Gemini Enterprise Agent Platform 上の Gemini Online Inference API に関する Service Level Agreement (SLA) ドキュメントに対して、管理上の修正 (administrative correction) を実施した。これは事務的な記載ミスを修正するものであり、SLA の条件や保証内容に実質的な変更はない。

本修正はサービスの機能や可用性目標に影響を与えるものではなく、ドキュメントの正確性を維持するための定期的なメンテナンスの一環である。

## サービスアップデートの詳細

### 対象 SLA の概要

Gemini Online Inference API on Gemini Enterprise Agent Platform の SLA は、以下の 2 つの SLO (Service Level Objective) を定義している。

**1. 月間稼働率 SLO**

| 対象サービス | 月間稼働率 |
|------|------|
| generateContent / streamGenerateContent メソッド | 99.5% |

**2. 月間レイテンシターゲット達成率 SLO (Provisioned Throughput)**

| 対象サービス | 月間レイテンシターゲット達成率 |
|------|------|
| streamGenerateContent メソッド (Provisioned Throughput) | 99% |

### レイテンシターゲット (対象モデル)

| モデル | レイテンシターゲット (TPS) |
|------|------|
| Gemini 2.5 Pro | 60 TPS (Long Context 除く) |
| Gemini 2.5 Flash | 80 TPS (Long Context 除く) |
| Gemini 2.5 Flash-lite | 110 TPS (Long Context 除く) |

### Financial Credit 体系

**稼働率 SLO 未達時:**

| 月間稼働率 | クレジット割合 |
|------|------|
| 99.0% - < 99.5% | 月額料金の 10% |
| 95.0% - < 99.0% | 月額料金の 25% |
| < 95.0% | 月額料金の 50% |

**レイテンシ SLO 未達時:**

| 月間レイテンシ達成率 | クレジット割合 |
|------|------|
| 95.0% - < 99.0% | 月額料金の 10% |
| 90.0% - < 95.0% | 月額料金の 25% |
| < 90.0% | 月額料金の 50% |

### 今回の修正内容

今回の修正は「clerical issue (事務的な記載ミス)」の修正であり、SLA の実質的な条件変更ではない。SLA ドキュメントの最終更新日は 2026 年 6 月 25 日に更新されている。

## 参考リンク

- [Gemini Online Inference API SLA](https://cloud.google.com/vertex-ai/generative-ai/sla)
- [公式リリースノート](https://cloud.google.com/release-notes#June_25_2026)

## まとめ

本アップデートは Gemini Online Inference API on Gemini Enterprise Agent Platform の SLA ドキュメントに対する管理上の修正であり、事務的な記載ミスの訂正に留まる。SLA の保証内容 (月間稼働率 99.5%、レイテンシターゲット達成率 99%) に変更はなく、ユーザーが対応すべきアクションはない。

---

**タグ**: #GeminiEnterpriseAgentPlatform #SLA #AdministrativeCorrection #VertexAI
