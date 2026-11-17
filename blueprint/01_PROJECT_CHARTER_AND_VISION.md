# 01. Project Charter & System Vision: AutoPace (ResilientCal)

---

## 1. Executive Summary & Identity

### Official Project Name
**AutoPace** (Sub-label / Repo Slug: `autopace` or `resilient-cal`)

### Pitch & Tagline
> **"The self-healing, capacity-first academic operating system that reschedules your week when life happens."**

### Core Philosophy
Traditional student planners and productivity tools fail because they are **brittle and punitive**. They assume 100% adherence to ideal schedules. The moment a student gets sick, an experiment runs late, or fatigue hits, the calendar collapses into an anxiety-inducing backlog of overdue red badges. Students abandon planners not from lack of discipline, but from **schedule paralysis and guilt**.

**AutoPace is built on two non-negotiable principles:**
1. **Finite Capacity Awareness:** Time is fixed, and human cognitive energy is finite. You cannot schedule 14 hours of deep study in a day with 6 hours of lectures and expect adherence.
2. **Forgiving Elastic Recovery:** When reality breaks the schedule, AutoPace offers automated, zero-guilt re-balancing with a single click.

---

## 2. Core Value Pillars

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                 AUTOPACE PILLARS                                  │
├─────────────────────────┬─────────────────────────┬───────────────────────────────┤
│   1. CAPACITY SHIELD    │   2. DYNAMIC RECOVERY   │    3. EDITORIAL MINIMALISM    │
│ Strict daily study cap  │ Auto-Heal, Triage MVP,  │ Zero AI-slop neon gradients,  │
│ protects sleep & rest.  │ Cascade Push, Micro-Run │ high-contrast tactile design. │
└─────────────────────────┴─────────────────────────┴───────────────────────────────┘
```

1. **The Capacity Shield (Burnout Prevention):**
   - Automatically tracks waking hours vs. fixed classes vs. meal/transit buffers.
   - Enforces a customizable daily cognitive focus ceiling (default: 5.5 hours/day).
   - Flags overloaded days in advance, before the student starts their week.

2. **The "Things Changed" Dynamic Recovery Engine:**
   - **Auto-Heal Buffers:** Automatically moves missed sessions into future open study buffers before deadlines without exceeding daily fatigue limits.
   - **Triage (MVP Mode):** In crisis weeks, mathematically scales down low/medium priority deliverables (by 25–30%) to safeguard high-stakes exams and lab submissions.
   - **Shift Today:** Moves today's delayed tasks forward by 1–2 hours, gracefully flowing late-night overflow into tomorrow morning.
   - **30-Minute Micro-Sprint:** Immediately breaks procrastination paralysis with a bite-sized, high-leverage starter task.

3. **External Real-World Connectivity:**
   - Live **iCal (`.ics`) subscription feed** so students can view their AutoPace schedule directly on iOS Calendar, Google Calendar, or Outlook.
   - Future-ready integration hooks for Canvas LMS, Blackboard, and syllabus parsing.

---

## 3. Engineering & Code Quality Standards

Any AI or engineer implementing this codebase **must adhere to these strict software craftsmanship rules**:

### Rule 1: Human-Readable & Self-Documenting Code
- Code is read 10x more often than it is written.
- Variable and function names must be descriptive and expressive (e.g., `calculate_remaining_cognitive_budget()` instead of `calc_rem()`, `find_contiguous_free_slots()` instead of `get_slots()`).
- Include meaningful docstrings and inline comments explaining the **"Why"** behind complex business logic (e.g., buffer padding, interval merging), not just the "What".

### Rule 2: Strict Typing & Data Integrity
- **Backend:** Python 3.12+ with strict Pydantic v2 schemas and SQLAlchemy 2.0 type annotations.
- **Frontend:** TypeScript or strictly validated ES2024 with PropTypes / typed interfaces. Zero implicit `any`.

### Rule 3: Decoupled Domain Architecture
- No business logic inside API route handlers or UI components.
- Controllers/Routers only validate input, call domain services, and return responses.
- Scheduler and Recovery algorithms must be pure, testable domain functions independent of database sessions or HTTP requests.

### Rule 4: Zero "AI-Vibe" Aesthetic Policy
- No generic, clichéd purple/indigo neon glows or gratuitous floating glassmorphism cards.
- No unsolicited chat-bot widgets taking up screen real estate.
- Use a calm, purposeful editorial palette inspired by high-end design systems (Linear, Raycast, Vercel, Tailwind Slate).
- Responsive, accessible contrast (WCAG AA/AAA compliant).
