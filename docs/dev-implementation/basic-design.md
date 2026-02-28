# 基本設計書：テーマ切替（ダーク/寒色/暖色）

## 1. アーキテクチャ方針
- CSS変数（デザイントークン）中心の実装
- ルート要素 data-theme 属性でテーマ切替
- バックエンドは最小限のテーマ設定保持・伝搬

## 2. デザイントークン
- --bg, --fg, --muted-fg, --card-bg
- --accent, --accent-contrast
- --border, --focus
- --success, --warning, --danger

## 3. テーマ定義
- dark: 暗背景、既存アクセント
- cool: 青〜シアン寄り背景/アクセント
- warm: 橙〜赤寄り背景/アクセント

## 4. データフロー
- ローカル: localStorage → ルート要素適用 → 切替 → 即時反映 → localStorage更新
- サーバ拡張: ホワイトリスト検証 → constraints_json/ui_preferences 保存

## 5. エラーハンドリング
- テーマID: {dark,cool,warm,system} のみ受理
- 未知値: デフォルトフォールバック
- CSS/HTML直接注入は拒否