# Todo Full-Stack Web App — Phase 2

A multi-user full-stack todo application built with Next.js, FastAPI, SQLModel, and Neon Serverless PostgreSQL using Spec-Driven Development with Claude Code and Spec-Kit Plus.

## Features

- **Add Task** — Create tasks with title and optional description via web form
- **View Tasks** — Display all tasks for the authenticated user with status indicators
- **Update Task** — Modify task title and description inline
- **Delete Task** — Remove a task permanently with confirmation
- **Mark Complete** — Toggle task completion status via checkbox
- **User Signup** — Create a new account with name, email, and password
- **User Signin** — Log in to access your tasks

All data is stored in Neon Serverless PostgreSQL. Each user's tasks are fully isolated.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 (App Router), TypeScript, Tailwind CSS |
| Backend | Python 3.13+, FastAPI, SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth (frontend) + JWT/EdDSA verification (backend) |
| Package Manager | UV (backend), npm (frontend) |

## Prerequisites

- Python 3.13+ with [UV](https://docs.astral.sh/uv/)
- Node.js 18+
- A [Neon](https://neon.tech) PostgreSQL database

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd todo_app1
```

### 2. Configure environment variables

**Backend** — create `backend/.env`:
```env
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>/<database>?ssl=require
BETTER_AUTH_SECRET=<your-secret>
CORS_ORIGINS=http://localhost:3000
```

**Frontend** — create `frontend/.env.local`:
```env
DATABASE_URL=postgresql://<user>:<password>@<host>/<database>?sslmode=require
BETTER_AUTH_SECRET=<your-secret>
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:3000
```

> `BETTER_AUTH_SECRET` must be the same in both files.

### 3. Install dependencies

```bash
# Backend
cd backend
uv sync

# Frontend
cd ../frontend
npm install
```

### 4. Run database migrations

Better Auth tables are created automatically on first run. Backend tables are created via SQLModel on startup.

### 5. Start the servers

```bash
# Terminal 1 — Backend (port 8000)
cd backend
uv run uvicorn todo_api.main:app --reload --port 8000

# Terminal 2 — Frontend (port 3000)
cd frontend
npm run dev
```

Open http://localhost:3000 in your browser.

## API Endpoints

All endpoints require a valid JWT token in the `Authorization: Bearer <token>` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## Project Structure

```
todo_app1/
├── CLAUDE.md                        # Root Claude Code instructions
├── README.md                        # This file
├── .specify/                        # Spec-Kit Plus config & templates
├── specs/002-fullstack-web-app/     # Feature specifications
├── history/prompts/                 # Prompt history records
├── frontend/
│   ├── CLAUDE.md                    # Frontend guidelines
│   ├── package.json
│   ├── middleware.ts                # Route protection
│   └── src/
│       ├── app/                     # Pages (signin, signup, dashboard)
│       ├── components/              # UI components (task-form, task-item, etc.)
│       └── lib/                     # API client, auth config
├── backend/
│   ├── CLAUDE.md                    # Backend guidelines
│   ├── pyproject.toml
│   └── src/todo_api/
│       ├── main.py                  # FastAPI app with CORS and lifespan
│       ├── config.py                # Environment variable loading
│       ├── db.py                    # Async database engine
│       ├── auth.py                  # JWT verification via JWKS
│       ├── models.py                # Task model + Pydantic schemas
│       └── routes/tasks.py          # CRUD endpoints
└── src/                             # Phase 1 console app (preserved)
```

## Authentication Flow

1. User signs up/in on the frontend via Better Auth
2. Better Auth issues a JWT token (EdDSA algorithm)
3. Frontend includes the token in every API request as `Authorization: Bearer <token>`
4. Backend fetches the public key from `/api/auth/jwks` and verifies the token
5. Backend extracts `user_id` from the token and enforces data isolation

## Development Approach

This project was built using **Spec-Driven Development (SDD)**:

1. **Constitution** — Defined principles and constraints (`.specify/memory/constitution.md`)
2. **Specification** — Feature requirements with acceptance criteria (`specs/002-fullstack-web-app/spec.md`)
3. **Plan** — Architecture decisions and tech stack (`specs/002-fullstack-web-app/plan.md`)
4. **Tasks** — Atomic implementation tasks (`specs/002-fullstack-web-app/tasks.md`)
5. **Implementation** — Code generated by Claude Code following the task plan

All spec artifacts are in the `specs/` directory. Prompt history records are in `history/prompts/`.
