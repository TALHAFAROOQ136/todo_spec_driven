# Implementation Plan: Full-Stack Web Todo App

**Branch**: `002-fullstack-web-app` | **Date**: 2026-02-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-fullstack-web-app/spec.md`

## Summary

Evolve the Phase 1 console todo app into a full-stack web application with user authentication, persistent database storage, RESTful API, and responsive web interface. The backend uses Python 3.13+ with FastAPI and SQLModel connected to Neon Serverless PostgreSQL. The frontend uses Next.js 16 (App Router) with TypeScript and Tailwind CSS. Authentication is handled by Better Auth (frontend) issuing JWT tokens, verified by PyJWT on the backend. The monorepo contains separate `frontend/` and `backend/` directories with independent toolchains.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, PyJWT, asyncpg, uvicorn (backend); Next.js 16, Better Auth 1.x, Tailwind CSS (frontend)
**Storage**: Neon Serverless PostgreSQL via SQLModel async + asyncpg driver
**Testing**: pytest + httpx (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web browsers (desktop + mobile), deployed as two services
**Project Type**: Web application (monorepo with frontend + backend)
**Performance Goals**: API responses <200ms p95. UI toggle completion <1s. Signup flow <30s. Task creation <10s.
**Constraints**: JWT tokens expire after 7 days. Task title max 200 chars. Description max 1000 chars. No offline mode. No pagination (assumes <100 tasks per user).
**Scale/Scope**: Multi-user (each user isolated). Typical user <100 tasks. No concurrent editing concerns.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Spec completed (7 user stories, 15 FRs, 8 SCs). All features trace to spec. |
| II. Persistent Data Store (Neon PostgreSQL) | PASS | Neon PostgreSQL with SQLModel ORM. `DATABASE_URL` env var. User isolation enforced. |
| III. Clean Monorepo Architecture | PASS | `frontend/` (Next.js 16 + TS + Tailwind) and `backend/` (Python 3.13+ + FastAPI + UV). Each with own CLAUDE.md. |
| IV. Full-Stack Web Features (MVP) | PASS | 5 CRUD operations + signup + signin. No extras (no priorities, tags, search, filters). |
| V. Responsive Web Interface | PASS | Tailwind CSS. Desktop + mobile. Loading states, success/error messages, visual status indicators. |
| VI. Authentication & User Isolation | PASS | Better Auth (frontend) + JWT verification via PyJWT (backend). Bearer token on all requests. User isolation on every operation. |
| VII. RESTful API Design | PASS | `/api/` prefix. RESTful conventions. Pydantic/SQLModel validation. HTTPException errors. 6 endpoints defined. |
| VIII. Simplicity & YAGNI | PASS | No extra abstractions. Env vars for secrets. Smallest viable diff. |

**Gate Result**: ALL PASS. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web-app/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI spec)
│   └── api.yaml         # REST API contract
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── CLAUDE.md                  # Backend-specific guidelines
├── pyproject.toml             # UV project config (FastAPI, SQLModel, PyJWT, asyncpg, uvicorn)
├── .env.example               # DATABASE_URL, BETTER_AUTH_SECRET template
├── alembic.ini                # Alembic migration config
├── migrations/
│   ├── env.py                 # Alembic env (imports SQLModel metadata)
│   └── versions/              # Auto-generated migration scripts
└── src/
    └── todo_api/
        ├── __init__.py        # Package marker
        ├── main.py            # FastAPI app, CORS, lifespan (create tables)
        ├── config.py          # Settings from env vars (DATABASE_URL, BETTER_AUTH_SECRET)
        ├── db.py              # Async engine, session factory, get_session dependency
        ├── auth.py            # JWT verification dependency (PyJWT + Bearer token)
        ├── models.py          # SQLModel models (User table not needed — auth is frontend-only; Task table)
        └── routes/
            ├── __init__.py
            └── tasks.py       # CRUD endpoints for tasks

frontend/
├── CLAUDE.md                  # Frontend-specific guidelines
├── package.json               # Next.js 16, Better Auth, Tailwind CSS
├── next.config.ts             # Next.js configuration
├── tailwind.config.ts         # Tailwind configuration
├── tsconfig.json              # TypeScript strict mode
├── .env.example               # BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL template
├── src/
│   ├── app/
│   │   ├── layout.tsx         # Root layout (global styles, providers)
│   │   ├── page.tsx           # Landing page (redirect to signin or dashboard)
│   │   ├── signin/
│   │   │   └── page.tsx       # Signin form
│   │   ├── signup/
│   │   │   └── page.tsx       # Signup form
│   │   ├── dashboard/
│   │   │   └── page.tsx       # Task list + CRUD operations (protected)
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/
│   │               └── route.ts  # Better Auth API route handler
│   ├── components/
│   │   ├── task-list.tsx      # Renders list of tasks
│   │   ├── task-item.tsx      # Single task with toggle, edit, delete
│   │   ├── task-form.tsx      # Add/edit task form
│   │   ├── auth-form.tsx      # Shared signin/signup form
│   │   └── empty-state.tsx    # "No tasks yet" message
│   └── lib/
│       ├── auth.ts            # Better Auth client instance + JWT plugin config
│       ├── auth-client.ts     # Better Auth client for components
│       └── api.ts             # Centralized API client (fetch wrapper with Bearer token)
└── proxy.ts                   # Next.js 16 proxy (protected route middleware)
```

**Structure Decision**: Web application monorepo with separate `frontend/` and `backend/` directories, matching the constitution's mandated structure. The backend follows a flat module layout under `src/todo_api/` with a `routes/` subfolder — minimal separation without over-engineering. The frontend follows Next.js 16 App Router conventions with `app/`, `components/`, and `lib/` directories. Better Auth handles user management entirely on the frontend side (users table managed by Better Auth's database adapter), so the backend only needs a `Task` model and JWT verification middleware.

## Key Design Decisions

### 1. Better Auth manages users, backend only stores tasks

Better Auth manages user registration, login, sessions, and JWT issuance entirely on the frontend. The backend does **not** have a users table — it only receives and verifies JWT tokens to extract `user_id`, then uses that to scope task queries. This avoids duplicating user management across two systems.

### 2. JWT with HS256 shared secret

The constitution mandates a shared secret (`BETTER_AUTH_SECRET`). Better Auth's JWT plugin will be configured to use HS256 with this secret. The backend verifies tokens using PyJWT with the same secret. This is the simplest approach that satisfies the constitution's requirements.

### 3. Async database access

SQLModel with `asyncpg` driver and `AsyncSession` for non-blocking database operations. Connection pooling configured with `pool_pre_ping=True` and `pool_recycle=300` to handle Neon's serverless connection lifecycle.

### 4. No Alembic for initial deployment

For the initial schema, use SQLModel's `create_all()` at startup. Alembic is included in the project structure for future migrations but not required for Phase 2's initial deployment. This follows YAGNI — we add migration tooling when we need schema changes.

### 5. Better Auth database adapter

Better Auth needs its own database to store user accounts and sessions. It will use the same Neon PostgreSQL database (via its built-in PostgreSQL adapter), keeping infrastructure simple. Better Auth manages its own tables (user, session, account, verification).

## Constitution Re-Check (Post-Design)

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | All design traces to spec FRs. No extras added. |
| II. Persistent Data Store | PASS | Neon PostgreSQL via SQLModel async. `DATABASE_URL` env var. |
| III. Clean Monorepo | PASS | `frontend/` + `backend/` with own CLAUDE.md files. Correct toolchains. |
| IV. Full-Stack Features | PASS | 7 user stories mapped to routes + components. No scope creep. |
| V. Responsive Web Interface | PASS | Tailwind CSS. Components for all UI states. |
| VI. Authentication & User Isolation | PASS | Better Auth + JWT + PyJWT. Bearer token. User isolation via `user_id` in all queries. |
| VII. RESTful API Design | PASS | 6 endpoints under `/api/`. Pydantic validation. HTTPException. |
| VIII. Simplicity & YAGNI | PASS | Flat module structure. No repository pattern. No Alembic migrations initially. |

**Post-Design Gate Result**: ALL PASS.

## Complexity Tracking

No constitution violations. No complexity justifications needed.
