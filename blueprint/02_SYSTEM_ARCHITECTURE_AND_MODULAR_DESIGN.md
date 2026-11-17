# 02. System Architecture & Modular Design

---

## 1. High-Level Architectural Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CLIENT TIER (React 19 + Vite)                         │
│  - Weekly / Multi-Week Interactive Canvas (Grid & Timeline view)            │
│  - Capacity Gauge & Burnout Guardrail Indicators                            │
│  - Recovery Drawer with Side-by-Side Diff Preview                           │
│  - Quick Intake Modals (Course, Fixed Commitment, Deadline)                 │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / JSON (REST API)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        API TIER (FastAPI 0.115+)                            │
│  - Dependency Injection (Database sessions, Config, Logger)                 │
│  - Pydantic v2 Serialization, Validation & RFC 7807 Error Handling          │
│  - CORS & Rate-Limiting Middleware                                          │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────────────┐     ┌───────────────────────────────────────┐
│     DOMAIN SERVICES LAYER     │     │        DATA ACCESS LAYER (ORM)        │
│ • Scheduling & Gap Engine     │     │ • SQLAlchemy 2.0 Declarative Models   │
│ • Recovery & Triage Service   │◄───►│ • Repositories (CRUD Operations)      │
│ • Capacity Calculation Engine │     │ • Neon Serverless PostgreSQL (Cloud)  │
│ • iCal Exporter Service       │     │ • SQLite (`autopace.db` for Local Dev)│
└───────────────────────────────┘     └───────────────────────────────────────┘
```

---

## 2. Directory & Package Structure

The project uses a clean, mono-repository directory layout that strictly separates concerns:

```text
autopace/
├── backend/
│   ├── app/
│   │   ├── api/                  # FastAPI routers and route definitions
│   │   │   ├── v1/
│   │   │   │   ├── courses.py
│   │   │   │   ├── commitments.py
│   │   │   │   ├── deadlines.py
│   │   │   │   ├── study_blocks.py
│   │   │   │   ├── recovery.py
│   │   │   │   ├── capacity.py
│   │   │   │   ├── calendar_sync.py
│   │   │   │   └── config.py
│   │   │   └── api_router.py
│   │   ├── core/                 # App configuration, logging, database connection
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── exceptions.py
│   │   ├── models/               # SQLAlchemy 2.0 ORM database models
│   │   │   ├── base.py
│   │   │   ├── course.py
│   │   │   ├── commitment.py
│   │   │   ├── deadline.py
│   │   │   ├── study_block.py
│   │   │   ├── student_config.py
│   │   │   └── recovery_event.py
│   │   ├── schemas/              # Pydantic v2 schemas (DTOs for Request/Response)
│   │   │   ├── course.py
│   │   │   ├── commitment.py
│   │   │   ├── deadline.py
│   │   │   ├── study_block.py
│   │   │   ├── recovery.py
│   │   │   └── capacity.py
│   │   ├── services/             # Pure business logic (framework-agnostic)
│   │   │   ├── scheduler_service.py
│   │   │   ├── recovery_service.py
│   │   │   ├── capacity_service.py
│   │   │   └── ical_service.py
│   │   └── main.py               # Application factory and ASGI entrypoint
│   ├── tests/                    # Automated testing suite
│   │   ├── conftest.py           # Pytest fixtures and mock DB sessions
│   │   ├── unit/                 # Pure domain algorithm tests
│   │   └── integration/          # API endpoint tests with TestClient
│   ├── alembic/                  # Database migration management
│   ├── requirements.txt          # Python dependencies pinned
│   └── seed.py                   # Realistic student scenario seeder
├── frontend/
│   ├── src/
│   │   ├── assets/               # Brand SVGs and design assets
│   │   ├── components/           # Reusable UI component primitives
│   │   │   ├── common/           # Button, Modal, Badge, Tooltip, Input, Card
│   │   │   ├── canvas/           # TimelineGrid, DayColumn, EventCard, HourRuler
│   │   │   ├── capacity/         # BurnoutMeter, DailyCapBar, RestStat
│   │   │   ├── recovery/         # RecoveryModal, DiffComparison, MicroActionBanner
│   │   │   └── forms/            # CourseForm, CommitmentForm, DeadlineForm
│   │   ├── hooks/                # Custom React hooks
│   │   │   ├── useSchedule.js    # Data fetching and optimistic mutation hook
│   │   │   ├── useCapacity.js    # Daily cognitive load computations
│   │   │   └── useRecovery.js    # Recovery preview and commit handlers
│   │   ├── services/             # Axios / Fetch client and API contract mapping
│   │   │   └── api.js
│   │   ├── styles/               # Design tokens, reset, utility classes
│   │   │   ├── tokens.css
│   │   │   ├── typography.css
│   │   │   └── main.css
│   │   ├── App.jsx               # Root application shell
│   │   └── main.jsx              # React DOM mounting
│   ├── tests/                    # Frontend tests
│   │   ├── unit/                 # Component rendering and logic tests (Vitest)
│   │   └── e2e/                  # Playwright browser end-to-end user flows
│   ├── package.json
│   └── vite.config.js
└── blueprint/                    # Master rebuild documentation
```

---

## 3. Database Schema & Data Models

### Database Engine
- **Storage:** SQLite 3 with WAL (Write-Ahead Logging) mode enabled for high concurrency.
- **ORM:** SQLAlchemy 2.0 with explicit relationship cascades and strict foreign keys.

### Entity Relationship Model

```
 ┌──────────────┐          1..*  ┌───────────────────┐
 │    Course    ├───────────────►│  FixedCommitment  │
 └───┬──────────┘                └───────────────────┘
     │ 1..*
     ▼
 ┌──────────────┐          1..*  ┌───────────────────┐
 │   Deadline   ├───────────────►│    StudyBlock     │
 └──────────────┘                └───────────────────┘

 ┌───────────────────┐           ┌───────────────────┐
 │   StudentConfig   │           │   RecoveryEvent   │
 └───────────────────┘           └───────────────────┘
```

### Detailed Schema Specifications

1. **`Course`**
   - `id`: Integer (PK, Auto-increment)
   - `code`: String(32), Unique, Indexed (e.g., `"CS 240"`, `"MATH 215"`)
   - `name`: String(128) (e.g., `"Discrete Mathematics"`)
   - `color`: String(16) (Hex code, default: `"#3B82F6"`)
   - `instructor`: String(128), Nullable
   - *Cascades:* Deleting a course deletes its commitments and deadlines.

2. **`FixedCommitment`** (Immutable Anchors)
   - `id`: Integer (PK, Auto-increment)
   - `course_id`: Integer, ForeignKey(`courses.id`), Nullable (can be a non-academic commitment like a campus job)
   - `title`: String(128) (e.g., `"CS 240 Lecture"`, `"Dining Hall Shift"`)
   - `commitment_type`: Enum (`"lecture"`, `"lab"`, `"discussion"`, `"work"`, `"sport"`, `"personal"`)
   - `day_of_week`: SmallInteger (0 = Monday, 6 = Sunday)
   - `start_time`: String(5) (`"HH:MM"`, e.g., `"09:30"`)
   - `end_time`: String(5) (`"HH:MM"`, e.g., `"11:00"`)
   - `location`: String(128), Nullable
   - `status`: Enum (`"scheduled"`, `"completed"`, `"missed"`)

3. **`Deadline`** (Deliverables Requiring Study Time)
   - `id`: Integer (PK, Auto-increment)
   - `course_id`: Integer, ForeignKey(`courses.id`)
   - `title`: String(128) (e.g., `"Problem Set 3"`, `"Midterm Exam"`)
   - `due_datetime`: DateTime (Timezone-aware ISO 8601)
   - `estimated_hours`: Float (e.g., `4.5`)
   - `completed_hours`: Float (default `0.0`)
   - `priority`: Enum (`"high"`, `"medium"`, `"low"`)
   - `status`: Enum (`"pending"`, `"completed"`, `"at_risk"`)
   - `notes`: Text, Nullable

4. **`StudyBlock`** (Flexible Work Sessions)
   - `id`: Integer (PK, Auto-increment)
   - `deadline_id`: Integer, ForeignKey(`deadlines.id`), Nullable
   - `title`: String(128) (e.g., `"PS3 - Coding Exercise"`)
   - `start_datetime`: DateTime (ISO 8601)
   - `end_datetime`: DateTime (ISO 8601)
   - `duration_minutes`: Integer (default `60`)
   - `status`: Enum (`"scheduled"`, `"completed"`, `"missed"`, `"recovered"`, `"skipped"`)
   - `notes`: Text, Nullable

5. **`StudentConfig`** (User Boundaries & Preferences)
   - `id`: Integer (PK, Auto-increment)
   - `max_daily_study_hours`: Float (default `5.5`)
   - `wake_time`: String(5) (default `"08:00"`)
   - `sleep_time`: String(5) (default `"23:00"`)
   - `preferred_chunk_minutes`: Integer (default `60`)
   - `min_gap_buffer_minutes`: Integer (default `15`)
   - `protect_weekends`: Boolean (default `false`)

6. **`RecoveryEvent`** (Audit Trail of Rescheduling Actions)
   - `id`: Integer (PK, Auto-increment)
   - `timestamp`: DateTime (default UTC now)
   - `trigger_type`: Enum (`"auto_heal"`, `"triage_mvp"`, `"shift_today"`, `"micro_action"`)
   - `description`: String(255)
   - `affected_blocks_count`: Integer
   - `details_json`: Text (stores before/after snapshot for diff/rollback)

---

## 4. Core Algorithm Specifications

### Algorithm A: Gap-Finding & Interval Scheduler (`scheduler_service.py`)
1. **Busy Interval Aggregation:**
   - Gather all fixed commitments for the day.
   - Gather already scheduled study blocks for the day.
   - Inject mandatory physiological buffers:
     - Lunch pause: `12:30 – 13:15`
     - Dinner pause: `18:30 – 19:15`
     - Transit / Cognitive reset buffer: `15 minutes` after any fixed block.
2. **Interval Merge:**
   - Sort intervals by `start_time` ascending.
   - Merge overlapping or touching intervals into contiguous busy spans.
3. **Free Window Inversion:**
   - Subtract merged busy spans from the waking window `[wake_time, sleep_time]`.
   - Filter free intervals to only those where `duration >= min_duration_minutes` (default 45 min).
4. **Cap-Aware Allocation:**
   - Before scheduling a block, calculate `current_day_scheduled_minutes + block_minutes`.
   - If sum exceeds `max_daily_study_hours * 60`, skip to the next available day. Never exceed the student's daily cognitive ceiling.

### Algorithm B: Dynamic Recovery Engine (`recovery_service.py`)
1. **Auto-Heal:**
   - Find all study blocks with status `"missed"`.
   - Locate the next earliest free slot between `now()` and the deadline's `due_datetime`.
   - Update `start_datetime`, `end_datetime`, mark status as `"recovered"`, and append a clear change note.
2. **Triage / MVP Mode:**
   - When weekly scheduled hours exceed total available capacity, identify low and medium priority deliverables.
   - Reduce estimated study hours for low-priority tasks by 30% and medium-priority by 20%.
   - Truncate or merge remaining flexible study blocks accordingly.
3. **Shift Today:**
   - Shift today's pending blocks forward by `N` minutes.
   - If shifted blocks breach `sleep_time`, gracefully cascade the overflow into tomorrow's first available study window.
