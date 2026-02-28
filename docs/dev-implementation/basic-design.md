# 基本設計書：テーマ切替（ダーク/寒色/暖色）

## 1. アーキテクチャ方針
### 1.1 基本方針
- UIの見た目切替は **CSS変数（デザイントークン）** を中心に実装し、テーマIDに応じてルート要素（例：`<html data-theme="cool">`）または `:root` の変数セットを切り替える。
- バックエンド（本リポジトリ）は、必要最小限の「テーマ設定値の保持・伝搬」を担い、UIが無い環境でも動作を壊さない。

### 1.2 デザイントークン（推奨）
- トークン例：
  - `--bg`, `--fg`, `--muted-fg`, `--card-bg`
  - `--accent`, `--accent-contrast`
  - `--border`, `--focus`
  - `--success`, `--warning`, `--danger`
- テーマ定義：
  - `dark`: 背景を暗く、アクセントは既存に近い色
  - `cool`: 背景/アクセントを青〜シアン寄りに
  - `warm`: 背景/アクセントを橙〜赤寄りに

## 2. 変更対象モジュール
### 2.1 ダッシュボード（別リポジトリ/別ディレクトリ想定）
- テーマ切替UI（設定メニュー/ヘッダー）
- CSS/スタイル基盤（CSS変数、テーマクラス/属性、コンポーネント配色）
- 永続化（localStorage 等）

### 2.2 本リポジトリ（Python基盤）
- （任意）SalesAgent：ダッシュボードからのリクエストpayloadに `ui_theme` が含まれる場合に受け取り、会話コンテキストへ保持
- （任意）ManagerAgent：会話の `constraints_json`（dev_ctx）に `ui_preferences` を格納して永続化
  - 既存実装で `constraints_json` が dict として利用される dev フローに整合させる
- （任意）DB：サーバ永続化が必要なら user_settings 的テーブル追加（ただし本リポジトリにユーザー概念が無いため、設計のみ）

## 3. データフロー/状態遷移
### 3.1 状態モデル
- `theme_id` ∈ {`dark`, `cool`, `warm`}（推奨で `system` も内部値として許容）

### 3.2 フロー（ローカル永続のみ：最小構成）
1. UI起動
2. localStorage から `theme_id` 読み込み
3. ルート要素へテーマ適用（data属性/クラス付与）
4. ユーザーが切替 → 即時適用 → localStorage 更新

### 3.3 フロー（サーバ永続あり：拡張構成）
1. UI起動
2. localStorage とサーバ保存値を解決（優先順位：明示ユーザー設定 > localStorage > system/default）
3. UIで切替
4. サーバへ `ui_preferences.theme_id` 更新メッセージ/API送信
5. バックエンドはホワイトリスト検証して保存（会話単位 or ユーザー単位）

### 3.4 本基盤での保持案（constraints_json活用）
- devフロー（constraints_json が dict として使われ得る）に合わせ、以下キーを追加：
  - `ui_preferences: { "theme_id": "cool" }`
- 通常フロー（constraints_json が list[str]）では、互換性維持のため「特別な制約文字列」として保持する案：
  - 例：`"ui_theme:cool"`（TaskPlanner/LLMプロンプト用。UI用途は別途）
- ただし、UIテーマは本来UI側の関心事であるため、会話制約に混ぜることの是非は運用判断（issues参照）。

## 4. エラーハンドリング方針
- 入力検証：テーマIDは `{dark,cool,warm,system}` のみ受理。未知値は無視してデフォルトへフォールバック。
- 失敗時の挙動：
  - UI：フォールバック適用し、設定は保存しない（または上書きで修正）
  - バックエンド：例外を投げず、ログに `invalid_theme_id` を記録して処理継続
- セキュリティ：CSS/HTMLを直接注入する文字列は受け取らない（テーマIDのみ）。

## 5. テスト戦略（概要）
- UI単体：テーマ切替で CSS 変数が切り替わること、主要コンポーネントの視認性をスナップショット/ビジュアルテストで確認
- 結合：永続化（localStorage/サーバ）と復元、複数ページ遷移での維持
- 回帰：Markdown/コードブロック/テーブル、成功/失敗ステータス表示の可読性
- バックエンド（拡張構成の場合）：テーマID検証、保存・取得、constraints_json 互換性（list/dict）
