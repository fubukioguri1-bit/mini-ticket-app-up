# 簡易タスク・チケット管理アプリ 仕様書 (SPEC.md)

## 1. 概要
プロジェクト内のタスク（チケット）を登録・一覧表示・ステータス更新・削除できるWebアプリケーション。

## 2. データモデル (`tickets` テーブル)

| カラム名 | 型 | 制約 | 説明 |
| :--- | :--- | :--- | :--- |
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | チケットID |
| title | TEXT | NOT NULL (1〜100文字) | チケットの件名 |
| assignee | TEXT | NOT NULL (1〜50文字) | 担当者名 |
| status | TEXT | NOT NULL | `TODO`, `DOING`, `DONE` のいずれか（初期値: `TODO`） |
| priority | TEXT | NOT NULL | `HIGH`, `MEDIUM`, `LOW` のいずれか（初期値: `LOW`） |
| created_at | TEXT | NOT NULL | 作成日時 (ISO8601形式) |

## 3. 画面・API仕様
### 3.1 画面表示 (`GET /`)
- 登録済みチケットの一覧をID降順で表示する。
- クエリパラメータ `?status=TODO` 等が指定された場合、該当ステータスで絞り込む。

### 3.2 チケット作成 (`POST /api/tickets`)
- **入力(JSON)**: `{"title": "件名", "assignee": "担当者"}`
- **バリデーション**:
  - `title` が空文字・空白のみ、または101文字以上の場合は `422 Unprocessable Entity` を返す。
  - `assignee` が空文字・空白のみ、または51文字以上の場合は `422 Unprocessable Entity` を返す。
- **正常時**: ステータス `TODO` でDBに登録し、`201 Created` と作成したチケットJSONを返す。

### 3.3 ステータス更新 (`PATCH /api/tickets/{ticket_id}`)
- **入力(JSON)**: `{"status": "DOING"}`
- **業務ルール**:
  - `status` は `TODO`, `DOING`, `DONE` 以外は `422` エラー。
  - 存在しない `ticket_id` の場合は `404 Not Found` を返す。
  - **禁止遷移ルール**: 一度 `DONE`（完了）になったチケットを `TODO` に直接戻すことは禁止する（`400 Bad Request` を返す）。※`DOING` への差し戻しは許可。
  - `priority` が `HIGH` のチケットは削除できない。

### 3.4 チケット削除 (`DELETE /api/tickets/{ticket_id}`)
- 存在しない `ticket_id` の場合は `404 Not Found` を返す。
- 正常時: DBから削除し、`204 No Content` を返す。