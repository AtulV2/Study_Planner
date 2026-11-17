# AutoPace (ResilientCal): Master Roadmap

Based on `blueprint/06_IMPLEMENTATION_ROADMAP_AND_AI_PROMPTS.md`.

## Phase Summary
- **Phase 1: Domain Core, Database & Algorithm Engine**
  - SQLAlchemy 2.0 dual-engine setup (SQLite WAL local, PostgreSQL Neon ready)
  - Models: Course, FixedCommitment, Deadline, StudyBlock, StudentConfig, RecoveryEvent
  - Services: Gap-finding arithmetic, daily study limit enforcement (5.5h max), recovery algorithms (auto-heal, triage-mvp, shift-today)
  - Pytest unit tests for all interval arithmetic & edge cases
  - Definition of Done: 100% unit tests passing with zero placeholders.

- **Phase 2: REST API & Data Contracts (FastAPI)**
  - Pydantic v2 schemas and RFC 7807 error responses
  - CRUD endpoints for courses, commitments, deadlines, study blocks
  - Recovery engine endpoints (`/preview`, `/auto-heal`, `/triage-mvp`, `/shift-today`, `/micro-action`)
  - Integration tests verifying HTTP status codes and cascade behaviors
  - Definition of Done: 100% integration tests passing with proper status codes.

- **Phase 3: Editorial UI System & Canvas Architecture (React 19 + Vite)**
  - Warm slate design tokens & Swiss typography primitives
  - Weekly Timeline Canvas with visual differentiation for fixed vs. flexible blocks
  - Burnout Guardrail Meter tracking cognitive load against the 5.5h daily limit
  - Definition of Done: Component library & canvas grid fully responsive and functioning.

- **Phase 4: Dynamic Recovery UI & Interactive Workflows**
  - "Things Changed" Recovery Modal with side-by-side Before/After diff preview
  - Quick action status toggles (Complete, Missed, Undo)
  - Micro-action launcher banner & Triage Downscaler UI
  - Definition of Done: Interactive recovery flow operational with visual confirmation.

- **Phase 5: Automated E2E Verification, iCal Feed & Launch Packaging**
  - Standard `.ics` iCalendar feed endpoint
  - Playwright automated browser test suite covering all critical user flows
  - Production README, developer onboarding guides, and Windows batch scripts
  - Definition of Done: All Playwright tests green; project fully runnable locally and on cloud.
