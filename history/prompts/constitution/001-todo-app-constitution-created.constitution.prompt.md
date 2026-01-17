---
id: 001
title: Todo App Constitution Created
stage: constitution
date: 2026-01-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 1-cli-todo-app
user: PMLS
command: /sp.constitution
labels: ["constitution", "phase-ii", "governance", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - No tests required for constitution
---

## Prompt

📜 sp.constitution

Todo App – Phase II (Full-Stack Web Application)

1. Project Identity

Project Name: Todo App

Phase: Phase II – Full-Stack Web Application

Objective:
Transform the Phase-I console-based todo application into a modern, secure, multi-user web application with persistent storage using a spec-driven, agentic workflow.

Development Rule:
❌ No manual coding
✅ All changes must be performed via Claude Code following Spec-Kit Plus

2. Technology Constitution

The system MUST use the following stack:

Frontend

Next.js 16+ (App Router)

TypeScript

Tailwind CSS

Better Auth (Authentication)

Backend

Python FastAPI

SQLModel (ORM)

Database

Neon Serverless PostgreSQL

Spec-Driven Workflow

Claude Code

GitHub Spec-Kit Plus

3. Architecture Principles

Monorepo architecture

Clear separation of concerns:

/frontend → UI & authentication

/backend → API & database logic

Stateless backend authentication using JWT

Backend must never trust client-side user IDs without JWT validation

All data access must be user-scoped

4. Agents & Responsibilities
4.1 Frontend Agent

Responsibilities

Implement Next.js App Router pages & layouts

Build responsive UI for task management

Integrate Better Auth (signup/signin)

Attach JWT token to every API request

Handle loading, error, and auth states

Owns

/frontend/app

/frontend/components

/frontend/lib/api.ts

/frontend/.env.local

4.2 Backend Agent

Responsibilities

Implement FastAPI REST endpoints

Define SQLModel schemas

Connect to Neon PostgreSQL

Enforce user-scoped data access

Handle validation and errors

Owns

/backend/main.py

/backend/models.py

/backend/routes/

/backend/db.py

/backend/.env

4.3 Authentication Agent

Responsibilities

Configure Better Auth to issue JWT tokens

Define JWT claims and expiry

Share secret between frontend and backend

Validate JWT in FastAPI middleware

Enforce authentication on all endpoints

Key Rule

BETTER_AUTH_SECRET must be identical in frontend & backend

4.4 Database Agent

Responsibilities

Maintain database schema consistency

Ensure foreign key integrity (tasks.user_id)

Optimize queries for user isolation

Manage migrations (if required)

4.5 Project Manager Agent

Responsibilities

Enforce Spec-Kit Plus workflow

Validate implementation against specs

Prevent scope creep

Confirm phase completion readiness

5. API Constitution
Authentication

All API endpoints require JWT

Missing or invalid token → 401 Unauthorized

Endpoints
GET    /api/{user_id}/tasks
POST   /api/{user_id}/tasks
GET    /api/{user_id}/tasks/{id}
PUT    /api/{user_id}/tasks/{id}
DELETE /api/{user_id}/tasks/{id}
PATCH  /api/{user_id}/tasks/{id}/complete

Enforcement Rules

JWT user ID must match {user_id} in URL

Users can only access their own tasks

Ownership enforced on every operation

6. Security Constitution

JWT-based stateless authentication

No backend session storage

Token expiry enabled (e.g., 7 days)

Authorization header required:

Authorization: Bearer <JWT_TOKEN>

7. Spec-Kit Governance Rules

All implementation must reference specs:

@specs/features/*

@specs/api/*

@specs/database/*

@specs/ui/*

Specs are the single source of truth

If behavior changes → update spec first

8. Phase-II Completion Criteria

Phase II is considered complete only when:

✅ All 5 basic todo features are web-based

✅ Authentication works end-to-end

✅ Tasks are persisted in Neon DB

✅ API is fully secured with JWT

✅ Frontend & backend run independently

✅ Spec-Kit Plus workflow is followed

9. Forward Compatibility

Architecture must remain extensible for:

Phase III (AI Chatbot)

Additional services or agents

No design decisions should block future AI integration

🔚 End of Constitution

## Response snapshot

Constitution successfully created and saved to `.specify/memory/constitution.md` with version 1.0.0.

The constitution defines:
- 6 core principles (Spec-Driven Development, Multi-Agent Architecture, Security-First, User-Scoped Data Access, Monorepo Architecture, Stateless Authentication)
- Technology stack requirements (Next.js 16+, TypeScript, Tailwind CSS, Better Auth, FastAPI, SQLModel, Neon PostgreSQL)
- Agent responsibilities for Frontend, Backend, Authentication, Database, and Project Manager agents
- API constitution with JWT authentication requirements and endpoint contracts
- Security constitution with JWT security, secret management, and authorization enforcement rules
- Spec-Kit governance workflow requirements
- Phase II completion criteria
- Forward compatibility considerations for Phase III

All placeholders filled with concrete values. No manual follow-up required.

## Outcome

- ✅ Impact: Project constitution created defining governance, principles, and constraints for Phase II full-stack web application
- 🧪 Tests: No tests required for constitution document
- 📁 Files: .specify/memory/constitution.md (created with version 1.0.0)
- 🔁 Next prompts: /sp.specify to create feature specs, /sp.plan to design implementation approach
- 🧠 Reflection: Constitution establishes clear agent boundaries, security requirements, and completion criteria for multi-user todo web app

## Evaluation notes (flywheel)

- Failure modes observed: None - all placeholders successfully filled from user input
- Graders run and results (PASS/FAIL): PASS - no unresolved placeholders, all sections complete, version and dates set
- Prompt variant (if applicable): Standard constitution creation from structured user input
- Next experiment (smallest change to try): N/A - constitution successfully created on first attempt
