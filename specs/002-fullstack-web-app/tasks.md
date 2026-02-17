# Tasks: Full-Stack Web Todo App

**Input**: Design documents from `/specs/002-fullstack-web-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api.yaml

**Tests**: Not explicitly requested in the feature specification. Test tasks are excluded.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize backend and frontend projects with correct dependencies and configuration files

- [x] T001 Create backend project structure with `backend/pyproject.toml` using UV (fastapi, sqlmodel, pyjwt, asyncpg, uvicorn, python-dotenv dependencies)
- [x] T002 Create backend package layout: `backend/src/todo_api/__init__.py` and `backend/src/todo_api/routes/__init__.py`
- [x] T003 [P] Create `backend/.env.example` with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS placeholders
- [x] T004 [P] Create `frontend/package.json` with Next.js 16, better-auth, tailwindcss, typescript dependencies and initialize with `npm install`
- [x] T005 [P] Create `frontend/tsconfig.json` with TypeScript strict mode configuration
- [x] T006 [P] Create `frontend/next.config.ts` with Next.js 16 configuration
- [x] T007 [P] Create `frontend/tailwind.config.ts` and `frontend/src/app/globals.css` with Tailwind CSS setup
- [x] T008 [P] Create `frontend/.env.example` with BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL placeholders
- [x] T009 [P] Create `backend/CLAUDE.md` with backend-specific development guidelines
- [x] T010 [P] Create `frontend/CLAUDE.md` with frontend-specific development guidelines

**Checkpoint**: Both projects initialized with dependencies installable via `uv sync` and `npm install`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Implement backend config module loading env vars (DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS) in `backend/src/todo_api/config.py`
- [x] T012 Implement async database engine and session factory with Neon-compatible pool settings (pool_pre_ping, pool_recycle=300) in `backend/src/todo_api/db.py`
- [x] T013 Implement Task SQLModel table model (id uuid PK, title, description, completed, user_id indexed, created_at, updated_at) in `backend/src/todo_api/models.py`
- [x] T014 Implement Pydantic request/response schemas (TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, MessageResponse) in `backend/src/todo_api/models.py`
- [x] T015 Implement JWT verification dependency using PyJWT with HS256 and HTTPBearer in `backend/src/todo_api/auth.py`
- [x] T016 Implement FastAPI app with CORS middleware, lifespan (create_all tables on startup), and router includes in `backend/src/todo_api/main.py`
- [x] T017 [P] Configure Better Auth server instance with JWT plugin (HS256, JWKS disabled) and PostgreSQL adapter in `frontend/src/lib/auth.ts`
- [x] T018 [P] Configure Better Auth client instance for frontend components in `frontend/src/lib/auth-client.ts`
- [x] T019 [P] Implement centralized API client (fetch wrapper attaching Bearer token from Better Auth session) in `frontend/src/lib/api.ts`
- [x] T020 Create Better Auth API route handler (catch-all) in `frontend/src/app/api/auth/[...all]/route.ts`
- [x] T021 Create root layout with global styles and providers in `frontend/src/app/layout.tsx`
- [x] T022 Implement proxy (Next.js 16 middleware) for route protection — redirect unauthenticated users to /signin in `frontend/proxy.ts`

**Checkpoint**: Foundation ready — backend starts with tables created, frontend serves pages with auth infrastructure. User story implementation can now begin.

---

## Phase 3: User Story 1 — User Signup (Priority: P1) 🎯 MVP

**Goal**: New users can create an account with name, email, password and be redirected to the dashboard

**Independent Test**: Navigate to /signup, fill in name/email/password, submit, verify redirect to /dashboard with empty task list

### Implementation for User Story 1

- [x] T023 [P] [US1] Create shared auth form component (name, email, password fields with validation) in `frontend/src/components/auth-form.tsx`
- [x] T024 [US1] Create signup page using auth-form with Better Auth signUp.email call, error handling (duplicate email, validation), and redirect to /dashboard in `frontend/src/app/signup/page.tsx`
- [x] T025 [US1] Create landing page that redirects authenticated users to /dashboard, unauthenticated to /signin in `frontend/src/app/page.tsx`

**Checkpoint**: User Story 1 fully functional — new users can sign up and reach the dashboard

---

## Phase 4: User Story 2 — User Signin (Priority: P1)

**Goal**: Returning users can sign in with email/password and be redirected to their dashboard

**Independent Test**: Create account (US1), sign out, navigate to /signin, enter credentials, verify redirect to /dashboard

### Implementation for User Story 2

- [x] T026 [US2] Create signin page using auth-form with Better Auth signIn.email call, error handling (invalid credentials), and redirect to /dashboard in `frontend/src/app/signin/page.tsx`
- [x] T027 [US2] Add sign-out functionality (Better Auth signOut call, redirect to /signin) accessible from the dashboard layout in `frontend/src/app/dashboard/page.tsx` (initial scaffold with sign-out button)

**Checkpoint**: User Story 2 fully functional — users can sign in, reach dashboard, and sign out

---

## Phase 5: User Story 3 — Add Task (Priority: P2)

**Goal**: Authenticated users can create tasks with title (required) and description (optional) via the dashboard

**Independent Test**: Sign in, click "Add Task", fill in title + description, submit, verify task appears in list with "incomplete" status

### Implementation for User Story 3

- [x] T028 [US3] Implement POST /api/{user_id}/tasks endpoint — create task with title/description, validate input, assign user_id from JWT, return 201 with TaskResponse in `backend/src/todo_api/routes/tasks.py`
- [x] T029 [US3] Create task form component (title required input, optional description textarea, submit/cancel, validation errors, success message) in `frontend/src/components/task-form.tsx`
- [x] T030 [US3] Integrate task-form into dashboard page with "Add Task" button toggle and API call via `lib/api.ts` in `frontend/src/app/dashboard/page.tsx`

**Checkpoint**: User Story 3 fully functional — tasks can be created and are persisted to the database

---

## Phase 6: User Story 4 — View Task List (Priority: P2)

**Goal**: Authenticated users see all their tasks on the dashboard with title, description, and completion status; user isolation enforced

**Independent Test**: Sign in with pre-existing tasks, verify all tasks displayed with correct status indicators; sign in as different user, verify only their tasks visible

### Implementation for User Story 4

- [x] T031 [US4] Implement GET /api/{user_id}/tasks endpoint — return all tasks for authenticated user filtered by user_id, return TaskListResponse in `backend/src/todo_api/routes/tasks.py`
- [x] T032 [P] [US4] Create empty-state component ("No tasks yet. Add your first task!") in `frontend/src/components/empty-state.tsx`
- [x] T033 [P] [US4] Create task-item component (display title, description, completed status with visual indicator — checkbox/strikethrough) in `frontend/src/components/task-item.tsx`
- [x] T034 [US4] Create task-list component (renders array of task-items or empty-state) in `frontend/src/components/task-list.tsx`
- [x] T035 [US4] Integrate task-list into dashboard page — fetch tasks on load via GET /api/{user_id}/tasks, pass to task-list, refresh after add in `frontend/src/app/dashboard/page.tsx`

**Checkpoint**: User Story 4 fully functional — dashboard displays all user tasks with correct status, empty state shown when no tasks

---

## Phase 7: User Story 5 — Mark Task as Complete/Incomplete (Priority: P3)

**Goal**: Users can toggle task completion status via a checkbox/toggle; UI updates immediately and persists

**Independent Test**: Sign in, view incomplete task, click toggle, verify visual change (strikethrough/checked), refresh page, verify persistence

### Implementation for User Story 5

- [x] T036 [US5] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint — toggle completed boolean, verify task ownership, return updated TaskResponse in `backend/src/todo_api/routes/tasks.py`
- [x] T037 [US5] Add toggle completion handler to task-item component — call PATCH endpoint via api.ts, update UI optimistically in `frontend/src/components/task-item.tsx`

**Checkpoint**: User Story 5 fully functional — completion toggle works, persists across refreshes

---

## Phase 8: User Story 6 — Update Task (Priority: P3)

**Goal**: Users can edit task title and description via an inline edit mode; changes persist

**Independent Test**: Sign in, click edit on a task, modify title/description, save, verify changes displayed; click edit then cancel, verify no changes

### Implementation for User Story 6

- [x] T038 [US6] Implement PUT /api/{user_id}/tasks/{task_id} endpoint — update title/description, validate input, verify ownership, return updated TaskResponse in `backend/src/todo_api/routes/tasks.py`
- [x] T039 [US6] Add edit mode to task-item component — toggle between display/edit views, reuse task-form for editing, call PUT endpoint, handle cancel/save in `frontend/src/components/task-item.tsx`

**Checkpoint**: User Story 6 fully functional — tasks can be edited and changes persist

---

## Phase 9: User Story 7 — Delete Task (Priority: P3)

**Goal**: Users can delete tasks with confirmation; task permanently removed from list and database

**Independent Test**: Sign in, click delete on a task, confirm, verify task removed; click delete then cancel, verify task remains; delete last task, verify empty state appears

### Implementation for User Story 7

- [x] T040 [US7] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint — verify ownership, delete task, return MessageResponse in `backend/src/todo_api/routes/tasks.py`
- [x] T041 [US7] Add delete handler to task-item component with confirmation dialog (confirm/cancel), call DELETE endpoint, remove from list in `frontend/src/components/task-item.tsx`

**Checkpoint**: User Story 7 fully functional — tasks can be deleted with confirmation, empty state shows when last task deleted

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T042 [P] Add responsive design refinements (mobile 375px to desktop 1920px) across all components using Tailwind breakpoints in `frontend/src/components/*.tsx`
- [x] T043 [P] Add loading states and error boundaries for API calls (spinner during fetch, error message on failure) in `frontend/src/app/dashboard/page.tsx`
- [x] T044 [P] Handle token expiration gracefully — redirect to /signin with "Session expired" message in `frontend/src/lib/api.ts` and `frontend/proxy.ts`
- [ ] T045 Validate full quickstart.md flow end-to-end (setup → signup → add task → view → toggle → edit → delete → signout → signin)
- [x] T046 [P] Add GET /api/{user_id}/tasks/{task_id} endpoint for single task retrieval (contract completeness) in `backend/src/todo_api/routes/tasks.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **US1 Signup (Phase 3)**: Depends on Phase 2
- **US2 Signin (Phase 4)**: Depends on Phase 2 (can parallel with US1)
- **US3 Add Task (Phase 5)**: Depends on Phase 2 (needs auth working from US1/US2 for manual testing)
- **US4 View Task List (Phase 6)**: Depends on Phase 2 (needs US3 for meaningful testing)
- **US5 Toggle Complete (Phase 7)**: Depends on Phase 2 (needs US4 for task display)
- **US6 Update Task (Phase 8)**: Depends on Phase 2 (needs US4 for task display)
- **US7 Delete Task (Phase 9)**: Depends on Phase 2 (needs US4 for task display)
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Signup)** + **US2 (Signin)**: Both P1, can be built in parallel after Phase 2. Auth infrastructure is shared in Phase 2.
- **US3 (Add Task)** + **US4 (View List)**: Both P2, can be built in parallel. US4 is more meaningful to test after US3 provides data.
- **US5 (Toggle)**, **US6 (Update)**, **US7 (Delete)**: All P3, can be built in parallel — each modifies `task-item.tsx` but different concerns.

### Within Each User Story

- Backend endpoint before frontend integration
- Models/schemas (Phase 2) before route handlers
- Components before page integration

### Parallel Opportunities

- **Phase 1**: T003–T010 all [P] — can run in parallel
- **Phase 2**: T017–T019 [P] — frontend lib files independent; T020–T022 can follow
- **Phase 3+4**: US1 and US2 can be built in parallel (different pages)
- **Phase 5+6**: T032, T033 [P] — empty-state and task-item are independent components
- **Phase 7+8+9**: US5, US6, US7 add different capabilities to task-item — can be sequenced within same component

---

## Parallel Example: Phase 2 Foundation

```bash
# These can run in parallel (different files):
Task T017: "Better Auth server config in frontend/src/lib/auth.ts"
Task T018: "Better Auth client config in frontend/src/lib/auth-client.ts"
Task T019: "API client wrapper in frontend/src/lib/api.ts"

# These must be sequential (dependency chain):
Task T011 → T012 → T013 → T014 → T015 → T016 (backend foundation chain)
```

## Parallel Example: User Stories 1 & 2

```bash
# After Phase 2, both auth stories can proceed in parallel:
Team A: T023 → T024 → T025 (Signup flow)
Team B: T026 → T027 (Signin flow)
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: US1 Signup
4. Complete Phase 4: US2 Signin
5. **STOP and VALIDATE**: Users can register, sign in, sign out, reach empty dashboard

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 + US2 → Auth works → **Deploy/Demo** (MVP auth)
3. US3 + US4 → Tasks can be created and viewed → **Deploy/Demo** (MVP tasks)
4. US5 + US6 + US7 → Full CRUD → **Deploy/Demo** (Feature complete)
5. Polish → Production-ready

### Suggested MVP Scope

**MVP = Phase 1 + Phase 2 + Phase 3 + Phase 4** (Setup + Foundation + Signup + Signin)
This gives a working authenticated app shell. Add US3+US4 for a usable todo app.

---

## Summary

| Metric | Value |
|--------|-------|
| **Total tasks** | 46 |
| **Phase 1 (Setup)** | 10 tasks |
| **Phase 2 (Foundation)** | 12 tasks |
| **US1 (Signup)** | 3 tasks |
| **US2 (Signin)** | 2 tasks |
| **US3 (Add Task)** | 3 tasks |
| **US4 (View List)** | 5 tasks |
| **US5 (Toggle)** | 2 tasks |
| **US6 (Update)** | 2 tasks |
| **US7 (Delete)** | 2 tasks |
| **Polish** | 5 tasks |
| **Parallel [P] tasks** | 18 tasks |

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable after Phase 2
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Backend endpoints defined in contracts/api.yaml — follow schemas exactly
- All task queries MUST include user_id in WHERE clause (data isolation)
