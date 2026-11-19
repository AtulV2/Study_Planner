# Project Overview

AutoPace tracks study blocks ("commitments") and automatically recovers missed sessions via a recovery algorithm. It stores data in a SQLite DB (`autopace.db`) and offers a public iCal feed for calendar integration.

The repository contains a full‑stack application:

- **Backend** – FastAPI + SQLAlchemy, exposing a REST API and an iCal endpoint.
- **Frontend** – React 19 powered by Vite, with components such as `CommandBar`, `BurnoutMeter`, `WeeklyCanvas`, `EventCard`, `RecoveryModal`, and `MicroActionBanner`.
- **Automation** – pytest suite, CI‑compatible scripts, and a set of development‑only artefacts under the `.ai` directory (now ignored via `.gitignore`).
