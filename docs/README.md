# Study Planner Documentation

Welcome to the **Study Planner** technical documentation. This directory provides in-depth guides for understanding the architecture, configuring the backend and frontend services, running automated tests, and deploying the system to production environments.

---

## Documentation Index

| Document | Description |
| :--- | :--- |
| **[Project Overview](OVERVIEW.md)** | Core domain problem, system objectives, and algorithmic guardrails. |
| **[Quick Start](QUICK_START.md)** | Rapid setup guide to get both services running locally in minutes. |
| **[Architecture Overview](ARCHITECTURE.md)** | System topology, domain model hierarchy, database design, and algorithmic workflows. |
| **[Backend Setup & Configuration](BACKEND_SETUP.md)** | Environment variables, database initialization, and backend directory structure. |
| **[Frontend Setup & Architecture](FRONTEND_SETUP.md)** | UI design system, component hierarchy, client API layer, and build instructions. |
| **[API Reference](API_REFERENCE.md)** | REST endpoint specifications, request/response schemas, and error formats. |
| **[Testing Guide](TESTING.md)** | Test suite structure, execution instructions, and test coverage standards. |
| **[Production Deployment](DEPLOYMENT.md)** | Production deployment instructions for Render (backend), Vercel (frontend), and Neon (PostgreSQL). |

---

## System Overview

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

For quick local setup, refer to the [Quick Start Guide](QUICK_START.md).
