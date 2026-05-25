# Drill Order System (SQLite User CRUD)

This module is intentionally broken for classroom debugging practice.

## Debugging Scenarios (Error Descriptions)
The following error scenarios are the intended classroom debugging topics for this module.

1. Missing config key leads to startup crash
- Category: configuration error
- Typical symptom: KeyError during DB connection setup
- Example: code tries to read SQLITE_PATH but config does not define it
- Related files: config.py, database.py

2. Blocking call inside async flow freezes the event loop
- Category: async runtime error
- Typical symptom: app appears to hang, tasks do not progress smoothly
- Example: using time.sleep() in async code instead of await asyncio.sleep()
- Related file: main.py

3. SQL/schema mismatch causes runtime DB failure
- Category: query/schema inconsistency
- Typical symptom: request fails at runtime with sqlite operational error
- Example: insert/update references a non-existing column name
- Related files: database.py, main.py

These errors are always active in code (no scenario switch).

## Structure
- `config.py`: SQLite file path configuration
- `database.py`: SQL operations and table initialization
- `main.py`: FastAPI endpoints
- Database file: `drill_order_system/user.db`

## Run
From project root:

```bash
uvicorn drill_order_system.main:app --reload
```

Expected behavior:
- API requests feel blocked because middleware uses `time.sleep()`.
- User operations that access DB path fail with `KeyError: 'SQLITE_PATH'`.
- Create user fails with SQL mismatch (`email_address` column does not exist).

Open API docs:
- `http://127.0.0.1:8000/docs`

## Endpoints
- `GET /health`
- `POST /users`
- `GET /users`
- `GET /users/{user_id}`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

## Example
Create user:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'
```
