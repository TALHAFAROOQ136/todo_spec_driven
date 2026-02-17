<!--
Sync Impact Report
- Version change: 2.0.0 → 3.0.0
- Modified principles:
  - IV. Full-Stack Web Features (MVP) → IV. AI Chatbot Features (MVP)
  - V. Responsive Web Interface → V. Conversational Chat Interface
- Added principles:
  - IX. MCP Server Architecture
  - X. OpenAI Agents SDK Integration
  - XI. Stateless Chat Architecture
- Added sections: Chat API Endpoint, MCP Tools Specification, Database Models (conversations, messages), Architecture Diagram
- Removed sections: None (Phase 2 principles retained and extended)
- Templates requiring updates: ⚠ pending (Phase 3 specs to be created)
- Follow-up TODOs: None
-->

# Todo AI Chatbot Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All features MUST be specified before implementation. No code is written manually. The workflow is strictly: Specify → Plan → Tasks → Implement via Claude Code. Every implementation change MUST trace back to a specification artifact. If a spec is missing or ambiguous, the agent MUST stop and request clarification rather than improvise.

### II. Persistent Data Store (Neon PostgreSQL)

All task data, conversations, and messages MUST be stored in a Neon Serverless PostgreSQL database using SQLModel as the ORM. Data MUST persist across application restarts. Each user's tasks and conversations MUST be isolated — users can only see and modify their own data. Database connection MUST be configured via environment variable (`DATABASE_URL`). No in-memory-only storage for production data.

### III. Clean Monorepo Architecture

- The project MUST follow a monorepo structure with separate `frontend/` and `backend/` directories.
- **Backend** MUST use Python 3.13+ with FastAPI framework and UV as the package manager.
- **Frontend** MUST use Next.js 15+ with App Router, TypeScript, and Tailwind CSS.
- Each directory MUST have its own `CLAUDE.md` with stack-specific guidelines.
- Root `CLAUDE.md` MUST provide project overview and navigation.
- Code MUST follow respective style guidelines: PEP 8 for Python, ESLint/Prettier for TypeScript.
- Type hints MUST be used in both Python (type annotations) and TypeScript (strict mode).

### IV. AI Chatbot Features (MVP Scope)

The application MUST retain all Phase 2 Basic Level features (task CRUD + auth) and additionally implement:

1. **Conversational Task Management** — Users can manage tasks via natural language through a chat interface (e.g., "Add a task to buy groceries", "Mark my first task as complete", "Show me all my tasks").
2. **MCP Tools for Task Operations** — An MCP server MUST expose task operations (add, list, complete, delete, update) as tools for the AI agent.
3. **Conversation Persistence** — All chat conversations and messages MUST be stored in the database. Users can resume conversations after server restart.
4. **Action Confirmations** — The chatbot MUST confirm actions taken (e.g., "Done! I've added 'Buy groceries' to your task list.").
5. **Error Handling** — The chatbot MUST handle errors gracefully and provide helpful responses when operations fail.

No intermediate or advanced features (priorities, tags, search, filters, recurring tasks, due dates, Kafka, Dapr) are in scope for Phase 3.

### V. Conversational Chat Interface

- The frontend MUST provide a ChatKit-based UI (OpenAI ChatKit) for the conversational interface.
- The existing task dashboard from Phase 2 MUST remain accessible alongside the chat interface.
- The chat interface MUST display conversation history with clear distinction between user and assistant messages.
- The UI MUST show loading/thinking states while the agent processes requests.
- The chat MUST support multi-turn conversations with context retention.
- Domain allowlist MUST be configured for hosted ChatKit deployment.

### VI. Authentication & User Isolation

- Authentication MUST be implemented using Better Auth on the frontend.
- Better Auth MUST issue JWT tokens upon login.
- Every API request from frontend to backend MUST include the JWT token in the `Authorization: Bearer <token>` header.
- The backend MUST verify JWT tokens using JWKS from Better Auth (`/api/auth/jwks`) with EdDSA algorithm.
- All API endpoints (task CRUD and chat) MUST enforce user isolation — users can only access their own tasks and conversations.
- Requests without a valid token MUST receive `401 Unauthorized`.
- Task and conversation ownership MUST be enforced on every operation.

### VII. RESTful API Design

- All backend API routes MUST be under `/api/` prefix.
- API MUST follow RESTful conventions with proper HTTP methods and status codes.
- Request/response bodies MUST use JSON format.
- All request validation MUST use Pydantic models.
- Errors MUST be returned as `HTTPException` with meaningful messages.
- API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |
| POST | `/api/chat` | Send message to AI chatbot |

### VIII. Simplicity & YAGNI

- Do not over-engineer. Build only what is specified.
- No abstractions, patterns, or frameworks beyond what the features require.
- Secrets and tokens MUST use environment variables (`.env` files) — never hardcoded.
- If in doubt, choose the simpler approach.

### IX. MCP Server Architecture

- An MCP (Model Context Protocol) server MUST be built using the Official MCP SDK.
- The MCP server MUST expose the following tools for the AI agent:

| Tool | Description | Parameters |
|------|-------------|------------|
| `add_task` | Create a new task | `user_id`, `title`, `description` |
| `list_tasks` | List all tasks for a user | `user_id` |
| `complete_task` | Toggle task completion | `user_id`, `task_id` |
| `delete_task` | Delete a task | `user_id`, `task_id` |
| `update_task` | Update task details | `user_id`, `task_id`, `title`, `description` |

- MCP tools MUST be stateless — all state is stored in the database.
- MCP tools MUST reuse the existing database models and session management from the backend.
- MCP tools MUST enforce user isolation (only operate on the authenticated user's tasks).

### X. OpenAI Agents SDK Integration

- The AI agent MUST be built using the OpenAI Agents SDK.
- The agent MUST use MCP tools to perform task operations — it MUST NOT directly access the database.
- The agent MUST maintain conversational context by loading conversation history from the database before each response.
- The agent MUST be configured with a clear system prompt that defines its role as a task management assistant.
- The agent MUST handle natural language commands including but not limited to:
  - Adding tasks ("Add a task to buy milk")
  - Listing tasks ("Show me my tasks", "What do I need to do?")
  - Completing tasks ("Mark the groceries task as done")
  - Deleting tasks ("Remove the dentist task")
  - Updating tasks ("Change the title of my first task")
- The agent MUST provide clear, confirmatory responses after each action.

### XI. Stateless Chat Architecture

- The chat endpoint (`POST /api/chat`) MUST be fully stateless — the server holds NO in-memory conversation state between requests.
- Conversation state MUST be persisted to the database using `Conversation` and `Message` models.
- The conversation flow for each request MUST follow this cycle:
  1. Receive user message with `conversation_id` (or create new conversation).
  2. Fetch conversation history from database.
  3. Build message array for agent (history + new message).
  4. Store user message in database.
  5. Run agent with MCP tools.
  6. Agent invokes appropriate MCP tool(s).
  7. Store assistant response in database.
  8. Return response to client.
  9. Server holds NO state (ready for next request).
- This architecture MUST support horizontal scaling — any server instance can handle any request.
- Conversations MUST be resumable after server restart.

## Technology Constraints

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15+ (App Router), TypeScript, Tailwind CSS |
| Chat UI | OpenAI ChatKit |
| Backend | Python 3.13+, FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth (frontend) + JWT verification via JWKS (backend) |
| AI Agent | OpenAI Agents SDK |
| MCP | Official MCP SDK |
| Package Manager | UV (backend), npm (frontend) |
| AI Development | Claude Code + Spec-Kit Plus |

- Frontend and backend MUST communicate via REST API only.
- The AI agent communicates with task operations exclusively through MCP tools.
- Shared secret (`BETTER_AUTH_SECRET`) MUST be consistent across frontend and backend.
- `OPENAI_API_KEY` MUST be configured via environment variable for the Agents SDK.
- Database connection string MUST be in `DATABASE_URL` environment variable.
- No direct database access from frontend — all data flows through the backend API.

## Database Models

### Existing (from Phase 2)

- **users** (managed by Better Auth) — `id`, `email`, `name`, `created_at`
- **tasks** — `id`, `user_id`, `title`, `description`, `completed`, `created_at`, `updated_at`

### New (Phase 3)

- **conversations** — `id` (UUID), `user_id` (FK → users.id), `title` (optional, auto-generated), `created_at`, `updated_at`
- **messages** — `id` (UUID), `conversation_id` (FK → conversations.id), `role` (enum: "user" | "assistant"), `content` (text), `created_at`

Indexes:
- `conversations.user_id` (for listing user's conversations)
- `messages.conversation_id` (for loading conversation history)

## Chat API Endpoint

### POST /api/chat

**Request:**
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-uuid-or-null"
}
```

**Response:**
```json
{
  "response": "Done! I've added 'Buy groceries' to your task list.",
  "conversation_id": "uuid-of-conversation"
}
```

- If `conversation_id` is null or omitted, a new conversation is created.
- JWT token MUST be included in the `Authorization` header.
- The endpoint MUST extract `user_id` from the JWT and pass it to the agent/MCP tools.

## Architecture

```text
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│  ChatKit UI     │────▶│  │         Chat Endpoint                  │  │     │    Neon DB      │
│  (Frontend)     │     │  │  POST /api/chat                        │  │     │  (PostgreSQL)   │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │  - tasks        │
│                 │     │                  ▼                           │     │  - conversations│
│                 │     │  ┌────────────────────────────────────────┐  │     │  - messages     │
│                 │◀────│  │      OpenAI Agents SDK                 │  │     │                 │
│                 │     │  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Server                     │  │     │                 │
│                 │     │  │  (MCP Tools for Task Operations)       │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

## Monorepo Structure

```text
todo_app1/
├── CLAUDE.md                     # Root Claude Code instructions
├── README.md                     # Project documentation
├── .specify/                     # Spec-Kit Plus config & templates
├── specs/                        # Feature specifications
├── history/                      # Prompt history records
├── frontend/
│   ├── CLAUDE.md                 # Frontend-specific guidelines
│   ├── package.json
│   ├── src/
│   │   ├── app/                  # Next.js pages and layouts
│   │   ├── components/           # Reusable UI components (+ ChatKit)
│   │   └── lib/                  # API client, auth, utilities
│   └── ...
├── backend/
│   ├── CLAUDE.md                 # Backend-specific guidelines
│   ├── pyproject.toml
│   ├── src/
│   │   └── todo_api/
│   │       ├── main.py           # FastAPI app entry point
│   │       ├── models.py         # SQLModel models (tasks + conversations + messages)
│   │       ├── routes/
│   │       │   ├── tasks.py      # Task CRUD endpoints
│   │       │   └── chat.py       # Chat endpoint
│   │       ├── db.py             # Database connection
│   │       ├── auth.py           # JWT verification middleware
│   │       ├── agent.py          # OpenAI Agents SDK agent config
│   │       └── mcp_server.py     # MCP server with task tools
│   └── ...
└── docker-compose.yml            # Local development setup (optional)
```

## Authentication Flow

1. User logs in on Frontend → Better Auth creates session and issues JWT token.
2. Frontend makes API call → Includes JWT token in `Authorization: Bearer <token>` header.
3. Backend receives request → Extracts token, verifies signature via JWKS with EdDSA.
4. Backend identifies user → Decodes token to get user ID.
5. Backend filters data → Returns only tasks/conversations belonging to that user.
6. For chat: user_id is passed to the agent → MCP tools operate only on that user's tasks.

## Security Requirements

- All endpoints require valid JWT token (except health check).
- Requests without token → `401 Unauthorized`.
- Token with mismatched `user_id` → `403 Forbidden`.
- Task and conversation ownership enforced on every operation.
- `OPENAI_API_KEY` MUST never be exposed to the frontend.
- MCP tools MUST validate `user_id` on every operation.

## Development Workflow

1. **Specify** — Write feature specification in `specs/` using Spec-Kit Plus templates.
2. **Plan** — Generate architectural plan via `/sp.plan`.
3. **Tasks** — Break plan into atomic, testable tasks via `/sp.tasks`.
4. **Implement** — Execute tasks via Claude Code. No manual coding.
5. **Validate** — Run both frontend and backend, verify all features work correctly.
6. **Record** — Create PHR for every significant interaction.

All code changes MUST be committed to Git with meaningful commit messages. The repository MUST contain:
- Constitution file (this document)
- `specs/` folder with all specification files
- `history/` folder with prompt history records
- `frontend/` folder with Next.js source code
- `backend/` folder with FastAPI source code
- `README.md` with comprehensive documentation
- `CLAUDE.md` files (root, frontend, backend)

## Governance

- This constitution is the highest authority for Phase 3 development decisions.
- All specifications, plans, and tasks MUST comply with these principles.
- Amendments require explicit user approval and version increment.
- When conflicts arise, the hierarchy is: Constitution > Specify > Plan > Tasks.
- Any architecturally significant decision MUST be surfaced for ADR consideration before implementation.
- Phase 1 (console app) and Phase 2 (web app) code is preserved and extended — Phase 2 task CRUD and auth MUST remain functional.

**Version**: 3.0.0 | **Ratified**: 2026-02-15 | **Last Amended**: 2026-02-17
