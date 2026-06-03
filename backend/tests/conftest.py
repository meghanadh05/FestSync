"""
Pytest configuration and shared fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app


# Test database URL (uses SQLite for testing)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def test_db():
    """Create a test database and session."""
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestingSessionLocal()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def mock_user_token():
    """Create a mock JWT token for testing."""
    from app.core.security import create_access_token

    token = create_access_token(
        data={
            "sub": "test-user-id",
            "email": "test@example.com",
        }
    )
    return token


@pytest.fixture
def headers_with_token(mock_user_token):
    """Create authorization headers with mock token."""
    return {
        "Authorization": f"Bearer {mock_user_token}",
        "Content-Type": "application/json",
    }
