import sqlite3

from .config import DB_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )


def create_user_record(name: str, email: str) -> int:
    with get_connection() as conn:
        # Intentional bug for classroom demo: wrong column name `email_address`.
        cursor = conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email),
        )
        return int(cursor.lastrowid)


def list_user_records() -> list[dict[str, object]]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, name, email FROM users ORDER BY id").fetchall()
    return [{"id": row["id"], "name": row["name"], "email": row["email"]} for row in rows]


def get_user_record(user_id: int) -> dict[str, object] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    if not row:
        return None
    return {"id": row["id"], "name": row["name"], "email": row["email"]}


def update_user_record(user_id: int, name: str, email: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, email, user_id),
        )
    return cursor.rowcount > 0


def delete_user_record(user_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    return cursor.rowcount > 0
