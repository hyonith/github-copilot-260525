# Python User CRUD API

A simple FastAPI project that provides CRUD endpoints for user data.

## Features
- Create a user
- List users
- Get user by ID
- Update user
- Delete user

## Project Structure
- `app/main.py`: FastAPI application and CRUD endpoints
- `requirements.txt`: Python dependencies

## Quick Start
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the API:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints
- `GET /health`
- `POST /users`
- `GET /users`
- `GET /users/{user_id}`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

## Example Request
Create user:
```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Jerry","email":"jerry@example.com"}'
```

Interactive docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
