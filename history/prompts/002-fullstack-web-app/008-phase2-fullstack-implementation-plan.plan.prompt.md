---
id: 008
title: Phase 2 Fullstack Implementation Plan
stage: plan
date: 2026-02-17
surface: agent
model: claude-opus-4-6
feature: 002-fullstack-web-app
branch: 002-fullstack-web-app
user: architect
command: sp.plan
labels: ["planning", "architecture", "fullstack", "fastapi", "nextjs", "better-auth"]
links:
  spec: specs/002-fullstack-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-fullstack-web-app/plan.md
  - specs/002-fullstack-web-app/research.md
  - specs/002-fullstack-web-app/data-model.md
  - specs/002-fullstack-web-app/quickstart.md
  - specs/002-fullstack-web-app/contracts/api.yaml
tests:
  - null
---

## Prompt

/sp.plan

## Response snapshot

Generated the complete implementation plan for Phase 2 Full-Stack Web Todo App. Executed Phase 0 (research) and Phase 1 (design & contracts) of the planning workflow.

**Phase 0 (Research)** resolved 7 research questions:
- RQ-1: Better Auth v1.x with JWT plugin (HS256 shared secret)
- RQ-2: PyJWT for backend JWT verification (replaced abandoned python-jose)
- RQ-3: SQLModel async with asyncpg driver for Neon PostgreSQL
- RQ-4: SQLModel create_all() for initial schema (Alembic deferred per YAGNI)
- RQ-5: Next.js 16 App Router with proxy.ts for route protection
- RQ-6: Better Auth uses same Neon database for user storage
- RQ-7: Centralized API client (lib/api.ts) with Bearer token

**Phase 1 (Design)** produced:
- data-model.md: Task entity (SQLModel) + Better Auth user tables + Pydantic request/response models + validation rules + state transitions
- contracts/api.yaml: OpenAPI 3.1 spec for 6 REST endpoints (GET/POST tasks, GET/PUT/DELETE task, PATCH toggle)
- quickstart.md: Developer setup guide (prerequisites, env config, install, run, verify)

**Key design decisions:**
1. Better Auth manages users; backend only stores tasks
2. JWT with HS256 shared secret (BETTER_AUTH_SECRET)
3. Async database access (asyncpg + pool_pre_ping + pool_recycle)
4. No Alembic migrations initially (create_all at startup)
5. Same Neon database for Better Auth and application

**Constitution check**: ALL 8 principles PASS (both pre-research and post-design gates).

## Outcome

- Impact: Complete planning artifacts generated for Phase 2 full-stack web app. All research questions resolved. All constitution gates pass. Ready for /sp.tasks.
- Tests: No tests generated (planning phase only)
- Files: plan.md, research.md, data-model.md, quickstart.md, contracts/api.yaml
- Next prompts: Run `/sp.tasks` to generate implementation task breakdown
- Reflection: Research revealed key insight that python-jose is abandoned in favor of PyJWT. Better Auth's JWT plugin defaults to asymmetric keys but can be configured for HS256 per constitution requirements. Next.js 16 renames middleware to proxy.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution gate PASS (all 8 principles, both checks)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run /sp.tasks to validate plan completeness via task decomposition
