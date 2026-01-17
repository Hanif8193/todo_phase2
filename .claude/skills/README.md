# Skills Documentation

This directory contains comprehensive skill documentation for full-stack development with Spec-Driven Development methodology.

## Skills Overview

### 1. Core Skills
**File:** `core-skills.md` (10KB)

Fundamental skills for Spec-Driven Development:
- Spec interpretation & clarification
- Cross-layer system thinking
- Incremental evolution from Phase-I
- Dependency-aware planning
- Validation via acceptance criteria

**Use when:** Planning features, creating specifications, designing system architecture

---

### 2. Backend Skills
**File:** `backend-skills.md` (35KB)

FastAPI + SQLModel + PostgreSQL backend development:
- REST API design
- JWT security patterns
- SQLModel schema design
- Async database handling
- User data isolation

**Use when:** Building APIs, implementing authentication, designing database schemas

**Tech Stack:** FastAPI, SQLModel, SQLAlchemy, PostgreSQL, Pydantic, Python-JOSE

---

### 3. Frontend Skills
**File:** `frontend-skills.md` (50KB)

Next.js App Router frontend development:
- App Router design patterns
- Auth-aware UI flows
- Secure API consumption
- State & error handling
- Responsive design principles

**Use when:** Building UI components, implementing authentication flows, managing client state

**Tech Stack:** Next.js 14+, React, TypeScript, Tailwind CSS, TanStack Query, React Hook Form, Zod

---

### 4. DevOps & Configuration Skills
**File:** `devops-config-skills.md` (41KB)

Environment configuration and deployment:
- Environment variable management
- Secure secrets handling
- Monorepo navigation
- Neon PostgreSQL configuration

**Use when:** Setting up projects, configuring environments, deploying applications

**Tech Stack:** Pydantic Settings, Neon PostgreSQL, Alembic, Vercel, Railway, Docker

---

### 5. AI-Assisted Development Skills
**File:** `ai-assisted-dev-skills.md` (42KB)

Working effectively with AI coding assistants:
- Prompt-driven implementation
- Task decomposition for Claude Code
- Iterative refinement without manual edits
- Phase-based architectural scaling

**Use when:** Working with Claude Code, planning AI-assisted workflows, designing scalable architectures

---

## Quick Reference

### By Development Phase

**Phase I (Foundation):**
- Core Skills → Spec interpretation, dependency planning
- Backend Skills → Data models, basic CRUD
- Frontend Skills → Basic components, simple state
- DevOps Skills → Environment setup, database config

**Phase II (Enhancement):**
- Core Skills → Incremental evolution, validation
- Backend Skills → Advanced features, optimization
- Frontend Skills → Complex state, responsive design
- DevOps Skills → Monorepo structure, secrets management

**Phase III (AI Integration):**
- AI-Assisted Skills → Phase-based scaling
- Backend Skills → AI service integration
- Frontend Skills → AI-powered UI components
- Core Skills → System thinking for AI features

### By Task Type

**Creating a New Feature:**
1. `core-skills.md` → Spec interpretation & planning
2. `ai-assisted-dev-skills.md` → Task decomposition
3. `backend-skills.md` / `frontend-skills.md` → Implementation patterns
4. `core-skills.md` → Validation via acceptance criteria

**Setting Up a New Project:**
1. `devops-config-skills.md` → Environment setup
2. `devops-config-skills.md` → Neon PostgreSQL config
3. `devops-config-skills.md` → Monorepo structure
4. `backend-skills.md` → Database models
5. `frontend-skills.md` → App Router setup

**Implementing Authentication:**
1. `backend-skills.md` → JWT security patterns
2. `backend-skills.md` → User data isolation
3. `frontend-skills.md` → Auth-aware UI flows
4. `frontend-skills.md` → Secure API consumption
5. `devops-config-skills.md` → Secrets handling

**Working with Claude Code:**
1. `ai-assisted-dev-skills.md` → Prompt-driven implementation
2. `ai-assisted-dev-skills.md` → Task decomposition
3. `ai-assisted-dev-skills.md` → Iterative refinement
4. `core-skills.md` → Acceptance criteria validation

### By Problem Type

**Performance Issues:**
- `backend-skills.md` → Async database handling (N+1 queries, eager loading)
- `frontend-skills.md` → State management (React Query caching)
- `devops-config-skills.md` → Neon connection pooling

**Security Concerns:**
- `backend-skills.md` → JWT security, user isolation
- `frontend-skills.md` → Secure API consumption
- `devops-config-skills.md` → Secrets handling

**Scaling Challenges:**
- `ai-assisted-dev-skills.md` → Phase-based scaling
- `core-skills.md` → Incremental evolution
- `backend-skills.md` → REST API design

**Code Quality:**
- `core-skills.md` → Cross-layer system thinking
- `ai-assisted-dev-skills.md` → Iterative refinement
- All skills → Best practices sections

---

## Skill Integration Examples

### Example 1: Adding Task Priority Feature

**Skills Applied:**
1. **Prompt-Driven Implementation** (`ai-assisted-dev-skills.md`)
   - Wrote detailed prompt with context, requirements, constraints

2. **Task Decomposition** (`ai-assisted-dev-skills.md`)
   - Broke down into: model update → API changes → frontend UI → testing

3. **SQLModel Schema Design** (`backend-skills.md`)
   - Added priority enum field with proper constraints

4. **App Router Patterns** (`frontend-skills.md`)
   - Created priority badge component with Tailwind styling

5. **Incremental Evolution** (`core-skills.md`)
   - Maintained backward compatibility with existing tasks

### Example 2: Setting Up New Monorepo Project

**Skills Applied:**
1. **Monorepo Navigation** (`devops-config-skills.md`)
   - Set up pnpm workspace structure

2. **Environment Variable Management** (`devops-config-skills.md`)
   - Created .env templates for backend and frontend

3. **Neon PostgreSQL Configuration** (`devops-config-skills.md`)
   - Configured async SQLAlchemy with connection pooling

4. **Secure Secrets Handling** (`devops-config-skills.md`)
   - Set up environment variable validation with Pydantic

5. **Phase-Based Architecture** (`ai-assisted-dev-skills.md`)
   - Designed extensible foundation for Phase II/III features

---

## Document Conventions

### Code Examples
- ✅ Good practices marked with checkmark
- ❌ Anti-patterns marked with X
- 🔮 Future phase capabilities marked with crystal ball

### Skill Sections
Each skill document follows this structure:
1. **Purpose** - Why this skill matters
2. **Key Capabilities** - What you'll be able to do
3. **Patterns & Examples** - How to apply the skill
4. **Success Criteria** - How to validate mastery
5. **References** - Links to related documentation

### Cross-References
Documents reference each other using:
- `See backend-skills.md section X` - Link to specific skill
- `Reference: devops-config-skills.md` - General reference
- `Follow pattern in core-skills.md` - Pattern reuse

---

## Contributing to Skills Documentation

### When to Update Skills Documents

**Add New Pattern:**
When you discover a better way to accomplish a task that should become standard practice.

**Update Examples:**
When technology versions change or better examples emerge.

**Add Troubleshooting:**
When you encounter and solve a common problem.

**Expand Coverage:**
When a new technology or pattern becomes essential to the stack.

### Document Update Process

1. Identify which skill document needs update
2. Follow existing document structure
3. Include code examples (good ✅ and bad ❌)
4. Add success criteria
5. Update this README if adding new sections

---

## Version History

- **2026-01-17** - Initial skill documentation created
  - Core Skills (5 skills)
  - Backend Skills (5 skills)
  - Frontend Skills (5 skills)
  - DevOps & Config Skills (4 skills)
  - AI-Assisted Dev Skills (4 skills)

---

## References

### Project Structure
- `.specify/memory/constitution.md` - Project coding standards
- `specs/<feature>/spec.md` - Feature specifications
- `specs/<feature>/plan.md` - Architectural plans
- `specs/<feature>/tasks.md` - Task breakdowns

### External Documentation
- **FastAPI:** https://fastapi.tiangolo.com/
- **SQLModel:** https://sqlmodel.tiangolo.com/
- **Next.js:** https://nextjs.org/docs
- **TanStack Query:** https://tanstack.com/query/latest
- **Neon:** https://neon.tech/docs
- **Tailwind CSS:** https://tailwindcss.com/

### Learning Resources
- Start with `core-skills.md` for fundamentals
- Then `ai-assisted-dev-skills.md` for effective AI collaboration
- Choose `backend-skills.md` or `frontend-skills.md` based on your role
- Reference `devops-config-skills.md` when setting up or deploying

---

## Quick Start Guide

### For New Developers

1. **Read First:**
   - `core-skills.md` - Understanding the methodology
   - `ai-assisted-dev-skills.md` - Working with Claude Code

2. **Setup Project:**
   - `devops-config-skills.md` - Environment configuration
   - `devops-config-skills.md` - Neon database setup

3. **Start Building:**
   - Backend: `backend-skills.md`
   - Frontend: `frontend-skills.md`

### For AI Agents

When processing user requests:
1. Identify which skills apply to the task
2. Reference relevant skill sections in your response
3. Follow patterns documented in skill files
4. Apply success criteria to validate output

### For Project Leads

Use these documents to:
- Standardize development practices across team
- Onboard new developers efficiently
- Review code against documented patterns
- Plan architectural evolution (Phase I → II → III)

---

**Total Documentation:** 178KB across 5 skill documents (23 individual skills)
