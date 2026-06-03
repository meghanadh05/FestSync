"""
Tests for health check endpoints.
"""

import pytest


class TestHealthCheck:
    """Health check endpoint tests."""

    def test_health_check(self, client):
        """Test basic health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "FestSync API"
        assert "version" in data

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data

    def test_api_v1_status(self, client):
        """Test API v1 status endpoint."""
        response = client.get("/api/v1/status")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
        assert data["version"] == "1.0.0"
