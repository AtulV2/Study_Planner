# Phase 2 Plan: REST API & Data Contracts (FastAPI)

**Approved By:** User (Autopilot pre-approval granted)  
**Status:** Approved & Locked  
**Timestamp:** 2026-11-17T21:52:30+05:30  

---

## 1. Objectives & Scope
Implement the complete REST API tier based on `blueprint/04_API_AND_DATA_CONTRACT_SPECIFICATION.md`:
1. **Pydantic v2 Schemas (`backend/app/schemas/`):**
   - Course (Create, Update, Response)
   - FixedCommitment (Create, Update, Response)
   - Deadline (Create, Update, Response)
   - StudyBlock (Create, Update, Response)
   - StudentConfig (Update, Response)
   - Recovery (Preview, AutoHeal, Triage, Shift, MicroAction, History)
   - RFC 7807 Error Response
2. **FastAPI Endpoints (`backend/app/api/v1/`):**
   - `/health` and `/seed`: System health diagnostics and realistic test student scenario generation.
   - `/config`: GET and PATCH student boundaries.
   - `/courses`: CRUD with 204 No Content on delete.
   - `/commitments`: CRUD for recurring anchors with 204 on delete.
   - `/deadlines`: CRUD for deliverables, plus `POST /deadlines/{id}/auto-schedule`.
   - `/study-blocks`: CRUD, manual insertions, status patches, and `POST /schedule/auto-fit-all`.
   - `/recovery`: Endpoints for `/preview`, `/auto-heal`, `/triage-mvp`, `/shift-today`, `/micro-action`, and `/history`.
3. **ASGI Application (`backend/app/main.py`):**
   - CORS middleware enabled for frontend development (`localhost:5173`).
   - RFC 7807 global exception handlers for `CapacityExceededError`, `EntityNotFoundError`, `ZeroGapsAvailableError`, etc.
   - Lifespan handler ensuring DB tables and default configuration are seeded.
4. **Integration Tests (`backend/tests/integration/`):**
   - End-to-end HTTP integration tests using `starlette.testclient.TestClient`.
   - Validate 200, 201, 204 status codes, cascade deletions, error codes, and recovery routes.

## 2. Definition of Done
- All routes functional and verified via FastAPI TestClient.
- 100% pass rate on integration tests.
- Audit report recorded in `.ai/04_audits/AUDIT_002_phase2.md`.
- Checkpoint locked in `.ai/03_checkpoints/CHECKPOINT_002_phase2.md`.
