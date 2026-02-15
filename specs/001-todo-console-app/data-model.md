# Data Model: Todo In-Memory Python Console App

**Branch**: `001-todo-console-app` | **Date**: 2026-02-15

## Entities

### Task

Represents a single todo item managed by the user.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | int | Yes | Auto-generated | Unique numeric identifier, monotonically incrementing from 1. Never reused after deletion. |
| title | str | Yes | — | Task title. Must be non-empty and non-whitespace. |
| description | str | No | "" | Optional task description. Empty string if not provided. |
| completed | bool | No | False | Completion status. False = incomplete, True = complete. |
| created_at | datetime | Yes | Auto-generated | Timestamp of when the task was created. Set at creation time. |

**Validation Rules**:
- `title` MUST be stripped of leading/trailing whitespace before validation.
- `title` MUST NOT be empty after stripping.
- `id` is assigned by the store, not by the user.
- `completed` can only be toggled (False → True or True → False), not set to an arbitrary value.

**State Transitions**:

```text
[Created] ──── completed=False
    │
    ▼
[Mark Complete] ──── completed=True
    │
    ▼
[Mark Incomplete] ──── completed=False  (toggle back)
```

Tasks can also be updated (title/description change) or deleted at any state.

### TaskStore (In-Memory Container)

Manages the collection of tasks and the ID counter.

| Field | Type | Description |
|-------|------|-------------|
| tasks | dict[int, Task] | Maps task ID to Task object. Empty on startup. |
| next_id | int | Next available ID. Starts at 1. Increments on each add. Never decrements. |

**Invariants**:
- `next_id` is always greater than any key in `tasks`.
- All keys in `tasks` are positive integers.
- No two tasks share the same ID.

## Relationships

```text
TaskStore 1 ──── contains ──── * Task
```

Single container holds all tasks. No relationships between tasks. No user entity in Phase 1.

## Data Lifecycle

1. **Application starts** → TaskStore initialized with empty `tasks={}` and `next_id=1`.
2. **Add task** → New Task created with `id=next_id`, stored in `tasks[next_id]`, `next_id` incremented.
3. **View tasks** → All values in `tasks` dict returned/displayed.
4. **Update task** → Task looked up by ID in `tasks`, fields modified in place.
5. **Delete task** → Task removed from `tasks` dict by ID. ID is not recycled.
6. **Mark complete** → Task looked up by ID, `completed` field toggled.
7. **Application exits** → All data in memory is lost.
