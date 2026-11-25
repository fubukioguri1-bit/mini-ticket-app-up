from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.database import get_connection,init_db
from app.models import StatusType, TicketCreate, TicketResponse, TicketStatusUpdate

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Mini Ticket App")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def read_index(request: Request, status: Optional[StatusType] = Query(None)) -> HTMLResponse:
    with get_connection() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM tickets WHERE status = ? ORDER BY id DESC", (status,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM tickets ORDER BY id DESC").fetchall()
    tickets = [dict(row) for row in rows]
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"tickets": tickets, "current_status": status or ""},
    )


@app.post("/api/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tickets (title, assignee, status, created_at) VALUES (?, ?, 'TODO', ?)",
            (ticket.title, ticket.assignee, now),
        )
        ticket_id = cursor.lastrowid
        conn.commit()
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return dict(row)


@app.patch("/api/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket_status(ticket_id: int, payload: TicketStatusUpdate) -> dict:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # SPEC 3.3: DONE から TODO への直接遷移を禁止
        if row["status"] == "DONE" and payload.status == "TODO":
            raise HTTPException(
                status_code=400, detail="DONEからTODOへ直接戻すことはできません"
            )

        conn.execute(
            "UPDATE tickets SET status = ? WHERE id = ?", (payload.status, ticket_id)
        )
        conn.commit()
        updated = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return dict(updated)


@app.delete("/api/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int) -> None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Ticket not found")
        conn.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
        conn.commit()