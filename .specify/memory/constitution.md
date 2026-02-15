<!--
Sync Impact Report
- Version change: 0.0.0 → 1.0.0
- Modified principles: N/A (initial creation)
- Added sections: All (6 principles, Technology Constraints, Development Workflow, Governance)
- Removed sections: All template placeholders replaced
- Templates requiring updates: ⚠ pending (first constitution, templates not yet customized)
- Follow-up TODOs: None
-->

# Todo Console App Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All features MUST be specified before implementation. No code is written manually. The workflow is strictly: Specify → Plan → Tasks → Implement via Claude Code. Every implementation change MUST trace back to a specification artifact. If a spec is missing or ambiguous, the agent MUST stop and request clarification rather than improvise.

### II. In-Memory Data Store

All task data MUST be stored in Python in-memory data structures (lists/dictionaries). No external databases, files, or persistence layers are allowed in Phase 1. Data resets on application restart. This keeps the scope minimal and focused on core CRUD logic.

### III. Clean Python Architecture

- Project MUST use Python 3.13+ with UV as the package/project manager.
- Source code MUST reside in `/src` directory with proper Python package structure.
- Code MUST follow PEP 8 style guidelines.
- Functions MUST be small, single-responsibility, and clearly named.
- No third-party runtime dependencies for core functionality; standard library only.
- Type hints SHOULD be used for function signatures.

### IV. Five Core Features (MVP Scope)

The application MUST implement exactly these five Basic Level features and nothing more:

1. **Add Task** — Create new todo items with title and description.
2. **View Task List** — Display all tasks with status indicators (complete/incomplete).
3. **Update Task** — Modify existing task title or description by ID.
4. **Delete Task** — Remove a task from the list by ID.
5. **Mark as Complete** — Toggle task completion status by ID.

No intermediate or advanced features (priorities, tags, search, filters, recurring tasks, due dates) are in scope for Phase 1.

### V. User-Friendly Console Interface

- The application MUST provide a clear, interactive command-line menu.
- Input/output MUST be human-readable with proper formatting.
- Invalid inputs MUST be handled gracefully with helpful error messages.
- The user MUST be able to navigate back to the main menu from any operation.
- Each task MUST have a unique auto-generated numeric ID visible to the user.

### VI. Simplicity & YAGNI

- Start simple. Do not over-engineer.
- No abstractions, design patterns, or frameworks beyond what the five features require.
- No configuration files, environment variables, or external dependencies for Phase 1.
- If in doubt, choose the simpler approach.

## Technology Constraints

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13+ |
| Package Manager | UV |
| Data Storage | In-memory (Python dict/list) |
| AI Development | Claude Code + Spec-Kit Plus |
| Interface | Console (stdin/stdout) |

- No databases, ORMs, or file-based persistence.
- No web frameworks or HTTP servers.
- No third-party libraries for core logic.

## Development Workflow

1. **Specify** — Write feature specification in `specs/` using Spec-Kit Plus templates.
2. **Plan** — Generate architectural plan via `/sp.plan`.
3. **Tasks** — Break plan into atomic, testable tasks via `/sp.tasks`.
4. **Implement** — Execute tasks via Claude Code. No manual coding.
5. **Validate** — Run the application, verify all five features work correctly.
6. **Record** — Create PHR for every significant interaction.

All code changes MUST be committed to Git with meaningful commit messages. The repository MUST contain:
- Constitution file (this document)
- `specs/` folder with all specification files
- `history/` folder with prompt history records
- `/src` folder with Python source code
- `README.md` with setup instructions
- `CLAUDE.md` with Claude Code instructions

## Governance

- This constitution is the highest authority for Phase 1 development decisions.
- All specifications, plans, and tasks MUST comply with these principles.
- Amendments require explicit user approval and version increment.
- When conflicts arise, the hierarchy is: Constitution > Specify > Plan > Tasks.
- Any architecturally significant decision MUST be surfaced for ADR consideration before implementation.

**Version**: 1.0.0 | **Ratified**: 2026-02-15 | **Last Amended**: 2026-02-15
