# Implementation Plan: Todo In-Memory Python Console App

**Branch**: `001-todo-console-app` | **Date**: 2026-02-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

## Summary

Build an interactive command-line todo application in Python 3.13+ that stores tasks in-memory using a dictionary. The app provides a numbered menu for 5 CRUD operations (Add, View, Update, Delete, Mark Complete) plus Exit. All input validation and error handling is done via standard library. The project uses UV for package management and follows a clean single-package structure under `src/`.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory Python dictionary (`dict[int, Task]`)
**Testing**: pytest (dev dependency only, not runtime)
**Target Platform**: Cross-platform console (Windows, macOS, Linux)
**Project Type**: Single project
**Performance Goals**: Instant response for all operations (<100ms). Start-up under 2 seconds.
**Constraints**: No third-party runtime dependencies. No file I/O or persistence. Standard library only.
**Scale/Scope**: Single user, single session, in-memory data (resets on restart)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Spec completed before plan. All features trace to FR-001 through FR-010. |
| II. In-Memory Data Store | PASS | Using `dict[int, Task]` in memory. No persistence. |
| III. Clean Python Architecture | PASS | Python 3.13+, UV, `/src` directory, PEP 8, stdlib only, type hints. |
| IV. Five Core Features (MVP) | PASS | Exactly 5 features specified. No extras. |
| V. User-Friendly Console Interface | PASS | Numbered menu, error messages, auto-generated IDs. |
| VI. Simplicity & YAGNI | PASS | Minimal modules, no abstractions beyond what's needed. |

**Gate Result**: ALL PASS. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (internal module interfaces)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
└── todo_app/
    ├── __init__.py      # Package marker (empty)
    ├── __main__.py      # Entry point: python -m todo_app
    ├── models.py        # Task dataclass definition
    ├── store.py         # TaskStore: in-memory CRUD operations
    └── cli.py           # Menu display, input handling, main loop

pyproject.toml           # UV project config, metadata, dev dependencies
```

**Structure Decision**: Single project layout under `src/todo_app/`. Three modules separate concerns cleanly: `models.py` (data), `store.py` (business logic), `cli.py` (user interface). The `__main__.py` enables running via `python -m todo_app`. This is the simplest viable separation that keeps each module focused and testable without over-engineering.

## Complexity Tracking

No constitution violations. No complexity justifications needed.
