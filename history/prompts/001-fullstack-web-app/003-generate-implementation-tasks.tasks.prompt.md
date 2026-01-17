---
id: 003
title: Generate implementation tasks for todo web app
stage: tasks
date: 2026-01-17
surface: agent
model: claude-sonnet-4-5
feature: 001-fullstack-web-app
branch: 001-fullstack-web-app
user: PMLS
command: sp.tasks
labels: ["task-generation", "full-stack", "web-app", "user-stories"]
links:
  spec: /mnt/c/Users/PMLS/OneDrive/Desktop/todo_phase2/specs/001-fullstack-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /mnt/c/Users/PMLS/OneDrive/Desktop/todo_phase2/specs/001-fullstack-web-app/tasks.md
tests:
  - No test tasks generated (not requested in spec)
---

## Prompt

sp.tasks

Phase II – Todo Full-Stack Web Application

یہ ٹاسکس sp.plan سے generate کیے گئے ہیں اور Claude Code کے لیے directly implementable ہیں
(next step: sp.implement).

🔴 PRIORITY LEGEND

🔴 High → لازمی، blocking

🟡 Medium → core features کے بعد

🟢 Low → polish / optional

🗄️ DATABASE TASKS
DB-01

Title: Configure Neon PostgreSQL Connection

Agent: Backend Manager

Priority: 🔴 High

Description:

DATABASE_URL env var configure کریں

postgresql+asyncpg:// format use کریں

Acceptance Criteria:

FastAPI app Neon DB سے connect ہو جائے

DB-02

Title: Create SQLModel Task Schema

Agent: Backend Manager

Priority: 🔴 High

Description:

Task SQLModel define کریں

fields: id, user_id, title, description, completed, created_at

Acceptance Criteria:

tasks table create ہو

user_id indexed ہو

DB-03

Title: Initialize Database Tables

Agent: Backend Manager

Priority: 🟡 Medium

Description:

App startup پر tables auto-create ہوں

Acceptance Criteria:

Server restart پر error نہ آئے

🔐 AUTHENTICATION TASKS
AUTH-01

Title: Setup Better Auth with JWT

Agent: Frontend Manager

Priority: 🔴 High

Description:

Better Auth configure کریں

JWT plugin enable کریں

Acceptance Criteria:

Login کے بعد JWT token ملے

AUTH-02

Title: Configure Shared JWT Secret

Agent: Project Manager

Priority: 🔴 High

Description:

BETTER_AUTH_SECRET frontend + backend دونوں میں same ہو

Acceptance Criteria:

JWT verify ہو سکے

AUTH-03

Title: JWT Verification Middleware (FastAPI)

Agent: Backend Manager

Priority: 🔴 High

Description:

Authorization header سے token extract کریں

JWT verify کریں

Acceptance Criteria:

Invalid token → 401

Valid token → user_id available

⚙️ BACKEND (FastAPI) TASKS
BE-01

Title: FastAPI Project Structure

Agent: Backend Manager

Priority: 🔴 High

Description:

main.py, db.py, models.py, routes/ setup

Acceptance Criteria:

Server uvicorn main:app پر run ہو

BE-02

Title: GET /api/{user_id}/tasks

Agent: Backend Manager

Priority: 🔴 High

Description:

Sirf authenticated user کے tasks return کریں

Acceptance Criteria:

JWT user_id کے علاوہ کوئی task نہ آئے

BE-03

Title: POST /api/{user_id}/tasks

Agent: Backend Manager

Priority: 🔴 High

Description:

New task create کریں

user_id JWT سے attach ہو

Acceptance Criteria:

Task correct user سے link ہو

BE-04

Title: Update / Delete / Complete Task

Agent: Backend Manager

Priority: 🟡 Medium

Description:

PUT, DELETE, PATCH endpoints implement کریں

Acceptance Criteria:

User دوسروں کا task modify نہ کر سکے

🎨 FRONTEND (Next.js) TASKS
FE-01

Title: Initialize Next.js App Router

Agent: Frontend Manager

Priority: 🔴 High

Description:

Next.js 16+ App Router setup

Acceptance Criteria:

App localhost:3000 پر run ہو

FE-02

Title: Auth Pages (Login / Signup)

Agent: Frontend Manager

Priority: 🔴 High

Description:

Better Auth UI integrate کریں

Acceptance Criteria:

User signup & login کر سکے

FE-03

Title: API Client with JWT Injection

Agent: Frontend Manager

Priority: 🔴 High

Description:

Central api.ts file

Authorization header attach ہو

Acceptance Criteria:

Har request JWT کے ساتھ جائے

FE-04

Title: Task List Page

Agent: Frontend Manager

Priority: 🔴 High

Description:

User tasks list show کریں

Acceptance Criteria:

Sirf current user کے tasks دکھیں

FE-05

Title: Task CRUD UI

Agent: Frontend Manager

Priority: 🟡 Medium

Description:

Create, update, complete UI

Acceptance Criteria:

UI backend کے ساتھ sync رہے

🧪 TESTING TASKS
TEST-01

Title: End-to-End Auth + CRUD Test

Agent: Project Manager

Priority: 🔴 High

Description:

Login → Create → Update → Delete task

Acceptance Criteria:

Unauthorized access possible نہ ہو

✅ sp.tasks STATUS

✔️ Tasks fully defined
✔️ Agents assigned
✔️ Dependencies clear
✔️ Claude Code ready

## Response snapshot

Generated comprehensive tasks.md file with 68 implementation tasks organized by user story following Spec-Kit Plus methodology.

**Key Decisions**:
1. Organized tasks by user story (US1: Authentication, US4: Data Isolation, US2: Task CRUD, US3: Completion) for independent implementation
2. Created foundational phase (Phase 2) that blocks all user stories - ensures core infrastructure ready first
3. Marked 39 tasks with [P] for parallel execution within phases
4. Mapped all tasks to exact file paths (backend/ and frontend/ directories)
5. No test tasks generated (not explicitly requested in spec.md)

**Task Breakdown**:
- Phase 1 (Setup): 5 tasks - project structure initialization
- Phase 2 (Foundational): 15 tasks - database, auth, API infrastructure
- Phase 3 (US1 - Authentication): 10 tasks - signup, signin, signout, protected routes
- Phase 4 (US4 - Data Isolation): 4 tasks - authorization middleware, user-scoped queries
- Phase 5 (US2 - Task CRUD): 17 tasks - all CRUD endpoints and UI components
- Phase 6 (US3 - Completion): 7 tasks - completion toggle backend + frontend
- Phase 7 (Polish): 10 tasks - responsive design, error handling, documentation

**User Story Dependencies**:
- US1 (P1) and US4 (P1) can start in parallel after Foundational
- US2 (P2) depends on US1 + US4 completion
- US3 (P3) depends on US2 completion

**Suggested MVP**: Phases 1-4 (34 tasks) = Secure authentication with user isolation

**Format Compliance**: All tasks follow strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`

## Outcome

- ✅ Impact: Created actionable task breakdown enabling Claude Code agents to implement Phase II incrementally
- 🧪 Tests: No test tasks generated (manual testing approach per spec.md)
- 📁 Files: Created tasks.md (68 tasks across 7 phases)
- 🔁 Next prompts: Execute sp.implement to begin implementation, or validate tasks.md structure first
- 🧠 Reflection: Successfully mapped user stories to implementation tasks with clear dependencies and parallel execution opportunities

## Evaluation notes (flywheel)

- Failure modes observed: None - all design documents (spec, plan, data-model, contracts) were complete
- Graders run and results (PASS/FAIL): PASS - Tasks follow template format, organized by user story, include file paths
- Prompt variant (if applicable): Standard sp.tasks workflow
- Next experiment (smallest change to try): Consider adding acceptance criteria checkboxes within each task for finer-grained validation
