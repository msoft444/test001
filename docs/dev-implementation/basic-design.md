# 基本設計書

## 1. アーキテクチャ方針
- CSR採用、計算ロジックは全てJavaScript。
- Python http.server で静的ファイル配信。
- python:3.11-slim ベースイメージ。

## 2. 変更対象モジュール
- src/static/index.html: UI構造（時計コンテナ追加、入力欄の構造化）
- src/static/style.css: 配色・レイアウト刷新（カードデザイン、時計スタイル）、ダークモードCSS変数
- src/static/script.js: 計算ロジック・イベント・ダークモード制御、時計更新ロジック
- Dockerfile: コンテナ定義

## 3. データフロー
1. 初期表示: アクセス → index.html返却
2. 時計更新: JSタイマー(setInterval) → 每秒DOM更新(transform rotate)
3. 入力・計算: 入力 → JS検知 → 計算 → DOM更新
4. モード切替: トグル → bodyにdark-modeクラス付与/削除 → CSS変数変更

## 4. エラーハンドリング
- 日付未入力/不正形式 → 結果欄に「無効な日付です」等表示
- 日数入力 → type="number"で制限