"""Integration tests for /api/v1/health and /api/v1/config endpoints."""

from fastapi.testclient import TestClient


def test_health_and_config_workflow(client: TestClient):
    """Verifies health check diagnostics and student configuration PATCH."""
    # 1. Health check (200)
    health_res = client.get("/api/v1/health")
    assert health_res.status_code == 200
    assert health_res.json()["status"] == "healthy"
    assert health_res.json()["database"] == "connected"

    # 2. Get config (200)
    config_res = client.get("/api/v1/config")
    assert config_res.status_code == 200
    data = config_res.json()
    assert data["max_daily_study_hours"] == 5.5
    assert data["wake_time"] == "08:00"

    # 3. Patch config (200)
    patch_res = client.patch(
        "/api/v1/config",
        json={"max_daily_study_hours": 6.0, "wake_time": "07:30"},
    )
    assert patch_res.status_code == 200
    updated = patch_res.json()
    assert updated["max_daily_study_hours"] == 6.0
    assert updated["wake_time"] == "07:30"
