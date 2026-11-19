# Quick Start Guide

This guide provides the fastest path to running **Study Planner** locally.

---

## Prerequisites

- **Python:** 3.11 or higher
- **Node.js:** 18.0 or higher
- **npm:** 9.0 or higher

---

## Step 1: Clone and Set Up Virtual Environment

```bash
# Clone the repository
git clone <repository-url>
cd r1

# Create and activate Python virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate
```

---

## Step 2: Set Up and Start Backend

```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Start the FastAPI backend
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

- API Base URL: `http://127.0.0.1:8000`
- Interactive OpenAPI Docs: `http://127.0.0.1:8000/docs`

---

## Step 3: Set Up and Start Frontend

In a separate terminal window:

```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```

- Frontend Application: `http://localhost:5173`

---

## Alternative: Windows One-Click Launcher

On Windows systems, you can start both backend and frontend servers in separate windows with a single command:

```cmd
start_all.bat
```

---

## Verifying the Installation

1. Open your browser and navigate to `http://localhost:5173`.
2. Click **Seed Demo Data** or open the Command Bar to populate sample courses and commitments.
3. Review the Weekly Canvas grid to ensure calendar blocks and burnout meters render properly.
