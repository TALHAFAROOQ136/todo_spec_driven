---
id: 007
title: Phase 3 Constitution Update - AI Chatbot
stage: constitution
date: 2026-02-17
surface: agent
model: claude-opus-4-6
feature: none
branch: master
user: TALHAFAROOQ136
command: /sp.constitution
labels: ["constitution", "phase3", "ai-chatbot", "mcp", "openai-agents"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (governance document)
---

## Prompt

todo.docx mein phase 3 read kro aur us ka constitution likho

## Response snapshot

Updated constitution from v2.0.0 to v3.0.0 for Phase 3 - Todo AI Chatbot. Major changes:
- Added 3 new principles: IX. MCP Server Architecture, X. OpenAI Agents SDK Integration, XI. Stateless Chat Architecture
- Modified principle IV to include AI chatbot features (conversational task management, MCP tools, conversation persistence)
- Modified principle V for ChatKit-based conversational UI
- Added database models for conversations and messages
- Added POST /api/chat endpoint specification
- Added architecture diagram showing ChatKit → FastAPI → Agents SDK → MCP → Neon DB flow
- Updated technology constraints to include OpenAI ChatKit, Agents SDK, and MCP SDK
- Updated monorepo structure with new backend files (chat.py, agent.py, mcp_server.py)

## Outcome

- ✅ Impact: Constitution updated to v3.0.0 covering all Phase 3 requirements from hackathon document
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify for Phase 3 features, /sp.plan for architecture
- 🧠 Reflection: Phase 3 adds significant architectural complexity with MCP + Agents SDK. The stateless chat architecture is critical for scalability.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create feature specs for chatbot, MCP server, and chat endpoint
