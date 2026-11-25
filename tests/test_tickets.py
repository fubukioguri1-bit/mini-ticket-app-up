from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

import app.database as db
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """テストごとに一時DBを作成してクリーンな状態で実行する"""
    test_db = tmp_path / "test_tickets.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)
    db.init_db()
    yield


def test_create_and_get_ticket():
    # SPEC 3.2: 正常作成
    res = client.post("/api/tickets", json={"title": "テストタスク", "assignee": "山田"})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "テストタスク"
    assert data["status"] == "TODO"

    # SPEC 3.1: 一覧画面表示
    html_res = client.get("/")
    assert html_res.status_code == 200
    assert "テストタスク" in html_res.text


def test_validation_error():
    # SPEC 3.2: 空白のみは422エラー
    res = client.post("/api/tickets", json={"title": "   ", "assignee": "山田"})
    assert res.status_code == 422


def test_status_transition_rule():
    # SPEC 3.3: DONE -> TODO の禁止遷移ルール検証
    res = client.post("/api/tickets", json={"title": "完了予定タスク", "assignee": "佐藤"})
    ticket_id = res.json()["id"]

    # TODO -> DONE はOK
    res_done = client.patch(f"/api/tickets/{ticket_id}", json={"status": "DONE"})
    assert res_done.status_code == 200

    # DONE -> TODO は400エラーになるべき
    res_back = client.patch(f"/api/tickets/{ticket_id}", json={"status": "TODO"})
    assert res_back.status_code == 400

    # DONE -> DOING はOK
    res_doing = client.patch(f"/api/tickets/{ticket_id}", json={"status": "DOING"})
    assert res_doing.status_code == 200