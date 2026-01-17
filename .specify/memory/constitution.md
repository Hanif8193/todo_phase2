# Todo App Constitution

<!--
Sync Impact Report:
- Version Change: [CONSTITUTION_VERSION] → 1.0.0
- Modified Principles: All placeholders filled with project-specific values
- Added Sections:
  * Technology Constitution
  * Agent Responsibilities
  * API & Security Rules
  * Spec-Kit Governance
  * Phase-II Completion Criteria
  * Forward Compatibility
- Removed Sections: Generic placeholder sections
- Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md - aligned with constitution check requirements
  ✅ .specify/templates/spec-template.md - aligned with scope/requirements
  ✅ .specify/templates/tasks-template.md - aligned with task categorization
- Follow-up TODOs: None - all placeholders filled
-->

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All implementation MUST follow Spec-Kit Plus workflow:
- No manual coding outside Claude Code
- All features require spec.md → plan.md → tasks.md progression
- Specs are single source of truth
- If behavior changes → update spec first, then implement

**Rationale**: Ensures traceability, prevents scope creep, and maintains alignment between intent and implementation.

### II. Multi-Agent Architecture

Development organized by domain-specific agents with clear ownership boundaries:
- **Frontend Agent**: Next.js App Router, UI, Better Auth integration, JWT handling
- **Backend Agent**: FastAPI, SQLModel, Neon PostgreSQL, user-scoped data access
- **Authentication Agent**: JWT token lifecycle, secret sharing, middleware validation
- **Database Agent**: Schema consistency, foreign key integrity, query optimization
- **Project Manager Agent**: Workflow enforcement, spec validation, phase completion gates

**Rationale**: Clear separation of concerns enables parallel work, prevents conflicts, and ensures domain expertise for each layer.

### III. Security-First (NON-NEGOTIABLE)

All API access MUST enforce stateless JWT authentication:
- No backend session storage
- Token expiry enabled (7 days)
- Authorization header required: `Authorization: Bearer <JWT_TOKEN>`
- JWT user ID MUST match {user_id} in URL path
- Users can only access their own resources
- `BETTER_AUTH_SECRET` identical in frontend and backend

**Rationale**: Zero-trust security model prevents unauthorized data access and ensures user isolation.

### IV. User-Scoped Data Access

All database queries MUST enforce user ownership:
- Every task record includes `user_id` foreign key
- Backend never trusts client-supplied user IDs without JWT validation
- All CRUD operations filtered by authenticated user
- No cross-user data leakage

**Rationale**: Prevents data breaches, ensures privacy, and enforces multi-tenancy at the data layer.

### V. Monorepo Architecture

Project structure maintains clear separation:
```
/frontend → Next.js 16+, TypeScript, Tailwind CSS, Better Auth
/backend  → Python FastAPI, SQLModel, JWT middleware
```
- Independent deployments (frontend & backend run separately)
- Shared configuration via environment variables
- Clear API contract boundaries

**Rationale**: Enables independent scaling, deployment flexibility, and technology isolation while maintaining single repository coherence.

### VI. Stateless Authentication

JWT-based authentication with no server-side sessions:
- Better Auth issues JWT tokens on signup/signin
- Frontend stores and includes JWT in all API requests
- Backend validates JWT signature and extracts user claims
- Token expiry handled client-side with refresh logic

**Rationale**: Enables horizontal scaling, reduces backend complexity, and follows modern stateless API patterns.

## Technology Constitution

### Stack Requirements (NON-NEGOTIABLE)

**Frontend Stack**:
- Next.js 16+ (App Router architecture)
- TypeScript
- Tailwind CSS
- Better Auth

**Backend Stack**:
- Python FastAPI
- SQLModel (ORM)
- Neon Serverless PostgreSQL

**Development Toolchain**:
- Claude Code
- GitHub Spec-Kit Plus

**Rationale**: These technologies are mandated for Phase II. Deviations require explicit spec amendment.

### Environment Configuration

All secrets and configuration MUST use environment variables:
- Frontend: `/frontend/.env.local`
- Backend: `/backend/.env`
- Never commit secrets to git
- `BETTER_AUTH_SECRET` shared across frontend/backend
- Database connection string from Neon dashboard

**Rationale**: Prevents credential leakage, enables environment-specific configuration, and follows 12-factor app principles.

## Agent Responsibilities

### Frontend Agent Ownership

**Implements**:
- Next.js App Router pages (`/frontend/app`)
- UI components (`/frontend/components`)
- API client with JWT attachment (`/frontend/lib/api.ts`)
- Better Auth signup/signin flows
- Loading states, error boundaries, auth redirects

**Enforces**:
- Responsive design (Tailwind CSS)
- TypeScript strict mode
- Authentication state management
- JWT token refresh logic

### Backend Agent Ownership

**Implements**:
- FastAPI route handlers (`/backend/routes/`)
- SQLModel schemas (`/backend/models.py`)
- Database connection (`/backend/db.py`)
- User-scoped query filters
- Validation and error responses

**Enforces**:
- JWT validation middleware
- User ID extraction from token
- 401 Unauthorized on invalid/missing tokens
- Foreign key constraints

### Authentication Agent Ownership

**Implements**:
- Better Auth configuration
- JWT token issuance (signup/signin)
- Token claims structure (user_id, email, expiry)
- Secret management across frontend/backend
- FastAPI JWT validation middleware

**Enforces**:
- Token expiry (7 days default)
- Signature verification
- User ID extraction for authorization

### Database Agent Ownership

**Implements**:
- SQLModel table definitions
- Foreign key relationships (`tasks.user_id → users.id`)
- Index optimization for user-scoped queries
- Migration scripts (if schema evolves)

**Enforces**:
- Referential integrity
- User isolation at schema level
- Query performance for multi-user access

### Project Manager Agent Ownership

**Validates**:
- All work follows Spec-Kit Plus workflow
- Implementation matches specs
- No scope creep or unapproved features
- Phase completion criteria met

**Prevents**:
- Manual coding outside Claude Code
- Spec deviations without amendment
- Phase progression without sign-off

## API Constitution

### Authentication Requirements

**All endpoints require JWT**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Missing or invalid token → 401 Unauthorized**

### Endpoint Contract

All task endpoints follow user-scoped pattern:
```
GET    /api/{user_id}/tasks
POST   /api/{user_id}/tasks
GET    /api/{user_id}/tasks/{id}
PUT    /api/{user_id}/tasks/{id}
DELETE /api/{user_id}/tasks/{id}
PATCH  /api/{user_id}/tasks/{id}/complete
```

**Enforcement Rules**:
- JWT `user_id` claim MUST match `{user_id}` in URL
- Backend extracts user ID from validated JWT, not URL parameter
- Users can only access their own tasks
- Ownership verified on every operation

### Error Responses

**Standard error format**:
```json
{
  "detail": "Error message"
}
```

**Common status codes**:
- `200 OK`: Successful GET/PUT/PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing/invalid JWT
- `403 Forbidden`: User owns resource but lacks permission
- `404 Not Found`: Resource doesn't exist or user doesn't own it

## Security Constitution

### JWT Security

- Stateless authentication (no backend sessions)
- Token expiry enabled (7 days recommended)
- Signature verification on every request
- User ID extracted from validated token only
- Tokens contain minimal claims (user_id, email, exp)

### Secret Management

- `BETTER_AUTH_SECRET` identical in frontend and backend
- Minimum 32-character random string
- Stored in `.env` files (never committed)
- Rotated if compromised

### Authorization Enforcement

- Backend never trusts client-supplied user IDs
- All queries filtered by JWT-extracted user ID
- No cross-user data access possible
- Database enforces user ownership via foreign keys

## Spec-Kit Governance

### Workflow Requirements

All implementation MUST follow:
1. **Spec Creation** (`/sp.specify`): Define feature requirements
2. **Planning** (`/sp.plan`): Design technical approach
3. **Task Generation** (`/sp.tasks`): Break into executable tasks
4. **Implementation** (`/sp.implement`): Execute tasks via agents

### Spec Authority

- Specs live in `/specs/[feature-name]/`
- Specs are single source of truth for requirements
- Implementation deviations require spec amendment first
- All code references corresponding spec sections

### Validation Gates

Before phase completion:
- All tasks completed and verified
- Implementation matches spec acceptance criteria
- No manual code outside agent workflow
- Tests pass (if TDD specified)
- Specs updated if behavior changed

## Phase-II Completion Criteria

Phase II is complete when all of the following are true:

✅ **All 5 basic todo features are web-based**:
  - Create task
  - View tasks
  - Update task
  - Delete task
  - Mark task as complete

✅ **Authentication works end-to-end**:
  - Users can sign up
  - Users can sign in
  - JWT tokens issued successfully
  - Tokens validated on every API request

✅ **Tasks persisted in Neon DB**:
  - Database schema deployed
  - Tasks table includes `user_id` foreign key
  - CRUD operations persist to PostgreSQL

✅ **API fully secured with JWT**:
  - All endpoints require valid JWT
  - User ID extraction from token
  - User-scoped data access enforced

✅ **Frontend & backend run independently**:
  - Frontend serves on separate port
  - Backend API runs independently
  - API client attaches JWT to requests

✅ **Spec-Kit Plus workflow followed**:
  - All features have specs
  - Implementation matches specs
  - No manual coding performed

## Forward Compatibility

### Phase III Preparation

Architecture MUST remain extensible for:
- AI Chatbot integration
- Additional microservices
- Expanded agent capabilities

**Design Constraints**:
- No tight coupling between UI and business logic
- API contract stability (versioning strategy if breaking changes needed)
- Database schema allows additions without migrations breaking existing code
- JWT claims extensible (additional optional fields allowed)

### Reversibility

Architectural decisions SHOULD be reversible where possible:
- Feature flags for new capabilities
- Backward-compatible API changes
- Database migrations with rollback scripts

**Rationale**: Phase III requirements may necessitate architectural adjustments. Flexibility reduces refactoring cost.

## Governance

### Constitution Authority

This constitution supersedes all other practices and guides. Any conflicts between this constitution and other documentation must be resolved in favor of the constitution or require an explicit amendment.

### Amendment Process

To amend this constitution:
1. Document proposed change with rationale
2. Assess impact on existing specs/plans/tasks
3. Update constitution version (semantic versioning)
4. Propagate changes to dependent templates
5. Create ADR for significant architectural amendments
6. Obtain approval before implementation

### Versioning Policy

- **MAJOR**: Backward incompatible governance or principle removals/redefinitions
- **MINOR**: New principles, sections, or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Review

All PRs and reviews MUST verify:
- Spec-Kit Plus workflow followed
- Specs updated before implementation
- Security principles enforced (JWT, user-scoping)
- Agent ownership boundaries respected
- No manual coding outside Claude Code

### Complexity Justification

Any deviations from core principles (e.g., additional backend services, alternative auth methods, cross-user features) MUST be justified in plan.md Complexity Tracking section.

**Version**: 1.0.0 | **Ratified**: 2026-01-17 | **Last Amended**: 2026-01-17
