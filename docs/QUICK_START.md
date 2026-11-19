# Quick Start
```bash
# Clone the repo
git clone <repo-url>
cd r1

# Install backend dependencies (Python 3.12+)
python -m venv .venv
. .venv/Scripts/activate
pip install -r backend/requirements.txt

# Run the backend (default http://127.0.0.1:8000)
uvicorn backend.app.main:app --reload

# Install frontend dependencies (Node 20+)
cd frontend
npm ci
npm run dev   # http://localhost:5173
```
Visit the UI in a browser and start adding commitments.