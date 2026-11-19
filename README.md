# Study Planner

A capacity-aware, self-healing academic workload management system designed to balance coursework, study sessions, and academic deadlines.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [One-Click Launcher (Windows)](#one-click-launcher-windows)
- [Automated Testing](#automated-testing)
- [Live Calendar Synchronization](#live-calendar-synchronization)
- [Documentation](#documentation)
- [License](#license)

---

## Overview

Academic schedules often suffer from unrealistic workload allocation, leading to academic burnout and missed deadlines. Traditional calendar tools require manual rescheduling whenever an unforeseen delay occurs.

**Study Planner** solves this by treating time as a finite capacity:
- It enforces configurable daily study hour limits (default: 5.5 hours/day).
- It injects mandatory biological pauses (lunch, dinner) and class transit buffers.
- When study sessions are missed, an integrated recovery engine recalculates schedules using mathematical gap-finding and triage algorithms instead of silently accumulating overdue tasks.

---

## Key Features

- **Capacity-Aware Workload Allocation:** Enforces daily cognitive caps and schedules study blocks within optimal daytime windows.
- **Dynamic Recovery Engine:** When a study block is missed, users can choose from three recovery strategies:
  1. *Auto-Heal:* Automatically finds open gap buffers prior to assignment deadlines.
  2. *Triage Mode:* Scalably downscales study targets for lower-priority tasks to protect critical exam prep.
  3. *Shift Forward:* Advances remaining blocks while respecting sleep and wake boundaries.
- **Transit & Meal Buffer Injection:** Automatically reserves dedicated intervals for lunch (12:30–13:15), dinner (18:30–19:15), and 15-minute buffers after each in-person class.
- **Live iCalendar Feed:** Exposes an RFC 5545 compliant `.ics` endpoint to subscribe to updated schedules via Google Calendar, Apple Calendar, or Microsoft Outlook.
- **Weekly Canvas Interface:** Interactive visual weekly calendar with real-time burnout capacity metering and quick-intake dialogs for courses, commitments, and deadlines.
- **Dual-Engine Persistence:** Default zero-config SQLite with WAL mode for local development, with native support for managed PostgreSQL (e.g., Neon) in production.

---

## Architecture

```
+-----------------------------------------------------------+
|                   Client Interface                        |
|        (React 19, Vite, Lucide Icons, Responsive Grid)    |
+-----------------------------------------------------------+
                             │
                      REST API / JSON
                             │
                             ▼
+-----------------------------------------------------------+
|                   Backend Service                         |
|      FastAPI, Pydantic v2, Pure Domain Algorithms        |
|   (Interval Merging, Capacity Allocator, Recovery Engine) |
+-----------------------------------------------------------+
          │                                  │
          ▼                                  ▼
+-----------------------+          +------------------------+
|   Relational Database |          |   External Subscribers |
|  (SQLite / PostgreSQL)|          | (Google/Apple Calendar)|
+-----------------------+          +------------------------+
```

---

## Repository Structure

```
study-planner/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST endpoints (courses, commitments, deadlines, recovery)
│   │   ├── core/            # Database engine, settings, and domain exceptions
│   │   ├── models/          # SQLAlchemy ORM models with cascading relationships
│   │   ├── schemas/         # Pydantic validation models
│   │   ├── services/        # Scheduling, capacity allocation, recovery, and iCal generation
│   │   └── main.py          # Application entry point and middleware configuration
│   ├── tests/               # Pytest test suite (unit and integration tests)
│   └── requirements.txt     # Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # UI components (WeeklyCanvas, CommandBar, Modals)
│   │   ├── services/        # API integration client
│   │   └── styles/          # Design system and typography styles
│   ├── package.json         # Node.js dependencies and scripts
│   └── vite.config.js       # Vite bundler configuration
└── docs/                    # Technical documentation and guides
```

---

## Getting Started

### Prerequisites

- **Python:** Version 3.11 or higher
- **Node.js:** Version 18.0 or higher
- **npm:** Version 9.0 or higher

### Backend Setup

1. Navigate to the project root and create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```

3. Install required Python packages:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Start the development server:
   ```bash
   python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

The interactive OpenAPI documentation will be accessible at:  
`http://127.0.0.1:8000/docs`

### Frontend Setup

1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

The application interface will be accessible at:  
`http://localhost:5173`

### One-Click Launcher (Windows)

On Windows systems, you can launch both backend and frontend servers simultaneously by double-clicking:
```
start_all.bat
```

---

## Automated Testing

The backend includes a comprehensive test suite covering database models, foreign key cascades, capacity allocation algorithms, buffer injections, and recovery strategies.

Run the test suite from the repository root:

```bash
python -m pytest backend/tests -v
```

All unit and integration tests validate domain rules against an isolated, in-memory SQLite database instance.

---

## Live Calendar Synchronization

Study Planner generates a live RFC 5545 calendar feed. To sync with your external calendar:

1. Copy the feed URL:
   ```text
   http://127.0.0.1:8000/api/v1/calendar/feed.ics
   ```
2. In Google Calendar, Apple Calendar, or Outlook, choose **Add Calendar** > **Subscribe from Web** (or **From URL**) and paste the address.

---

## Documentation

Comprehensive project documentation is maintained in the [`docs/`](docs/) directory:

- [Documentation Index](docs/README.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Backend Setup & Configuration](docs/BACKEND_SETUP.md)
- [Frontend Setup & Components](docs/FRONTEND_SETUP.md)
- [API Reference](docs/API_REFERENCE.md)
- [Testing Guide](docs/TESTING.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

---

## License

This project is licensed under the [MIT License](LICENSE).
