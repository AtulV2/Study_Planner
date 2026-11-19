# Testing Guide

This guide details the testing strategy, test suite organization, and execution procedures for the **Study Planner** application.

---

## 1. Testing Philosophy

The test suite validates core domain rules using deterministic, automated tests:
- **In-Memory Persistence:** Unit and integration tests run against an isolated SQLite in-memory database (`sqlite:///:memory:`) using `StaticPool` and explicit foreign key pragmas (`PRAGMA foreign_keys=ON;`).
- **Domain Independence:** Scheduling, interval merging, and recovery algorithms are tested both as pure mathematical services and through full HTTP integration workflows.
- **Fast Feedback:** The entire backend test suite executes in under two seconds.

---

## 2. Test Suite Organization

```
backend/tests/
├── conftest.py                  # Pytest fixtures: clean DB session and FastAPI TestClient
├── unit/
│   ├── test_models.py           # Model creation, relationships, and cascade deletion rules
│   ├── test_scheduler.py        # Interval merging, meal/transit buffers, and study cap limits
│   └── test_recovery.py         # Auto-heal, triage downscaling, and shift overflow logic
└── integration/
    ├── test_courses_api.py      # Course CRUD workflows and unique constraint enforcement
    ├── test_commitments_api.py  # Commitment management and schedule alignment
    ├── test_deadlines_api.py    # Deadline intake and automatic study block placement
    ├── test_recovery_api.py     # Recovery preview diffs and strategy execution
    ├── test_ical_api.py         # RFC 5545 calendar export formatting and headers
    └── test_seed_and_health.py  # Health check and scenario seeding endpoints
```

---

## 3. Running Tests

Ensure your Python virtual environment is activated before running tests.

### Run All Tests
```bash
python -m pytest backend/tests -v
```

### Run Unit Tests Only
```bash
python -m pytest backend/tests/unit -v
```

### Run Integration Tests Only
```bash
python -m pytest backend/tests/integration -v
```

### Run Specific Test Module
```bash
python -m pytest backend/tests/unit/test_scheduler.py -v
```

---

## 4. Test Coverage Areas

### Cascade Deletions & Model Integrity (`test_models.py`)
- Verifies that deleting a `Course` automatically cascades and deletes all associated `Commitment` and `Deadline` records.
- Verifies that deleting a `Deadline` deletes all associated `StudyBlock` records.

### Interval Mathematics & Buffers (`test_scheduler.py`)
- Verifies merging of contiguous, overlapping, and disjoint busy intervals.
- Verifies automatic injection of 45-minute lunch, 45-minute dinner, and 15-minute transit buffers.
- Verifies gap detection respects student wake (`08:00`) and sleep (`23:00`) boundaries.
- Verifies strict enforcement of the 5.5-hour daily study ceiling.

### Recovery Mechanics (`test_recovery.py`)
- Verifies mathematical gap-finding for missed sessions.
- Verifies triage percentage downscaling based on task priority weights.
- Verifies forward shifting when blocks overflow bedtime into the subsequent day.
