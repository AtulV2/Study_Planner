"""Pydantic schemas for FixedCommitment entity."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class FixedCommitmentBase(BaseModel):
    course_id: int | None = Field(default=None, description="Nullable course FK")
    title: str = Field(..., max_length=128)
    commitment_type: str = Field(
        default="lecture",
        description="lecture, lab, discussion, work, sport, personal",
    )
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    start_time: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="HH:MM format")
    end_time: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="HH:MM format")
    location: str | None = Field(default=None, max_length=128)
    status: str = Field(default="scheduled", description="scheduled, completed, missed")


class FixedCommitmentCreate(FixedCommitmentBase):
    pass


class FixedCommitmentUpdate(BaseModel):
    course_id: int | None = None
    title: str | None = None
    commitment_type: str | None = None
    day_of_week: int | None = Field(default=None, ge=0, le=6)
    start_time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    end_time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    location: str | None = None
    status: str | None = None


class FixedCommitmentResponse(FixedCommitmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
