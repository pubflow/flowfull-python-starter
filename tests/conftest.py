"""
Pytest Configuration and Fixtures

This module provides shared fixtures for testing.
"""

import asyncio
from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.lib.database.connection import Base
from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> TestClient:
    """
    Create test client.

    Returns:
        FastAPI test client
    """
    return TestClient(app)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create test database session.

    Yields:
        Test database session
    """
    # Create in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    # Cleanup
    await engine.dispose()


@pytest.fixture
def mock_session_data() -> dict:
    """
    Mock session data for testing.

    Returns:
        Mock session data dictionary
    """
    return {
        "user_id": "test-user-123",
        "email": "test@example.com",
        "name": "Test User",
        "user_type": "user",
        "organization_id": "test-org-123",
        "permissions": ["read", "write"],
        "expires_at": "2024-12-31T23:59:59Z",
        "validated_at": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_session_id() -> str:
    """
    Mock session ID for testing.

    Returns:
        Mock session ID
    """
    return "test-session-id-12345678"
