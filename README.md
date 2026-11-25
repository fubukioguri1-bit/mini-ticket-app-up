# mini-ticket-app

チケットを受け取ってステータスおよび優先度（`HIGH` / `MEDIUM` / `LOW`）別に管理する簡易チケット管理アプリ

## 背景・ゴール（完了基準）
- **背景**: タスクをチケットとして受け取ってチーム内で管理する
- **MVPのゴール**:
  - [x] チケットの作成・一覧表示・ステータス更新・削除ができる
  - [x] ステータスごとにフィルタリングできる
  - [x] 優先度（`HIGH`, `MEDIUM`, `LOW` / 初期値 `LOW`）を設定でき、`HIGH` のチケットは誤削除を防止できる

## 技術スタック
- **Frontend**: HTML (Jinja2) / Vanilla JavaScript
- **Backend**: Python / FastAPI / SQLite
- **Test / Tools**: pytest / GitHub Actions

## ディレクトリ構成
※AIや開発者が参照先を迷わないよう、主要なフォルダの役割を記載します。

```text
mini-ticket-app/
├─app                              # 画面・ルーティング・DB・モデル
│  │  database.py
│  │  main.py
│  │  models.py
│  └─templates
│          index.html
├─static                           # フロントエンドJS
│      app.js
└─tests                            # テストコード
        test_tickets.py
```

## 環境構築・起動手順

### 1. リポジトリのクローン
```bash
git clone https://github.com
cd mini-ticket-app
```

### 2. 依存パッケージのインストールと起動
```bash
pip install fastapi uvicorn jinja2 pydantic pytest httpx
uvicorn app.main:app --reload
```
ブラウザで `http://127.0.0.1:8000` にアクセスして動作を確認します。

### 3. テストの実行
```bash
pytest
```

## 開発ルール・運用
- 仕様変更は `SPEC.md` を起点に行い、実装・テスト・ドキュメントの整合性を保つ。
- 作業は **Issue単位** で分割し、1つずつ完了させてから次の作業へ進む。
- 機密情報（APIキーやパスワード）は絶対にコミットせず、`.env` で管理する。
- プルリクエスト作成前に `pytest` とセキュリティチェックを通す。