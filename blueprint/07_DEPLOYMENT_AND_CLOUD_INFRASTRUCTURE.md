# 07. Locked Cloud Deployment & Infrastructure: Vercel + Render + Neon

---

## 1. Locked Production Stack Overview

The production deployment architecture for AutoPace is **100% cloud-hosted on zero-cost tiers**, requiring zero credit cards while maintaining enterprise-grade uptime and performance.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          LOCKED CLOUD ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  FRONTEND: Vercel                                                           │
│  • Framework: React 19 + Vite (Single Page Application)                     │
│  • Edge CDN: Global SSL/HTTPS, asset compression, HTTP/2                    │
│  • Live URL: https://autopace.vercel.app                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                      │ (Encrypted HTTPS REST API Calls)
│                                      ▼
│  BACKEND: Render (Web Service)                                              │
│  • Runtime: Python 3.12+ (FastAPI + Uvicorn)                                │
│  • Container: Linux Web Service running on port $PORT                       │
│  • Live URL: https://autopace-api.onrender.com                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                      │ (SSL Pooled Connection)
│                                      ▼
│  DATABASE: Neon Serverless PostgreSQL                                       │
│  • Engine: PostgreSQL 16 (Serverless, Auto-scaling)                         │
│  • Connection: Pooled connection string with `sslmode=require`              │
│  • Local Parity: Seamless fallback to SQLite (`autopace.db`) for offline dev│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Database Layer Specification: Dual SQLite / Neon PostgreSQL

To ensure developers can run and test offline while deploying to Neon in production, the data access layer in `backend/app/core/database.py` must dynamically resolve the engine:

### `backend/app/core/database.py` Implementation Contract

```python
"""
Database session factory and engine manager.
Supports local SQLite for development/testing and Neon PostgreSQL for production.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Fetch connection string from environment; fallback to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./autopace.db")

# 2. Normalize legacy "postgres://" prefixes (used by some cloud hosts) to SQLAlchemy's "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Configure dialect-specific engine parameters
connect_args = {}
engine_kwargs = {
    "echo": os.getenv("SQL_DEBUG", "false").lower() == "true",
}

if "sqlite" in DATABASE_URL:
    # SQLite requires disabling same-thread checks for FastAPI concurrency
    connect_args["check_same_thread"] = False
else:
    # Neon Serverless PostgreSQL: connection pooling configuration
    engine_kwargs.update({
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True, # Automatically recycle dropped connections
        "pool_recycle": 300,
    })

# 4. Create Engine & Session Factory
engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency yielding an isolated database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Required Backend Dependencies (`backend/requirements.txt`)
```text
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
```

---

## 3. Backend Deployment Contract: Render

### Render Web Service Configuration
- **Repository:** Connected GitHub repository (`main` branch)
- **Root Directory:** `backend`
- **Environment:** `Python 3`
- **Region:** Frankfurt (EU) or Oregon (US) — match the Neon database region for lowest latency
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Backend Environment Variables (Configured in Render Dashboard)
| Variable | Value / Format | Purpose |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://user:pass@ep-xyz-pooler.region.neon.tech/neondb?sslmode=require` | Pooled Neon PostgreSQL connection string |
| `FRONTEND_URL` | `https://autopace.vercel.app` | Production frontend domain for strict CORS allowance |
| `ENVIRONMENT` | `production` | Enables production optimizations and disables debug traces |
| `PYTHONUNBUFFERED` | `1` | Ensures real-time stdout log streaming in Render console |

### CORS Middleware Implementation in `backend/app/main.py`
```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AutoPace API",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None
)

# Allow local Vite dev server and production Vercel deployment
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    os.getenv("FRONTEND_URL", "https://autopace.vercel.app")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

---

## 4. Frontend Deployment Contract: Vercel

### Vercel Project Configuration
- **Framework Preset:** `Vite`
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Node Version:** `18.x` or `20.x`

### Dynamic API Endpoint Handling in Frontend
In `frontend/src/services/api.js`:
```javascript
// Automatically falls back to local FastAPI server if VITE_API_URL is unset
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  // Handle HTTP 204 No Content gracefully
  if (response.status === 204) {
    return null;
  }

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}
```

### Frontend Environment Variables (Configured in Vercel Dashboard)
| Variable | Value | Purpose |
| :--- | :--- | :--- |
| `VITE_API_URL` | `https://autopace-api.onrender.com` | Directs production frontend calls to the Render backend |

### Client-Side SPA Routing (`frontend/vercel.json`)
To ensure deep links and client-side refreshes do not return 404:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

---

## 5. End-to-End Deployment Verification Checklist

Before releasing to production, verify:
- [ ] Neon database tables auto-create via `Base.metadata.create_all(bind=engine)` or Alembic on startup.
- [ ] Render healthcheck `GET https://autopace-api.onrender.com/api/v1/health` returns `200 OK` and `"database": "connected (PostgreSQL)"`.
- [ ] Vercel frontend loads with zero CORS console errors.
- [ ] Seed action `/api/v1/seed` successfully writes demo records into Neon PostgreSQL.
- [ ] Status updates (complete/missed) persist across page reloads.
