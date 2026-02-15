# Module Interface Contracts: Todo Console App

**Branch**: `001-todo-console-app` | **Date**: 2026-02-15

> Since this is a CLI application (not a web API), contracts define internal module interfaces rather than HTTP endpoints.

## Module: `models.py`

### Task (dataclass)

```text
Task:
  id: int
  title: str
  description: str = ""
  completed: bool = False
  created_at: datetime = <auto>
```

**Contract**: Immutable ID after creation. Title and description are mutable. Completed is togglable.

---

## Module: `store.py`

### TaskStore

#### add(title: str, description: str = "") → Task

- **Precondition**: `title` is non-empty after stripping whitespace.
- **Postcondition**: Returns newly created Task with auto-assigned ID. `next_id` incremented.
- **Error**: Raises `ValueError` if title is empty/whitespace.

#### get(task_id: int) → Task | None

- **Precondition**: `task_id` is a positive integer.
- **Postcondition**: Returns Task if found, `None` if not found.

#### get_all() → list[Task]

- **Precondition**: None.
- **Postcondition**: Returns list of all tasks (may be empty). Order: insertion order.

#### update(task_id: int, title: str | None = None, description: str | None = None) → Task | None

- **Precondition**: `task_id` exists. At least one of `title` or `description` is provided.
- **Postcondition**: Returns updated Task. Fields not provided remain unchanged. If `title` is provided, it must be non-empty after stripping.
- **Error**: Returns `None` if task not found. Raises `ValueError` if new title is empty/whitespace.

#### delete(task_id: int) → Task | None

- **Precondition**: `task_id` is a positive integer.
- **Postcondition**: Returns deleted Task if found and removed, `None` if not found. ID is never reused.

#### toggle_complete(task_id: int) → Task | None

- **Precondition**: `task_id` is a positive integer.
- **Postcondition**: Returns Task with toggled `completed` field if found, `None` if not found.

---

## Module: `cli.py`

### main() → None

- **Behavior**: Runs the main menu loop. Creates a TaskStore instance. Dispatches user choices to the appropriate store methods. Handles all user input, validation, and output formatting. Loop exits when user selects Exit.

### Internal functions (not part of public contract)

- `display_menu()` — Prints numbered menu options.
- `handle_add(store)` — Prompts for title/description, calls `store.add()`.
- `handle_view(store)` — Calls `store.get_all()`, formats and prints tasks.
- `handle_update(store)` — Prompts for ID and new values, calls `store.update()`.
- `handle_delete(store)` — Prompts for ID, calls `store.delete()`.
- `handle_toggle(store)` — Prompts for ID, calls `store.toggle_complete()`.
- `get_task_id_input()` — Prompts user for numeric task ID, validates input.

---

## Module: `__main__.py`

### Entry point

```text
from todo_app.cli import main
main()
```

**Contract**: Imports and calls `main()`. No other logic.

---

## Dependency Flow

```text
__main__.py → cli.py → store.py → models.py
```

- `cli.py` depends on `store.py` (calls CRUD methods) and `models.py` (reads Task attributes for display).
- `store.py` depends on `models.py` (creates Task instances).
- `models.py` has no internal dependencies (only stdlib `datetime`).
- No circular dependencies.
