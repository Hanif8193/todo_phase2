---
id: 002
title: Implementation Plan Phase II
stage: plan
date: 2026-01-17
surface: agent
model: claude-sonnet-4-5
feature: 001-fullstack-web-app
branch: 001-fullstack-web-app
user: hanif
command: /sp.plan
labels: ["planning", "phase-2", "fullstack", "architecture", "design"]
links:
  spec: specs/001-fullstack-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-fullstack-web-app/plan.md
  - specs/001-fullstack-web-app/research.md
  - specs/001-fullstack-web-app/data-model.md
  - specs/001-fullstack-web-app/contracts/auth.openapi.yaml
  - specs/001-fullstack-web-app/contracts/tasks.openapi.yaml
  - specs/001-fullstack-web-app/quickstart.md
tests:
  - Manual testing workflow documented in quickstart.md
  - 8 acceptance test scenarios defined
  - Multi-user isolation test specified
  - API contract validation via OpenAPI specs
---

## Prompt

```text
sp.plan

Phase II – Todo Full-Stack Web Application

1. Plan Objective

اس پلان کا مقصد Phase II کو اس طرح توڑنا ہے کہ:

ہر کام واضح (actionable) ہو

Frontend, Backend, Database, Auth سب cover ہوں

Dependencies clear ہوں

Agents کو واضح ذمہ داریاں ملیں

Claude Code بغیر manual coding کے implement کر سکے

2. Agents & Responsibilities
🧑‍💼 Project Manager Agent

Specs پڑھنا اور consistency maintain کرنا

Task ordering & dependencies ensure کرنا

Acceptance criteria verify کرنا

🎨 Frontend Manager Agent

Next.js App Router setup

UI pages & components

API integration

JWT handling (client-side)

⚙️ Backend Manager Agent

FastAPI app

REST endpoints

JWT verification

SQLModel integration

🧠 AI Feature Agent

(Phase II میں limited)

Auth flow correctness

Error handling patterns

Security edge cases

3. High-Level Execution Order (Dependencies)
Database Schema
   ↓
Backend Models & DB Connection
   ↓
JWT Auth Verification (Backend)
   ↓
API Endpoints
   ↓
Frontend Auth Integration
   ↓
Frontend Task UI
   ↓
End-to-End Testing

4. Task Breakdown (Grouped by Component)
🗄️ DATABASE TASKS
DB-01: Configure Neon PostgreSQL Connection

Agent: Backend Manager

Description: DATABASE_URL env var setup with asyncpg

Depends On: None

Acceptance Criteria:

App connects to Neon successfully

Priority: 🔴 High

DB-02: Define SQLModel Task Schema

Agent: Backend Manager

Description: Create Task model with user_id foreign key

Depends On: DB-01

Acceptance Criteria:

tasks table created

user_id indexed

Priority: 🔴 High

DB-03: Database Initialization & Migrations

Agent: Backend Manager

Description: Create tables on startup

Depends On: DB-02

Acceptance Criteria:

Tables auto-created without error

Priority: 🟡 Medium

🔐 AUTHENTICATION TASKS
AUTH-01: Better Auth Setup (Frontend)

Agent: Frontend Manager

Description: Configure Better Auth with JWT enabled

Depends On: None

Acceptance Criteria:

Login returns JWT token

Priority: 🔴 High

AUTH-02: Shared JWT Secret Configuration

Agent: Project Manager

Description: BETTER_AUTH_SECRET env var in frontend & backend

Depends On: AUTH-01

Acceptance Criteria:

Same secret used on both sides

Priority: 🔴 High

AUTH-03: JWT Verification Middleware (Backend)

Agent: Backend Manager

Description: Verify JWT, extract user_id

Depends On: AUTH-02

Acceptance Criteria:

Invalid token → 401

Valid token → user context available

Priority: 🔴 High

⚙️ BACKEND TASKS (FastAPI)
BE-01: FastAPI Project Structure

Agent: Backend Manager

Description: Setup main.py, db.py, models.py, routes/

Depends On: DB-01

Acceptance Criteria:

Server runs without errors

Priority: 🔴 High

BE-02: GET /api/{user_id}/tasks

Agent: Backend Manager

Description: Return only authenticated user's tasks

Depends On: AUTH-03, DB-02

Acceptance Criteria:

Tasks filtered by JWT user_id

Priority: 🔴 High

BE-03: POST /api/{user_id}/tasks

Agent: Backend Manager

Description: Create task for authenticated user

Depends On: BE-02

Acceptance Criteria:

user_id auto-attached from JWT

Priority: 🔴 High

BE-04: PUT / DELETE / PATCH Task Endpoints

Agent: Backend Manager

Description: Update, delete, toggle completion

Depends On: BE-03

Acceptance Criteria:

Cannot modify another user's task

Priority: 🟡 Medium

🎨 FRONTEND TASKS (Next.js)
FE-01: Next.js App Router Setup

Agent: Frontend Manager

Description: Initialize frontend structure

Depends On: None

Acceptance Criteria:

App runs on localhost:3000

Priority: 🔴 High

FE-02: Auth Pages (Login / Signup)

Agent: Frontend Manager

Description: UI + Better Auth integration

Depends On: AUTH-01

Acceptance Criteria:

User can login/signup

Priority: 🔴 High

FE-03: API Client with JWT Injection

Agent: Frontend Manager

Description: Centralized api.ts attaching Authorization header

Depends On: AUTH-01

Acceptance Criteria:

All requests include JWT

Priority: 🔴 High

FE-04: Task List Page

Agent: Frontend Manager

Description: Display user's tasks

Depends On: BE-02, FE-03

Acceptance Criteria:

Only own tasks visible

Priority: 🔴 High

FE-05: Task Create / Update UI

Agent: Frontend Manager

Description: Forms for CRUD operations

Depends On: FE-04

Acceptance Criteria:

UI reflects backend changes

Priority: 🟡 Medium

🧪 TESTING & VALIDATION
TEST-01: End-to-End Auth + CRUD Test

Agent: Project Manager

Description: Login → create → update → delete task

Depends On: All above

Acceptance Criteria:

No unauthorized access

Priority: 🔴 High

5. Plan Completeness Checklist ✅

 All specs referenced

 Frontend tasks defined

 Backend tasks defined

 Database tasks defined

 Auth & security covered

 Dependencies clear

 Tasks actionable for Claude Code

✅ Status

sp.plan COMPLETE & READY
```

## Response snapshot

Executed comprehensive `/sp.plan` workflow for Phase II Todo Full-Stack Web Application:

**Phase 0 (Research) - COMPLETE**:
- Created `research.md` resolving 6 technical unknowns
- Researched Better Auth JWT configuration with HS256 algorithm
- Documented JWT secret sharing strategy using shared BETTER_AUTH_SECRET
- Defined Neon PostgreSQL setup with asyncpg driver
- Documented FastAPI JWT middleware using python-jose library
- Established Next.js App Router auth patterns with Better Auth hooks
- Defined SQLModel user-scoped query patterns with ownership verification

**Phase 1 (Design) - COMPLETE**:
- Created comprehensive `plan.md` with technical context, constitution check, project structure
- Documented 5 architectural decision points (JWT vs sessions, Better Auth, user_id in URL, monorepo, concurrency)
- Identified 5 key risks with mitigation strategies
- Created `data-model.md` with full schema definitions for User and Task entities
- Defined validation rules, indexes, and state transitions
- Created OpenAPI 3.0 contracts:
  - `auth.openapi.yaml`: Signup, signin, signout endpoints
  - `tasks.openapi.yaml`: Complete CRUD + completion toggle endpoints
- Created `quickstart.md` with developer setup, 8 test scenarios, troubleshooting guide

**Constitutional Compliance**:
✅ All core principles validated (Spec-Driven Development, Multi-Agent Architecture, Security-First)
✅ Technology stack matches requirements exactly
✅ User-scoped data access enforced at all layers
✅ Stateless JWT authentication as mandated
✅ No constitutional violations detected

**Key Deliverables**:
1. Implementation plan with clear phases and dependencies
2. Complete data model with User and Task entities
3. API contracts for authentication and task management
4. Developer quickstart guide with environment setup
5. Research documentation for all technical decisions
6. Security enforcement patterns and validation rules

**Architecture Highlights**:
- Monorepo with independent frontend/backend deployments
- Stateless JWT authentication (7-day expiry)
- User-scoped database queries with composite indexes
- Better Auth for token generation, python-jose for validation
- Next.js 16+ App Router with React Server Components support
- FastAPI with SQLModel ORM and Neon PostgreSQL

**Ready for Next Phase**:
All Phase 0 and Phase 1 artifacts complete. Ready to run `/sp.tasks` to generate actionable implementation tasks with clear agent assignments and dependency ordering.

## Outcome

- ✅ Impact: Complete implementation plan with Phase 0 research and Phase 1 design artifacts. All technical unknowns resolved. Constitution compliance validated. 6 planning documents created (plan.md, research.md, data-model.md, 2 OpenAPI contracts, quickstart.md).
- 🧪 Tests: 8 acceptance test scenarios documented in quickstart.md (signup, create task, complete task, edit, delete, persistence, signin/signout, multi-user isolation)
- 📁 Files: 6 files created in specs/001-fullstack-web-app/ (plan.md, research.md, data-model.md, contracts/auth.openapi.yaml, contracts/tasks.openapi.yaml, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate dependency-ordered implementation tasks. Consider `/sp.adr` for documenting architectural decisions (JWT vs sessions, Better Auth selection, monorepo structure).
- 🧠 Reflection: Planning phase successfully completed following Spec-Kit Plus methodology. All architectural decisions justified with clear rationale and alternatives considered. Security-first principles enforced throughout design (JWT validation, user isolation, password hashing). Research phase eliminated all unknowns before design. Ready for task generation and agent-based implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None. All constitutional requirements met. No technical blockers identified.
- Graders run and results (PASS/FAIL): Constitution Check: PASS (all 6 core principles validated, technology stack compliant, security requirements met). Design completeness: PASS (data model, API contracts, quickstart guide all complete). Research thoroughness: PASS (all 6 unknowns resolved with code examples).
- Prompt variant (if applicable): Standard sp.plan workflow with bilingual input (Urdu + English). Successfully processed mixed-language requirements.
- Next experiment (smallest change to try): Consider auto-generating .env.example files from environment variable documentation in quickstart.md. Could add validation script to check BETTER_AUTH_SECRET matches between frontend/backend during setup.
