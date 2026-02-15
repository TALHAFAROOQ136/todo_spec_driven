# Quickstart: Todo In-Memory Python Console App

**Branch**: `001-todo-console-app` | **Date**: 2026-02-15

## Prerequisites

- Python 3.13+
- UV package manager

## Setup

```bash
# Clone the repository
git clone <repo-url>
cd todo_app1

# Install dependencies with UV
uv sync

# Or install in editable mode
uv pip install -e .
```

## Running the Application

```bash
# Option 1: Run as module
uv run python -m todo_app

# Option 2: Run via console script (after install)
uv run todo
```

## Usage

The application displays an interactive menu:

```
===== Todo App =====
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Exit
====================
Choose an option:
```

### Add a Task

Select option `1`, enter a title (required) and description (optional).

### View All Tasks

Select option `2` to see all tasks with their ID, status, title, and description.

### Update a Task

Select option `3`, enter the task ID, then provide new title and/or description. Press Enter to skip a field (keeps current value).

### Delete a Task

Select option `4`, enter the task ID to remove.

### Mark Complete/Incomplete

Select option `5`, enter the task ID to toggle its completion status.

### Exit

Select option `6` to quit the application.

## Notes

- All data is stored in memory. Tasks are lost when the application exits.
- Task IDs are auto-generated and never reused after deletion.
- This is Phase 1 (console only). No persistence, no web UI, no authentication.
