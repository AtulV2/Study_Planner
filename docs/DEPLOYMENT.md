# Production Deployment Guide

This guide details the step-by-step procedure for deploying **Study Planner** to a production cloud architecture using:
- **Database:** Neon (Serverless PostgreSQL)
- **Backend:** Render (FastAPI Docker Web Service)
- **Frontend:** Vercel (React 19 Static Site)

---

## 1. Production Architecture

```
+-----------------------------------------------------------+
|                    Vercel (Frontend)                      |
|             https://study-planner.vercel.app              |
+-----------------------------------------------------------+
                             │
                  HTTPS API Requests (CORS)
                             │
                             ▼
+-----------------------------------------------------------+
|                    Render (Backend)                       |
|           https://study-planner-api.onrender.com          |
|                 FastAPI in Docker Container               |
+-----------------------------------------------------------+
                             │
                    Encrypted SSL Pool
                             │
                             ▼
+-----------------------------------------------------------+
|                    Neon (PostgreSQL)                      |
|                Serverless Postgres Database               |
+-----------------------------------------------------------+
```

---

## 2. Step 1: Database Setup (Neon PostgreSQL)

1. Sign in to your [Neon Console](https://console.neon.tech).
2. Click **Create Project**:
   - **Project Name:** `study-planner-db`
   - **Postgres Version:** Latest (v16 or v17)
   - **Region:** Select the region closest to your Render service (e.g., US East / Oregon).
3. Once provisioned, locate the **Connection Details** panel.
4. Select **Pooled Connection** and copy the connection string. It will look like:
   ```text
   postgresql://<username>:<password>@<endpoint>-pooler.region.neon.tech/neondb?sslmode=require
   ```

---

## 3. Step 2: Backend Deployment (Render)

1. Sign in to the [Render Dashboard](https://dashboard.render.com).
2. Click **New +** > **Web Service**.
3. Select your connected GitHub repository.
4. Configure service settings:
   - **Name:** `study-planner-backend`
   - **Region:** Match your Neon database region.
   - **Language:** `Docker` (Render automatically detects `Dockerfile` in the root).
   - **Branch:** `main`
5. Configure Environment Variables under the **Environment** tab:
   - `DATABASE_URL`: Paste your Neon pooled connection string.
   - `CORS_ORIGINS`: Set to your Vercel domain (e.g., `https://study-planner.vercel.app` or `*` for initial setup).
6. Configure the Health Check path:
   - **Health Check Path:** `/api/v1/health`
7. Click **Create Web Service**.
8. Once the build finishes and the service status is **Live**, copy your public URL:
   `https://study-planner-backend.onrender.com`

---

## 4. Step 3: Frontend Deployment (Vercel)

1. Sign in to [Vercel](https://vercel.com).
2. Click **Add New...** > **Project** and import your GitHub repository.
3. In the project configuration screen:
   - **Framework Preset:** `Vite`
   - **Root Directory:** Edit and select `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`
4. Expand **Environment Variables**:
   - `VITE_BACKEND_URL`: Set to your Render backend URL (e.g., `https://study-planner-backend.onrender.com`).
5. Click **Deploy**.

---

## 5. Verification & Smoke Test

Once both services are deployed:

1. **Test Backend Health:**
   ```bash
   curl https://study-planner-backend.onrender.com/api/v1/health
   ```
   Expected response:
   ```json
   {"status":"healthy","version":"1.0.0","database":"connected"}
   ```

2. **Open Frontend:**
   Navigate to your Vercel deployment URL in a browser.
3. **Verify Interactive Functionality:**
   - Click **Seed Demo Data** to populate sample courses and commitments.
   - Confirm that the Weekly Canvas grid renders all scheduled blocks and that the Burnout Meter calculates daily totals.
4. **Subscribe to Calendar:**
   Verify that you can download the calendar feed:
   `https://study-planner-backend.onrender.com/api/v1/calendar/feed.ics`
