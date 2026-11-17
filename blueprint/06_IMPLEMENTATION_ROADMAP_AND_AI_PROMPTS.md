# 06. Implementation Roadmap & AI Execution Prompts

---

## 1. Master Implementation Roadmap

This blueprint divides the rebuild into 5 discrete, verifiable engineering phases. Each phase has a strict **Definition of Done (DoD)** that must pass automated testing before proceeding to the next.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: Domain Core, Database & Algorithm Engine                           │
│  - SQLAlchemy 2.0 models + SQLite WAL setup                                 │
│  - Pure Python gap-finding, capacity calculator & recovery logic            │
│  - 100% Pytest unit test coverage on all mathematical scheduling cases      │
├─────────────────────────────────────────────────────────────────────────────┤
│ PHASE 2: REST API & Data Contracts (FastAPI)                                │
│  - Pydantic v2 schemas with validation & RFC 7807 error handlers            │
│  - CRUD endpoints for Courses, Commitments, Deadlines, and Blocks           │
│  - Recovery engine endpoints (`preview`, `auto-heal`, `triage`, `shift`)    │
│  - Integration tests verifying HTTP 200, 201, 204 status codes              │
├─────────────────────────────────────────────────────────────────────────────┤
│ PHASE 3: Editorial UI System & Canvas Architecture (React 19 + Vite)        │
│  - Slate design tokens, typography, and tactile UI primitives               │
│  - Weekly Timeline Canvas with distinct Fixed vs. Flexible visual cards     │
│  - Burnout Guardrail Meter showing daily study hours against 5.5h cap       │
├─────────────────────────────────────────────────────────────────────────────┤
│ PHASE 4: Dynamic Recovery UI & Interactive Workflows                        │
│  - "Things Changed" Recovery Modal with side-by-side Before/After diff      │
│  - Quick-action status toggles (Complete, Missed, Undo)                     │
│  - Micro-action launcher banner and Triage Downscaler UI                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ PHASE 5: Automated E2E Verification, iCal Feed & Launch Packaging           │
│  - Standard `.ics` iCalendar export endpoint                                │
│  - Playwright automated browser test suite verifying every button & modal   │
│  - Production README, architecture documentation, and Windows bat launchers │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Copy-Paste AI Execution Prompts

When you are ready to have the AI write the code, copy and paste the corresponding phase prompt below. Each prompt is engineered to enforce human-readable, production-grade code without lazy placeholders.

---

### Prompt for Phase 1: Domain Models, Database & Core Algorithms

```markdown
You are a Principal Software Architect. We are rebuilding "AutoPace" (a capacity-aware, self-healing student calendar) from scratch based on the master specifications in `blueprint/`.

Your objective in this turn is to implement PHASE 1 strictly:
1. Initialize the backend project structure according to `blueprint/02_SYSTEM_ARCHITECTURE_AND_MODULAR_DESIGN.md`.
2. Configure `backend/app/core/database.py` with SQLAlchemy 2.0 supporting dual SQLite (local development) and Neon Serverless PostgreSQL (production) with connection pooling, and include `psycopg2-binary` in dependencies as specified in `blueprint/07_DEPLOYMENT_AND_CLOUD_INFRASTRUCTURE.md`.
3. Implement declarative models in `backend/app/models/`:
   - `Course`, `FixedCommitment`, `Deadline`, `StudyBlock`, `StudentConfig`, `RecoveryEvent`.
   - Ensure all cascade delete relationships are explicitly defined.
4. Implement pure domain algorithms in `backend/app/services/`:
   - `scheduler_service.py`: Gap-finding algorithm, interval merging, mandatory meal buffer injection, and daily study cap enforcement (5.5h max).
   - `recovery_service.py`: Auto-heal missed sessions, triage MVP downscaler, and shift-today cascade.
5. Create comprehensive Pytest unit tests in `backend/tests/unit/`:
   - Test interval arithmetic, capacity boundaries, midnight rollovers, and zero-gap edge cases as specified in `blueprint/05_COMPREHENSIVE_AUTOMATED_TESTING_SUITE.md`.

STRICT CONSTRAINTS:
- Write clean, human-readable, self-documenting code with clear docstrings explaining the "Why".
- Absolutely NO placeholders (e.g., `# TODO`, `pass`, or `...`). Every function must be fully implemented.
- Run `pytest` and verify that all unit tests pass before concluding this turn.
```

---

### Prompt for Phase 2: FastAPI REST API & Integration Tests

```markdown
You are a Senior Backend Engineer. We are continuing the AutoPace rebuild, implementing PHASE 2 based on `blueprint/04_API_AND_DATA_CONTRACT_SPECIFICATION.md`.

Your objective in this turn:
1. Implement Pydantic v2 schemas in `backend/app/schemas/` with strict type annotations and field validations.
2. Build FastAPI route handlers in `backend/app/api/v1/`:
   - `courses.py`: List, create, update, delete courses.
   - `commitments.py`: List, create, update, delete fixed classes/shifts.
   - `deadlines.py`: List, create, update, delete deliverables, and single-deadline auto-fit.
   - `study_blocks.py`: List, update status, delete, and `/schedule/auto-fit-all`.
   - `recovery.py`: Endpoints for `/recovery/preview`, `/recovery/auto-heal`, `/recovery/triage-mvp`, `/recovery/shift-today`, and `/recovery/micro-action`.
   - `seed.py`: Realistic student test week generator.
3. Implement RFC 7807 standardized error handling and CORS middleware in `backend/app/main.py`.
4. Create integration tests in `backend/tests/integration/` using FastAPI `TestClient`:
   - Test all CRUD workflows, HTTP 204 responses on delete, and database cascade deletions.

STRICT CONSTRAINTS:
- Keep route handlers thin; delegate all business logic to `services/`.
- Ensure delete endpoints return HTTP 204 No Content with empty bodies.
- Run `pytest` to confirm 100% pass rate on integration tests before concluding this turn.
```

---

### Prompt for Phase 3: Modern Editorial Frontend & Weekly Canvas

```markdown
You are a Senior Frontend Engineer and Design Systems specialist. We are building the AutoPace client interface following `blueprint/03_UI_UX_DESIGN_SPECIFICATION.md`.

Your objective in this turn:
1. Set up React 19 + Vite in `frontend/` with Lucide icons.
2. Establish design tokens in `frontend/src/styles/tokens.css` and `typography.css`:
   - Warm slate palette (`#0F172A`, `#F8FAFC`, `#FFFFFF`), tactile borders (`#E2E8F0`), zero neon-slop purple gradients.
   - High-clarity typography (*Plus Jakarta Sans* and *JetBrains Mono* for clocks and metrics).
3. Build reusable UI primitives: `Button`, `Modal`, `Badge`, `Toast`, `Input`.
4. Build the Weekly Workload Canvas:
   - Monday to Sunday 7-day responsive grid.
   - Clearly differentiate Fixed Commitments (solid slate anchor bars) vs. Study Blocks (fluid, movable cards with checkmarks).
5. Build the Burnout Guardrail Meter:
   - Visual daily progress bar measuring committed hours against the 5.5h study ceiling with Amber overload warning pills.
6. Connect the frontend to the backend REST API via `frontend/src/services/api.js`.

STRICT CONSTRAINTS:
- Avoid generic AI-generated card bloat. Keep spacing clean, tactile, and intentional.
- Ensure all components are modular, cleanly typed, and include proper PropTypes/interfaces.
- Verify responsive rendering and launch the dev server to confirm zero compilation errors.
```

---

### Prompt for Phase 4: Dynamic Recovery UI & Interactive Workflows

```markdown
You are a Full-Stack Engineer. We are implementing the flagship feature of AutoPace: the "Things Changed" Dynamic Recovery Engine UI.

Your objective in this turn:
1. Build `RecoveryModal.jsx`:
   - When opened, query `/api/v1/recovery/preview` and render an intuitive side-by-side **Before vs. After** diff table.
   - Provide 3 clear tabs: Auto-Heal Buffers, Triage (MVP Mode), and Shift Today.
   - Include a single-click "Apply Recovery Plan" button with optimistic UI updates and an Undo toast notification.
2. Build interactive event card triggers:
   - Single-click checkmark to toggle "completed" status.
   - Single-click "Missed" flag that immediately surfaces the sticky Recovery Notice banner: *"Missed session detected. Click here to rebalance your week."*
   - Trash icon that deletes the block and handles HTTP 204 without throwing JSON parsing errors.
3. Build quick intake modals:
   - `AddCourseModal`, `AddCommitmentModal`, and `AddDeadlineModal` with real-time field validation.
4. Implement the "30-Minute Micro-Action" inertia breaker widget.

STRICT CONSTRAINTS:
- Ensure all mutations update state optimistically with instantaneous visual feedback.
- Every modal must close cleanly on `Esc` key press or backdrop click.
```

---

### Prompt for Phase 5: Automated E2E Verification & GitHub Launch Prep

```markdown
You are a QA Automation Lead and Open-Source Maintainer. We are concluding the AutoPace rebuild by enforcing automated end-to-end verification and packaging for GitHub.

Your objective in this turn:
1. Implement the iCalendar export endpoint:
   - `GET /api/v1/calendar/feed.ics` returning standard RFC 5545 iCalendar format so students can subscribe via Apple/Google Calendar.
2. Build the Playwright test suite in `frontend/tests/e2e/autopace.spec.js` following `blueprint/05_COMPREHENSIVE_AUTOMATED_TESTING_SUITE.md`:
   - Verify every button: Add Class, Add Deadline, Auto-Fit Gaps, Recover Schedule, status toggles, and delete icons.
   - Test edge cases: 0 free gaps, weekend protection, and cascading deletions.
3. Generate production launcher scripts for Windows:
   - `start_backend.bat` and `start_frontend.bat`.
4. Create a comprehensive, public-facing `README.md` at project root with:
   - Clear architectural diagram and philosophy statement.
   - One-command quick start instructions.
   - Full REST API reference.
   - Automated testing execution instructions.

STRICT CONSTRAINTS:
- Run Playwright and Pytest to guarantee that 100% of tests pass across both backend and frontend.
```
