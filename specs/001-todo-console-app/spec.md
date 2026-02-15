# Feature Specification: Todo In-Memory Python Console App

**Feature Branch**: `001-todo-console-app`
**Created**: 2026-02-15
**Status**: Draft
**Input**: User description: "Phase 1 — Build a command-line todo application that stores tasks in memory with 5 basic CRUD features using Python 3.13+ and UV"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a New Task (Priority: P1)

As a user, I want to add a new task with a title and description so that I can track things I need to do.

**Why this priority**: Adding tasks is the most fundamental operation. Without it, the app has no purpose. This is the entry point for all other features.

**Independent Test**: Can be fully tested by running the app, selecting "Add Task", entering a title and description, and verifying the task appears in the list.

**Acceptance Scenarios**:

1. **Given** the app is running and showing the main menu, **When** the user selects "Add Task" and enters title "Buy groceries" and description "Milk, eggs, bread", **Then** the system creates a task with an auto-generated unique numeric ID, displays a confirmation message with the task ID, and returns to the main menu.
2. **Given** the user is adding a task, **When** the user enters a title but leaves the description empty, **Then** the system creates the task with an empty description and confirms creation.
3. **Given** the user is adding a task, **When** the user enters an empty title, **Then** the system displays an error message "Title cannot be empty" and prompts the user to re-enter the title.

---

### User Story 2 - View All Tasks (Priority: P1)

As a user, I want to view all my tasks with their status so that I can see what I need to do and what is already done.

**Why this priority**: Viewing tasks is essential to make any other feature useful. Users need to see task IDs to update, delete, or complete tasks.

**Independent Test**: Can be tested by adding a few tasks and then selecting "View Tasks" to verify all tasks display with correct IDs, titles, descriptions, and status indicators.

**Acceptance Scenarios**:

1. **Given** there are 3 tasks in memory (2 incomplete, 1 complete), **When** the user selects "View Tasks", **Then** the system displays all 3 tasks showing: ID, title, description, and a status indicator (e.g., `[ ]` for incomplete, `[x]` for complete).
2. **Given** there are no tasks in memory, **When** the user selects "View Tasks", **Then** the system displays a message "No tasks found" and returns to the main menu.

---

### User Story 3 - Mark Task as Complete (Priority: P2)

As a user, I want to mark a task as complete or incomplete so that I can track my progress.

**Why this priority**: Toggling completion status is core to a todo app's value proposition — tracking what's done vs. what's pending.

**Independent Test**: Can be tested by adding a task, marking it complete, viewing the list to verify the status changed, then toggling it back to incomplete.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists and is incomplete, **When** the user selects "Mark Complete" and enters ID 1, **Then** the system marks the task as complete, displays a confirmation "Task 1 marked as complete", and returns to the main menu.
2. **Given** a task with ID 1 exists and is already complete, **When** the user selects "Mark Complete" and enters ID 1, **Then** the system toggles the task back to incomplete, displays "Task 1 marked as incomplete", and returns to the main menu.
3. **Given** no task with ID 99 exists, **When** the user selects "Mark Complete" and enters ID 99, **Then** the system displays "Task not found" and returns to the main menu.

---

### User Story 4 - Update a Task (Priority: P2)

As a user, I want to update the title or description of an existing task so that I can correct mistakes or add more detail.

**Why this priority**: Users frequently need to edit tasks after creation. This supports iterative task management.

**Independent Test**: Can be tested by adding a task, selecting "Update Task", entering the task ID, providing a new title or description, and verifying the changes in the task list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists with title "Buy groceries", **When** the user selects "Update Task", enters ID 1, and provides new title "Buy groceries and fruits", **Then** the system updates the title, displays confirmation, and returns to the main menu.
2. **Given** a task with ID 1 exists, **When** the user selects "Update Task", enters ID 1, and leaves the new title empty (presses Enter), **Then** the system keeps the existing title unchanged (only updates fields where the user provided new input).
3. **Given** no task with ID 99 exists, **When** the user selects "Update Task" and enters ID 99, **Then** the system displays "Task not found" and returns to the main menu.

---

### User Story 5 - Delete a Task (Priority: P2)

As a user, I want to delete a task I no longer need so that my task list stays clean and relevant.

**Why this priority**: Cleanup is important for usability, but lower priority than creation, viewing, and completion.

**Independent Test**: Can be tested by adding a task, noting its ID, selecting "Delete Task", entering the ID, and verifying it no longer appears in the task list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** the user selects "Delete Task" and enters ID 1, **Then** the system removes the task, displays "Task 1 deleted", and returns to the main menu.
2. **Given** no task with ID 99 exists, **When** the user selects "Delete Task" and enters ID 99, **Then** the system displays "Task not found" and returns to the main menu.
3. **Given** a task with ID 1 is deleted, **When** the user views all tasks, **Then** the deleted task does not appear in the list.

---

### User Story 6 - Navigate the Main Menu (Priority: P1)

As a user, I want a clear interactive menu that lets me choose what action to take so that I can easily use all features of the app.

**Why this priority**: The menu is the user's gateway to all features. Without a good menu, no feature is accessible.

**Independent Test**: Can be tested by running the app and verifying the menu displays all options, handles invalid choices gracefully, and allows exiting the application.

**Acceptance Scenarios**:

1. **Given** the app starts, **When** the main menu loads, **Then** the system displays a numbered list of all available actions: (1) Add Task, (2) View Tasks, (3) Update Task, (4) Delete Task, (5) Mark Complete, (6) Exit.
2. **Given** the main menu is displayed, **When** the user enters an invalid option (e.g., "7" or "abc"), **Then** the system displays "Invalid choice, please try again" and re-displays the menu.
3. **Given** the main menu is displayed, **When** the user selects "Exit", **Then** the system displays a goodbye message and terminates gracefully.

---

### Edge Cases

- What happens when the user enters a non-numeric value when prompted for a task ID? The system MUST display an error and re-prompt.
- What happens when the user enters only whitespace as a title? The system MUST treat it as empty and reject it.
- What happens when the data store has many tasks (e.g., 100+)? The system displays all of them in a readable format.
- What happens when the app restarts? All data is lost (in-memory only). This is expected behavior for Phase 1.
- What happens when a deleted task's ID is used for another operation? The system MUST display "Task not found".

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an interactive command-line menu with numbered options for all 5 task operations plus Exit.
- **FR-002**: System MUST allow users to create tasks with a required title (non-empty, non-whitespace) and an optional description.
- **FR-003**: System MUST auto-generate a unique numeric ID for each task upon creation. IDs MUST NOT be reused after deletion.
- **FR-004**: System MUST display all tasks with their ID, title, description, and completion status indicator.
- **FR-005**: System MUST allow users to update the title and/or description of an existing task by its ID. Fields left blank during update MUST retain their current values.
- **FR-006**: System MUST allow users to delete a task by its ID, removing it permanently from the in-memory store.
- **FR-007**: System MUST allow users to toggle the completion status of a task by its ID (incomplete to complete or complete to incomplete).
- **FR-008**: System MUST handle invalid inputs gracefully (non-numeric IDs, invalid menu choices, empty titles) with clear error messages and re-prompting.
- **FR-009**: System MUST store all task data in Python in-memory data structures only. No files, databases, or external storage.
- **FR-010**: System MUST allow the user to exit the application gracefully from the main menu.

### Key Entities

- **Task**: Represents a single todo item. Key attributes: unique numeric ID, title (required, non-empty string), description (optional string), completion status (boolean, default incomplete), creation timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task and see it in the task list within a single interaction (under 30 seconds for the complete add-and-view flow).
- **SC-002**: Users can perform all 5 operations (add, view, update, delete, mark complete) without encountering unhandled errors.
- **SC-003**: 100% of invalid inputs (wrong menu choice, non-numeric ID, empty title) produce a helpful error message instead of a crash.
- **SC-004**: Users can complete a full workflow (add 3 tasks, view list, mark 1 complete, update 1, delete 1, view final list) in under 3 minutes.
- **SC-005**: Application starts and shows the main menu within 2 seconds of launch.

## Assumptions

- The application runs in a standard terminal/console environment with text input/output.
- Only one user operates the application at a time (single-user, single-session).
- Data persistence across sessions is explicitly out of scope for Phase 1.
- No authentication or authorization is required.
- The application uses Python standard library only — no third-party packages for core logic.
- Task IDs are sequential integers starting from 1, never reused after deletion.

## Out of Scope

- Priorities, tags, or categories for tasks.
- Search, filter, or sort functionality.
- Recurring tasks or due dates.
- Multi-user support or authentication.
- Data persistence (file/database storage).
- Web or graphical user interface.
- Undo/redo functionality.
