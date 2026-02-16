"""
Pytest configuration and shared fixtures.

Uses an in-memory SQLite database so tests never touch NeonDB.
Each test function gets a fresh database via the session-scoped engine
and function-scoped session override.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# In-memory SQLite for tests (no external DB required)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

test_session_maker = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    """Create all tables once per test session."""
    # Import models to register them with SQLModel metadata
    from models import User, Task  # noqa: F401

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(autouse=True)
async def clean_tables():
    """Truncate all rows between tests for isolation."""
    yield
    async with test_session_maker() as session:
        from sqlalchemy import text
        await session.execute(text("DELETE FROM tasks"))
        await session.execute(text("DELETE FROM users"))
        await session.commit()


@pytest_asyncio.fixture
async def client():
    """
    Async HTTP test client with DB dependency overridden to use in-memory SQLite.
    """
    from main import app
    from db import get_session

    async def override_get_session():
        async with test_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def registered_user(client: AsyncClient):
    """Register a user and return {token, user} from the signup response."""
    resp = await client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "password123",
    })
    assert resp.status_code == 201
    return resp.json()


@pytest_asyncio.fixture
async def auth_headers(registered_user):
    """Return Authorization headers for the registered test user."""
    token = registered_user["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def user_id(registered_user):
    """Return the integer user_id of the registered test user."""
    return registered_user["user"]["id"]
