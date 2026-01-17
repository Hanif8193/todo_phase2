# Implementation Plan: Phase II - Todo Full-Stack Web Application

**Branch**: `001-fullstack-web-app` | **Date**: 2026-01-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fullstack-web-app/spec.md`

## Summary

This plan implements a secure, multi-user web-based todo application with full authentication, database persistence, and user-scoped data isolation. The system migrates Phase I console functionality to a modern web architecture using Next.js (frontend), FastAPI (backend), Better Auth (JWT authentication), and Neon PostgreSQL (database). Users can sign up, sign in, and perform full CRUD operations on tasks that are completely isolated from other users' data.

**Technical Approach**: Monorepo architecture with independent frontend/backend deployments, stateless JWT authentication, user-scoped database queries, and agent-based implementation workflow following Spec-Kit Plus methodology.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x with Next.js 16+ (App Router)
- Backend: Python 3.11+ with FastAPI

**Primary Dependencies**:
- Frontend: Next.js 16+, Better Auth, Tailwind CSS
- Backend: FastAPI, SQLModel, python-jose (JWT), asyncpg
- Database: Neon Serverless PostgreSQL

**Storage**:
- Primary: Neon PostgreSQL (cloud-hosted, serverless)
- Schema: Users table, Tasks table with user_id foreign key
- Connection: asyncpg driver via SQLModel

**Testing**:
- Frontend: Manual testing via browser (automated testing in future phases)
- Backend: Manual API testing via Postman/curl (pytest in future phases)
- Integration: End-to-end auth + CRUD workflow verification

**Target Platform**:
- Frontend: Modern web browsers (Chrome, Firefox, Safari, Edge) + mobile browsers
- Backend: Linux server (development: local, production: cloud hosting)
- Deployment: Independent frontend/backend services

**Project Type**: Web (monorepo with frontend/ and backend/ directories)

**Performance Goals**:
- API response time: < 500ms p95 for CRUD operations
- Frontend perceived response: < 1 second for UI interactions
- Database queries: < 200ms for user-scoped task retrieval

**Constraints**:
- Stateless authentication (no server-side sessions)
- User data isolation enforced at database and API layers
- JWT tokens expire after 7 days
- Shared BETTER_AUTH_SECRET between frontend and backend

**Scale/Scope**:
- Initial deployment: 10-100 concurrent users
- Database: Hundreds to thousands of tasks per user
- No pagination required initially (optimize later if needed)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Core Principles Compliance

**I. Spec-Driven Development**:
- ✅ Feature has spec.md defining all requirements
- ✅ Plan.md (this file) created before implementation
- ✅ tasks.md will be generated via /sp.tasks before coding
- ✅ All implementation via Claude Code agents (no manual coding)

**II. Multi-Agent Architecture**:
- ✅ Frontend Agent: Next.js UI, Better Auth integration, JWT handling
- ✅ Backend Agent: FastAPI routes, SQLModel schemas, JWT middleware
- ✅ Auth Agent: Better Auth setup, JWT secret management, token validation
- ✅ Database Agent: Schema design, foreign keys, user-scoped queries
- ✅ Project Manager Agent: Workflow enforcement, phase gates, spec validation

**III. Security-First**:
- ✅ All API endpoints require JWT authentication
- ✅ Stateless JWT tokens (no backend sessions)
- ✅ Token expiry enabled (7 days)
- ✅ Authorization header: `Authorization: Bearer <JWT_TOKEN>`
- ✅ JWT user_id MUST match {user_id} in URL path
- ✅ BETTER_AUTH_SECRET shared between frontend/backend

**IV. User-Scoped Data Access**:
- ✅ Tasks table includes user_id foreign key
- ✅ All queries filtered by authenticated user_id from JWT
- ✅ Backend never trusts client-supplied user IDs
- ✅ No cross-user data leakage possible

**V. Monorepo Architecture**:
- ✅ /frontend directory for Next.js application
- ✅ /backend directory for FastAPI application
- ✅ Independent deployments (different ports, separate processes)
- ✅ Clear API contract boundaries

**VI. Stateless Authentication**:
- ✅ Better Auth issues JWT tokens on signup/signin
- ✅ Frontend stores and includes JWT in all API requests
- ✅ Backend validates JWT signature and extracts claims
- ✅ No server-side session storage

### ✅ Technology Stack Compliance

- ✅ Frontend: Next.js 16+ (App Router) ✓
- ✅ Frontend: TypeScript ✓
- ✅ Frontend: Tailwind CSS ✓
- ✅ Frontend: Better Auth ✓
- ✅ Backend: Python FastAPI ✓
- ✅ Backend: SQLModel (ORM) ✓
- ✅ Backend: Neon PostgreSQL ✓

### ✅ Security Requirements

- ✅ All endpoints require JWT validation
- ✅ User isolation enforced at database layer
- ✅ Secrets stored in .env files (never committed)
- ✅ BETTER_AUTH_SECRET minimum 32 characters

### 📋 Constitution Compliance Summary

**Status**: ✅ PASS - All constitutional requirements met

**No violations detected**. This plan fully adheres to:
- Spec-Kit Plus workflow
- Multi-agent architecture
- Security-first principles
- User-scoped data access
- Mandated technology stack
- Stateless authentication

## Project Structure

### Documentation (this feature)

```text
specs/001-fullstack-web-app/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file - implementation plan (IN PROGRESS)
├── research.md          # Phase 0: Technical research and decisions (PENDING)
├── data-model.md        # Phase 1: Database schema and entity definitions (PENDING)
├── quickstart.md        # Phase 1: Developer setup and testing guide (PENDING)
├── contracts/           # Phase 1: API contracts and OpenAPI specs (PENDING)
│   ├── auth.openapi.yaml
│   └── tasks.openapi.yaml
├── checklists/          # Generated requirements checklist (EXISTS)
│   └── requirements.md
└── tasks.md             # Phase 2: Actionable implementation tasks (NOT YET CREATED - use /sp.tasks)
```

### Source Code (repository root)

```text
# Web Application Structure (frontend + backend monorepo)

backend/
├── main.py              # FastAPI application entry point
├── db.py                # Database connection and session management
├── models.py            # SQLModel schemas (User, Task)
├── auth.py              # JWT validation middleware
├── routes/
│   ├── __init__.py
│   ├── auth.py          # Better Auth integration endpoints (if needed)
│   └── tasks.py         # Task CRUD endpoints
├── config.py            # Environment configuration
├── requirements.txt     # Python dependencies
└── .env                 # Backend environment variables (BETTER_AUTH_SECRET, DATABASE_URL)

frontend/
├── app/                 # Next.js App Router
│   ├── layout.tsx       # Root layout with auth provider
│   ├── page.tsx         # Landing/home page
│   ├── signin/
│   │   └── page.tsx     # Sign-in page
│   ├── signup/
│   │   └── page.tsx     # Sign-up page
│   └── dashboard/
│       └── page.tsx     # Protected task management dashboard
├── components/
│   ├── TaskList.tsx     # Task list display component
│   ├── TaskForm.tsx     # Task create/edit form
│   └── TaskItem.tsx     # Individual task item with actions
├── lib/
│   ├── api.ts           # Centralized API client with JWT injection
│   └── auth.ts          # Better Auth configuration
├── package.json         # Node dependencies
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
└── .env.local           # Frontend environment variables (BETTER_AUTH_SECRET, API_URL)

.env.example             # Template for required environment variables
README.md                # Project setup instructions
```

**Structure Decision**: Web application monorepo with clear frontend/backend separation. This structure supports:
- Independent deployment of frontend (static hosting) and backend (API server)
- Technology isolation (TypeScript frontend, Python backend)
- Clear API contract boundaries
- Phase III AI integration without architectural changes

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**Status**: No violations detected. No complexity justification required.

All architectural decisions align with constitutional principles:
- Two-service architecture (frontend + backend) is standard for web applications
- Stateless JWT authentication is mandated by constitution
- User-scoped data access enforced at multiple layers (UI, API, database)
- Technology stack exactly matches constitutional requirements

---

## Phase 0: Research & Unknowns

**Objective**: Resolve all technical unknowns and research best practices before design phase.

**Status**: PENDING (to be created in research.md)

### Research Tasks

The following areas require investigation and documentation in `research.md`:

1. **Better Auth Configuration**
   - How to configure Better Auth with JWT-only mode (no sessions)
   - JWT token structure and claims (user_id, email, exp)
   - Frontend integration patterns (React hooks, auth provider)
   - Backend JWT validation without Better Auth SDK

2. **JWT Secret Sharing**
   - Best practices for sharing BETTER_AUTH_SECRET between frontend/backend
   - Secret generation recommendations (length, randomness)
   - Environment variable configuration patterns

3. **Neon PostgreSQL Setup**
   - Connection string format for Neon
   - asyncpg driver configuration with SQLModel
   - Database initialization and table creation patterns
   - Connection pooling recommendations

4. **FastAPI JWT Middleware**
   - JWT validation libraries (python-jose vs alternatives)
   - Middleware patterns for extracting user_id from tokens
   - Error handling for invalid/expired tokens
   - Dependency injection for authenticated user context

5. **Next.js App Router Auth Patterns**
   - Protected route implementation (middleware vs component-level)
   - Client-side JWT storage (localStorage vs cookies)
   - Token refresh strategies
   - Redirect handling for unauthenticated users

6. **SQLModel User-Scoped Queries**
   - Best practices for filtering by user_id
   - Foreign key relationship patterns
   - Index optimization for user-scoped queries

**Deliverable**: `research.md` with decisions, rationale, and code examples for each area.

---

## Phase 1: Design & Contracts

**Objective**: Create data models, API contracts, and developer quickstart guide.

**Status**: PENDING (Phase 0 must complete first)

### 1.1 Data Model (`data-model.md`)

**Entities**:

**User**
- `id`: Integer, primary key, auto-increment
- `email`: String, unique, indexed, required
- `password_hash`: String, required (hashed via Better Auth)
- `created_at`: Timestamp, default now()

**Task**
- `id`: Integer, primary key, auto-increment
- `user_id`: Integer, foreign key → users.id, indexed, required
- `title`: String, required, max 200 characters
- `description`: Text, optional
- `is_completed`: Boolean, default false
- `created_at`: Timestamp, default now()
- `updated_at`: Timestamp, default now(), auto-update on modification

**Relationships**:
- User → Tasks: One-to-many (cascade delete: when user deleted, delete all tasks)
- Task → User: Many-to-one (user_id foreign key)

**Indexes**:
- `users.email`: Unique index (for signin lookup)
- `tasks.user_id`: Index (for user-scoped queries)
- `tasks(user_id, created_at)`: Composite index (for sorted task retrieval)

**Validation Rules**:
- User email: Must be valid email format
- User password: Minimum 8 characters (enforced by Better Auth)
- Task title: Cannot be empty, max 200 characters
- Task description: Optional, max 2000 characters

### 1.2 API Contracts (`contracts/`)

**Authentication Endpoints** (`contracts/auth.openapi.yaml`):

```yaml
POST /auth/signup
  Request: { email: string, password: string }
  Response 201: { token: string, user: { id: number, email: string } }
  Response 400: { detail: "Email already registered" }

POST /auth/signin
  Request: { email: string, password: string }
  Response 200: { token: string, user: { id: number, email: string } }
  Response 401: { detail: "Invalid credentials" }

POST /auth/signout
  Request: Authorization: Bearer <token>
  Response 200: { message: "Signed out successfully" }
```

**Task Endpoints** (`contracts/tasks.openapi.yaml`):

```yaml
GET /api/{user_id}/tasks
  Headers: Authorization: Bearer <token>
  Response 200: [{ id, title, description, is_completed, created_at, updated_at }]
  Response 401: { detail: "Unauthorized" }
  Response 403: { detail: "Cannot access other user's tasks" }

POST /api/{user_id}/tasks
  Headers: Authorization: Bearer <token>
  Request: { title: string, description?: string }
  Response 201: { id, title, description, is_completed, created_at, updated_at }
  Response 400: { detail: "Title is required" }

GET /api/{user_id}/tasks/{id}
  Headers: Authorization: Bearer <token>
  Response 200: { id, title, description, is_completed, created_at, updated_at }
  Response 404: { detail: "Task not found" }

PUT /api/{user_id}/tasks/{id}
  Headers: Authorization: Bearer <token>
  Request: { title: string, description?: string }
  Response 200: { id, title, description, is_completed, created_at, updated_at }

DELETE /api/{user_id}/tasks/{id}
  Headers: Authorization: Bearer <token>
  Response 204: (no content)

PATCH /api/{user_id}/tasks/{id}/complete
  Headers: Authorization: Bearer <token>
  Request: { is_completed: boolean }
  Response 200: { id, title, description, is_completed, created_at, updated_at }
```

**Security Enforcement**:
- All endpoints (except signup/signin) require valid JWT
- JWT `user_id` claim MUST match `{user_id}` in URL path
- Backend extracts user_id from JWT, ignores URL parameter for data access
- 401 for missing/invalid tokens, 403 for user_id mismatch

### 1.3 Quickstart Guide (`quickstart.md`)

**Developer Setup**:
1. Clone repository
2. Configure environment variables (.env.example → .env)
3. Install backend dependencies (pip install -r backend/requirements.txt)
4. Install frontend dependencies (cd frontend && npm install)
5. Start backend (uvicorn main:app --reload)
6. Start frontend (npm run dev)
7. Access application at http://localhost:3000

**Environment Variables**:
- `BETTER_AUTH_SECRET`: Shared 32+ character secret
- `DATABASE_URL`: Neon PostgreSQL connection string
- `API_URL`: Backend API base URL (http://localhost:8000)

**Testing Workflow**:
1. Navigate to http://localhost:3000/signup
2. Create account with email/password
3. Verify automatic signin after signup
4. Create tasks via dashboard
5. Verify tasks persist across page refresh
6. Sign out and sign back in
7. Verify tasks still visible
8. Create second account (different browser/incognito)
9. Verify data isolation (no cross-user access)

**Deliverables**:
- `data-model.md` with full schema
- `contracts/auth.openapi.yaml`
- `contracts/tasks.openapi.yaml`
- `quickstart.md` with setup and testing instructions

---

## Phase 2: Task Breakdown

**Status**: NOT STARTED (Phase 1 must complete first)

**Process**: Run `/sp.tasks` command to generate `tasks.md` with dependency-ordered, actionable implementation tasks.

**Expected Task Categories**:
1. Database Setup (DB-01 to DB-03)
2. Authentication Configuration (AUTH-01 to AUTH-03)
3. Backend Implementation (BE-01 to BE-04)
4. Frontend Implementation (FE-01 to FE-05)
5. Integration Testing (TEST-01)

**Agent Assignments**:
- Database Agent: DB tasks
- Auth Agent: AUTH tasks
- Backend Agent: BE tasks
- Frontend Agent: FE tasks
- Project Manager Agent: TEST tasks, workflow validation

---

## Architectural Decision Points

### AD-1: Stateless JWT vs Session-Based Auth
**Decision**: Stateless JWT tokens
**Rationale**:
- Enables horizontal scaling (no shared session store)
- Simplifies backend (no session management)
- Constitution mandates stateless authentication
**Trade-offs**:
- Cannot invalidate tokens server-side (must wait for expiry)
- Token size larger than session ID
- Mitigated by 7-day expiry and refresh logic

### AD-2: Better Auth for JWT Generation
**Decision**: Use Better Auth library for token issuance
**Rationale**:
- Handles password hashing securely
- Generates standard JWT tokens
- Provides React hooks for frontend
**Trade-offs**:
- Adds dependency
- Backend must validate tokens independently (Better Auth SDK not used on backend)
- Alternative: Manual JWT generation with python-jose (more complex)

### AD-3: User ID in URL Path
**Decision**: Include `{user_id}` in API endpoint paths
**Rationale**:
- Makes REST endpoints more semantic
- Aligns with resource ownership pattern
- Backend still validates user_id from JWT (URL param ignored for authorization)
**Trade-offs**:
- Redundant (user_id already in token)
- Could simplify to `/api/tasks` but less RESTful
- Decision: Keep for clarity and future extensibility

### AD-4: Monorepo vs Separate Repositories
**Decision**: Monorepo with frontend/ and backend/
**Rationale**:
- Simplifies development (single clone)
- Easier contract synchronization
- Shared documentation and specs
**Trade-offs**:
- Independent deployment still required
- Different tech stacks in same repo
- Mitigated by clear directory separation

### AD-5: Last-Write-Wins for Concurrent Updates
**Decision**: No optimistic locking initially
**Rationale**:
- Simpler implementation
- Low concurrency expected for single-user task editing
- Can add version field later if needed
**Trade-offs**:
- Concurrent edits could overwrite each other
- Acceptable for Phase II scope
- Revisit in Phase III if needed

---

## Risk Analysis

### Risk 1: JWT Secret Misconfiguration
**Likelihood**: Medium | **Impact**: Critical
**Scenario**: Frontend and backend use different BETTER_AUTH_SECRET values
**Consequence**: All authentication fails (frontend tokens rejected by backend)
**Mitigation**:
- Explicit setup validation in quickstart.md
- Error messages clearly indicate JWT verification failure
- Test with two different secrets to verify error handling

### Risk 2: User ID Extraction from JWT
**Likelihood**: Medium | **Impact**: High
**Scenario**: Backend incorrectly extracts user_id or trusts URL parameter
**Consequence**: Data isolation breach (users access other users' tasks)
**Mitigation**:
- Explicit test case in TEST-01 (attempt cross-user access)
- Code review requirement for JWT middleware
- Integration test with two users

### Risk 3: Database Connection Failures
**Likelihood**: Low | **Impact**: High
**Scenario**: Neon database connection string invalid or network issues
**Consequence**: Application cannot start or intermittent errors
**Mitigation**:
- Connection validation on startup
- Clear error messages for connection failures
- Retry logic with exponential backoff

### Risk 4: Token Expiry UX
**Likelihood**: Medium | **Impact**: Medium
**Scenario**: User's token expires while using app
**Consequence**: API requests fail with 401, user loses context
**Mitigation**:
- Frontend detects 401 and redirects to signin with message
- Future: Implement token refresh before expiry
- 7-day expiry reduces likelihood

### Risk 5: CORS Configuration
**Likelihood**: Medium | **Impact**: Medium
**Scenario**: Backend doesn't allow frontend origin for CORS
**Consequence**: Browser blocks API requests
**Mitigation**:
- FastAPI CORS middleware configured with frontend URL
- Development: Allow localhost:3000
- Production: Allow deployed frontend domain

---

## Success Metrics

**Phase Completion Criteria**:
- ✅ All Phase 0 research tasks documented in research.md
- ✅ All Phase 1 design artifacts created (data-model.md, contracts/, quickstart.md)
- ✅ Constitution Check re-validated after design
- ✅ No unresolved technical unknowns
- ✅ All agent context files updated

**Implementation Readiness**:
- Clear data model with validation rules
- Complete API contracts with error cases
- Developer setup guide tested
- Agent assignments clear
- Dependency graph established

---

## Next Steps

1. **Execute Phase 0**: Create `research.md` by researching all technical unknowns
2. **Execute Phase 1**: Generate data-model.md, contracts/, quickstart.md
3. **Re-validate Constitution**: Ensure design adheres to all principles
4. **Update Agent Context**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
5. **Generate Tasks**: Run `/sp.tasks` to create tasks.md with actionable items
6. **Phase Sign-off**: Project Manager Agent validates completion before implementation

---

**Plan Status**: ✅ COMPLETE - Ready for Phase 0 Research

**Prepared by**: Claude Code (Spec-Driven Development Agent)
**Date**: 2026-01-17
**Constitution Version**: 1.0.0
