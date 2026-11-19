# Frontend Setup & Architecture

This guide covers the setup, component architecture, styling conventions, and build processes for the **Study Planner** frontend application.

---

## 1. System Requirements

- **Node.js:** 18.0 or higher
- **npm:** 9.0 or higher

---

## 2. Installation & Local Development

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Launch the Vite development server:
   ```bash
   npm run dev
   ```

The local application server will run at:  
`http://localhost:5173`

---

## 3. Directory Structure

```
frontend/src/
├── components/
│   ├── canvas/
│   │   ├── WeeklyCanvas.jsx      # 7-day responsive time-grid canvas
│   │   ├── CommandBar.jsx        # Top control bar, branding, and quick actions
│   │   ├── BurnoutMeter.jsx      # Visual capacity metrics and threshold indicators
│   │   └── EventCard.jsx         # Rendered calendar events with actions and status
│   └── modals/
│       ├── RecoveryModal.jsx     # Side-by-side Before/After recovery diff viewer
│       ├── CourseModal.jsx       # Course intake dialog with color selection
│       ├── CommitmentModal.jsx   # Fixed class and recurring commitment modal
│       ├── DeadlineModal.jsx     # Assignment/exam deadline intake modal
│       └── MicroActionBanner.jsx # Recommended next action card
├── services/
│   └── api.js                    # Centralized REST client with error interception
├── styles/
│   ├── design-tokens.css         # Color palettes, typography, spacing, and borders
│   └── canvas.css                # Grid alignment, event positioning, and responsive rules
├── App.jsx                       # Root application state and view orchestrator
└── main.jsx                      # React 19 entry point and DOM mounting
```

---

## 4. Component Architecture

### `WeeklyCanvas`
Renders a 7-day calendar grid from 07:00 to 23:00. Calculates exact vertical offsets (`top`, `height`) based on event start and end timestamps. Differentiates between:
- Fixed class commitments (high-contrast borders and badge indicators).
- Study blocks (associated course colors and completion toggles).
- Buffer intervals (visual shading for meals and class transit pauses).

### `CommandBar`
Houses application title branding, quick-action dialog buttons (`+ Course`, `+ Class`, `+ Deadline`), and demo data seeding controls.

### `BurnoutMeter`
Displays real-time daily study load against the 5.5-hour cognitive capacity threshold. Automatically changes styling state:
- Green / Neutral: Nominal workload (< 70%).
- Amber / Warning: Heavy workload (70% – 99%).
- Red / Over Capacity: Exceeded workload (>= 100%).

### `RecoveryModal`
Displays a side-by-side diff when a study session is missed:
- **Before Column:** Original schedule with the missed block highlighted.
- **After Column:** Recalculated schedule showing new time slots for shifted study sessions.
- **Strategy Selector:** Allows users to execute *Auto-Heal*, *Triage Mode*, or *Shift Forward*.

---

## 5. Styling & Design System

The frontend employs a tactile slate design system without extraneous decorations:
- **Typography:**
  - Body & UI Headings: `Plus Jakarta Sans`
  - Timestamps, Durations & Math Metrics: `JetBrains Mono`
- **Color Tokens:**
  - Neutral Backgrounds: `#F8FAFC`, `#FFFFFF`, `#F1F5F9`
  - High-Contrast Text: `#0F172A`, `#334155`, `#64748B`
  - Accent / Focus: `#2563EB` (Royal Blue)
  - Status Indicators: `#16A34A` (Success), `#D97706` (Warning), `#DC2626` (Danger)

---

## 6. Production Build

To compile static assets for production deployment:

```bash
npm run build
```

The compiled bundles and HTML files are output to `frontend/dist/`.

To preview the production build locally:

```bash
npm run preview
```
