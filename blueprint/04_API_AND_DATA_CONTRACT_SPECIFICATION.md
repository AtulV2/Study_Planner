# 04. API & Data Contract Specification

---

## 1. REST API Standards & Protocols

- **Base URL:** `/api/v1`
- **Data Exchange Format:** UTF-8 JSON
- **Date/Time Standard:** ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`) in UTC
- **Time Format (Wall Clock):** `"HH:MM"` (24-hour format, e.g. `"09:30"`, `"14:00"`)
- **Error Standard:** Standardized error response body with machine-readable `code` and human-readable `message`.

```json
{
  "error": {
    "code": "CAPACITY_EXCEEDED",
    "message": "Cannot schedule 120 minutes on Tuesday without exceeding the 5.5h daily study limit.",
    "details": {
      "day": "2026-11-18",
      "current_load_minutes": 310,
      "requested_minutes": 120,
      "max_limit_minutes": 330
    }
  }
}
```

---

## 2. API Endpoints Matrix

### Core & Diagnostics
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | System health, database connection, count statistics | `200 OK` |
| `POST` | `/seed` | Resets & seeds a rich, realistic student test scenario | `200 OK` |
| `GET` | `/config` | Get student boundaries (wake/sleep times, daily study cap) | `200 OK` |
| `PATCH` | `/config` | Update student preferences and cognitive limits | `200 OK` |

### Courses
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/courses` | Retrieve all enrolled courses | `200 OK` |
| `POST` | `/courses` | Create a new course | `201 Created` |
| `PATCH` | `/courses/{id}` | Update course metadata (color, name, instructor) | `200 OK` |
| `DELETE` | `/courses/{id}` | Delete a course and cascade delete its commitments | `204 No Content` |

### Fixed Commitments (Classes, Shifts, Sports)
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/commitments` | List all weekly recurring commitments | `200 OK` |
| `POST` | `/commitments` | Add a new recurring class or shift | `201 Created` |
| `PATCH` | `/commitments/{id}` | Update commitment time or status (`scheduled`, `completed`, `missed`) | `200 OK` |
| `DELETE` | `/commitments/{id}` | Remove a fixed commitment | `204 No Content` |

### Deadlines & Deliverables
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/deadlines` | List pending and completed deadlines | `200 OK` |
| `POST` | `/deadlines` | Create a new assignment/exam deliverable | `201 Created` |
| `PATCH` | `/deadlines/{id}` | Update deadline details, priority, or status | `200 OK` |
| `DELETE` | `/deadlines/{id}` | Delete deadline and cascade delete associated study blocks | `204 No Content` |
| `POST` | `/deadlines/{id}/auto-schedule` | Auto-allocates study sessions for this specific deadline | `200 OK` |

### Study Blocks (Flexible Focus Sessions)
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/study-blocks` | List scheduled, completed, and missed study blocks | `200 OK` |
| `POST` | `/study-blocks` | Manually insert a study session block | `201 Created` |
| `PATCH` | `/study-blocks/{id}` | Update block status (`scheduled`, `completed`, `missed`, `recovered`) | `200 OK` |
| `DELETE` | `/study-blocks/{id}` | Delete an individual study session | `204 No Content` |
| `POST` | `/schedule/auto-fit-all` | Global allocator: Fits all unfulfilled deadlines into free gaps | `200 OK` |

### Dynamic Recovery Engine
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `POST` | `/recovery/preview` | Generates a non-destructive before/after recovery preview diff | `200 OK` |
| `POST` | `/recovery/auto-heal` | Commits reallocation of missed blocks into future buffers | `200 OK` |
| `POST` | `/recovery/triage-mvp` | Commits downscaling of low/medium priority deliverables | `200 OK` |
| `POST` | `/recovery/shift-today` | Pushes today's remaining blocks forward | `200 OK` |
| `GET` | `/recovery/micro-action` | Returns a single 30–45 min inertia-breaking starter task | `200 OK` |
| `GET` | `/recovery/history` | Audit log of past recovery interventions | `200 OK` |

### Calendar Feeds & Synchronization
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/calendar/feed.ics` | Standard iCalendar subscription feed for Apple/Google Calendar | `200 OK` (text/calendar) |

---

## 3. Detailed Request & Response Schemas (Pydantic V2)

### 1. `CourseCreate` / `CourseResponse`
```json
// Request POST /courses
{
  "code": "CS 240",
  "name": "Data Structures & Algorithms",
  "color": "#3B82F6",
  "instructor": "Dr. Sarah Chen"
}

// Response 201 Created
{
  "id": 1,
  "code": "CS 240",
  "name": "Data Structures & Algorithms",
  "color": "#3B82F6",
  "instructor": "Dr. Sarah Chen",
  "created_at": "2026-11-17T12:00:00Z"
}
```

### 2. `FixedCommitmentCreate`
```json
// Request POST /commitments
{
  "course_id": 1,
  "title": "CS 240 Lecture",
  "commitment_type": "lecture",
  "day_of_week": 0, // 0 = Monday, 6 = Sunday
  "start_time": "10:00",
  "end_time": "11:30",
  "location": "Turing Hall 101"
}
```

### 3. `DeadlineCreate`
```json
// Request POST /deadlines
{
  "course_id": 1,
  "title": "Problem Set 3 - Balanced Trees",
  "due_datetime": "2026-11-20T23:59:00Z",
  "estimated_hours": 4.5,
  "priority": "high",
  "notes": "Need to implement AVL insertion and unit tests."
}
```

### 4. `RecoveryPreviewResponse`
```json
// Response POST /recovery/preview?strategy=auto_heal
{
  "strategy": "auto_heal",
  "status": "feasible",
  "disrupted_count": 2,
  "recovered_count": 2,
  "changes": [
    {
      "block_id": 14,
      "title": "PS3 - Coding Exercise",
      "original_slot": "2026-11-17T14:00:00Z - 15:30:00Z",
      "proposed_slot": "2026-11-18T10:15:00Z - 11:45:00Z",
      "target_day_capacity_after": "4.2h / 5.5h",
      "reason": "Absorbed into Wednesday morning study buffer before Thursday deadline."
    }
  ],
  "warnings": []
}
```
