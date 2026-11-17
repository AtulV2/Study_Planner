"""Integration tests for /api/v1/courses endpoints."""

from fastapi.testclient import TestClient


def test_courses_crud_workflow(client: TestClient):
    """Verifies complete CRUD lifecycle on courses."""
    # 1. Create Course (201 Created)
    payload = {
        "code": "CS 240",
        "name": "Data Structures & Algorithms",
        "color": "#3B82F6",
        "instructor": "Dr. Sarah Chen",
    }
    response = client.post("/api/v1/courses", json=payload)
    assert response.status_code == 201
    data = response.json()
    course_id = data["id"]
    assert data["code"] == "CS 240"
    assert data["name"] == "Data Structures & Algorithms"

    # 2. Duplicate rejection (400)
    dup_res = client.post("/api/v1/courses", json=payload)
    assert dup_res.status_code == 400

    # 3. List Courses (200)
    list_res = client.get("/api/v1/courses")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # 4. Patch Course (200)
    patch_res = client.patch(f"/api/v1/courses/{course_id}", json={"name": "Advanced Data Structures"})
    assert patch_res.status_code == 200
    assert patch_res.json()["name"] == "Advanced Data Structures"

    # 5. Delete Course (204 No Content)
    del_res = client.delete(f"/api/v1/courses/{course_id}")
    assert del_res.status_code == 204
    assert del_res.text == ""

    # 6. Verify deleted (404)
    get_res = client.patch(f"/api/v1/courses/{course_id}", json={"name": "Ghost Course"})
    assert get_res.status_code == 404
