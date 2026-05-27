import sqlite3

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from .database import (
    create_user_record,
    delete_user_record,
    get_user_record,
    init_db,
    list_user_records,
    update_user_record,
)

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


init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "User CRUD API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate) -> User:
    try:
        user_id = create_user_record(payload.name, str(payload.email))
    except sqlite3.IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        ) from exc
    return User(id=user_id, **payload.model_dump())


@app.get("/users", response_model=list[User])
def list_users() -> list[User]:
    rows = list_user_records()
    return [User(id=int(row["id"]), name=str(row["name"]), email=str(row["email"])) for row in rows]


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    row = get_user_record(user_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return User(id=int(row["id"]), name=str(row["name"]), email=str(row["email"]))


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, payload: UserUpdate) -> User:
    row = get_user_record(user_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    current_name = str(row["name"])
    current_email = str(row["email"])
    updated_name = payload.name if payload.name is not None else current_name
    updated_email = str(payload.email) if payload.email is not None else current_email

    try:
        updated = update_user_record(user_id, updated_name, updated_email)
    except sqlite3.IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        ) from exc

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return User(id=user_id, name=updated_name, email=updated_email)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> None:
    deleted = delete_user_record(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None
