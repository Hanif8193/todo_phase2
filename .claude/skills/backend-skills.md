# Backend Skills for FastAPI + SQLModel Applications

## Overview
This document defines backend-specific technical skills for building secure, scalable APIs using FastAPI, SQLModel, and PostgreSQL. These skills ensure proper API design, authentication security, database modeling, and multi-tenant data isolation.

---

## 1. REST API Design

### Purpose
Design consistent, predictable, and scalable RESTful APIs following HTTP standards and best practices.

### Key Capabilities
- **Resource Modeling**: Map domain entities to RESTful resources
- **HTTP Method Selection**: Choose appropriate verbs (GET, POST, PUT, PATCH, DELETE)
- **Status Code Usage**: Return semantically correct HTTP status codes
- **Request/Response Design**: Structure payloads for clarity and extensibility
- **Error Handling**: Provide actionable error messages with proper codes

### RESTful Resource Patterns

```python
# Resource: /api/tasks

# GET /api/tasks - List all tasks (with pagination)
# Response: 200 OK
{
  "items": [
    {"id": 1, "title": "Task 1", "status": "pending"},
    {"id": 2, "title": "Task 2", "status": "completed"}
  ],
  "total": 2,
  "page": 1,
  "page_size": 20
}

# GET /api/tasks/{id} - Retrieve single task
# Response: 200 OK, 404 Not Found
{
  "id": 1,
  "title": "Task 1",
  "description": "Details...",
  "status": "pending",
  "created_at": "2026-01-17T10:00:00Z",
  "updated_at": "2026-01-17T10:00:00Z"
}

# POST /api/tasks - Create new task
# Request:
{
  "title": "New Task",
  "description": "Optional description"
}
# Response: 201 Created (with Location header)
{
  "id": 3,
  "title": "New Task",
  "status": "pending",
  "created_at": "2026-01-17T11:00:00Z"
}

# PUT /api/tasks/{id} - Full replacement
# PATCH /api/tasks/{id} - Partial update
# Request:
{
  "status": "completed"
}
# Response: 200 OK, 404 Not Found

# DELETE /api/tasks/{id}
# Response: 204 No Content, 404 Not Found
```

### FastAPI Implementation Pattern

```python
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# Request/Response Models
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int

# Endpoints
@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user)
):
    """List all tasks with pagination"""
    pass

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get a specific task by ID"""
    task = await get_task_by_id(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new task"""
    return await create_task_for_user(task, current_user.id)

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    """Partially update a task"""
    existing_task = await get_task_by_id(task_id, current_user.id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return await update_task_partial(existing_task, task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user)
):
    """Delete a task"""
    deleted = await delete_task_by_id(task_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
```

### HTTP Status Code Guidelines

```text
Success Codes:
- 200 OK: Standard success response (GET, PUT, PATCH)
- 201 Created: Resource created (POST)
- 204 No Content: Success with no body (DELETE)

Client Error Codes:
- 400 Bad Request: Malformed request or validation failure
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Authenticated but not authorized
- 404 Not Found: Resource doesn't exist
- 409 Conflict: Resource conflict (duplicate, version mismatch)
- 422 Unprocessable Entity: Semantic validation error

Server Error Codes:
- 500 Internal Server Error: Unexpected server failure
- 503 Service Unavailable: Temporary outage
```

### Success Criteria
- Consistent URL patterns across resources
- Appropriate HTTP methods and status codes
- Clear request/response schemas with Pydantic models
- Proper error responses with actionable messages
- Pagination support for list endpoints

---

## 2. JWT Security Patterns

### Purpose
Implement secure authentication and authorization using JSON Web Tokens (JWT) with proper token lifecycle management.

### Key Capabilities
- **Token Generation**: Create secure JWTs with appropriate claims
- **Token Validation**: Verify signature, expiration, and claims
- **Refresh Token Flow**: Implement secure token renewal
- **Token Revocation**: Handle logout and token invalidation
- **Secret Management**: Protect signing keys and sensitive data

### JWT Structure

```text
JWT = <header>.<payload>.<signature>

Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload (Claims):
{
  "sub": "user_id",           # Subject (user identifier)
  "exp": 1737198000,          # Expiration timestamp
  "iat": 1737194400,          # Issued at timestamp
  "jti": "unique_token_id",   # JWT ID (for revocation)
  "email": "user@example.com", # Custom claim
  "role": "admin"              # Custom claim
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

### Implementation Pattern

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Never hardcode!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

security = HTTPBearer()

# Models
class TokenData(BaseModel):
    user_id: int
    email: str
    role: Optional[str] = None

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Token Generation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4())  # Unique token ID for revocation
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: int):
    """Create a long-lived refresh token"""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token Validation
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Validate JWT and return current user"""
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode and verify token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        # Check if token is revoked (check against database/cache)
        jti = payload.get("jti")
        if await is_token_revoked(jti):
            raise credentials_exception

        # Fetch user from database
        user = await get_user_by_id(int(user_id))
        if user is None:
            raise credentials_exception

        return user

    except JWTError:
        raise credentials_exception

# Login Endpoint
@router.post("/auth/login", response_model=TokenPair)
async def login(email: str, password: str):
    """Authenticate user and return token pair"""
    user = await authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    refresh_token = create_refresh_token(user.id)

    # Store refresh token in database for revocation tracking
    await store_refresh_token(user.id, refresh_token)

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token
    )

# Refresh Endpoint
@router.post("/auth/refresh", response_model=TokenPair)
async def refresh_token(refresh_token: str):
    """Issue new access token using refresh token"""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = int(payload.get("sub"))

        # Verify refresh token exists in database
        if not await verify_refresh_token(user_id, refresh_token):
            raise HTTPException(status_code=401, detail="Token revoked")

        user = await get_user_by_id(user_id)

        # Issue new access token
        new_access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )

        return TokenPair(
            access_token=new_access_token,
            refresh_token=refresh_token
        )

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

# Logout Endpoint
@router.post("/auth/logout", status_code=204)
async def logout(
    refresh_token: str,
    current_user: User = Depends(get_current_user)
):
    """Revoke refresh token"""
    await revoke_refresh_token(current_user.id, refresh_token)
```

### Security Best Practices

```text
1. Secret Management:
   - Store JWT_SECRET_KEY in environment variables
   - Use strong random keys (at least 256 bits)
   - Rotate secrets periodically
   - Never commit secrets to version control

2. Token Expiration:
   - Access tokens: Short-lived (15-30 minutes)
   - Refresh tokens: Longer-lived (7-30 days)
   - Always include 'exp' claim

3. Token Storage (Client-side):
   - Access token: Memory or sessionStorage
   - Refresh token: HttpOnly cookie (preferred) or secure storage
   - Never store in localStorage (XSS vulnerable)

4. Token Revocation:
   - Store refresh tokens in database
   - Implement logout to revoke tokens
   - Track token JTI for access token revocation
   - Use Redis for fast revocation checks

5. Transport Security:
   - Always use HTTPS in production
   - Set proper CORS policies
   - Include tokens in Authorization header, not URL params
```

### Success Criteria
- Tokens have proper expiration times
- Secret keys stored in environment variables
- Refresh token flow implemented
- Token revocation on logout
- HTTPS enforced in production

---

## 3. SQLModel Schema Design

### Purpose
Design type-safe, maintainable database schemas using SQLModel that balance normalization, performance, and application needs.

### Key Capabilities
- **Entity Modeling**: Map domain concepts to database tables
- **Relationship Design**: Define one-to-many, many-to-many associations
- **Type Safety**: Leverage Python type hints for validation
- **Migration Planning**: Design schema changes for safe evolution
- **Index Strategy**: Optimize query performance

### SQLModel Patterns

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums for constrained values
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# Base Model (shared fields)
class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# User Model
class User(TimestampMixin, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    role: str = Field(default="user", max_length=50)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "role": "user"
            }
        }

# Task Model
class Task(TimestampMixin, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, index=True)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)

    # Foreign Key (user data isolation)
    user_id: int = Field(foreign_key="users.id", index=True)

    # Relationships
    user: User = Relationship(back_populates="tasks")
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model="TaskTag")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write API docs and deployment guide",
                "status": "pending",
                "priority": "high"
            }
        }

# Tag Model (many-to-many example)
class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=100, index=True)
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color

    # Relationships
    tasks: List[Task] = Relationship(back_populates="tags", link_model="TaskTag")

# Join Table for Many-to-Many
class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
```

### Schema Design Principles

```text
1. Normalization:
   - Avoid data duplication
   - Use foreign keys for relationships
   - Create join tables for many-to-many

2. Type Safety:
   - Use Python type hints (int, str, Optional[T])
   - Leverage Enums for constrained values
   - Define max_length for string fields

3. Indexing Strategy:
   - Index foreign keys (user_id)
   - Index frequently queried fields (email, status)
   - Index fields used in WHERE/ORDER BY clauses
   - Avoid over-indexing (impacts write performance)

4. Constraints:
   - Unique constraints (email, composite keys)
   - NOT NULL for required fields
   - Foreign key constraints for referential integrity
   - Check constraints (min/max values)

5. Timestamps:
   - Always include created_at, updated_at
   - Use UTC timezone (datetime.utcnow)
   - Consider soft deletes (deleted_at field)
```

### Migration Pattern (Alembic)

```python
# alembic/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Create Date: 2026-01-17
"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
```

### Success Criteria
- All tables have primary keys
- Foreign keys properly defined with indexes
- Appropriate constraints (unique, not null)
- Timestamp fields on all tables
- Enums used for constrained values

---

## 4. Async Database Handling

### Purpose
Efficiently manage database connections and queries using async/await patterns for high concurrency and performance.

### Key Capabilities
- **Connection Pooling**: Manage database connections efficiently
- **Async Queries**: Execute non-blocking database operations
- **Transaction Management**: Handle ACID operations correctly
- **Error Handling**: Gracefully handle database errors
- **Performance Optimization**: Use batching, eager loading

### Async Database Setup

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
import os

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")  # postgresql+asyncpg://user:pass@host/db

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL (disable in production)
    pool_size=10,  # Number of persistent connections
    max_overflow=20,  # Additional connections when pool exhausted
    pool_pre_ping=True,  # Verify connections before use
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Allow access to objects after commit
)

# Dependency for FastAPI
async def get_session() -> AsyncSession:
    """Provide database session to endpoints"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### CRUD Operations

```python
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

# CREATE
async def create_task(session: AsyncSession, task: Task) -> Task:
    """Create a new task"""
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

# READ - Single
async def get_task_by_id(
    session: AsyncSession,
    task_id: int,
    user_id: int
) -> Optional[Task]:
    """Get task by ID with user isolation"""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()

# READ - Multiple
async def get_user_tasks(
    session: AsyncSession,
    user_id: int,
    status: Optional[TaskStatus] = None,
    skip: int = 0,
    limit: int = 20
) -> List[Task]:
    """Get paginated tasks for a user"""
    statement = select(Task).where(Task.user_id == user_id)

    if status:
        statement = statement.where(Task.status == status)

    statement = statement.offset(skip).limit(limit).order_by(Task.created_at.desc())

    result = await session.execute(statement)
    return result.scalars().all()

# UPDATE
async def update_task(
    session: AsyncSession,
    task: Task,
    update_data: dict
) -> Task:
    """Update task with partial data"""
    for key, value in update_data.items():
        if value is not None:
            setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)
    return task

# DELETE
async def delete_task(
    session: AsyncSession,
    task_id: int,
    user_id: int
) -> bool:
    """Delete task with user isolation"""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True
```

### Transaction Management

```python
async def transfer_task_ownership(
    session: AsyncSession,
    task_id: int,
    from_user_id: int,
    to_user_id: int
) -> Task:
    """Transfer task ownership atomically"""
    async with session.begin():  # Start transaction
        # Verify source user owns task
        task = await get_task_by_id(session, task_id, from_user_id)
        if not task:
            raise ValueError("Task not found or not owned by user")

        # Verify target user exists
        target_user = await get_user_by_id(session, to_user_id)
        if not target_user:
            raise ValueError("Target user not found")

        # Transfer ownership
        task.user_id = to_user_id
        task.updated_at = datetime.utcnow()

        # Transaction auto-commits on context exit
        # Rolls back on exception

    await session.refresh(task)
    return task
```

### Eager Loading (N+1 Prevention)

```python
from sqlalchemy.orm import selectinload

async def get_tasks_with_tags(
    session: AsyncSession,
    user_id: int
) -> List[Task]:
    """Load tasks with related tags in single query"""
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .options(selectinload(Task.tags))  # Eager load tags
    )
    result = await session.execute(statement)
    return result.scalars().all()
```

### Batch Operations

```python
async def bulk_create_tasks(
    session: AsyncSession,
    tasks: List[Task]
) -> List[Task]:
    """Create multiple tasks efficiently"""
    session.add_all(tasks)
    await session.commit()

    for task in tasks:
        await session.refresh(task)

    return tasks

async def bulk_update_status(
    session: AsyncSession,
    task_ids: List[int],
    user_id: int,
    new_status: TaskStatus
) -> int:
    """Update status for multiple tasks"""
    statement = (
        update(Task)
        .where(
            Task.id.in_(task_ids),
            Task.user_id == user_id
        )
        .values(status=new_status, updated_at=datetime.utcnow())
    )
    result = await session.execute(statement)
    await session.commit()
    return result.rowcount
```

### Error Handling

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

async def create_user_safe(session: AsyncSession, user: User) -> User:
    """Create user with error handling"""
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower():
            raise ValueError("User with this email already exists")
        raise

    except SQLAlchemyError as e:
        await session.rollback()
        raise RuntimeError(f"Database error: {str(e)}")
```

### Success Criteria
- All database operations use async/await
- Connection pooling configured
- Transactions used for multi-step operations
- N+1 queries prevented with eager loading
- Proper error handling and rollback

---

## 5. User Data Isolation

### Purpose
Ensure users can only access their own data through automatic filtering and authorization checks at the database and API layers.

### Key Capabilities
- **Automatic Filtering**: Add user_id clauses to all queries
- **Authorization Checks**: Verify ownership before modifications
- **Multi-Tenancy**: Support multiple users with isolated data
- **Audit Logging**: Track data access for security
- **Defensive Programming**: Fail closed on authorization errors

### Data Isolation Patterns

```python
# 1. Database Layer - Always filter by user_id
async def get_user_tasks(
    session: AsyncSession,
    user_id: int,
    filters: Optional[dict] = None
) -> List[Task]:
    """CORRECT: Always include user_id filter"""
    statement = select(Task).where(Task.user_id == user_id)

    # Add additional filters
    if filters:
        if filters.get("status"):
            statement = statement.where(Task.status == filters["status"])

    result = await session.execute(statement)
    return result.scalars().all()

# INCORRECT - Missing user isolation
async def get_all_tasks_INSECURE(session: AsyncSession) -> List[Task]:
    """ANTI-PATTERN: No user filtering"""
    statement = select(Task)  # ❌ Returns all users' tasks!
    result = await session.execute(statement)
    return result.scalars().all()

# 2. API Layer - Extract user from JWT
@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)  # ✅ Get user from JWT
):
    """List only current user's tasks"""
    tasks = await get_user_tasks(session, current_user.id)
    return tasks

# 3. Authorization Checks - Verify ownership
@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete task with ownership verification"""
    # Fetch with user filter
    task = await get_task_by_id(session, task_id, current_user.id)

    if not task:
        # Don't leak existence - return 404 for both cases
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()

    return {"message": "Task deleted"}
```

### Multi-Tenancy Schema Design

```python
# All tables should have user_id foreign key
class Task(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    # ✅ User isolation field
    user_id: int = Field(foreign_key="users.id", index=True)

    user: User = Relationship(back_populates="tasks")

# Composite unique constraints for multi-tenancy
class UserSettings(SQLModel, table=True):
    __tablename__ = "user_settings"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    key: str = Field(max_length=100)
    value: str

    # ✅ Ensure unique keys per user
    __table_args__ = (
        UniqueConstraint('user_id', 'key', name='uq_user_settings'),
    )
```

### Repository Pattern with Isolation

```python
class TaskRepository:
    """Encapsulate data access with automatic user isolation"""

    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID (auto-filtered by user)"""
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == self.user_id  # ✅ Automatic isolation
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 20) -> List[Task]:
        """List tasks (auto-filtered by user)"""
        statement = (
            select(Task)
            .where(Task.user_id == self.user_id)  # ✅ Automatic isolation
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, task_data: TaskCreate) -> Task:
        """Create task (auto-assigned to user)"""
        task = Task(
            **task_data.dict(),
            user_id=self.user_id  # ✅ Automatic assignment
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update task (auto-verified ownership)"""
        task = await self.get_by_id(task_id)  # Uses isolated query
        if not task:
            return None

        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

# Usage in endpoint
@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List tasks using repository pattern"""
    repo = TaskRepository(session, current_user.id)
    tasks = await repo.list()
    return tasks
```

### Audit Logging

```python
class AuditLog(TimestampMixin, table=True):
    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    action: str = Field(max_length=50)  # CREATE, READ, UPDATE, DELETE
    resource_type: str = Field(max_length=50)  # task, user, etc.
    resource_id: int
    ip_address: Optional[str] = Field(max_length=45)
    user_agent: Optional[str]

async def log_access(
    session: AsyncSession,
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: int,
    request: Request
):
    """Log data access for security auditing"""
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    session.add(log)
    await session.commit()
```

### Security Checklist

```text
✅ All queries include user_id filter
✅ User extracted from JWT (Depends(get_current_user))
✅ Foreign keys indexed for performance
✅ 404 returned for both missing and unauthorized resources (don't leak existence)
✅ Repository pattern encapsulates isolation logic
✅ Audit logs track data access
✅ Integration tests verify isolation
✅ No raw SQL without parameterization
```

### Success Criteria
- All database queries filtered by user_id
- Current user extracted from JWT in all endpoints
- Authorization checks before all modifications
- Repository pattern used for consistent isolation
- Audit logging for sensitive operations
- Integration tests verify users can't access others' data

---

## Integration Example: Complete CRUD with All Skills

```python
# main.py - Complete FastAPI application
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os

app = FastAPI(title="Task API", version="1.0.0")
security = HTTPBearer()

# Database setup (Skill 4)
from database import get_session

# Models (Skill 3)
from models import User, Task, TaskCreate, TaskUpdate, TaskResponse

# Auth (Skill 2)
from auth import get_current_user

# Repository (Skill 5)
from repositories import TaskRepository

# REST API (Skill 1)
@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new task"""
    repo = TaskRepository(session, current_user.id)
    task = await repo.create(task_data)
    return task

@app.get("/api/tasks", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all tasks for current user"""
    repo = TaskRepository(session, current_user.id)
    tasks = await repo.list(skip=skip, limit=limit)
    return tasks

@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific task"""
    repo = TaskRepository(session, current_user.id)
    task = await repo.get_by_id(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.patch("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a task"""
    repo = TaskRepository(session, current_user.id)
    task = await repo.update(task_id, task_data)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a task"""
    repo = TaskRepository(session, current_user.id)
    deleted = await repo.delete(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
```

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- SQLAlchemy Async: https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html
- JWT Best Practices: https://tools.ietf.org/html/rfc8725
- Python Jose (JWT): https://python-jose.readthedocs.io/
- `.specify/memory/constitution.md` - Project-specific security standards
