"""Integration tests for /api/v1/commitments endpoints."""

from fastapi.testclient import TestClient


def test_commitments_crud_workflow(client: TestClient):
    """Verifies creating, listing, updating, and deleting fixed commitments."""
    # Create course first
    c_res = client.post(
        "/api/v1/courses",
        json={"code": "MATH 215", "name": "Calculus", "color": "#10B981"},
    )
    course_id = c_res.json()["id"]

    # 1. Create Commitment (201)
    payload = {
        "course_id": course_id,
        "title": "MATH 215 Discussion",
        "commitment_type": "discussion",
        "day_of_week": 1,
        "start_time": "14:00",
        "end_time": "15:30",
        "location": "Euler Hall 204",
        "status": "scheduled",
    }
    create_res = client.post("/api/v1/commitments", json=payload)
    assert create_res.status_code == 201
    data = create_res.json()
    comm_id = data["id"]
    assert data["start_time"] == "14:00"

    # 2. List Commitments (200)
    list_res = client.get("/api/v1/commitments")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # 3. Patch Commitment (200)
    patch_res = client.patch(f"/api/v1/commitments/{comm_id}", json={"status": "completed"})
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "completed"

    # 4. Delete Commitment (204)
    del_res = client.delete(f"/api/v1/commitments/{comm_id}")
    assert del_res.status_code == 204
    assert del_res.text == ""
