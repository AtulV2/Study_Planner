# Phase 3 Plan: Editorial UI System & Canvas Architecture (React 19 + Vite)

**Approved By:** User (Autopilot pre-approval granted)  
**Status:** Approved & Locked  
**Timestamp:** 2026-11-17T22:00:00+05:30  

---

## 1. Objectives & Scope
Build the client application adhering to the Swiss Editorial modern craft standards in `blueprint/03_UI_UX_DESIGN_SPECIFICATION.md`:
1. **Frontend Infrastructure (`frontend/`):**
   - React 19 + Vite setup with zero external bloat.
   - Pinned dependencies (`react`, `react-dom`, `@vitejs/plugin-react`, `lucide-react`, `vite`).
2. **Design Tokens & Typography (`frontend/src/styles/`):**
   - `tokens.css`: Warm slate palette (`#F8FAFC`, `#0F172A`, `#E2E8F0`, `#2563EB`, `#059669`, `#D97706`, `#DC2626`).
   - `typography.css`: Plus Jakarta Sans headings & JetBrains Mono time metrics.
   - `main.css`: Reset, tactile shadows, crisp 1px borders, smooth transitions.
3. **API Integration & State Management (`frontend/src/services/` & `hooks/`):**
   - `api.js`: Communicates with FastAPI backend (`/api/v1/`).
   - `useSchedule.js`: Fetching, cache invalidation, and optimistic state mutations.
4. **Canvas & Layout Primitives (`frontend/src/components/`):**
   - `CommandBar`: Brand header, "Seed Demo Week", "Auto-Fit All", "Add Course/Commitment/Deadline", "Recover Schedule".
   - `BurnoutMeter`: Daily cognitive load bar across Mon-Sun with capacity risk pills.
   - `WeeklyCanvas`: 7-day responsive grid (Monday to Sunday) with hour ruler.
   - `EventCard`: Distinct visual styling for Fixed Commitments (solid anchors) vs Study Blocks (fluid cards with hover status toggles for Complete, Missed, Delete).
   - Quick Add Modals for Course, Fixed Commitment, and Deadline.
5. **Build & Unit Verification:**
   - Compile production build (`npm run build`).

## 2. Definition of Done
- Complete frontend compiles without errors.
- Visual hierarchy strictly matches the Anti-"AI-Slop" editorial design specification.
- Full two-way data sync with FastAPI backend.
- Audit report recorded in `.ai/04_audits/AUDIT_003_phase3.md`.
- Checkpoint locked in `.ai/03_checkpoints/CHECKPOINT_003_phase3.md`.
