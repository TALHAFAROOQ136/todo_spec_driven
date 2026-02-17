# Data Model: Full-Stack Web Todo App

**Feature**: 002-fullstack-web-app
**Date**: 2026-02-17

## Entities

### Task (Backend — SQLModel)

The primary application entity. Stored in Neon PostgreSQL, managed by the FastAPI backend.

| Field | Type | Constraints | Source |
|-------|------|-------------|--------|
| `id` | `uuid` (UUID v4) | Primary key, auto-generated | — |
| `title` | `str` | Required, max 200 chars | FR-004, FR-013 |
| `description` | `str` | Optional (default empty), max 1000 chars | FR-004, FR-013 |
| `completed` | `bool` | Default `False` | FR-006 |
| `user_id` | `str` | Required, indexed. Extracted from JWT. | FR-009 |
| `created_at` | `datetime` | Auto-set on creation (UTC) | Spec: Key Entities |
| `updated_at` | `datetime` | Auto-set on creation and update (UTC) | Spec: Key Entities |

**Table name**: `task`

**Indexes**:
- Primary key on `id`
- Index on `user_id` (all queries filter by user)

**SQLModel definition sketch**:
```python
import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime

class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )
```

### User (Frontend — Better Auth managed)

Managed entirely by Better Auth. The backend does **not** define or interact with this table. Better Auth creates and manages these tables automatically via its PostgreSQL adapter.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` | Better Auth auto-generated ID |
| `name` | `str` | User's display name |
| `email` | `str` | Unique, used for login |
| `emailVerified` | `bool` | Managed by Better Auth |
| `image` | `str` | Optional avatar URL |
| `createdAt` | `datetime` | Auto-set by Better Auth |
| `updatedAt` | `datetime` | Auto-set by Better Auth |

**Additional Better Auth tables** (auto-managed):
- `session` — Active user sessions
- `account` — Authentication provider accounts
- `verification` — Email/token verification records

## Validation Rules

### Task creation (POST)
- `title`: Required. Must be 1-200 characters. Trimmed of whitespace.
- `description`: Optional. Max 1000 characters if provided.

### Task update (PUT)
- `title`: Required. Must be 1-200 characters. Trimmed of whitespace.
- `description`: Optional. Max 1000 characters if provided.
- `completed` status is NOT changed via update — use the toggle endpoint.

### User signup
- `name`: Required. Non-empty.
- `email`: Required. Valid email format. Unique across users.
- `password`: Required. Minimum 8 characters.

## Pydantic Request/Response Models (Backend)

```python
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

# --- Request Models ---

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)

class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)

# --- Response Models ---

class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]

class MessageResponse(BaseModel):
    message: str
```

## State Transitions

### Task completion status
```
incomplete (default) ──PATCH /complete──▶ complete
complete ──PATCH /complete──▶ incomplete
```
Toggle operation: flips `completed` between `True` and `False`.

### User authentication state
```
anonymous ──signup──▶ authenticated (redirected to dashboard)
anonymous ──signin──▶ authenticated (redirected to dashboard)
authenticated ──signout──▶ anonymous (redirected to signin)
authenticated ──token expires──▶ anonymous (redirected to signin with message)
```

## Relationships

```
User (Better Auth) 1──────* Task (Backend)
  │                          │
  └── user.id (JWT sub) ────── task.user_id
```

The relationship is enforced at the application level, not via foreign key constraint, because the User table is managed by Better Auth on the frontend and the Task table is managed by the backend. The `user_id` in the Task table stores the Better Auth user ID extracted from the JWT token.

## Data Isolation

All task queries MUST include `user_id` in the WHERE clause:
- `SELECT ... FROM task WHERE user_id = :uid` (list)
- `SELECT ... FROM task WHERE id = :id AND user_id = :uid` (get/update/delete/toggle)

If a task exists but belongs to a different user, the API returns `403 Forbidden`.
