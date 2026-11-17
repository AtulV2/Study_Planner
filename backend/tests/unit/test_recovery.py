"""Unit tests verifying auto-heal, triage MVP downscaling, and shift-today recovery."""

from datetime import date, datetime, time, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.app.models.course import Course
from backend.app.models.deadline import Deadline
from backend.app.models.study_block import StudyBlock
from backend.app.models.recovery_event import RecoveryEvent
from backend.app.services.recovery_service import RecoveryService


def test_auto_heal_missed_blocks(db_session: Session):
    """Verifies missed study blocks are rescheduled into valid future gaps."""
    now = datetime(2026, 11, 18, 10, 0, tzinfo=timezone.utc)

    course = Course(code="CS 240", name="Data Structures", color="#3B82F6")
    db_session.add(course)
    db_session.commit()

    due_dt = now + timedelta(days=2)
    deadline = Deadline(
        course_id=course.id,
        title="Lab Assignment",
        due_datetime=due_dt,
        estimated_hours=2.0,
        priority="high",
    )
    db_session.add(deadline)
    db_session.commit()

    # Block in the past marked missed
    missed_start = now - timedelta(hours=2)
    missed_block = StudyBlock(
        deadline_id=deadline.id,
        title="Lab Work Session",
        start_datetime=missed_start,
        end_datetime=missed_start + timedelta(hours=1),
        duration_minutes=60,
        status="missed",
    )
    db_session.add(missed_block)
    db_session.commit()

    # Test preview non-destructive diff
    preview = RecoveryService.preview_recovery(db_session, current_time=now)
    assert len(preview) == 1
    assert preview[0]["resolvable"] is True
    assert preview[0]["status_change"] == "missed -> recovered"

    # Execute auto-heal
    result = RecoveryService.auto_heal(db_session, current_time=now)
    assert result["status"] == "success"
    assert result["healed_count"] == 1

    # Verify block is now recovered and scheduled after `now`
    db_session.refresh(missed_block)
    assert missed_block.status == "recovered"
    assert missed_block.start_datetime >= now
    assert "Auto-healed" in missed_block.notes

    # Verify RecoveryEvent logged
    events = db_session.execute(select(RecoveryEvent).where(RecoveryEvent.trigger_type == "auto_heal")).scalars().all()
    assert len(events) == 1
    assert events[0].affected_blocks_count == 1


def test_triage_mvp_downscaling(db_session: Session):
    """Verifies triage mode reduces low priority by 30% and medium by 20%."""
    now = datetime(2026, 11, 18, 9, 0, tzinfo=timezone.utc)

    course = Course(code="ENGL 101", name="Literature", color="#8B5CF6")
    db_session.add(course)
    db_session.commit()

    dl_low = Deadline(
        course_id=course.id,
        title="Optional Reading Essay",
        due_datetime=now + timedelta(days=3),
        estimated_hours=10.0,
        priority="low",
    )
    dl_med = Deadline(
        course_id=course.id,
        title="Weekly Response Paper",
        due_datetime=now + timedelta(days=3),
        estimated_hours=10.0,
        priority="medium",
    )
    dl_high = Deadline(
        course_id=course.id,
        title="Final Research Project",
        due_datetime=now + timedelta(days=3),
        estimated_hours=10.0,
        priority="high",
    )
    db_session.add_all([dl_low, dl_med, dl_high])
    db_session.commit()

    result = RecoveryService.triage_mvp(db_session)
    assert result["status"] == "success"

    db_session.refresh(dl_low)
    db_session.refresh(dl_med)
    db_session.refresh(dl_high)

    # Low priority should be 10.0 * 0.70 = 7.0 hours
    assert dl_low.estimated_hours == 7.0
    # Medium priority should be 10.0 * 0.80 = 8.0 hours
    assert dl_med.estimated_hours == 8.0
    # High priority should remain 10.0 hours
    assert dl_high.estimated_hours == 10.0


def test_shift_today_and_bedtime_overflow(db_session: Session):
    """Verifies shift-today pushes blocks forward and overflows into tomorrow if past bedtime."""
    # Start at 21:30 (bedtime is 23:00)
    now = datetime(2026, 11, 18, 21, 30, tzinfo=timezone.utc)

    # Block scheduled at 22:00 for 60 min (ends at 23:00)
    late_block = StudyBlock(
        title="Late Night Review",
        start_datetime=datetime(2026, 11, 18, 22, 0, tzinfo=timezone.utc),
        end_datetime=datetime(2026, 11, 18, 23, 0, tzinfo=timezone.utc),
        duration_minutes=60,
        status="scheduled",
    )
    db_session.add(late_block)
    db_session.commit()

    # Shift by 60 minutes -> proposed end 24:00 (past 23:00 bedtime)
    result = RecoveryService.shift_today(db_session, shift_minutes=60, current_time=now)
    assert result["status"] == "success"
    assert result["shifted_count"] == 1

    db_session.refresh(late_block)
    # Block should have overflowed into tomorrow morning (2026-11-19 at 08:00 wake_time)
    assert late_block.start_datetime.date() == date(2026, 11, 19)
    assert late_block.start_datetime.time() == time(8, 0)
    assert "Shifted today past bedtime into tomorrow morning" in late_block.notes


def test_get_micro_action(db_session: Session):
    """Verifies micro-action starter returns a 30-35 min focus task."""
    now = datetime(2026, 11, 18, 14, 0, tzinfo=timezone.utc)

    block = StudyBlock(
        title="Deep Reading",
        start_datetime=now + timedelta(minutes=10),
        end_datetime=now + timedelta(minutes=70),
        duration_minutes=60,
        status="scheduled",
    )
    db_session.add(block)
    db_session.commit()

    action = RecoveryService.get_micro_action(db_session, current_time=now)
    assert action is not None
    assert action["type"] == "study_block"
    assert action["duration_minutes"] <= 35
    assert "Quick Start" in action["title"]
