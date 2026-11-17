"""Pydantic schemas for Recovery requests and responses."""

from datetime import datetime
from typing import List, Any, Dict
from pydantic import BaseModel, ConfigDict, Field


class RecoveryDiffItem(BaseModel):
    block_id: int
    title: str
    original_slot: str | None = None
    proposed_slot: str | None = None
    target_day_capacity_after: str | None = None
    reason: str | None = None
    resolvable: bool = True
    status_change: str = "missed -> recovered"


class RecoveryPreviewResponse(BaseModel):
    strategy: str = "auto_heal"
    status: str = "feasible"
    disrupted_count: int = 0
    recovered_count: int = 0
    changes: List[RecoveryDiffItem] = []
    warnings: List[str] = []


class ShiftTodayRequest(BaseModel):
    shift_minutes: int = Field(default=60, ge=15, le=360)


class RecoveryEventResponse(BaseModel):
    id: int
    timestamp: datetime
    trigger_type: str
    description: str
    affected_blocks_count: int
    details_json: str

    model_config = ConfigDict(from_attributes=True)


class MicroActionResponse(BaseModel):
    type: str
    title: str
    duration_minutes: int
    suggested_prompt: str
    deadline_id: int | None = None
    block_id: int | None = None
