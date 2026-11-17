"""Pytest configuration and shared database session fixtures."""

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from backend.app.core.database import Base
from backend.app.models.course import Course
from backend.app.models.commitment import FixedCommitment
from backend.app.models.deadline import Deadline
from backend.app.models.study_block import StudyBlock
from backend.app.models.student_config import StudentConfig
from backend.app.models.recovery_event import RecoveryEvent


@pytest.fixture(scope="function")
def db_session() -> Session:
    """Creates a clean, isolated in-memory SQLite database for each test function."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    # Enforce SQLite foreign keys in-memory
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
    session = TestingSessionLocal()

    # Pre-seed default student config
    config = StudentConfig(
        max_daily_study_hours=5.5,
        wake_time="08:00",
        sleep_time="23:00",
        preferred_chunk_minutes=60,
        min_gap_buffer_minutes=15,
        protect_weekends=False,
    )
    session.add(config)
    session.commit()

    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)
