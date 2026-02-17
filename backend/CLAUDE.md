# Backend — FastAPI Todo API

## Tech Stack
- Python 3.13+, FastAPI, SQLModel, PyJWT, asyncpg, uvicorn
- Package manager: UV (`uv sync` to install)

## Run
```bash
cd backend
uv run uvicorn todo_api.main:app --reload --port 8000
```

## Structure
- `src/todo_api/main.py` — App entrypoint with CORS and lifespan
- `src/todo_api/config.py` — Settings from env vars
- `src/todo_api/db.py` — Async engine + session factory
- `src/todo_api/auth.py` — JWT verification dependency
- `src/todo_api/models.py` — SQLModel Task table + Pydantic schemas
- `src/todo_api/routes/tasks.py` — CRUD endpoints

## Rules
- All task queries MUST filter by `user_id` (data isolation)
- JWT verified via PyJWT with HS256 using `BETTER_AUTH_SECRET`
- Use `AsyncSession` for all DB operations
- Env vars loaded from `.env` via python-dotenv
