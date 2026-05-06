# Gemini Enterprise Agent Platform: Audio Track Extraction バグ修正

**リリース日**: 2026-05-06

**サービス**: Gemini Enterprise Agent Platform

**機能**: Gemini Embedding 2 - Audio Track Extraction 修正

**ステータス**: Fixed

## 概要

Gemini Enterprise Agent Platform の Gemini Embedding 2 モデルにおいて、`audio_track_extraction` 機能が正常に動作しない不具合が修正されました。この修正により、動画入力からオーディオトラックを抽出してビデオフレームとインターリーブする機能が正常に利用可能になりました。

**アップデート前の課題**

- Gemini Embedding 2 で `audio_track_extraction` オプションを有効にしても、動画からオーディオトラックが抽出されなかった
- 動画の埋め込みベクトル生成時に音声情報が含まれず、マルチモーダル検索の精度に影響があった
- Issue #504505771 として報告されていた既知の問題

**アップデート後の改善**

- `audio_track_extraction` 機能が正常に動作するようになった
- 動画入力時にオーディオトラックが正しく抽出され、ビデオフレームとインターリーブされるようになった
- 動画コンテンツのマルチモーダル埋め込み生成がドキュメント通りに機能するようになった

## サービスアップデートの詳細

### Audio Track Extraction 機能について

Gemini Embedding 2 は Google のマルチモーダル埋め込み生成モデルであり、テキスト、画像、ドキュメント、音声、動画の入力を受け付けて 3072 次元のベクトルを生成します。Audio Track Extraction は動画入力時にオーディオトラックを抽出してビデオフレームとインターリーブする機能です。

### 影響範囲

この修正は Gemini Embedding 2 モデル (`gemini-embedding-2`) のみに影響します。他のモデルには影響しません。

## 技術仕様

### Audio Track Extraction の仕様

| 項目 | 詳細 |
|------|------|
| 対象モデル | gemini-embedding-2 |
| 動画最大長 (音声抽出有効時) | 約 81 秒 (8192 トークン制限) |
| 音声最大長 | 180 秒 |
| 対応動画フォーマット | MOV, MP4 (コーデック: AV1, H264, H265, VP9) |
| 対応音声フォーマット | MP3, WAV |
| トークン消費 | 音声: 25 tokens/秒、ビデオフレーム: 66 tokens/フレーム、タイムスタンプ: 10 tokens/秒 |

### トークン計算例

動画を 1 FPS (デフォルト) で処理し、`audio_track_extraction` を有効にした場合:

- 1 秒あたりの消費: 66 tokens (1 フレーム) + 25 tokens (音声 1 秒) + 10 tokens (タイムスタンプ) = 101 tokens
- 最大処理時間: 8192 / 101 = 約 81 秒

## 関連サービス・機能

- **Gemini Embedding 2**: マルチモーダル埋め込み生成モデル (GA: 2026年4月22日リリース)
- **Gemini Enterprise Agent Platform**: 旧 Vertex AI から名称変更されたプラットフォーム

## 参考リンク

- [公式リリースノート](https://docs.cloud.google.com/release-notes#May_06_2026)
- [Issue Tracker #504505771](https://issuetracker.google.com/504505771)
- [Gemini Embedding 2 ドキュメント](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/embedding-2)
- [マルチモーダル埋め込み取得ガイド](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-multimodal-embeddings)

## まとめ

Gemini Embedding 2 の `audio_track_extraction` 機能の不具合が修正されました。動画からの埋め込みベクトル生成でオーディオ情報も含めたマルチモーダル処理を行っているユーザーは、この修正により正常な動作が期待できます。特に対応は不要ですが、以前この機能が動作しなかったために回避策を取っていた場合は、正規の `audio_track_extraction` 機能の利用を再開できます。

---

**タグ**: #GeminiEnterpriseAgentPlatform #GeminiEmbedding2 #AudioTrackExtraction #BugFix #Multimodal #Embeddings
