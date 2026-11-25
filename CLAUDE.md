# Project Rules (Spec-Driven Development)

## 1. 最優先事項
- 実装の「正」は常に `SPEC.md` である。仕様にない機能を勝手に追加しないこと。
- 仕様変更時は、必ず先に `SPEC.md` を更新・承認してからコードを変更すること。

## 2. 技術スタックと規約
- Backend: Python / FastAPI / SQLite (標準の sqlite3 を使用)
- Frontend: Jinja2 HTML + Vanilla JS (`static/app.js`)
- HTML内にインラインの `<script>` を記述することを禁止する。JSはすべて `static/app.js` に分離し、JSDocで型を明記すること。
- Pythonの関数には必ず型ヒント（Type Hints）を記述すること。
- 変更後は必ず `pytest` を実行し、全テストがパスすることを確認すること。