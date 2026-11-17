"""Capacity service module for cognitive load calculations and burnout guardrails."""

from datetime import date, datetime, timezone
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from backend.app.models.study_block import StudyBlock
from backend.app.models.student_config import StudentConfig
from backend.app.core.config import settings


class CapacityService:
    """Calculates student cognitive load and enforces daily study caps."""

    @staticmethod
    def get_or_create_config(db: Session) -> StudentConfig:
        """Retrieves active student configuration or instantiates defaults."""
        config = db.execute(select(StudentConfig)).scalars().first()
        if not config:
            config = StudentConfig(
                max_daily_study_hours=settings.DEFAULT_MAX_DAILY_STUDY_HOURS,
                wake_time=settings.DEFAULT_WAKE_TIME,
                sleep_time=settings.DEFAULT_SLEEP_TIME,
                preferred_chunk_minutes=settings.DEFAULT_PREFERRED_CHUNK_MINUTES,
                min_gap_buffer_minutes=settings.DEFAULT_MIN_GAP_BUFFER_MINUTES,
                protect_weekends=settings.DEFAULT_PROTECT_WEEKENDS,
            )
            db.add(config)
            db.commit()
            db.refresh(config)
        return config

    @staticmethod
    def get_daily_study_minutes(db: Session, target_date: date) -> int:
        """Sums duration of all active study blocks scheduled for a specific date."""
        start_of_day = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=timezone.utc)
        end_of_day = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, tzinfo=timezone.utc)

        blocks = db.execute(
            select(StudyBlock).where(
                StudyBlock.start_datetime >= start_of_day,
                StudyBlock.start_datetime <= end_of_day,
                StudyBlock.status.in_(["scheduled", "completed", "recovered"]),
            )
        ).scalars().all()

        return sum(block.duration_minutes for block in blocks)

    @classmethod
    def evaluate_day_capacity(cls, db: Session, target_date: date, additional_minutes: int = 0) -> Dict[str, Any]:
        """Evaluates daily capacity against configured burnout thresholds."""
        config = cls.get_or_create_config(db)
        max_minutes = int(config.max_daily_study_hours * 60)
        current_minutes = cls.get_daily_study_minutes(db, target_date)
        projected_minutes = current_minutes + additional_minutes
        remaining_minutes = max(0, max_minutes - projected_minutes)

        load_ratio = projected_minutes / max_minutes if max_minutes > 0 else 1.0

        if load_ratio > 1.0:
            status = "over_capacity"  # Exceeded daily limit
            risk_level = "red"
        elif load_ratio >= 0.8:
            status = "near_capacity"  # 80%+ limit warning
            risk_level = "amber"
        else:
            status = "healthy"
            risk_level = "green"

        return {
            "date": target_date.isoformat(),
            "max_minutes": max_minutes,
            "current_minutes": current_minutes,
            "projected_minutes": projected_minutes,
            "remaining_minutes": remaining_minutes,
            "load_ratio": round(load_ratio, 3),
            "status": status,
            "risk_level": risk_level,
            "exceeds_cap": projected_minutes > max_minutes,
        }
