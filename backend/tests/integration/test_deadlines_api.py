"""Integration tests for /api/v1/deadlines and auto-scheduling endpoints."""

from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient


def test_deadlines_crud_and_autoschedule(client: TestClient):
    """Verifies creating deadline, auto-scheduling study blocks, and deleting with cascades."""
    c_res = client.post(
        "/api/v1/courses",
        json={"code": "CS 240", "name": "Data Structures", "color": "#3B82F6"},
    )
    course_id = c_res.json()["id"]

    due_dt = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()
    # 1. Create Deadline (201)
    payload = {
        "course_id": course_id,
        "title": "Problem Set 3",
        "due_datetime": due_dt,
        "estimated_hours": 3.0,
        "priority": "high",
        "notes": "Red-Black Tree balance tests",
    }
    create_res = client.post("/api/v1/deadlines", json=payload)
    assert create_res.status_code == 201
    deadline_id = create_res.json()["id"]

    # 2. Trigger auto-schedule for this deadline (200)
    sched_res = client.post(f"/api/v1/deadlines/{deadline_id}/auto-schedule")
    assert sched_res.status_code == 200
    blocks = sched_res.json()
    assert len(blocks) > 0

    # 3. List Study Blocks (200)
    blocks_res = client.get("/api/v1/study-blocks")
    assert blocks_res.status_code == 200
    assert len(blocks_res.json()) == len(blocks)

    # 4. Delete deadline (204) and ensure cascade deletes study blocks
    del_res = client.delete(f"/api/v1/deadlines/{deadline_id}")
    assert del_res.status_code == 204

    # Verify blocks are gone
    remaining_blocks = client.get("/api/v1/study-blocks").json()
    assert len(remaining_blocks) == 0
