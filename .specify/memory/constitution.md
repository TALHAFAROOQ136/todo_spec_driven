<!--
Sync Impact Report
- Version change: 1.0.0 → 2.0.0
- Modified principles:
  - II. In-Memory Data Store → II. Persistent Data Store (Neon PostgreSQL)
  - III. Clean Python Architecture → III. Clean Monorepo Architecture
  - IV. Five Core Features (MVP) → IV. Full-Stack Web Features (MVP)
  - V. User-Friendly Console Interface → V. Responsive Web Interface
  - VI. Simplicity & YAGNI → VI. Authentication & User Isolation
  - Added: VII. RESTful API Design
  - Added: VIII. Simplicity & YAGNI
- Added sections: API Endpoints, Monorepo Structure
- Removed sections: Console-specific constraints
- Templates requiring updates: ⚠ pending (Phase 2 update)
- Follow-up TODOs: None
-->

# Todo Full-Stack Web App Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All features MUST be specified before implementation. No code is written manually. The workflow is strictly: Specify → Plan → Tasks → Implement via Claude Code. Every implementation change MUST trace back to a specification artifact. If a spec is missing or ambiguous, the agent MUST stop and request clarification rather than improvise.

### II. Persistent Data Store (Neon PostgreSQL)

All task data MUST be stored in a Neon Serverless PostgreSQL database using SQLModel as the ORM. Data MUST persist across application restarts. Each user's tasks MUST be isolated — users can only see and modify their own tasks. Database connection MUST be configured via environment variable (`DATABASE_URL`). No in-memory-only storage for production data.

### III. Clean Monorepo Architecture

- The project MUST follow a monorepo structure with separate `frontend/` and `backend/` directories.
- **Backend** MUST use Python 3.13+ with FastAPI framework and UV as the package manager.
- **Frontend** MUST use Next.js 16+ with App Router, TypeScript, and Tailwind CSS.
- Each directory MUST have its own `CLAUDE.md` with stack-specific guidelines.
- Root `CLAUDE.md` MUST provide project overview and navigation.
- Code MUST follow respective style guidelines: PEP 8 for Python, ESLint/Prettier for TypeScript.
- Type hints MUST be used in both Python (type annotations) and TypeScript (strict mode).

### IV. Full-Stack Web Features (MVP Scope)

The application MUST implement all 5 Basic Level features as a web application:

1. **Add Task** — Create new todo items with title and description via web form.
2. **View Task List** — Display all tasks for the authenticated user with status indicators.
3. **Update Task** — Modify existing task title or description via web interface.
4. **Delete Task** — Remove a task permanently via web interface.
5. **Mark as Complete** — Toggle task completion status via web interface.

Additionally, the application MUST implement:

6. **User Signup** — New users can create accounts.
7. **User Signin** — Existing users can log in to access their tasks.

No intermediate or advanced features (priorities, tags, search, filters, recurring tasks, due dates) are in scope for Phase 2.

### V. Responsive Web Interface

- The frontend MUST provide a clean, responsive UI built with Tailwind CSS.
- The interface MUST work on desktop and mobile screen sizes.
- User feedback MUST be immediate — loading states, success messages, and error messages.
- Navigation MUST be intuitive with clear call-to-action buttons.
- The UI MUST show task status visually (e.g., strikethrough for completed, checkbox toggle).
- All API calls from frontend MUST go through a centralized API client (`/lib/api.ts`).

### VI. Authentication & User Isolation

- Authentication MUST be implemented using Better Auth on the frontend.
- Better Auth MUST issue JWT tokens upon login.
- Every API request from frontend to backend MUST include the JWT token in the `Authorization: Bearer <token>` header.
- The backend MUST verify JWT tokens using the shared secret (`BETTER_AUTH_SECRET` environment variable).
- All API endpoints MUST enforce user isolation — users can only access their own tasks.
- Requests without a valid token MUST receive `401 Unauthorized`.
- Task ownership MUST be enforced on every operation.

### VII. RESTful API Design

- All backend API routes MUST be under `/api/` prefix.
- API MUST follow RESTful conventions with proper HTTP methods and status codes.
- Request/response bodies MUST use JSON format.
- All request validation MUST use Pydantic models.
- Errors MUST be returned as `HTTPException` with meaningful messages.
- API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

### VIII. Simplicity & YAGNI

- Do not over-engineer. Build only what is specified.
- No abstractions, patterns, or frameworks beyond what the features require.
- Secrets and tokens MUST use environment variables (`.env` files) — never hardcoded.
- If in doubt, choose the simpler approach.

## Technology Constraints

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16+ (App Router), TypeScript, Tailwind CSS |
| Backend | Python 3.13+, FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth (frontend) + JWT verification (backend) |
| Package Manager | UV (backend), npm/pnpm (frontend) |
| AI Development | Claude Code + Spec-Kit Plus |

- Frontend and backend MUST communicate via REST API only.
- Shared secret (`BETTER_AUTH_SECRET`) MUST be consistent across frontend and backend.
- Database connection string MUST be in `DATABASE_URL` environment variable.
- No direct database access from frontend — all data flows through the backend API.

## Monorepo Structure

```text
todo_app1/
├── CLAUDE.md                     # Root Claude Code instructions
├── README.md                     # Project documentation
├── .specify/                     # Spec-Kit Plus config & templates
├── specs/                        # Feature specifications
├── history/                      # Prompt history records
├── frontend/
│   ├── CLAUDE.md                 # Frontend-specific guidelines
│   ├── package.json
│   ├── src/
│   │   ├── app/                  # Next.js pages and layouts
│   │   ├── components/           # Reusable UI components
│   │   └── lib/                  # API client, auth, utilities
│   └── ...
├── backend/
│   ├── CLAUDE.md                 # Backend-specific guidelines
│   ├── pyproject.toml
│   ├── src/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── models.py             # SQLModel database models
│   │   ├── routes/               # API route handlers
│   │   ├── db.py                 # Database connection
│   │   └── auth.py               # JWT verification middleware
│   └── ...
└── docker-compose.yml            # Local development setup (optional)
```

## API Endpoint Contracts

### Authentication Flow

1. User logs in on Frontend → Better Auth creates session and issues JWT token.
2. Frontend makes API call → Includes JWT token in `Authorization: Bearer <token>` header.
3. Backend receives request → Extracts token, verifies signature using shared secret.
4. Backend identifies user → Decodes token to get user ID, matches with URL `{user_id}`.
5. Backend filters data → Returns only tasks belonging to that user.

### Security Requirements

- All endpoints require valid JWT token (except health check).
- Requests without token → `401 Unauthorized`.
- Token with mismatched `user_id` → `403 Forbidden`.
- Task ownership enforced on every CRUD operation.
- JWT tokens MUST have expiry (e.g., 7 days).

## Development Workflow

1. **Specify** — Write feature specification in `specs/` using Spec-Kit Plus templates.
2. **Plan** — Generate architectural plan via `/sp.plan`.
3. **Tasks** — Break plan into atomic, testable tasks via `/sp.tasks`.
4. **Implement** — Execute tasks via Claude Code. No manual coding.
5. **Validate** — Run both frontend and backend, verify all features work correctly.
6. **Record** — Create PHR for every significant interaction.

All code changes MUST be committed to Git with meaningful commit messages. The repository MUST contain:
- Constitution file (this document)
- `specs/` folder with all specification files
- `history/` folder with prompt history records
- `frontend/` folder with Next.js source code
- `backend/` folder with FastAPI source code
- `README.md` with comprehensive documentation
- `CLAUDE.md` files (root, frontend, backend)

## Governance

- This constitution is the highest authority for Phase 2 development decisions.
- All specifications, plans, and tasks MUST comply with these principles.
- Amendments require explicit user approval and version increment.
- When conflicts arise, the hierarchy is: Constitution > Specify > Plan > Tasks.
- Any architecturally significant decision MUST be surfaced for ADR consideration before implementation.
- Phase 1 (console app) code in `src/` is preserved for reference but NOT used in Phase 2.

**Version**: 2.0.0 | **Ratified**: 2026-02-15 | **Last Amended**: 2026-02-15
