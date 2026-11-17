# 03. UI/UX Design Specification: The Anti-"AI-Slop" Standard

---

## 1. Aesthetic Philosophy: Editorial Swiss Precision

The user interface of AutoPace must look and feel like an elite, purpose-built operating system—comparable to **Linear, Raycast, Things 3, or Vercel**—and strictly avoid the generic clichés of AI-generated web apps.

```
❌ AVOID (The "AI-Slop" Vibe):
• Gratuitous neon purple/pink floating gradients
• Heavy blurry glassmorphism on every card
• Decorative floating sparkle icons with no functional purpose
• Unsolicited chat-bubble overlays blocking user work
• Tiny, unaligned cards with unpredictable padding and erratic borders

✅ DEMAND (AutoPace Modern Craft):
• High-contrast, tactile slate palette with intentional whitespace
• Crisp 1px subtle borders (`#E2E8F0` light, `#1E293B` dark)
• Monospace accents for time/numerical metrics (*JetBrains Mono*)
• Clear semantic visual hierarchy: Fixed commitments look like solid structural pillars;
  flexible focus blocks look like fluid, movable tiles.
• Instant keyboard shortcuts and deterministic hover/active feedback
```

---

## 2. Design System & Token Foundation

### Color Palette Tokens (Warm Slate Theme)

```css
:root {
  /* Surfaces & Backgrounds */
  --bg-app: #F8FAFC;          /* Canvas background: clean, soft slate white */
  --bg-surface: #FFFFFF;      /* Primary card/modal surface */
  --bg-surface-subtle: #F1F5F9;/* Headers, table bars, dividers */
  --bg-surface-hover: #E2E8F0; /* Interactive hover state */
  
  /* Text & Contrast */
  --text-primary: #0F172A;    /* Slate 900: High clarity deep charcoal */
  --text-secondary: #475569;  /* Slate 600: Supporting context */
  --text-muted: #94A3B8;      /* Slate 400: Placeholders, minor timestamps */
  --text-inverse: #FFFFFF;    /* Clean white for solid badges */

  /* Borders & Dividers */
  --border-subtle: #E2E8F0;   /* 1px crisp divider */
  --border-strong: #CBD5E1;   /* Focus states & modal outlines */

  /* Intentional Semantic Accents (No Purple Neon) */
  --accent-focus: #2563EB;     /* Royal Cobalt: Active study sessions & primary actions */
  --accent-fixed: #334155;     /* Deep Slate: Fixed classes & lectures (solid anchors) */
  --accent-safe: #059669;      /* Emerald: Healthy capacity & completed tasks */
  --accent-warning: #D97706;   /* Amber: Capacity overload warning (>5.5h) */
  --accent-danger: #DC2626;    /* Crimson: Missed session or at-risk deadline */
  --accent-recovery: #0284C7;  /* Sky Blue: Dynamic recovery trigger & preview */

  /* Shadows (Tactile, Soft, Never Blurry Slop) */
  --shadow-sm: 0 1px 2px 0 rgba(15, 23, 42, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
  --shadow-modal: 0 20px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
}
```

### Typography Hierarchy

* **Primary Sans:** `Plus Jakarta Sans`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `sans-serif`  
  *Crisp geometric clarity, perfect tracking for data-dense productivity tools.*
* **Monospace Code/Time:** `JetBrains Mono`, `ui-monospace`, `monospace`  
  *Used for exact clock times (`09:30 – 11:00`), hour counts (`4.5h`), and course codes (`CS 240`).*

| Element | Size | Weight | Tracking | Line Height |
| :--- | :--- | :--- | :--- | :--- |
| **App Title** | `18px` | `700` | `-0.02em` | `1.2` |
| **Section Header** | `14px` | `600` | `-0.01em` | `1.4` |
| **Card Title** | `13px` | `600` | `0` | `1.3` |
| **Body Text** | `13px` | `400` | `0` | `1.5` |
| **Time Badge / Monospace** | `11px` | `500` | `0.02em` | `1.2` |
| **Micro Labels** | `10px` | `700` | `0.05em` (Uppercase) | `1.0` |

---

## 3. Core Screen Layouts & Component Specifications

The application layout is structured around 3 coordinated zones:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. GLOBAL COMMAND BAR (App Title | Week Selector | Quick Add | Recover Btn) │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. CAPACITY & BURNOUT SHIELD BAR (Mon to Sun Capacity Utilization Meters)   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. THE WEEKLY WORKLOAD CANVAS                                               │
│ ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────────┐ │
│ │ MON     │ TUE     │ WED     │ THU     │ FRI     │ SAT     │ SUN         │ │
│ │ 3.5h/5h │ 5.0h/5h │ 6.5h ⚠️ │ 4.0h/5h │ 2.0h/5h │ 0.0h/5h │ 1.5h/5h     │ │
│ ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────────┤ │
│ │ [CLASS] │ [FOCUS] │ [CLASS] │ [CLASS] │ [FOCUS] │ (Free)  │ [FOCUS]     │ │
│ │ CS 240  │ PS 3    │ CS 240  │ CS 240  │ Review  │         │ Prep Quiz   │ │
│ │ (Solid) │ (Fluid) │ (Solid) │ (Solid) │ (Fluid) │         │ (Fluid)     │ │
│ └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component A: The Weekly Canvas Grid
* **Visual Differentiation:**
  - **Fixed Commitments (Classes, Shifts):** Solid slate border, solid left indicator bar, subtle background tint matching course color. Cannot be dragged or modified by the auto-scheduler.
  - **Study Blocks (Flexible Focus):** Lighter card surface, dashed or rounded border, clear checkbox/toggle circle for "Complete", subtle "Missed" indicator if past start time.
* **Hover State:** Reveals subtle, non-intrusive action buttons:
  - Checkmark (Mark Done)
  - Alert/Missed (Mark Missed -> triggers recovery recommendation)
  - Trash (Delete session)

### Component B: The Burnout Guardrail Meter
* Positioned directly below the day headers.
* Displays a segmented horizontal bar representing:
  - Fixed hours (Slate)
  - Scheduled study hours (Blue)
  - Safe remaining buffer (Light Gray)
* **Burnout Threshold Warning:** If total study hours exceed the student's configured daily cap (e.g. `> 5.5h`), the bar turns soft Amber (`#D97706`), showing an alert pill: `"Overload (+1.2h) — Risk of Fatigue"`.

### Component C: The "Things Changed" Recovery Modal / Drawer
When the user clicks **"Recover Schedule"** or marks an event as missed:
* **Never silently alter the user's schedule without showing a visual diff.**
* The modal presents a side-by-side **Before vs. After** preview:
  ```
  BEFORE (Disrupted)              AFTER (Healed)
  -------------------------------------------------------------
  [Missed] PS3 Coding (Mon 14:00) ──► [Recovered] PS3 Coding (Tue 10:15)
  Day Load: Over capacity         ──► Load balanced (4.2h/5.5h)
  ```
* Provides 3 clear recovery tabs:
  1. **Auto-Heal Buffers:** Fits missed blocks into open slots before deadline.
  2. **Triage (MVP Mode):** Trims 25% from low-priority tasks to save exam prep.
  3. **Shift Today:** Moves today's remaining blocks forward by 1–2 hours.
* Action Buttons:
  - `Cancel` (Leaves schedule unchanged)
  - `Apply Recovery Plan` (Single-click optimistic commit with undo toast)

---

## 4. Edge Case UI States & Ergonomics

1. **Empty Canvas State:**
   - If a student has no classes or deliverables, do **not** display a blank white page.
   - Display a thoughtful empty state: `"Your week is completely open. Add your recurring classes or click 'Seed Demo Week' to explore."`
2. **Over-Constrained Week (Zero Free Gaps Available):**
   - If a student has 40 hours of classes and 30 hours of deadlines, the scheduler cannot mathematically fit everything.
   - The UI must display an honest **Triage Banner**: `"Schedule mathematically full. 3.5 hours of study cannot fit before Friday's deadline. Click 'Triage Week' to downscale low-stakes deliverables."`
3. **Optimistic Updates & Toast Notifications:**
   - When marking a task complete, deleting a card, or executing recovery, update the UI instantly (0ms latency).
   - Show a non-blocking toast at bottom-right with an `"Undo (Z)"` action button.
