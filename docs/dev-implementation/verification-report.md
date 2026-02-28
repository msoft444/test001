# 統合レビュー & 品質監査レポート（Step 5: テーマ切替拡張）

## 監査結果: Pass（条件付き合格）

テーマ切替機能（cool/warm）の最小実装は要件を満たし、テストは全19件 Pass。
既存ダークモードトグルとの二重制御に起因する UX 不整合を中リスクとして指摘するが、差し戻し不要。

---

## 1. 実装差分サマリ

| 変更対象 | 変更内容 | 行数 |
|----------|----------|------|
| src/static/index.html (CSS) | `:root` に --accent/--warning 追加、`[data-theme="cool"]`/`[data-theme="warm"]` トークンブロック追加、select要素スタイル追加 | +46行 |
| src/static/index.html (HTML) | テーマ選択カード (`<select id="theme-select">`) 追加 | +12行 |
| src/static/index.html (JS) | DEFAULT_THEME, ALLOWED_THEMES, applyTheme(), localStorage 永続化ロジック追加 | +20行 |
| tests/test_app_red.py | テーマ関連テスト3件追加 | +25行 |
| docs/ | 要件定義・基本設計・レビューログをテーマ拡張向けに更新 | 差分のみ |

---

## 2. 非機能要件チェック結果

| 項目 | 判定 | 備考 |
|------|------|------|
| パフォーマンス | Pass | CSS変数切替のみ、DOMリフロー最小 |
| セキュリティ | Pass | ALLOWED_THEMES ホワイトリスト検証済、setAttribute に検証済み値のみ |
| 保守性 | Pass | トークンベース設計、テーマ追加は CSS ブロック＋配列追記のみ |
| 互換性 | Pass（注意） | 既存 body.dark-mode との併存は意図的だが競合リスクあり |
| ファイルサイズ | Pass | 21.8KB（+80行追加、妥当な増分） |
| コーディング規約 | Pass | 既存インラインスタイルと一貫 |

---

## 3. テスト健全性チェック結果

- **テスト件数**: 19件（+3件追加）、全 Pass
- **ハック有無**: なし
- **形骸テスト**: なし（assertIn で HTML ソースの実在要素を検証、トートロジーなし）
- **過度な実装依存**: 軽微（文字列一致チェックのためリファクタで壊れ得るが許容範囲）

### 追加テスト詳細

| テスト名 | 検証内容 | 健全性 |
|----------|----------|--------|
| test_html_has_theme_selector_for_dark_cool_warm | UI要素(theme-select, value属性)の存在 | 正当 |
| test_inline_script_validates_theme_with_whitelist_and_fallback | ホワイトリスト・localStorage・data-theme・DEFAULT_THEME | 正当 |
| test_inline_style_defines_cool_and_warm_theme_tokens | CSSセレクタ・カスタムプロパティ | 正当 |

---

## 4. 主要リスク

### R1（中）: ダークモードトグルとテーマ select の二重制御
- `body.dark-mode` クラスと `[data-theme]` 属性が独立して存在
- body レベルの CSS 変数が html レベルの data-theme を上書きするため、dark toggle ON + cool/warm 選択時に視覚的不整合が発生
- **推奨**: 次フェーズでダークモードトグルをテーマ select に統合し単一制御に一本化

### R2（中）: `[data-theme="dark"]` CSS ブロックの欠如
- theme-select で "dark" 選択時に `data-theme="dark"` が設定されるが対応 CSS ルールなし
- :root のライトモードデフォルトが適用され、期待するダーク外観にならない
- **推奨**: `[data-theme="dark"]` ブロック追加、または theme-select "dark" 選択時に body.dark-mode を連動トグル

### R3（低）: アクセシビリティ未検証
- cool/warm テーマの WCAG AA コントラスト比は目視では妥当だが正式計測未実施

---

## 5. 差し戻し要否: 不要

R1/R2 は改善推奨だが、要件の機能範囲（cool/warm テーマ追加、ホワイトリスト検証、localStorage 永続化、data-theme 反映）は満たされており、テストも健全に Pass。差し戻しは不要。
