"""Unit tests verifying ORM model definitions, foreign keys, and cascading deletes."""

from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.app.models.course import Course
from backend.app.models.commitment import FixedCommitment
from backend.app.models.deadline import Deadline
from backend.app.models.study_block import StudyBlock
from backend.app.models.student_config import StudentConfig
from backend.app.models.recovery_event import RecoveryEvent


def test_course_creation_and_retrieval(db_session: Session):
    """Verifies course entity persistence and fields."""
    course = Course(
        code="CS 240",
        name="Data Structures and Algorithms",
        color="#3B82F6",
        instructor="Dr. Sarah Chen",
    )
    db_session.add(course)
    db_session.commit()

    retrieved = db_session.execute(select(Course).where(Course.code == "CS 240")).scalar_one()
    assert retrieved.name == "Data Structures and Algorithms"
    assert retrieved.color == "#3B82F6"
    assert retrieved.created_at is not None


def test_course_cascade_deletes_commitments_and_deadlines(db_session: Session):
    """Verifies deleting a course cascades to associated commitments and deadlines."""
    course = Course(code="PHYS 101", name="General Physics", color="#10B981")
    db_session.add(course)
    db_session.commit()

    commitment = FixedCommitment(
        course_id=course.id,
        title="Physics Lab",
        commitment_type="lab",
        day_of_week=1,
        start_time="14:00",
        end_time="16:00",
    )
    deadline = Deadline(
        course_id=course.id,
        title="Physics Problem Set 1",
        due_datetime=datetime.now(timezone.utc) + timedelta(days=5),
        estimated_hours=3.0,
        priority="high",
    )
    db_session.add_all([commitment, deadline])
    db_session.commit()

    # Confirm created
    assert db_session.execute(select(FixedCommitment).where(FixedCommitment.course_id == course.id)).scalars().first()
    assert db_session.execute(select(Deadline).where(Deadline.course_id == course.id)).scalars().first()

    # Delete course
    db_session.delete(course)
    db_session.commit()

    # Confirm cascades deleted children
    remaining_commitments = db_session.execute(select(FixedCommitment).where(FixedCommitment.course_id == course.id)).scalars().all()
    remaining_deadlines = db_session.execute(select(Deadline).where(Deadline.course_id == course.id)).scalars().all()
    assert len(remaining_commitments) == 0
    assert len(remaining_deadlines) == 0


def test_deadline_cascade_deletes_study_blocks(db_session: Session):
    """Verifies deleting a deadline cascades to its associated study blocks."""
    course = Course(code="MATH 215", name="Calculus III", color="#F59E0B")
    db_session.add(course)
    db_session.commit()

    deadline = Deadline(
        course_id=course.id,
        title="Calc Exam 1",
        due_datetime=datetime.now(timezone.utc) + timedelta(days=3),
        estimated_hours=4.0,
        priority="high",
    )
    db_session.add(deadline)
    db_session.commit()

    now = datetime.now(timezone.utc)
    block1 = StudyBlock(
        deadline_id=deadline.id,
        title="Calc Review 1",
        start_datetime=now,
        end_datetime=now + timedelta(hours=1),
        duration_minutes=60,
    )
    block2 = StudyBlock(
        deadline_id=deadline.id,
        title="Calc Review 2",
        start_datetime=now + timedelta(days=1),
        end_datetime=now + timedelta(days=1, hours=1),
        duration_minutes=60,
    )
    db_session.add_all([block1, block2])
    db_session.commit()

    assert len(db_session.execute(select(StudyBlock).where(StudyBlock.deadline_id == deadline.id)).scalars().all()) == 2

    # Delete deadline
    db_session.delete(deadline)
    db_session.commit()

    # Verify study blocks cascaded
    remaining_blocks = db_session.execute(select(StudyBlock).where(StudyBlock.deadline_id == deadline.id)).scalars().all()
    assert len(remaining_blocks) == 0


def test_recovery_event_logging(db_session: Session):
    """Verifies RecoveryEvent logs intervention snapshots properly."""
    event = RecoveryEvent(
        trigger_type="auto_heal",
        description="Rescheduled missed session",
        affected_blocks_count=1,
        details_json='{"status": "recovered"}',
    )
    db_session.add(event)
    db_session.commit()

    retrieved = db_session.get(RecoveryEvent, event.id)
    assert retrieved is not None
    assert retrieved.trigger_type == "auto_heal"
    assert retrieved.affected_blocks_count == 1
