"""Study blocks and schedule allocation endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.core.database import get_db
from backend.app.models.study_block import StudyBlock
from backend.app.models.deadline import Deadline
from backend.app.schemas.study_block import (
    StudyBlockCreate,
    StudyBlockUpdate,
    StudyBlockResponse,
)
from backend.app.services.scheduler_service import SchedulerService

router = APIRouter(tags=["study_blocks"])


@router.get("/study-blocks", response_model=List[StudyBlockResponse])
def get_study_blocks(db: Session = Depends(get_db)):
    """List all scheduled, completed, and missed study blocks."""
    return db.execute(select(StudyBlock).order_by(StudyBlock.start_datetime.asc())).scalars().all()


@router.post("/study-blocks", response_model=StudyBlockResponse, status_code=status.HTTP_201_CREATED)
def create_study_block(payload: StudyBlockCreate, db: Session = Depends(get_db)):
    """Manually insert a study session block."""
    if payload.deadline_id:
        dl = db.get(Deadline, payload.deadline_id)
        if not dl:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated deadline not found")

    block = StudyBlock(**payload.model_dump())
    db.add(block)
    db.commit()
    db.refresh(block)
    return block


@router.patch("/study-blocks/{block_id}", response_model=StudyBlockResponse)
def update_study_block(block_id: int, payload: StudyBlockUpdate, db: Session = Depends(get_db)):
    """Update block status (scheduled, completed, missed, recovered) or schedule."""
    block = db.get(StudyBlock, block_id)
    if not block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study block not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(block, field, val)

    db.commit()
    db.refresh(block)
    return block


@router.delete("/study-blocks/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study_block(block_id: int, db: Session = Depends(get_db)):
    """Delete an individual study session."""
    block = db.get(StudyBlock, block_id)
    if not block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study block not found")

    db.delete(block)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/schedule/auto-fit-all", response_model=Dict[str, Any])
def auto_fit_all_unfulfilled(db: Session = Depends(get_db)):
    """Global allocator: Fits all unfulfilled deadlines into free gaps."""
    return SchedulerService.auto_fit_all(db)
