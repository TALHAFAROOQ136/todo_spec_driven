# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/module-interfaces.md, research.md, quickstart.md

**Tests**: Not requested in feature specification. Test tasks omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, UV config, and package structure

- [x] T001 Initialize UV project with `uv init` and configure pyproject.toml at repository root with project name "todo-app", Python >=3.13, and console script entry `todo = "todo_app.cli:main"`
- [x] T002 Create package directory structure: `src/todo_app/__init__.py` (empty package marker)
- [x] T003 Create entry point module `src/todo_app/__main__.py` that imports and calls `main()` from `todo_app.cli` (enables `python -m todo_app`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Task dataclass and TaskStore class that ALL user stories depend on, plus the main menu loop shell

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement Task dataclass in `src/todo_app/models.py` with fields: id (int), title (str), description (str, default ""), completed (bool, default False), created_at (datetime, default factory datetime.now). Use type hints.
- [x] T005 Implement TaskStore class skeleton in `src/todo_app/store.py` with `__init__` method initializing `self.tasks: dict[int, Task] = {}` and `self.next_id: int = 1`. Import Task from models.
- [x] T006 Implement main menu loop shell in `src/todo_app/cli.py`: create `display_menu()` function that prints the numbered menu (1-Add, 2-View, 3-Update, 4-Delete, 5-Mark Complete, 6-Exit), create `main()` function with while-loop that calls `display_menu()`, reads user choice via `input()`, dispatches to placeholder handler functions, handles invalid input with "Invalid choice, please try again", and exits gracefully on option 6 with goodbye message. Create a TaskStore instance inside `main()`.
- [x] T007 Implement `get_task_id_input()` helper in `src/todo_app/cli.py` that prompts user for a task ID, validates it is a positive integer, displays error and re-prompts on non-numeric input, and returns the validated int.

**Checkpoint**: App runs (`uv run python -m todo_app`), shows menu, handles invalid choices, exits on option 6. No CRUD operations yet.

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1)

**Goal**: Users can create todo items with title and description via the console menu.

**Independent Test**: Run app → select "1" → enter title "Buy groceries" and description "Milk, eggs" → see confirmation with task ID → verify task was created.

### Implementation for User Story 1

- [x] T008 [US1] Implement `add(title: str, description: str = "") -> Task` method in `src/todo_app/store.py`: strip title whitespace, raise ValueError if empty, create Task with `id=self.next_id`, store in `self.tasks`, increment `self.next_id`, return the new Task.
- [x] T009 [US1] Implement `handle_add(store: TaskStore)` function in `src/todo_app/cli.py`: prompt for title (required, loop until non-empty with "Title cannot be empty" error), prompt for description (optional, allow empty), call `store.add()`, display confirmation "Task {id} created: {title}".
- [x] T010 [US1] Wire menu option "1" in `main()` to call `handle_add(store)` in `src/todo_app/cli.py`.

**Checkpoint**: Can add tasks via menu. Confirmation message shows generated ID.

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can see all tasks with ID, status indicator, title, and description.

**Independent Test**: Add 2-3 tasks → select "2" → verify all tasks listed with `[ ]` for incomplete and `[x]` for complete.

### Implementation for User Story 2

- [x] T011 [US2] Implement `get_all() -> list[Task]` method in `src/todo_app/store.py`: return `list(self.tasks.values())` preserving insertion order.
- [x] T012 [US2] Implement `handle_view(store: TaskStore)` function in `src/todo_app/cli.py`: call `store.get_all()`, if empty display "No tasks found", otherwise display each task formatted as `[x]` or `[ ]` followed by ID, title, and description.
- [x] T013 [US2] Wire menu option "2" in `main()` to call `handle_view(store)` in `src/todo_app/cli.py`.

**Checkpoint**: MVP functional — can add tasks and view them. Full add-then-view workflow works.

---

## Phase 5: User Story 3 - Mark Task as Complete (Priority: P2)

**Goal**: Users can toggle a task's completion status between complete and incomplete.

**Independent Test**: Add a task → mark it complete → view to verify `[x]` → mark it again → view to verify `[ ]`.

### Implementation for User Story 3

- [x] T014 [P] [US3] Implement `toggle_complete(task_id: int) -> Task | None` method in `src/todo_app/store.py`: look up task by ID, if not found return None, otherwise toggle `task.completed`, return the updated Task.
- [x] T015 [US3] Implement `handle_toggle(store: TaskStore)` function in `src/todo_app/cli.py`: call `get_task_id_input()` for the ID, call `store.toggle_complete()`, if None display "Task not found", otherwise display "Task {id} marked as complete" or "Task {id} marked as incomplete" based on new status.
- [x] T016 [US3] Wire menu option "5" in `main()` to call `handle_toggle(store)` in `src/todo_app/cli.py`.

**Checkpoint**: Can toggle task completion. View confirms status change.

---

## Phase 6: User Story 4 - Update a Task (Priority: P2)

**Goal**: Users can modify the title and/or description of an existing task.

**Independent Test**: Add a task → update its title → view to verify change → update only description (leave title blank) → verify title unchanged.

### Implementation for User Story 4

- [x] T017 [P] [US4] Implement `update(task_id: int, title: str | None = None, description: str | None = None) -> Task | None` method in `src/todo_app/store.py`: look up task by ID, if not found return None, if title provided and non-empty after strip update `task.title`, if title provided but empty/whitespace raise ValueError, if description provided update `task.description`, return updated Task.
- [x] T018 [US4] Implement `handle_update(store: TaskStore)` function in `src/todo_app/cli.py`: call `get_task_id_input()`, prompt for new title (press Enter to skip), prompt for new description (press Enter to skip), call `store.update()` passing None for skipped fields, handle ValueError for empty title, if task None display "Task not found", otherwise display confirmation.
- [x] T019 [US4] Wire menu option "3" in `main()` to call `handle_update(store)` in `src/todo_app/cli.py`.

**Checkpoint**: Can update tasks. Skipped fields retain original values.

---

## Phase 7: User Story 5 - Delete a Task (Priority: P2)

**Goal**: Users can permanently remove a task from the list by ID.

**Independent Test**: Add a task → note ID → delete it → view to confirm it's gone → try deleting same ID → see "Task not found".

### Implementation for User Story 5

- [x] T020 [P] [US5] Implement `delete(task_id: int) -> Task | None` method in `src/todo_app/store.py`: look up task by ID, if not found return None, remove from `self.tasks` using `pop()`, return the deleted Task. Do not decrement `next_id`.
- [x] T021 [US5] Implement `handle_delete(store: TaskStore)` function in `src/todo_app/cli.py`: call `get_task_id_input()`, call `store.delete()`, if None display "Task not found", otherwise display "Task {id} deleted".
- [x] T022 [US5] Wire menu option "4" in `main()` to call `handle_delete(store)` in `src/todo_app/cli.py`.

**Checkpoint**: Can delete tasks. Deleted IDs are never reused. All 5 CRUD operations functional.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup, README, and validation of full workflow

- [x] T023 [P] Create README.md at repository root with: project description, prerequisites (Python 3.13+, UV), setup instructions (`uv sync`), run instructions (`uv run python -m todo_app`), feature list, and note about in-memory storage.
- [x] T024 Validate full workflow per quickstart.md: run app, add 3 tasks, view list, mark 1 complete, update 1, delete 1, view final list, exit. Confirm all operations work correctly and no unhandled errors occur.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion — BLOCKS all user stories
- **US1 - Add Task (Phase 3)**: Depends on Foundational (Phase 2)
- **US2 - View Tasks (Phase 4)**: Depends on US1 (Phase 3) — needs tasks to display
- **US3 - Mark Complete (Phase 5)**: Depends on Foundational (Phase 2) — can run parallel with US4, US5
- **US4 - Update Task (Phase 6)**: Depends on Foundational (Phase 2) — can run parallel with US3, US5
- **US5 - Delete Task (Phase 7)**: Depends on Foundational (Phase 2) — can run parallel with US3, US4
- **Polish (Phase 8)**: Depends on all user stories complete

### User Story Dependencies

```text
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational: models + store + menu + entry)
    │
    ├──────────────────────────────────┐
    ▼                                  ▼
Phase 3 (US1: Add)          Phase 5 (US3: Mark Complete) [P]
    │                        Phase 6 (US4: Update)        [P]
    ▼                        Phase 7 (US5: Delete)        [P]
Phase 4 (US2: View)
    │
    ▼
Phase 8 (Polish)
```

### Within Each User Story

- Store method first (business logic)
- CLI handler second (user interface)
- Wire to menu third (integration)

### Parallel Opportunities

- **Phase 5, 6, 7** (US3, US4, US5): All three store methods (T014, T017, T020) touch different methods in the same file but are independent. Their CLI handlers (T015, T018, T021) are also independent functions. These can be implemented in parallel.
- **T023** (README) can be done in parallel with any phase after Setup.

---

## Parallel Example: User Stories 3, 4, 5

```text
# After Phase 2 (Foundational) completes, these can run in parallel:

Stream A (US3 - Mark Complete):
  T014 → T015 → T016

Stream B (US4 - Update):
  T017 → T018 → T019

Stream C (US5 - Delete):
  T020 → T021 → T022
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T007)
3. Complete Phase 3: US1 - Add Task (T008-T010)
4. Complete Phase 4: US2 - View Tasks (T011-T013)
5. **STOP and VALIDATE**: Add tasks and view them. MVP working.

### Full Delivery

6. Complete Phases 5-7: US3, US4, US5 (can be parallel)
7. Complete Phase 8: Polish (README + full validation)
8. All 5 features operational. Ready for submission.

---

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | 24 |
| Setup tasks | 3 (T001-T003) |
| Foundational tasks | 4 (T004-T007) |
| US1 (Add) tasks | 3 (T008-T010) |
| US2 (View) tasks | 3 (T011-T013) |
| US3 (Mark Complete) tasks | 3 (T014-T016) |
| US4 (Update) tasks | 3 (T017-T019) |
| US5 (Delete) tasks | 3 (T020-T022) |
| Polish tasks | 2 (T023-T024) |
| Parallel opportunities | US3+US4+US5 can run in parallel; README parallel with any |
| MVP scope | Phase 1-4 (US1+US2): 13 tasks |

## Notes

- No test tasks generated (not requested in spec)
- All source files under `src/todo_app/`
- `store.py` methods are independent per user story — safe to implement in parallel
- `cli.py` handler functions are independent per user story — safe to implement in parallel
- Menu wiring tasks (T010, T013, T016, T019, T022) are sequential within their story
- Commit after each phase checkpoint for clean git history
