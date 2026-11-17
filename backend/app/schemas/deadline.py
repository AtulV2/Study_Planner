"""Pydantic schemas for Deadline entity."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DeadlineBase(BaseModel):
    course_id: int
    title: str = Field(..., max_length=128)
    due_datetime: datetime
    estimated_hours: float = Field(..., gt=0.0)
    completed_hours: float = Field(default=0.0, ge=0.0)
    priority: str = Field(default="medium", description="high, medium, low")
    status: str = Field(default="pending", description="pending, completed, at_risk")
    notes: str | None = None


class DeadlineCreate(DeadlineBase):
    pass


class DeadlineUpdate(BaseModel):
    course_id: int | None = None
    title: str | None = None
    due_datetime: datetime | None = None
    estimated_hours: float | None = Field(default=None, gt=0.0)
    completed_hours: float | None = Field(default=None, ge=0.0)
    priority: str | None = None
    status: str | None = None
    notes: str | None = None


class DeadlineResponse(DeadlineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
