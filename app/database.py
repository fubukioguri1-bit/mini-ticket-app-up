import sqlite3
from pathlib import Path

DB_PATH = Path("tickets.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                assignee TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'TODO',
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()