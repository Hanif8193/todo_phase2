"""
Database configuration and connection management.

This module handles:
- SQLite database for development/testing
- SQLModel engine and session configuration
- Database initialization and table creation
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment, default to SQLite for easy setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app.db")

# Use SQLite for development (no external dependencies needed)
if DATABASE_URL.startswith("postgresql://"):
    # Convert postgresql:// to postgresql+asyncpg:// for async support
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    # Replace sslmode with ssl for asyncpg
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("sslmode=", "ssl=")
elif DATABASE_URL.startswith("sqlite"):
    # Ensure SQLite uses async driver
    if "aiosqlite" not in DATABASE_URL:
        ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
    else:
        ASYNC_DATABASE_URL = DATABASE_URL
else:
    # Default to SQLite with async support
    ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./todo_app.db"

# Create async engine for database operations
# For serverless (Vercel), use smaller pool to avoid connection limits
# NeonDB pooler supports up to 10000 connections, but each function instance should use fewer
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,  # Disable SQL logging in production for performance
    future=True,
    pool_size=5,  # Smaller pool for serverless
    max_overflow=10,  # Limited overflow for serverless
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """
    Initialize database by creating all tables.

    This function should be called on application startup.
    It creates all tables defined in SQLModel schemas.
    """
    async with engine.begin() as conn:
        # Import models to ensure they're registered with SQLModel
        from models import User, Task

        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Database tables created successfully")


async def get_session() -> AsyncSession:
    """
    Dependency function for FastAPI to provide database sessions.

    Usage in FastAPI routes:
        @app.get("/endpoint")
        async def endpoint(session: AsyncSession = Depends(get_session)):
            # Use session here
            pass

    Yields:
        AsyncSession: Database session that automatically commits/rollbacks
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def close_db():
    """
    Close database connections.

    This function should be called on application shutdown.
    """
    await engine.dispose()
    print("Database connections closed")
