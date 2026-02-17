# Quickstart: Full-Stack Web Todo App

**Feature**: 002-fullstack-web-app
**Date**: 2026-02-17

## Prerequisites

- Python 3.13+
- Node.js 20+ (LTS)
- UV (Python package manager): `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- npm or pnpm (Node package manager)
- Neon PostgreSQL account (https://neon.tech — free tier available)
- Git

## Environment Setup

### 1. Clone and checkout feature branch

```bash
git checkout 002-fullstack-web-app
```

### 2. Create Neon database

1. Sign up at https://console.neon.tech
2. Create a new project (e.g., "todo-app")
3. Copy the connection string from the dashboard

### 3. Configure environment variables

**Backend** (`backend/.env`):
```env
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxxxx.neon.tech/dbname?ssl=require
BETTER_AUTH_SECRET=your-shared-secret-at-least-32-chars
CORS_ORIGINS=http://localhost:3000
```

**Frontend** (`frontend/.env.local`):
```env
BETTER_AUTH_SECRET=your-shared-secret-at-least-32-chars
DATABASE_URL=postgresql://user:password@ep-xxxxx.neon.tech/dbname?sslmode=require
NEXT_PUBLIC_API_URL=http://localhost:8000
```

> The `BETTER_AUTH_SECRET` must be identical in both backend and frontend.
> The frontend `DATABASE_URL` uses `postgresql://` (for Better Auth's adapter).
> The backend `DATABASE_URL` uses `postgresql+asyncpg://` (for SQLModel async).

### 4. Install backend dependencies

```bash
cd backend
uv sync
```

### 5. Install frontend dependencies

```bash
cd frontend
npm install
```

## Running the Application

### Start backend (terminal 1)

```bash
cd backend
uv run uvicorn todo_api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### Start frontend (terminal 2)

```bash
cd frontend
npm run dev
```

The web app will be available at `http://localhost:3000`.

## Verifying the Setup

1. Open `http://localhost:3000` — you should see the signin page
2. Click "Sign up" — create an account
3. After signup, you should be redirected to the dashboard
4. Try adding a task — it should appear in the list
5. Check `http://localhost:8000/docs` — you should see the OpenAPI documentation

## Project Structure

```
todo_app1/
├── backend/           # Python FastAPI backend
│   ├── src/todo_api/  # Application source
│   ├── pyproject.toml # UV config + dependencies
│   └── .env           # Environment variables (not committed)
├── frontend/          # Next.js 16 frontend
│   ├── src/           # Application source
│   ├── package.json   # npm config + dependencies
│   └── .env.local     # Environment variables (not committed)
└── specs/             # Design artifacts
```

## Key Dependencies

### Backend
| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `sqlmodel` | ORM (SQLAlchemy + Pydantic) |
| `asyncpg` | Async PostgreSQL driver |
| `pyjwt` | JWT token verification |

### Frontend
| Package | Purpose |
|---------|---------|
| `next` | React framework (v16+) |
| `better-auth` | Authentication (signup, signin, JWT) |
| `tailwindcss` | Utility-first CSS framework |
| `typescript` | Type-safe JavaScript |

## Common Issues

**"Connection refused" on backend**: Ensure the backend is running on port 8000 and CORS_ORIGINS includes `http://localhost:3000`.

**"Invalid token" errors**: Ensure `BETTER_AUTH_SECRET` is identical in both `.env` files.

**Database connection errors**: Ensure `DATABASE_URL` uses `?ssl=require` suffix and the Neon database is active.

**Tables not created**: The backend creates tables on startup via `create_all()`. Check the backend logs for SQLAlchemy errors.
