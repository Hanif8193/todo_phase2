---
description: "Implementation tasks for Phase II - Todo Full-Stack Web Application"
---

# Tasks: Phase II - Todo Full-Stack Web Application

**Input**: Design documents from `/specs/001-fullstack-web-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/ (all complete)

**Tests**: Not explicitly requested in spec.md - tasks focus on implementation only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Web application with monorepo structure:
- Backend: `backend/` directory (FastAPI + SQLModel + Neon PostgreSQL)
- Frontend: `frontend/` directory (Next.js App Router + Better Auth + Tailwind)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create monorepo directory structure (backend/, frontend/, .env.example, README.md)
- [X] T002 [P] Initialize backend Python project with FastAPI dependencies in backend/requirements.txt
- [X] T003 [P] Initialize frontend Next.js project with TypeScript and Tailwind CSS in frontend/
- [X] T004 [P] Create .env.example file documenting BETTER_AUTH_SECRET, DATABASE_URL, API_URL variables
- [X] T005 [P] Create README.md with project overview and setup instructions

**Checkpoint**: Project structure ready for foundational implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Configuration

- [X] T006 Configure Neon PostgreSQL connection in backend/db.py with asyncpg engine
- [X] T007 [P] Create SQLModel User schema in backend/models.py (id, email, password_hash, created_at)
- [X] T008 [P] Create SQLModel Task schema in backend/models.py (id, user_id, title, description, is_completed, created_at, updated_at)
- [X] T009 Implement database initialization function in backend/db.py (create_all tables on startup)
- [X] T010 [P] Add composite index for tasks(user_id, created_at) in backend/models.py

### Authentication Infrastructure

- [X] T011 Setup Better Auth with JWT plugin in frontend/lib/auth.ts
- [X] T012 [P] Configure shared BETTER_AUTH_SECRET in frontend/.env.local and backend/.env
- [X] T013 Implement JWT verification middleware in backend/auth.py (extract user_id from token)
- [X] T014 [P] Create authentication dependency for FastAPI routes in backend/auth.py (get_current_user)

### Backend API Structure

- [X] T015 Create FastAPI application entry point in backend/main.py (CORS, startup, routes)
- [X] T016 [P] Create backend configuration manager in backend/config.py (load env vars)
- [X] T017 [P] Setup API routing structure with backend/routes/__init__.py

### Frontend Infrastructure

- [X] T018 Create Next.js root layout with Better Auth provider in frontend/app/layout.tsx
- [X] T019 [P] Create centralized API client with JWT injection in frontend/lib/api.ts
- [X] T020 [P] Configure Tailwind CSS in frontend/tailwind.config.js with custom theme

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Account Creation and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, sign in, and sign out with secure JWT authentication

**Independent Test**: Create new account → automatic signin → signout → signin again → verify session persists

### Implementation for User Story 1

- [X] T021 [P] [US1] Implement signup endpoint POST /auth/signup in backend/routes/auth.py
- [X] T022 [P] [US1] Implement signin endpoint POST /auth/signin in backend/routes/auth.py
- [X] T023 [P] [US1] Implement signout endpoint POST /auth/signout in backend/routes/auth.py
- [X] T024 [P] [US1] Create signup page UI in frontend/app/signup/page.tsx with form validation
- [X] T025 [P] [US1] Create signin page UI in frontend/app/signin/page.tsx with form validation
- [X] T026 [US1] Add logout button and handler in frontend/app/layout.tsx
- [X] T027 [US1] Implement protected route middleware in frontend/middleware.ts (redirect unauthenticated users)
- [X] T028 [US1] Add error handling for invalid credentials in frontend/app/signin/page.tsx
- [X] T029 [US1] Add error handling for duplicate email in frontend/app/signup/page.tsx
- [X] T030 [US1] Create landing page in frontend/app/page.tsx with links to signup/signin

**Checkpoint**: Users can create accounts, sign in, sign out, and are redirected appropriately

---

## Phase 4: User Story 4 - Multi-User Data Isolation (Priority: P1)

**Goal**: Ensure complete privacy - users cannot see or modify other users' tasks

**Independent Test**: Create two accounts → add tasks to each → verify neither can access the other's tasks via UI or API manipulation

**Note**: This story is implemented alongside US2 and US3 but tested independently for security verification

### Implementation for User Story 4

- [X] T031 [P] [US4] Implement user_id validation in JWT middleware in backend/auth.py (compare token vs URL)
- [X] T032 [P] [US4] Add 403 Forbidden response for user_id mismatch in backend/auth.py
- [X] T033 [US4] Enforce user_id filtering in all task queries in backend/routes/tasks.py
- [X] T034 [US4] Add integration test documentation in README.md for two-user isolation test

**Checkpoint**: Authorization layer prevents cross-user data access at API level

---

## Phase 5: User Story 2 - Task Management (CRUD Operations) (Priority: P2)

**Goal**: Allow users to create, view, update, and delete their personal tasks

**Independent Test**: After signin → create task → view list → edit task → delete task → verify persistence across refresh

### Implementation for User Story 2

- [X] T035 [P] [US2] Implement GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py (user-scoped query)
- [X] T036 [P] [US2] Implement POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py (create task)
- [X] T037 [P] [US2] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py (single task)
- [X] T038 [P] [US2] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py (update task)
- [X] T039 [P] [US2] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py (delete task)
- [X] T040 [US2] Add title validation (non-empty, max 200 chars) in backend/routes/tasks.py
- [X] T041 [US2] Add description validation (optional, max 2000 chars) in backend/routes/tasks.py
- [X] T042 [P] [US2] Create task dashboard page in frontend/app/dashboard/page.tsx (protected route)
- [X] T043 [P] [US2] Create TaskList component in frontend/components/TaskList.tsx
- [X] T044 [P] [US2] Create TaskForm component in frontend/components/TaskForm.tsx (create + edit)
- [X] T045 [P] [US2] Create TaskItem component in frontend/components/TaskItem.tsx (display + actions)
- [X] T046 [US2] Implement task creation API call in frontend/lib/api.ts
- [X] T047 [US2] Implement task update API call in frontend/lib/api.ts
- [X] T048 [US2] Implement task deletion API call in frontend/lib/api.ts
- [X] T049 [US2] Add loading states for async operations in frontend/components/TaskList.tsx
- [X] T050 [US2] Add error handling and user feedback messages in frontend/app/dashboard/page.tsx
- [X] T051 [US2] Add empty state message when user has no tasks in frontend/components/TaskList.tsx

**Checkpoint**: Users can perform full CRUD operations on tasks with data persisting correctly

---

## Phase 6: User Story 3 - Task Completion Tracking (Priority: P3)

**Goal**: Enable users to mark tasks as complete/incomplete with visual distinction

**Independent Test**: Create task → mark complete (verify visual change) → mark incomplete → refresh page (verify persistence)

### Implementation for User Story 3

- [X] T052 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/routes/tasks.py
- [X] T053 [US3] Add is_completed validation (boolean only) in backend/routes/tasks.py
- [X] T054 [US3] Implement task completion toggle API call in frontend/lib/api.ts
- [X] T055 [US3] Add completion checkbox/toggle to TaskItem component in frontend/components/TaskItem.tsx
- [X] T056 [US3] Add visual styling for completed tasks (strikethrough, color change) in frontend/components/TaskItem.tsx
- [X] T057 [US3] Add optimistic UI update for completion toggle in frontend/components/TaskItem.tsx
- [X] T058 [US3] Update updated_at timestamp on completion toggle in backend/routes/tasks.py

**Checkpoint**: Task completion status toggles work with immediate visual feedback and persistence

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T059 [P] Add responsive design breakpoints for mobile in frontend/components/ (all components)
- [X] T060 [P] Add consistent error styling and toast notifications in frontend/app/layout.tsx
- [X] T061 [P] Optimize task list rendering for large lists in frontend/components/TaskList.tsx
- [X] T062 Add loading skeleton for task list in frontend/components/TaskList.tsx
- [X] T063 [P] Add API request/response logging in backend/main.py
- [X] T064 [P] Document API endpoints in README.md with example requests
- [ ] T065 Run quickstart.md validation workflow (signup → signin → CRUD → two-user test)
- [X] T066 [P] Add favicon and page titles in frontend/app/layout.tsx
- [X] T067 [P] Configure production environment variables documentation in .env.example
- [X] T068 Final code review and cleanup across backend/ and frontend/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 4 (Phase 4)**: Depends on Foundational phase completion (parallel with US1)
- **User Story 2 (Phase 5)**: Depends on US1 and US4 completion (needs authentication + authorization)
- **User Story 3 (Phase 6)**: Depends on US2 completion (needs existing task management)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Authentication)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P1 - Data Isolation)**: Can start after Foundational (Phase 2) - Integrates with US1 authentication
- **User Story 2 (P2 - Task CRUD)**: Depends on US1 (authentication) and US4 (authorization) completion
- **User Story 3 (P3 - Completion Tracking)**: Depends on US2 (must have tasks to complete)

### Within Each User Story

**User Story 1 (Authentication)**:
- Backend endpoints before frontend pages
- Signup/Signin endpoints can be built in parallel
- Protected route middleware requires working authentication

**User Story 4 (Data Isolation)**:
- Middleware validation before route enforcement
- Integration test documentation is final step

**User Story 2 (Task CRUD)**:
- All backend endpoints marked [P] can run in parallel (different operations)
- All frontend components marked [P] can run in parallel (different files)
- API client functions depend on backend endpoints existing
- Frontend components depend on API client being ready

**User Story 3 (Completion Tracking)**:
- Backend endpoint before frontend implementation
- Visual styling happens after toggle logic works

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Within Foundational phase:
  - Database schemas (T007, T008) can run in parallel
  - T010 index creation depends on T008 completion
  - Auth setup (T011, T012, T013, T014) can run in parallel after database ready
  - Backend API structure (T016, T017) can run in parallel
  - Frontend infrastructure (T018, T019, T020) can run in parallel
- User Story 1 and User Story 4 can start in parallel after Foundational
- Within each story, tasks marked [P] can run in parallel

---

## Parallel Example: User Story 2 Backend Endpoints

```bash
# Launch all backend endpoints for User Story 2 together:
Task T035: "Implement GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py"
Task T036: "Implement POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py"
Task T037: "Implement GET /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py"
Task T038: "Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py"
Task T039: "Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py"
```

## Parallel Example: User Story 2 Frontend Components

```bash
# Launch all frontend components for User Story 2 together:
Task T043: "Create TaskList component in frontend/components/TaskList.tsx"
Task T044: "Create TaskForm component in frontend/components/TaskForm.tsx"
Task T045: "Create TaskItem component in frontend/components/TaskItem.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 4 (Data Isolation)
5. **STOP and VALIDATE**: Test authentication and two-user isolation independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + User Story 4 → Test independently → Deploy/Demo (Secure auth MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (Full task management!)
4. Add User Story 3 → Test independently → Deploy/Demo (Complete feature set!)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication)
   - Developer B: User Story 4 (Data Isolation) - integrates with A
3. Once US1 + US4 complete:
   - Developer C: User Story 2 (Task CRUD)
4. Once US2 complete:
   - Developer D: User Story 3 (Completion Tracking)
5. Stories complete and integrate independently

---

## Task Summary

### Total Tasks: 68

**By Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 15 tasks
- Phase 3 (US1 - Authentication): 10 tasks
- Phase 4 (US4 - Data Isolation): 4 tasks
- Phase 5 (US2 - Task CRUD): 17 tasks
- Phase 6 (US3 - Completion): 7 tasks
- Phase 7 (Polish): 10 tasks

**By User Story**:
- User Story 1 (Authentication): 10 tasks
- User Story 4 (Data Isolation): 4 tasks
- User Story 2 (Task CRUD): 17 tasks
- User Story 3 (Completion Tracking): 7 tasks
- Shared Infrastructure: 30 tasks

**Parallel Opportunities**:
- Setup phase: 4 tasks can run in parallel
- Foundational phase: 12 tasks can run in parallel (in groups)
- User Story 1: 7 tasks can run in parallel (backend + frontend split)
- User Story 4: 2 tasks can run in parallel
- User Story 2: 12 tasks can run in parallel (backend endpoints + frontend components)
- User Story 3: 1 task can run in parallel
- Polish phase: 8 tasks can run in parallel

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 + Phase 4 (Setup + Foundation + Authentication + Data Isolation) = 34 tasks

This provides a secure, working authentication system with proper user isolation, ready for task management features to be added incrementally.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US1 and US4 work together to provide secure authentication foundation
- US2 and US3 build on top of secure foundation
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
