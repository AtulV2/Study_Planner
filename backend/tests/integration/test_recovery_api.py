"""Integration tests for /api/v1/recovery endpoints."""

from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient


def test_recovery_endpoints_flow(client: TestClient):
    """Verifies preview, auto-heal, triage, shift-today, micro-action, and history endpoints."""
    # Seed scenario
    seed_res = client.post("/api/v1/seed")
    assert seed_res.status_code == 200

    # 1. Test preview recovery (200)
    prev_res = client.post("/api/v1/recovery/preview")
    assert prev_res.status_code == 200
    prev_data = prev_res.json()
    assert "disrupted_count" in prev_data
    assert "changes" in prev_data

    # 2. Test auto-heal (200)
    heal_res = client.post("/api/v1/recovery/auto-heal")
    assert heal_res.status_code == 200
    assert heal_res.json()["status"] == "success"

    # 3. Test micro-action (200)
    micro_res = client.get("/api/v1/recovery/micro-action")
    assert micro_res.status_code == 200
    assert micro_res.json() is not None

    # 4. Test shift-today (200)
    shift_res = client.post("/api/v1/recovery/shift-today", json={"shift_minutes": 60})
    assert shift_res.status_code == 200

    # 5. Test triage MVP (200)
    triage_res = client.post("/api/v1/recovery/triage-mvp")
    assert triage_res.status_code == 200

    # 6. Test history (200)
    hist_res = client.get("/api/v1/recovery/history")
    assert hist_res.status_code == 200
    history_events = hist_res.json()
    assert len(history_events) >= 3
