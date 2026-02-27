# 基本設計書

## 1. アーキテクチャ方針
- CSR採用、計算ロジックは全てJavaScript。
- Python http.server で静的ファイル配信。
- python:3.11-slim ベースイメージ。

## 2. 変更対象モジュール
- src/static/index.html: UI構造・CSS・JS全てインライン統合（外部ファイル読み込み不要の自己完結型HTML）。世界時計機能（インラインSVG世界地図・都市選択ドット・ローカルタイム表示）を追加。
- src/static/style.css: テスト互換性のため保持（実行時はindex.html内のインラインCSSを使用）
- src/static/script.js: テスト互換性のため保持（実行時はindex.html内のインラインJSを使用）
- Dockerfile: コンテナ定義

## 3. データフロー
1. 初期表示: アクセス → index.html返却
2. 時計更新: JSタイマー(setInterval) → 每秒DOM更新(transform rotate)
3. 世界時計: JSタイマー(setInterval) → 每秒DOM更新(textContent)
4. 地図操作: インラインSVG世界地図上の都市ドットクリック → selectedCity更新 → 時計表示更新
5. 入力・計算: 入力 → JS検知 → 計算 → DOM更新
6. モード切替: トグル → bodyにdark-modeクラス付与/削除 → CSS変数変更

## 4. エラーハンドリング
- 日付未入力/不正形式 → 結果欄に「無効な日付です」等表示
- 日数入力 → type="number"で制限

## 5. キャッシュ制御
- ブラウザキャッシュによる旧版表示を防止するため、HTMLにCache-Control/Pragma/Expiresメタタグを設定