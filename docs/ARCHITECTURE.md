# Architecture Overview

```
+---------------------+          +-------------------+
|  Browser (React)   | <--API-->|   FastAPI Server  |
|  http://localhost:5173 |     | http://127.0.0.1:8000 |
+---------------------+          +-------------------+
          |                               |
          |   SQLite DB (autopace.db)      |
          +-------------------------------+
```

- **Frontend** (React 19 + Vite) renders UI components and calls the backend via the axios wrapper in `frontend/src/services/api.js`.
- **Backend** (FastAPI) provides REST endpoints for CRUD operations on commitments, recovery calculations, and an iCal feed (`/api/v1/ical`).
- **Database**: SQLite file `autopace.db` lives in the project root; SQLAlchemy ORM maps models (`backend/app/models`).
- **Recovery Engine** (`backend/app/services/recovery.py`) runs on demand or via a scheduled task to generate "recovered" study blocks for missed sessions.
- **Automation**: Pytest suite validates both frontend build output and backend API contracts.
