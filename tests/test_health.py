"""
Health Check Tests

Tests for health check endpoints.
"""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Test basic health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "environment" in data
    assert "version" in data


def test_detailed_health_check(client: TestClient) -> None:
    """Test detailed health check endpoint."""
    response = client.get("/health/detailed")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data
    assert "database" in data["components"]
    assert "cache" in data["components"]


def test_cache_health(client: TestClient) -> None:
    """Test cache health endpoint."""
    response = client.get("/health/cache")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "cache_stats" in data


def test_database_health(client: TestClient) -> None:
    """Test database health endpoint."""
    response = client.get("/health/database")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database_type" in data
