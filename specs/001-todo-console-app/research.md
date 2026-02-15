# Research: Todo In-Memory Python Console App

**Branch**: `001-todo-console-app` | **Date**: 2026-02-15

## Research Summary

No NEEDS CLARIFICATION items were identified in the Technical Context. All technology choices are well-defined by the constitution and spec. This research documents the decisions made and alternatives considered.

## Decision 1: In-Memory Data Structure

**Decision**: Use `dict[int, Task]` where key = task ID, value = Task dataclass.

**Rationale**: Dictionary provides O(1) lookup by ID, which is the primary access pattern (update, delete, mark complete all require ID lookup). A list would require O(n) search for every ID-based operation.

**Alternatives considered**:
- `list[Task]` — Simpler but requires linear search by ID. Rejected because ID-based operations dominate the feature set.
- `OrderedDict` — Maintains insertion order. Unnecessary since regular `dict` preserves insertion order in Python 3.7+.

## Decision 2: Task ID Generation

**Decision**: Use a monotonically incrementing integer counter. Start at 1. Never reuse IDs after deletion.

**Rationale**: Simple, predictable, human-readable. The counter is a single integer stored alongside the task dictionary. Incrementing it on each add ensures uniqueness even after deletions.

**Alternatives considered**:
- UUID — Too complex for a console app. Users need to type IDs manually.
- Reuse deleted IDs — Violates FR-003 and could confuse users referencing old IDs.

## Decision 3: Task Data Representation

**Decision**: Use Python `dataclass` from the standard library.

**Rationale**: Dataclasses provide clean, typed data containers with `__init__`, `__repr__`, and `__eq__` auto-generated. Perfect fit for a simple entity with 5 fields. No third-party dependency needed.

**Alternatives considered**:
- Plain dict — Lacks type safety and structure. Easy to misspell keys.
- NamedTuple — Immutable, which makes toggling completion status awkward (requires creating a new object).
- Regular class — More boilerplate for the same result. Dataclass is simpler.

## Decision 4: Project Structure

**Decision**: Three-module layout: `models.py`, `store.py`, `cli.py` under `src/todo_app/`.

**Rationale**: Separates data definition, business logic, and user interface. Each module has a single responsibility. Small enough to not be over-engineered but separated enough to be testable.

**Alternatives considered**:
- Single file (`main.py`) — Too monolithic for 5 features with validation logic. Hard to test.
- More granular modules (separate file per feature) — Over-engineered for this scope. Violates constitution principle VI.

## Decision 5: Entry Point

**Decision**: Use `__main__.py` for `python -m todo_app` execution plus a console script entry in `pyproject.toml`.

**Rationale**: `python -m todo_app` is the standard Python pattern for runnable packages. Adding a console script (`todo`) in pyproject.toml gives users a convenient command after `uv pip install -e .`.

**Alternatives considered**:
- Standalone `main.py` at repo root — Non-standard, doesn't leverage package structure.
- Click/Typer CLI framework — Third-party dependency, violates constitution principle III (stdlib only).

## Decision 6: Timestamp Handling

**Decision**: Use `datetime.datetime.now()` from the standard library for `created_at` field.

**Rationale**: Standard library, no dependency. Sufficient for recording when a task was created. No timezone complexity needed for a single-user console app.

**Alternatives considered**:
- `time.time()` (Unix timestamp) — Less human-readable when displaying tasks.
- Third-party (arrow, pendulum) — Violates stdlib-only constraint.

## Open Items

None. All decisions are resolved.
