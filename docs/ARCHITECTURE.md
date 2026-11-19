# Architecture Overview

This document describes the technical architecture, domain models, algorithms, and design patterns used in **Study Planner**.

---

## 1. System Topology

Study Planner is organized as a decoupled full-stack application:

```
+-----------------------------------------------------------+
|                   Frontend (Client)                       |
|   React 19 + Vite + Lucide React + Modern CSS Variables   |
+-----------------------------------------------------------+
                             │
                      REST API / JSON
                             │
                             ▼
+-----------------------------------------------------------+
|                   Backend API (FastAPI)                   |
|       Routing, Dependency Injection, RFC 7807 Errors      |
+-----------------------------------------------------------+
                             │
                             ▼
+-----------------------------------------------------------+
|                   Domain Services Layer                   |
|   SchedulerService │ CapacityService │ RecoveryService    |
|               ICalService │ SeedService                   |
+-----------------------------------------------------------+
                             │
                             ▼
+-----------------------------------------------------------+
|                   Persistence Layer                       |
|       SQLAlchemy 2.0 ORM (Declarative Base & Pool)        |
|          SQLite (Local WAL) / PostgreSQL (Production)     |
+-----------------------------------------------------------+
```

---

## 2. Backend Architecture

The backend follows clean layered architecture principles where business logic remains framework-agnostic:

### Directory Structure
- `backend/app/api/v1/`: HTTP route handlers and request validation via Pydantic schemas.
- `backend/app/core/`: Configuration via Pydantic Settings, database engine pooling, and domain exceptions.
- `backend/app/models/`: SQLAlchemy 2.0 declarative database models with cascading delete rules.
- `backend/app/schemas/`: Strongly-typed Pydantic DTOs for request/response serialization and validation.
- `backend/app/services/`: Pure business logic implementations (interval mathematics, capacity tracking, recovery strategies).
- `backend/app/main.py`: ASGI lifecycle management, CORS configuration, and exception middleware.

---

## 3. Domain Model & Entity Relationships

The relational model enforces academic structure and cascading lifecycles:

```
+-------------------+       1:N       +-------------------+
|      Course       |---------------->|    Commitment     |
| (Code, Name, Color)                 | (Class/Study/Fixed|
+-------------------+                 +-------------------+
          │
          │ 1:N
          ▼
+-------------------+       1:N       +-------------------+
|     Deadline      |---------------->|    StudyBlock     |
| (Due Date, Hours) |                 |(Scheduled Intervals
+-------------------+                 +-------------------+

+-------------------+                 +-------------------+
|   StudentConfig   |                 |   RecoveryEvent   |
| (Caps, Sleep/Wake)|                 |  (Audit History)  |
+-------------------+                 +-------------------+
```

### Entity Responsibilities
1. **Course:** Academic container (e.g., `CS 101`) defining code, name, color tokens, and credit weighting.
2. **Commitment:** Calendar commitments categorized as `class` (fixed lecture/lab), `study` (allocated study time), or `fixed` (personal/extracurricular anchor).
3. **Deadline:** Academic milestones (assignments, midterms, projects) requiring estimated study effort, tracking remaining hours and priority levels (`critical`, `high`, `medium`, `low`).
4. **StudyBlock:** Concrete, scheduled blocks of study time allocated to complete a specific `Deadline`. Includes start time, end time, and status (`scheduled`, `completed`, `missed`).
5. **StudentConfig:** Student cognitive constraints: daily maximum study hours, wake time, sleep time, meal hours, and buffer durations.
6. **RecoveryEvent:** Historical audit record tracking recovery triggers, applied strategy, and shifted blocks.

---

## 4. Core Algorithms

### Interval Merging & Gap Finding (`scheduler.py`)
To schedule study sessions without collisions:
1. All fixed commitments and class sessions for a target day are retrieved.
2. Mandatory meal intervals (lunch: 12:30–13:15, dinner: 18:30–19:15) and 15-minute post-class transit buffers are appended to the occupied list.
3. Overlapping and contiguous intervals are mathematically merged using time-interval union logic.
4. Complement intervals between student wake time and sleep time are computed, yielding verified "free gaps".

### Capacity & Burnout Calculation (`capacity.py`)
1. For any given day, all scheduled study blocks and study commitments are summed.
2. The total is evaluated against the configured daily ceiling (default: 5.5 hours):
   - **Nominal (0 – 70%):** Healthy workload.
   - **Elevated (70 – 99%):** Approaching maximum cognitive threshold.
   - **Over Capacity (>= 100%):** Triggers capacity warning and requires rescheduling.

### Dynamic Recovery Engine (`recovery.py`)
When a study block is flagged as missed, three recovery strategies are evaluated:
1. **Auto-Heal:** Searches future days prior to the assignment deadline, identifying free gap intervals that do not exceed the daily study cap.
2. **Triage Mode (MVP):** Downscales low-priority study targets by 30% and medium-priority by 20% to preserve high-priority exam preparation.
3. **Shift Forward:** Pushes remaining daily commitments later into the day, overflowing past bedtime into the next morning's earliest free gap.

---

## 5. Error Handling & Standards

The application implements **RFC 7807 (Problem Details for HTTP APIs)**:
- Standardized error envelopes with `type`, `title`, `status`, `detail`, and `instance`.
- Custom domain exceptions (`CapacityExceededError`, `ZeroGapsAvailableError`, `ScheduleConflictError`, `EntityNotFoundError`) mapped to appropriate HTTP status codes via FastAPI exception handlers.
