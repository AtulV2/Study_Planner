# API Reference

This document provides a reference for the **Study Planner** REST API endpoints under `/api/v1`.

Interactive OpenAPI documentation is also served at `http://localhost:8000/docs`.

---

## 1. Global Conventions

- **Base URL:** `/api/v1`
- **Request & Response Body:** `application/json` (except `/calendar/feed.ics` which returns `text/calendar`)
- **Datetime Format:** ISO 8601 strings in UTC (e.g., `2026-11-20T14:00:00Z`)

### Standard Error Response (RFC 7807 Problem Details)
```json
{
  "type": "https://errors.studyplanner.app/capacity-exceeded",
  "title": "Capacity Exceeded",
  "status": 409,
  "detail": "Scheduling this session exceeds the 5.5 hour daily study capacity limit.",
  "instance": "/api/v1/deadlines/1/schedule",
  "invalid_params": []
}
```

---

## 2. System & Diagnostics

### `GET /api/v1/health`
Checks server and database health status.
- **Response `200 OK`:**
  ```json
  {
    "status": "healthy",
    "version": "1.0.0",
    "database": "connected"
  }
  ```

### `POST /api/v1/seed`
Populates sample academic courses, class commitments, and deadlines for testing.
- **Response `200 OK`:**
  ```json
  {
    "status": "success",
    "message": "Academic scenario seeded successfully."
  }
  ```

---

## 3. Courses

### `GET /api/v1/courses`
Lists all enrolled academic courses.

### `POST /api/v1/courses`
Enrolls a new course.
- **Request Body:**
  ```json
  {
    "code": "CS 101",
    "name": "Introduction to Computer Science",
    "color": "#2563EB",
    "credits": 4
  }
  ```
- **Response `201 Created`**

### `PATCH /api/v1/courses/{course_id}`
Updates course attributes (name, color, credits).

### `DELETE /api/v1/courses/{course_id}`
Deletes a course. Cascades to associated commitments, deadlines, and study blocks.

---

## 4. Commitments

### `GET /api/v1/commitments`
Retrieves all fixed recurring weekly commitments (classes, labs, recurring events).

### `POST /api/v1/commitments`
Creates a fixed commitment.
- **Request Body:**
  ```json
  {
    "title": "Algorithms Lecture",
    "course_id": 1,
    "day_of_week": 1,
    "start_time": "10:00",
    "end_time": "11:30",
    "location": "Hall A",
    "commitment_type": "class"
  }
  ```

### `PATCH /api/v1/commitments/{commitment_id}`
Updates commitment details.

### `DELETE /api/v1/commitments/{commitment_id}`
Removes a fixed commitment.

---

## 5. Deadlines & Scheduling

### `GET /api/v1/deadlines`
Lists all pending and completed deadlines.

### `POST /api/v1/deadlines`
Creates an assignment or exam deadline deliverable.
- **Request Body:**
  ```json
  {
    "title": "Problem Set 3",
    "course_id": 1,
    "due_datetime": "2026-11-25T23:59:00Z",
    "estimated_hours": 6.0,
    "priority": "high"
  }
  ```

### `POST /api/v1/deadlines/{deadline_id}/schedule`
Triggers capacity-aware scheduling to place required study blocks into open calendar gaps prior to the deadline date.

### `DELETE /api/v1/deadlines/{deadline_id}`
Deletes a deadline and cascades removal of all associated study blocks.

---

## 6. Study Blocks

### `GET /api/v1/study-blocks`
Retrieves study blocks, filterable by date range or deadline association.

### `PATCH /api/v1/study-blocks/{block_id}`
Updates status of a study block (`scheduled`, `completed`, `missed`).
- **Request Body:**
  ```json
  {
    "status": "missed"
  }
  ```

---

## 7. Dynamic Recovery Engine

### `POST /api/v1/recovery/preview?strategy={strategy}`
Generates a side-by-side Before/After diff preview of proposed schedule adjustments.
- **Query Parameter:** `strategy` (`auto_heal`, `triage_mvp`, or `shift_today`)
- **Response `200 OK`:**
  ```json
  {
    "strategy": "auto_heal",
    "status": "feasible",
    "disrupted_count": 1,
    "recovered_count": 1,
    "changes": [
      {
        "block_id": 3,
        "title": "Problem Set 3 Focus Session",
        "original_slot": "2026-11-20 14:00 - 15:30",
        "proposed_slot": "2026-11-21 09:30 - 11:00",
        "target_day_capacity_after": "Feasible",
        "resolvable": true,
        "status_change": "rescheduled"
      }
    ],
    "warnings": []
  }
  ```

### `POST /api/v1/recovery/apply`
Applies proposed schedule changes from the `auto_heal` strategy and commits updates to the database.

### `POST /api/v1/recovery/triage-mvp`
Applies proportional study target downscaling (-30% low priority, -20% medium priority) to safeguard critical deadlines.

### `POST /api/v1/recovery/shift-today`
Shifts remaining blocks today forward by a specified duration, cascading into tomorrow if necessary.

### `GET /api/v1/recovery/micro-action`
Returns a single, immediate micro-action recommendation to help the student restart momentum after a disruption.

---

## 8. Calendar Export

### `GET /api/v1/calendar/feed.ics`
Generates a standard RFC 5545 iCalendar subscription feed containing all scheduled study blocks.
- **Content-Type:** `text/calendar; charset=utf-8`
- **Content-Disposition:** `attachment; filename="study_planner_schedule.ics"`
