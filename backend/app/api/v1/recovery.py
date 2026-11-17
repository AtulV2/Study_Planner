"""Recovery engine endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.core.database import get_db
from backend.app.models.recovery_event import RecoveryEvent
from backend.app.schemas.recovery import (
    RecoveryPreviewResponse,
    ShiftTodayRequest,
    RecoveryEventResponse,
    MicroActionResponse,
    RecoveryDiffItem,
)
from backend.app.services.recovery_service import RecoveryService

router = APIRouter(prefix="/recovery", tags=["recovery"])


@router.post("/preview", response_model=RecoveryPreviewResponse)
def preview_recovery(strategy: str = "auto_heal", db: Session = Depends(get_db)):
    """Generates non-destructive before/after recovery preview diff."""
    raw_diffs = RecoveryService.preview_recovery(db)
    changes: List[RecoveryDiffItem] = []

    for d in raw_diffs:
        orig = f"{d['original_start']} - {d['original_end']}" if d.get("original_start") else None
        prop = f"{d['proposed_start']} - {d['proposed_end']}" if d.get("proposed_start") else None
        changes.append(
            RecoveryDiffItem(
                block_id=d["block_id"],
                title=d["title"],
                original_slot=orig,
                proposed_slot=prop,
                target_day_capacity_after="Feasible",
                reason="Rescheduled into viable study buffer gap before deadline.",
                resolvable=d["resolvable"],
                status_change=d["status_change"],
            )
        )

    return RecoveryPreviewResponse(
        strategy=strategy,
        status="feasible" if all(c.resolvable for c in changes) else "partial",
        disrupted_count=len(changes),
        recovered_count=sum(1 for c in changes if c.resolvable),
        changes=changes,
        warnings=["Some sessions could not be rescheduled within deadline bounds."] if any(not c.resolvable for c in changes) else [],
    )


@router.post("/auto-heal", response_model=Dict[str, Any])
def auto_heal(db: Session = Depends(get_db)):
    """Commits reallocation of missed blocks into future buffers."""
    return RecoveryService.auto_heal(db)


@router.post("/triage-mvp", response_model=Dict[str, Any])
def triage_mvp(db: Session = Depends(get_db)):
    """Commits downscaling of low/medium priority deliverables."""
    return RecoveryService.triage_mvp(db)


@router.post("/shift-today", response_model=Dict[str, Any])
def shift_today(payload: ShiftTodayRequest, db: Session = Depends(get_db)):
    """Pushes today's remaining blocks forward, overflowing past bedtime into tomorrow."""
    return RecoveryService.shift_today(db, shift_minutes=payload.shift_minutes)


@router.get("/micro-action", response_model=MicroActionResponse | None)
def get_micro_action(db: Session = Depends(get_db)):
    """Returns a single 30-45 min inertia-breaking starter task."""
    action = RecoveryService.get_micro_action(db)
    if not action:
        return None
    return MicroActionResponse(**action)


@router.get("/history", response_model=List[RecoveryEventResponse])
def get_recovery_history(db: Session = Depends(get_db)):
    """Audit log of past recovery interventions."""
    return db.execute(select(RecoveryEvent).order_by(RecoveryEvent.timestamp.desc())).scalars().all()
