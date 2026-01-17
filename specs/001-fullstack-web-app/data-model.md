# Data Model - Todo Full-Stack Web Application

**Feature**: Phase II - Todo Full-Stack Web Application
**Date**: 2026-01-17
**Status**: COMPLETE

## Overview

This document defines the complete database schema, entity relationships, validation rules, and indexing strategy for the Todo application. The schema enforces user isolation at the database layer through foreign key relationships and indexed user-scoped queries.

---

## Database Technology

**PostgreSQL Version**: 14+ (Neon Serverless PostgreSQL)
**ORM**: SQLModel (Pydantic + SQLAlchemy)
**Migration Strategy**: Auto-create tables on startup (Phase II), Alembic for future schema changes

---

## Entity Definitions

### User Entity

**Purpose**: Represents a registered user account with authentication credentials.

**Table**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User's email address (used for signin) |
| `password_hash` | VARCHAR(255) | NOT NULL | Hashed password (bcrypt/argon2 via Better Auth) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp (UTC) |

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
```

**Validation Rules**:
- `email`: Must be valid email format (RFC 5322 compliant)
- `email`: Case-insensitive uniqueness (lowercase before storage)
- `password`: Minimum 8 characters (enforced by Better Auth, not database)
- `password_hash`: Never exposed in API responses
- `created_at`: Auto-set on insert, never updated

**Indexes**:
- PRIMARY KEY on `id` (auto-indexed)
- UNIQUE INDEX on `email` (for fast signin lookup)

**Cascade Behavior**:
- ON DELETE: Cascade delete all tasks when user is deleted
- Prevents orphaned tasks in database

---

### Task Entity

**Purpose**: Represents a single to-do item owned by exactly one user.

**Table**: `tasks`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique task identifier |
| `user_id` | INTEGER | FOREIGN KEY (users.id), NOT NULL, INDEX | Owner user ID |
| `title` | VARCHAR(200) | NOT NULL | Task title (required) |
| `description` | TEXT | NULL | Optional task description |
| `is_completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp (UTC) |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp (UTC) |

**SQLModel Definition**:
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tasks")
```

**Validation Rules**:
- `title`: Cannot be empty string (validated at API layer)
- `title`: Maximum 200 characters
- `description`: Optional, maximum 2000 characters
- `is_completed`: Boolean only (true/false)
- `user_id`: Must reference existing user (foreign key constraint)
- `created_at`: Auto-set on insert, never updated
- `updated_at`: Auto-updated on every modification

**Indexes**:
- PRIMARY KEY on `id` (auto-indexed)
- INDEX on `user_id` (for user-scoped queries)
- COMPOSITE INDEX on `(user_id, created_at)` (for sorted retrieval)

**Cascade Behavior**:
- ON DELETE user: Cascade delete all user's tasks
- Prevents orphaned tasks

---

## Entity Relationships

### User ↔ Task Relationship

**Type**: One-to-Many (1:N)

**Cardinality**:
- One User → Zero or Many Tasks
- One Task → Exactly One User

**Foreign Key**:
- `tasks.user_id` → `users.id`

**Cascade Rules**:
- DELETE User → CASCADE DELETE all user's tasks
- UPDATE User.id → CASCADE UPDATE tasks.user_id (rare, IDs immutable)

**Relationship Diagram**:
```
┌─────────────────┐          ┌─────────────────┐
│     users       │          │     tasks       │
├─────────────────┤          ├─────────────────┤
│ id (PK)         │──────┐   │ id (PK)         │
│ email (UNIQUE)  │      │   │ user_id (FK)    │
│ password_hash   │      └──→│ title           │
│ created_at      │          │ description     │
└─────────────────┘          │ is_completed    │
                             │ created_at      │
                             │ updated_at      │
                             └─────────────────┘
    1                             0..*
```

**SQLModel Relationship Configuration**:
```python
# User side
tasks: List["Task"] = Relationship(
    back_populates="user",
    sa_relationship_kwargs={"cascade": "all, delete"}
)

# Task side
user: User = Relationship(back_populates="tasks")
```

---

## Indexing Strategy

### Index 1: Primary Keys
**Columns**: `users.id`, `tasks.id`
**Type**: B-tree (default)
**Purpose**: Unique identification, auto-indexed
**Performance**: O(log n) lookups

### Index 2: User Email (Unique)
**Columns**: `users.email`
**Type**: B-tree, UNIQUE
**Purpose**: Fast signin lookup by email
**Query Pattern**: `SELECT * FROM users WHERE email = 'user@example.com'`
**Performance**: O(log n) lookup

### Index 3: Task User ID
**Columns**: `tasks.user_id`
**Type**: B-tree
**Purpose**: Fast user-scoped task queries
**Query Pattern**: `SELECT * FROM tasks WHERE user_id = 123`
**Performance**: O(log n) lookup + O(m) scan (m = user's task count)

### Index 4: Task User ID + Created At (Composite)
**Columns**: `tasks(user_id, created_at)`
**Type**: B-tree
**Purpose**: Sorted task retrieval (newest first)
**Query Pattern**: `SELECT * FROM tasks WHERE user_id = 123 ORDER BY created_at DESC`
**Performance**: O(log n) lookup, results already sorted

**Index Definition (SQL)**:
```sql
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

**SQLModel Auto-Indexing**:
- Primary keys: Auto-indexed
- Foreign keys: Auto-indexed
- Explicit `index=True` in Field definition

---

## Validation Rules

### User Validation

**Email Validation**:
```python
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

def validate_email(email: str) -> str:
    email = email.strip().lower()
    if not EMAIL_REGEX.match(email):
        raise ValueError("Invalid email format")
    return email
```

**Password Validation** (handled by Better Auth):
- Minimum 8 characters
- No maximum length (reasonable limit: 128 chars)
- No complexity requirements (Phase II simplicity)

### Task Validation

**Title Validation**:
```python
def validate_title(title: str) -> str:
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty")
    if len(title) > 200:
        raise ValueError("Task title exceeds 200 characters")
    return title
```

**Description Validation**:
```python
def validate_description(description: Optional[str]) -> Optional[str]:
    if description is None:
        return None
    description = description.strip()
    if len(description) > 2000:
        raise ValueError("Task description exceeds 2000 characters")
    return description if description else None
```

**Completion Status Validation**:
```python
def validate_is_completed(is_completed: bool) -> bool:
    if not isinstance(is_completed, bool):
        raise ValueError("is_completed must be true or false")
    return is_completed
```

---

## State Transitions

### Task State Machine

**States**:
1. **Incomplete** (`is_completed = false`) - Default state
2. **Complete** (`is_completed = true`) - User marked as done

**Transitions**:
```
┌─────────────┐          Mark Complete          ┌─────────────┐
│ Incomplete  │ ──────────────────────────────→ │  Complete   │
│ (default)   │                                  │             │
└─────────────┘ ←────────────────────────────── └─────────────┘
                      Mark Incomplete
```

**Valid Transitions**:
- Incomplete → Complete (user finishes task)
- Complete → Incomplete (user reopens task)

**Invalid Transitions**: None (all state changes allowed)

**Side Effects**:
- All transitions update `updated_at` timestamp
- No notification triggers (Phase II out of scope)

---

## Data Access Patterns

### Create User
```python
async def create_user(session: AsyncSession, email: str, password_hash: str) -> User:
    email = validate_email(email)
    user = User(email=email, password_hash=password_hash)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
```

### Get User by Email (for signin)
```python
async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    email = validate_email(email)
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
```

### Create Task (User-Scoped)
```python
async def create_task(
    session: AsyncSession,
    user_id: int,
    title: str,
    description: Optional[str] = None
) -> Task:
    title = validate_title(title)
    description = validate_description(description)

    task = Task(user_id=user_id, title=title, description=description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

### Get All User Tasks (Sorted by Newest)
```python
async def get_user_tasks(session: AsyncSession, user_id: int) -> List[Task]:
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    result = await session.execute(statement)
    return result.scalars().all()
```

### Get Single Task (with Ownership Verification)
```python
async def get_task(
    session: AsyncSession,
    task_id: int,
    user_id: int
) -> Optional[Task]:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # CRITICAL: Ownership check
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()
```

### Update Task (with Ownership Verification)
```python
async def update_task(
    session: AsyncSession,
    task_id: int,
    user_id: int,
    title: str,
    description: Optional[str] = None
) -> Optional[Task]:
    task = await get_task(session, task_id, user_id)
    if not task:
        return None  # Task doesn't exist or user doesn't own it

    task.title = validate_title(title)
    task.description = validate_description(description)
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)
    return task
```

### Toggle Task Completion (with Ownership Verification)
```python
async def toggle_task_completion(
    session: AsyncSession,
    task_id: int,
    user_id: int,
    is_completed: bool
) -> Optional[Task]:
    task = await get_task(session, task_id, user_id)
    if not task:
        return None

    task.is_completed = validate_is_completed(is_completed)
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)
    return task
```

### Delete Task (with Ownership Verification)
```python
async def delete_task(
    session: AsyncSession,
    task_id: int,
    user_id: int
) -> bool:
    task = await get_task(session, task_id, user_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True
```

---

## Security Considerations

### User Isolation Enforcement

**Database Layer**:
- Foreign key constraint: `tasks.user_id` MUST reference valid `users.id`
- Cascade delete: User deletion removes all associated tasks

**Query Layer**:
- ALL task queries filtered by `user_id` from JWT token
- NEVER trust client-supplied user IDs in query construction

**API Layer**:
- JWT middleware extracts authenticated `user_id`
- Compare JWT `user_id` with URL parameter
- Return 403 Forbidden if mismatch

### Data Sanitization

**Input Sanitization**:
- Trim whitespace from all string inputs
- Lowercase emails before storage
- Validate max lengths before database insertion

**Output Sanitization**:
- NEVER return `password_hash` in API responses
- Use Pydantic response models to exclude sensitive fields

**SQL Injection Prevention**:
- SQLModel ORM auto-parameterizes queries
- Never use string concatenation for SQL

---

## Performance Characteristics

### Query Performance (100 users, 100 tasks each = 10,000 rows)

**Get User Tasks** (with composite index):
- Index lookup: O(log 10000) ≈ 13 comparisons
- Scan user's tasks: O(100) rows
- Total: ~113 operations
- Without index: O(10000) full table scan

**Get Single Task**:
- Primary key lookup: O(log 10000) ≈ 13 comparisons
- Ownership check: Included in query (no additional cost)

**Create Task**:
- Insert: O(log 10000) for index update
- Foreign key check: O(log 100) for user existence

**Update Task**:
- Lookup: O(log 10000)
- Update: O(log 10000) for index update

**Delete Task**:
- Lookup: O(log 10000)
- Delete: O(log 10000) for index removal

### Scalability

**Current Architecture Supports**:
- 1,000 users: < 10ms query times
- 10,000 users: < 20ms query times
- 100,000 users: < 50ms query times (may need partitioning)

**Bottlenecks**:
- Single table for all tasks (future: partition by user_id range)
- No query result caching (future: Redis cache)

---

## Migration Strategy

### Phase II (Auto-Create)
```python
# backend/db.py
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

**Creates**:
- `users` table with all columns and indexes
- `tasks` table with all columns and indexes
- Foreign key constraints

### Future Phases (Alembic)
```bash
# Generate migration
alembic revision --autogenerate -m "Add due_date column"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

**Example Migration** (Adding `due_date` column):
```python
# alembic/versions/001_add_due_date.py
def upgrade():
    op.add_column('tasks', sa.Column('due_date', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('tasks', 'due_date')
```

---

## Data Retention

**Phase II Policy**:
- No automatic deletion
- User accounts persist indefinitely
- Tasks persist until explicitly deleted by user
- Soft deletes NOT implemented (hard deletes only)

**Future Considerations**:
- Archive completed tasks after 90 days (soft delete)
- Delete inactive accounts after 2 years
- Add `deleted_at` column for soft deletes

---

## Appendix: Complete SQL Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

---

**Data Model Status**: ✅ COMPLETE
**Date Completed**: 2026-01-17
**Validated By**: Claude Code (Spec-Driven Development Agent)
