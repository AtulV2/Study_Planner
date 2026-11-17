"""Student configuration endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.student_config import (
    StudentConfigUpdate,
    StudentConfigResponse,
)
from backend.app.services.capacity_service import CapacityService

router = APIRouter(prefix="/config", tags=["config"])


@router.get("", response_model=StudentConfigResponse)
def get_student_config(db: Session = Depends(get_db)):
    """Get student boundaries (wake/sleep times, daily study cap)."""
    return CapacityService.get_or_create_config(db)


@router.patch("", response_model=StudentConfigResponse)
def update_student_config(payload: StudentConfigUpdate, db: Session = Depends(get_db)):
    """Update student preferences and cognitive limits."""
    config = CapacityService.get_or_create_config(db)
    update_data = payload.model_dump(exclude_unset=True)

    for field, val in update_data.items():
        setattr(config, field, val)

    db.commit()
    db.refresh(config)
    return config
