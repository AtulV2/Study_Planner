"""Deadlines endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.core.database import get_db
from backend.app.models.deadline import Deadline
from backend.app.models.course import Course
from backend.app.schemas.deadline import DeadlineCreate, DeadlineUpdate, DeadlineResponse
from backend.app.schemas.study_block import StudyBlockResponse
from backend.app.services.scheduler_service import SchedulerService

router = APIRouter(prefix="/deadlines", tags=["deadlines"])


@router.get("", response_model=List[DeadlineResponse])
def get_deadlines(db: Session = Depends(get_db)):
    """List all pending and completed deadlines."""
    return db.execute(select(Deadline).order_by(Deadline.due_datetime.asc())).scalars().all()


@router.post("", response_model=DeadlineResponse, status_code=status.HTTP_201_CREATED)
def create_deadline(payload: DeadlineCreate, db: Session = Depends(get_db)):
    """Create a new deadline deliverable."""
    course = db.get(Course, payload.course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated course not found")

    deadline = Deadline(**payload.model_dump())
    db.add(deadline)
    db.commit()
    db.refresh(deadline)
    return deadline


@router.patch("/{deadline_id}", response_model=DeadlineResponse)
def update_deadline(deadline_id: int, payload: DeadlineUpdate, db: Session = Depends(get_db)):
    """Update deadline fields or status."""
    dl = db.get(Deadline, deadline_id)
    if not dl:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deadline not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(dl, field, val)

    db.commit()
    db.refresh(dl)
    return dl


@router.delete("/{deadline_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deadline(deadline_id: int, db: Session = Depends(get_db)):
    """Delete a deadline and cascade delete associated study blocks."""
    dl = db.get(Deadline, deadline_id)
    if not dl:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deadline not found")

    db.delete(dl)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{deadline_id}/auto-schedule", response_model=List[StudyBlockResponse])
def auto_schedule_deadline(deadline_id: int, db: Session = Depends(get_db)):
    """Auto-allocates study sessions for this specific deadline."""
    dl = db.get(Deadline, deadline_id)
    if not dl:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deadline not found")

    blocks = SchedulerService.auto_schedule_deadline(db, deadline_id)
    return blocks
