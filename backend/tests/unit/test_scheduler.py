"""Unit tests verifying interval arithmetic, gap extraction, and 5.5h study cap enforcement."""

from datetime import date, datetime, time, timedelta, timezone
from sqlalchemy.orm import Session
from backend.app.models.course import Course
from backend.app.models.commitment import FixedCommitment
from backend.app.models.deadline import Deadline
from backend.app.models.study_block import StudyBlock
from backend.app.models.student_config import StudentConfig
from backend.app.services.scheduler_service import SchedulerService, TimeInterval
from backend.app.services.capacity_service import CapacityService


def test_interval_merge_logic():
    """Verifies interval merge behaves correctly for overlapping and contiguous spans."""
    base_dt = datetime(2026, 11, 18, 9, 0, tzinfo=timezone.utc)

    # Overlapping intervals
    i1 = TimeInterval(start=base_dt, end=base_dt + timedelta(hours=2))  # 09:00 - 11:00
    i2 = TimeInterval(start=base_dt + timedelta(hours=1), end=base_dt + timedelta(hours=3))  # 10:00 - 12:00
    # Contiguous interval
    i3 = TimeInterval(start=base_dt + timedelta(hours=3), end=base_dt + timedelta(hours=4))  # 12:00 - 13:00
    # Disjoint interval
    i4 = TimeInterval(start=base_dt + timedelta(hours=5), end=base_dt + timedelta(hours=6))  # 14:00 - 15:00

    merged = SchedulerService.merge_intervals([i1, i2, i3, i4])
    assert len(merged) == 2
    assert merged[0].start == base_dt
    assert merged[0].end == base_dt + timedelta(hours=4)  # 09:00 - 13:00 unified
    assert merged[1].start == base_dt + timedelta(hours=5)
    assert merged[1].end == base_dt + timedelta(hours=6)


def test_meal_and_transit_buffers(db_session: Session):
    """Verifies mandatory lunch, dinner, and 15m post-activity transit buffers."""
    target_date = date(2026, 11, 18)  # Wednesday (weekday = 2)

    course = Course(code="CS 240", name="Data Structures", color="#3B82F6")
    db_session.add(course)
    db_session.commit()

    # Fixed commitment from 10:00 to 11:30 on Wednesday (weekday=2)
    commitment = FixedCommitment(
        course_id=course.id,
        title="CS 240 Lecture",
        day_of_week=2,
        start_time="10:00",
        end_time="11:30",
    )
    db_session.add(commitment)
    db_session.commit()

    busy_spans = SchedulerService.get_day_busy_intervals(db_session, target_date)

    # 1. Check fixed commitment has 15m buffer appended (ends at 11:45)
    transit_comm = [b for b in busy_spans if b.start.time() == time(10, 0)]
    assert len(transit_comm) == 1
    assert transit_comm[0].end.time() == time(11, 45)

    # 2. Check lunch buffer (12:30 - 13:15)
    lunch = [b for b in busy_spans if b.start.time() == time(12, 30) and b.end.time() == time(13, 15)]
    assert len(lunch) == 1

    # 3. Check dinner buffer (18:30 - 19:15)
    dinner = [b for b in busy_spans if b.start.time() == time(18, 30) and b.end.time() == time(19, 15)]
    assert len(dinner) == 1


def test_free_gaps_finding(db_session: Session):
    """Verifies free study gaps are extracted correctly between waking hours."""
    target_date = date(2026, 11, 18)  # Wednesday
    gaps = SchedulerService.find_free_gaps(db_session, target_date, min_duration_minutes=45)

    # On a clear day, morning slot: 08:00 to 12:30 (lunch)
    morning_slot = next((g for g in gaps if g.start.time() == time(8, 0)), None)
    assert morning_slot is not None
    assert morning_slot.end.time() == time(12, 30)
    assert morning_slot.duration_minutes == 270  # 4.5 hours


def test_daily_study_cap_enforcement(db_session: Session):
    """Verifies scheduler strictly enforces the 5.5-hour daily cap and spills to next day."""
    target_date = date(2026, 11, 18)  # Wednesday

    course = Course(code="CS 240", name="Data Structures", color="#3B82F6")
    db_session.add(course)
    db_session.commit()

    # Deadline requiring 8 hours of study, due 3 days later
    due_dt = datetime(2026, 11, 21, 18, 0, tzinfo=timezone.utc)
    deadline = Deadline(
        course_id=course.id,
        title="Major Project",
        due_datetime=due_dt,
        estimated_hours=8.0,
        priority="high",
    )
    db_session.add(deadline)
    db_session.commit()

    # Run auto-scheduler
    allocated_blocks = SchedulerService.auto_schedule_deadline(
        db_session,
        deadline.id,
        start_from_date=target_date,
    )

    assert len(allocated_blocks) > 0

    # Verify Day 1 load does not exceed 5.5 hours (330 minutes)
    day1_minutes = CapacityService.get_daily_study_minutes(db_session, target_date)
    assert day1_minutes <= 330, f"Day 1 minutes ({day1_minutes}) exceeded 330m cap!"

    # Verify Day 2 receives the overflow
    day2_date = target_date + timedelta(days=1)
    day2_minutes = CapacityService.get_daily_study_minutes(db_session, day2_date)
    assert day2_minutes > 0, "Expected overflow blocks on Day 2"
    assert day2_minutes <= 330, f"Day 2 minutes ({day2_minutes}) exceeded 330m cap!"

    # Total allocated should equal 8.0 hours (480 minutes)
    total_minutes = sum(b.duration_minutes for b in allocated_blocks)
    assert total_minutes == 480
