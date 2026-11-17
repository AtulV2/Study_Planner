"""Seed and health diagnostic endpoints."""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func, text

from backend.app.core.database import get_db, Base, engine
from backend.app.models.course import Course
from backend.app.models.commitment import FixedCommitment
from backend.app.models.deadline import Deadline
from backend.app.models.study_block import StudyBlock
from backend.app.models.student_config import StudentConfig
from backend.app.models.recovery_event import RecoveryEvent

router = APIRouter(tags=["diagnostics"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """System health, database connectivity, and entity count statistics."""
    courses_count = db.execute(select(func.count(Course.id))).scalar() or 0
    commitments_count = db.execute(select(func.count(FixedCommitment.id))).scalar() or 0
    deadlines_count = db.execute(select(func.count(Deadline.id))).scalar() or 0
    blocks_count = db.execute(select(func.count(StudyBlock.id))).scalar() or 0

    return {
        "status": "healthy",
        "database": "connected",
        "counts": {
            "courses": courses_count,
            "commitments": commitments_count,
            "deadlines": deadlines_count,
            "study_blocks": blocks_count,
        },
    }


@router.post("/seed")
def seed_scenario(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Resets database and populates a rich, realistic student schedule."""
    # Wipe existing data
    db.query(RecoveryEvent).delete()
    db.query(StudyBlock).delete()
    db.query(Deadline).delete()
    db.query(FixedCommitment).delete()
    db.query(Course).delete()
    db.query(StudentConfig).delete()
    db.commit()

    # 1. Student configuration
    config = StudentConfig(
        max_daily_study_hours=5.5,
        wake_time="08:00",
        sleep_time="23:00",
        preferred_chunk_minutes=60,
        min_gap_buffer_minutes=15,
        protect_weekends=False,
    )
    db.add(config)

    # 2. Courses
    cs240 = Course(code="CS 240", name="Data Structures & Algorithms", color="#3B82F6", instructor="Dr. Sarah Chen")
    math215 = Course(code="MATH 215", name="Multivariable Calculus", color="#10B981", instructor="Prof. Elena Rostova")
    engl101 = Course(code="ENGL 101", name="Academic Writing & Rhetoric", color="#F59E0B", instructor="Dr. James Baldwin")
    db.add_all([cs240, math215, engl101])
    db.commit()

    # 3. Fixed Commitments (Mon=0, Wed=2, Fri=4)
    c1 = FixedCommitment(
        course_id=cs240.id,
        title="CS 240 Lecture",
        commitment_type="lecture",
        day_of_week=0,
        start_time="10:00",
        end_time="11:30",
        location="Turing Hall 101",
    )
    c2 = FixedCommitment(
        course_id=cs240.id,
        title="CS 240 Lecture",
        commitment_type="lecture",
        day_of_week=2,
        start_time="10:00",
        end_time="11:30",
        location="Turing Hall 101",
    )
    c3 = FixedCommitment(
        course_id=math215.id,
        title="MATH 215 Discussion",
        commitment_type="discussion",
        day_of_week=1,
        start_time="14:00",
        end_time="15:30",
        location="Euler 204",
    )
    c4 = FixedCommitment(
        course_id=None,
        title="Campus Tech Desk Shift",
        commitment_type="work",
        day_of_week=3,
        start_time="13:00",
        end_time="17:00",
        location="Library Commons",
    )
    db.add_all([c1, c2, c3, c4])

    # 4. Deadlines
    now = datetime.now(timezone.utc)
    dl1 = Deadline(
        course_id=cs240.id,
        title="Problem Set 3 - Balanced BSTs",
        due_datetime=now + timedelta(days=3),
        estimated_hours=4.0,
        priority="high",
        notes="Implement AVL tree rotation and rebalancing routines.",
    )
    dl2 = Deadline(
        course_id=math215.id,
        title="Midterm Exam 1",
        due_datetime=now + timedelta(days=5),
        estimated_hours=6.0,
        priority="high",
        notes="Stokes Theorem and Green's Theorem practice.",
    )
    dl3 = Deadline(
        course_id=engl101.id,
        title="Close Reading Paper",
        due_datetime=now + timedelta(days=6),
        estimated_hours=3.0,
        priority="medium",
        notes="Draft 1500 words on modern dystopian themes.",
    )
    db.add_all([dl1, dl2, dl3])
    db.commit()

    # 5. Study blocks (including one missed block for recovery showcase)
    b1 = StudyBlock(
        deadline_id=dl1.id,
        title="CS 240 - Tree Traversal Review",
        start_datetime=now - timedelta(hours=3),
        end_datetime=now - timedelta(hours=2),
        duration_minutes=60,
        status="missed",
        notes="Missed due to student illness.",
    )
    b2 = StudyBlock(
        deadline_id=dl1.id,
        title="CS 240 - AVL Code Implementation",
        start_datetime=now + timedelta(hours=2),
        end_datetime=now + timedelta(hours=3, minutes=30),
        duration_minutes=90,
        status="scheduled",
    )
    b3 = StudyBlock(
        deadline_id=math215.id,
        title="MATH 215 - Problem Set Review",
        start_datetime=now + timedelta(days=1, hours=2),
        end_datetime=now + timedelta(days=1, hours=3),
        duration_minutes=60,
        status="scheduled",
    )
    db.add_all([b1, b2, b3])
    db.commit()

    return {
        "status": "success",
        "message": "Realistic student scenario seeded successfully.",
        "courses_created": 3,
        "commitments_created": 4,
        "deadlines_created": 3,
        "study_blocks_created": 3,
    }
