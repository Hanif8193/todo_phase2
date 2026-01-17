"""
SQLModel database schemas for User and Task entities.

This module defines:
- User model for authentication and user management
- Task model for todo items with user ownership
- Database indexes for query optimization
"""

from sqlmodel import SQLModel, Field, Relationship, Column, Index
from sqlalchemy import String, Text, Boolean, TIMESTAMP
from typing import Optional, List
from datetime import datetime


class User(SQLModel, table=True):
    """
    User model for authentication and account management.

    Attributes:
        id: Primary key, auto-incremented
        email: Unique email address for signin
        password_hash: Bcrypt hashed password (never store plaintext!)
        created_at: Account creation timestamp

    Relationships:
        tasks: One-to-many relationship with Task model
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False, index=True)
    )
    password_hash: str = Field(sa_column=Column(String(255), nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(TIMESTAMP, nullable=False),
    )

    # Relationship to tasks (one user has many tasks)
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    class Config:
        """Pydantic configuration for the User model."""

        arbitrary_types_allowed = True


class Task(SQLModel, table=True):
    """
    Task model for todo items with user ownership and completion tracking.

    Attributes:
        id: Primary key, auto-incremented
        user_id: Foreign key to users table (owner of this task)
        title: Task title (required, max 200 characters)
        description: Optional task description (max 2000 characters)
        is_completed: Completion status (default: False)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp (auto-updated)

    Relationships:
        user: Many-to-one relationship with User model

    Indexes:
        - (user_id, created_at): Composite index for user-scoped queries
    """

    __tablename__ = "tasks"
    __table_args__ = (
        # Composite index for efficient user-scoped queries ordered by creation time
        Index("idx_tasks_user_created", "user_id", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(sa_column=Column(String(200), nullable=False))
    description: Optional[str] = Field(
        default=None, sa_column=Column(Text, nullable=True)
    )
    is_completed: bool = Field(default=False, sa_column=Column(Boolean, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(TIMESTAMP, nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(TIMESTAMP, nullable=False),
    )

    # Relationship to user (many tasks belong to one user)
    user: Optional[User] = Relationship(back_populates="tasks")

    class Config:
        """Pydantic configuration for the Task model."""

        arbitrary_types_allowed = True


# Pydantic models for API request/response (without database-specific fields)


class UserCreate(SQLModel):
    """Request model for user registration."""

    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=100)


class UserLogin(SQLModel):
    """Request model for user signin."""

    email: str
    password: str


class UserResponse(SQLModel):
    """Response model for user data (excludes password_hash)."""

    id: int
    email: str
    created_at: datetime


class TaskCreate(SQLModel):
    """Request model for task creation."""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskUpdate(SQLModel):
    """Request model for task updates."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskResponse(SQLModel):
    """Response model for task data."""

    id: int
    user_id: int
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime


class TaskCompletionToggle(SQLModel):
    """Request model for toggling task completion status."""

    is_completed: bool
