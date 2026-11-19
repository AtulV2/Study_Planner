# Backend Setup

- **Entry point:** `backend/app/main.py`
- **Database:** SQLite file `autopace.db` created automatically on first run.
- **Key modules:**
  - `backend/app/api/v1/api_router.py` – API routing.
  - `backend/app/services` – business logic for commitments, recovery, and iCal.
- **Environment variables:** See `.env.example` for any required configuration (none for local development).
- **Running locally:**
  ```bash
  cd backend
  uvicorn app.main:app --reload   # http://127.0.0.1:8000
  ```
