# Phase 1 Plan: Domain Core, Database & Algorithm Engine

**Approved By:** User (Autopilot pre-approval granted)  
**Status:** Approved & Locked  
**Timestamp:** 2026-11-17T21:43:00+05:30  

---

## 1. Objectives & Scope
Implement the domain core for AutoPace:
1. Pinned dependencies in `backend/requirements.txt`.
2. Core configuration and dual-engine SQLAlchemy 2.0 database connection (`backend/app/core/`):
   - SQLite WAL mode + Foreign Key enforcement for local development.
   - Neon Serverless PostgreSQL connection pooling configuration for production.
3. Declarative ORM models with explicit cascading relationships in `backend/app/models/`:
   - `Course`, `FixedCommitment`, `Deadline`, `StudyBlock`, `StudentConfig`, `RecoveryEvent`.
4. Pure Python domain services in `backend/app/services/`:
   - `scheduler_service.py`: Gap-finding algorithm, interval arithmetic, meal buffer injection (lunch 12:30-13:15, dinner 18:30-19:15), transit buffer (15m after fixed commitments), and daily 5.5h study cap enforcement.
   - `capacity_service.py`: Daily scheduled hours, cognitive load calculation, burnout thresholds.
   - `recovery_service.py`: Dynamic auto-heal, triage/MVP priority downscaler (30% low, 20% medium), and shift-today cascade.
5. Unit tests in `backend/tests/unit/`:
   - `test_models.py`: Foreign key integrity & cascade deletes.
   - `test_scheduler.py`: Free slot extraction, buffer injection, cap limits.
   - `test_recovery.py`: Auto-heal rescheduling, MVP downscaling, bedtime overflow handling.

## 2. Definition of Done
- All models, core configs, and service logic fully implemented with zero placeholders.
- 100% pass rate across Pytest unit tests.
- Audit report generated in `.ai/04_audits/AUDIT_001_phase1.md`.
- Checkpoint created and state updated in `.ai/CURRENT_STATE.md`.
