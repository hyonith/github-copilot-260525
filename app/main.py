import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="User CRUD API", version="1.0.0")


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class User(UserBase):
    id: int


DB_PATH = Path(__file__).resolve().parent / "users.db"


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


init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate) -> User:
    with get_connection() as conn:
        try:
            # Intentional bug for classroom demo: wrong column name `email_address`.
            cursor = conn.execute(
                "INSERT INTO users (name, email_address) VALUES (?, ?)",
                (payload.name, payload.email),
            )
            user_id = int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            ) from exc
    return User(id=user_id, **payload.model_dump())


@app.get("/users", response_model=list[User])
def list_users() -> list[User]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, name, email FROM users ORDER BY id").fetchall()
    return [User(id=row["id"], name=row["name"], email=row["email"]) for row in rows]


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return User(id=row["id"], name=row["name"], email=row["email"])


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, payload: UserUpdate) -> User:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        current_name = row["name"]
        current_email = row["email"]
        updated_name = payload.name if payload.name is not None else current_name
        updated_email = payload.email if payload.email is not None else current_email

        try:
            conn.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (updated_name, updated_email, user_id),
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            ) from exc

    return User(id=user_id, name=updated_name, email=updated_email)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> None:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None
