# Backend Setup & Configuration

This guide provides technical details for setting up, configuring, and maintaining the **Study Planner** backend service.

---

## 1. System Requirements

- **Python:** 3.11 or higher
- **Package Manager:** `pip` (or `uv` / `poetry`)
- **Virtual Environment:** Recommended (`venv` or `conda`)

---

## 2. Installation Steps

1. Navigate to the repository root:
   ```bash
   cd r1
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r backend/requirements.txt
   ```

---

## 3. Configuration & Environment Variables

Configuration is managed via Pydantic Settings (`backend/app/core/config.py`). Environment variables can be defined in a `.env` file in the project root:

| Variable | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | string | `Study Planner` | Application display name. |
| `API_V1_PREFIX` | string | `/api/v1` | URL prefix for REST endpoints. |
| `DATABASE_URL` | string | `sqlite:///./study_planner.db` | SQLAlchemy connection string (SQLite or PostgreSQL). |
| `DEFAULT_MAX_DAILY_STUDY_HOURS` | float | `5.5` | Daily study limit ceiling in hours. |
| `DEFAULT_WAKE_TIME` | string | `08:00` | Start of daily available window (HH:MM). |
| `DEFAULT_SLEEP_TIME` | string | `23:00` | End of daily available window (HH:MM). |
| `DEFAULT_PREFERRED_CHUNK_MINUTES` | int | `60` | Target duration for scheduled study blocks. |
| `DEFAULT_MIN_GAP_BUFFER_MINUTES` | int | `15` | Minimum transit buffer inserted after classes. |
| `LUNCH_START` / `LUNCH_END` | string | `12:30` / `13:15` | Mandatory daily lunch break interval. |
| `DINNER_START` / `DINNER_END` | string | `18:30` / `19:15` | Mandatory daily dinner break interval. |

---

## 4. Running the Development Server

Execute the ASGI application from the repository root:

```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **Health Check:** `http://127.0.0.1:8000/api/v1/health`
- **Interactive OpenAPI Documentation:** `http://127.0.0.1:8000/docs`
- **Alternative ReDoc UI:** `http://127.0.0.1:8000/redoc`

---

## 5. Database Management

### Local Development (SQLite)
By default, the backend initializes a local SQLite database named `study_planner.db`. Write-Ahead Logging (WAL) and foreign key pragmas are enabled automatically on connection.

### Production (PostgreSQL)
To connect to an external PostgreSQL database (such as Neon), set the `DATABASE_URL` environment variable:

```bash
DATABASE_URL=postgresql://user:password@ep-sample.region.neon.tech/neondb?sslmode=require
```

The database connection pool automatically adapts to PostgreSQL dialects with connection recycling and pre-ping checks.

---

## 6. Pre-Seeding Demo Scenarios

The backend provides a seed endpoint to populate realistic demo courses, commitments, and deadlines:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/seed
```

This endpoint wipes previous demo records and inserts a complete academic schedule for immediate testing.
