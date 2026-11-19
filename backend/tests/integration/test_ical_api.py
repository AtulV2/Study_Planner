"""Integration test for /api/v1/calendar/feed.ics endpoint."""

from fastapi.testclient import TestClient


def test_ical_feed_export(client: TestClient):
    """Verifies iCalendar RFC 5545 feed generation and headers."""
    # Seed scenario first
    client.post("/api/v1/seed")

    response = client.get("/api/v1/calendar/feed.ics")
    assert response.status_code == 200
    assert "text/calendar" in response.headers["content-type"]
    assert "study_planner_schedule.ics" in response.headers["content-disposition"]

    content = response.text
    assert "BEGIN:VCALENDAR" in content
    assert "END:VCALENDAR" in content
    assert "BEGIN:VEVENT" in content
    assert "SUMMARY:" in content
    assert "UID:studyplanner-studyblock-" in content
