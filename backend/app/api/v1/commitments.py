"""Fixed commitments endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.core.database import get_db
from backend.app.models.commitment import FixedCommitment
from backend.app.models.course import Course
from backend.app.schemas.commitment import (
    FixedCommitmentCreate,
    FixedCommitmentUpdate,
    FixedCommitmentResponse,
)

router = APIRouter(prefix="/commitments", tags=["commitments"])


@router.get("", response_model=List[FixedCommitmentResponse])
def get_commitments(db: Session = Depends(get_db)):
    """List all recurring weekly commitments."""
    return db.execute(select(FixedCommitment).order_by(FixedCommitment.day_of_week.asc(), FixedCommitment.start_time.asc())).scalars().all()


@router.post("", response_model=FixedCommitmentResponse, status_code=status.HTTP_201_CREATED)
def create_commitment(payload: FixedCommitmentCreate, db: Session = Depends(get_db)):
    """Create a fixed recurring class or shift."""
    if payload.course_id:
        course = db.get(Course, payload.course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated course not found")

    commitment = FixedCommitment(**payload.model_dump())
    db.add(commitment)
    db.commit()
    db.refresh(commitment)
    return commitment


@router.patch("/{commitment_id}", response_model=FixedCommitmentResponse)
def update_commitment(commitment_id: int, payload: FixedCommitmentUpdate, db: Session = Depends(get_db)):
    """Update commitment attributes or status."""
    comm = db.get(FixedCommitment, commitment_id)
    if not comm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commitment not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(comm, field, val)

    db.commit()
    db.refresh(comm)
    return comm


@router.delete("/{commitment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commitment(commitment_id: int, db: Session = Depends(get_db)):
    """Remove a fixed commitment."""
    comm = db.get(FixedCommitment, commitment_id)
    if not comm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commitment not found")

    db.delete(comm)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
