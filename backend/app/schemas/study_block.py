"""Pydantic schemas for StudyBlock entity."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class StudyBlockBase(BaseModel):
    deadline_id: int | None = None
    title: str = Field(..., max_length=128)
    start_datetime: datetime
    end_datetime: datetime
    duration_minutes: int = Field(default=60, gt=0)
    status: str = Field(
        default="scheduled",
        description="scheduled, completed, missed, recovered, skipped",
    )
    notes: str | None = None


class StudyBlockCreate(StudyBlockBase):
    pass


class StudyBlockUpdate(BaseModel):
    deadline_id: int | None = None
    title: str | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    duration_minutes: int | None = Field(default=None, gt=0)
    status: str | None = None
    notes: str | None = None


class StudyBlockResponse(StudyBlockBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
