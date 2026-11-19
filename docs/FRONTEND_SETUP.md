# Frontend Setup

- **Entry point:** `frontend/src/main.jsx`
- **Key components:** located under `frontend/src/components/` (e.g., `CommandBar`, `BurnoutMeter`, `WeeklyCanvas`, `EventCard`, `RecoveryModal`, `MicroActionBanner`).
- **Styling:** CSS variables are defined in `frontend/src/styles/*.css`.
- **Running locally:**
  ```bash
  cd frontend
  npm ci            # install dependencies
  npm run dev        # start dev server at http://localhost:5173
  ```
- **Production build:**
  ```bash
  npm run build      # outputs static files to `dist/`
  ```
- **Note:** The UI uses the backend API at `http://127.0.0.1:8000`. Adjust `frontend/src/services/api.js` if you run the backend on a different host/port.
