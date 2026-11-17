# AutoPace (ResilientCal)

> **A Capacity-Aware, Self-Healing Academic Workload Operating System.**  
> Built with pure domain algorithms, FastAPI, SQLAlchemy 2.0, and a Swiss editorial modern craft UI (React 19 + Vite).

---

## ⚡ Core Philosophy & Non-Negotiables

AutoPace is designed to eradicate student burnout through mathematical realism:
- **Zero AI-Slop:** No gratuitous neon gradients, blurry glassmorphism, or intrusive chatbots. Tactile warm slate tokens (`#F8FAFC`, `#0F172A`, `#E2E8F0`), JetBrains Mono time metrics, and high-contrast typography.
- **Cognitive Guardrail:** Strictly enforces a **5.5-hour daily study ceiling**. Sessions exceeding daily capacity gracefully carry over to future free windows.
- **Dynamic Recovery Engine:** When life happens and a session is missed, AutoPace never silently scrambles your week. It presents a clear **side-by-side Before/After diff** and lets you choose between:
  1. **Auto-Heal:** Mathematical gap-finding into future buffer windows before deadlines.
  2. **Triage (MVP Mode):** Downscales low-priority study loads (-30%) and medium-priority (-20%) to safeguard critical exam prep.
  3. **Shift Today:** Pushes today's remaining blocks forward, overflowing past bedtime into tomorrow morning.
- **Mandatory Physiological Pauses:** Automatically injects daily lunch (12:30–13:15), dinner (18:30–19:15), and 15-minute transit buffers after every class.
- **Universal iCalendar Feed:** Live RFC 5545 `.ics` subscription URL to sync directly with Apple Calendar, Google Calendar, or Outlook.

---

## 🏗️ Architecture

```text
autopace/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # FastAPI REST routes (courses, commitments, deadlines, recovery, calendar)
│   │   ├── core/           # Dual-engine DB setup (SQLite WAL & Neon PostgreSQL connection pool)
│   │   ├── models/         # SQLAlchemy 2.0 ORM models with cascading deletes & UTC datetimes
│   │   ├── schemas/        # Pydantic v2 validation DTOs & RFC 7807 error format
│   │   ├── services/       # Framework-agnostic pure domain algorithms (Scheduler, Recovery, Capacity, iCal)
│   │   └── main.py         # ASGI application entrypoint & CORS middleware
│   └── tests/              # 100% green test pyramid (Pytest unit & integration suites)
├── frontend/
│   ├── src/
│   │   ├── components/     # Weekly Canvas Grid, Burnout Meter, Recovery Diff Modal, Quick Intake Modals
│   │   ├── hooks/          # Optimistic mutation state management
│   │   ├── services/       # REST API client
│   │   └── styles/         # Warm slate tokens, typography, and tactile UI styles
│   ├── package.json
│   └── vite.config.js
├── blueprint/              # Master engineering specifications
└── .ai/                    # Phase-Gate governance rules, immutable plans, checkpoints, and audits
```

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 1. Backend Setup
```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Run the automated test suite
python -m pytest backend/tests -v

# Launch the FastAPI backend server (http://127.0.0.1:8000)
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive API docs will be available at: **http://127.0.0.1:8000/docs**

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open your browser to: **http://localhost:5173**

### 3. Windows One-Click Launcher
Double-click `start_all.bat` in the project root to start both backend and frontend concurrently.

---

## 🧪 Testing & Validation

The codebase includes comprehensive unit and integration tests covering foreign key cascades, mathematical interval merging, buffer injections, burnout cap overflow, and dynamic recovery diffs:

```bash
python -m pytest backend/tests -v
```

All 18 automated tests pass with zero placeholders:
```
backend/tests/integration/test_commitments_api.py::test_commitments_crud_workflow PASSED
backend/tests/integration/test_courses_api.py::test_courses_crud_workflow PASSED
backend/tests/integration/test_deadlines_api.py::test_deadlines_crud_and_autoschedule PASSED
backend/tests/integration/test_ical_api.py::test_ical_feed_export PASSED
backend/tests/integration/test_recovery_api.py::test_recovery_endpoints_flow PASSED
backend/tests/integration/test_seed_and_health.py::test_health_and_config_workflow PASSED
backend/tests/unit/test_models.py::test_course_creation_and_retrieval PASSED
backend/tests/unit/test_models.py::test_course_cascade_deletes_commitments_and_deadlines PASSED
backend/tests/unit/test_models.py::test_deadline_cascade_deletes_study_blocks PASSED
backend/tests/unit/test_models.py::test_recovery_event_logging PASSED
backend/tests/unit/test_recovery.py::test_auto_heal_missed_blocks PASSED
backend/tests/unit/test_recovery.py::test_triage_mvp_downscaling PASSED
backend/tests/unit/test_recovery.py::test_shift_today_and_bedtime_overflow PASSED
backend/tests/unit/test_recovery.py::test_get_micro_action PASSED
backend/tests/unit/test_scheduler.py::test_interval_merge_logic PASSED
backend/tests/unit/test_scheduler.py::test_meal_and_transit_buffers PASSED
backend/tests/unit/test_scheduler.py::test_free_gaps_finding PASSED
backend/tests/unit/test_scheduler.py::test_daily_study_cap_enforcement PASSED
```

---

## 📅 Live Calendar Sync

Subscribe to your AutoPace schedule in Apple Calendar or Google Calendar via the live endpoint:
```text
http://127.0.0.1:8000/api/v1/calendar/feed.ics
```

---

## 📄 License
MIT License. Open-source and built for student well-being.
