"""API endpoint tests."""
import pytest
from fastapi.testclient import TestClient
from agentic_workflows.api.server import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_readiness_check():
    response = client.get("/api/ready")
    assert response.status_code == 200

def test_liveness_check():
    response = client.get("/api/live")
    assert response.status_code == 200

def test_list_workflows():
    response = client.get("/api/workflows/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_plugins():
    response = client.get("/api/plugins/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 3  # At least 3 built-in plugins
