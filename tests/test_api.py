"""
API Routes Tests

Tests for API endpoints.
"""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Flowfull Python Starter"
    assert data["version"] == "0.1.0"
    assert "environment" in data


def test_public_route(client: TestClient) -> None:
    """Test public route without authentication."""
    response = client.get("/api/v1/public")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "This is a public route"
    assert data["authenticated"] is False


def test_protected_route_without_auth(client: TestClient) -> None:
    """Test protected route without authentication should fail."""
    response = client.get("/api/v1/protected")

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_profile_route_without_auth(client: TestClient) -> None:
    """Test profile route without authentication should fail."""
    response = client.get("/api/v1/profile")

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_content_route_without_auth(client: TestClient) -> None:
    """Test content route without authentication (should work as guest)."""
    response = client.get("/api/v1/content")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome, guest!"
    assert data["authenticated"] is False
    assert data["premium_content"] is False
