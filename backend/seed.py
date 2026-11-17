"""Standalone script to seed the database."""

from backend.app.core.database import SessionLocal, Base, engine
from backend.app.api.v1.seed import seed_scenario

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        result = seed_scenario(db)
        print("Database seeded:", result)
    finally:
        db.close()
