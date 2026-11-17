"""Pydantic schemas for StudentConfig entity."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class StudentConfigBase(BaseModel):
    max_daily_study_hours: float = Field(default=5.5, gt=0.0, le=16.0)
    wake_time: str = Field(default="08:00", pattern=r"^\d{2}:\d{2}$")
    sleep_time: str = Field(default="23:00", pattern=r"^\d{2}:\d{2}$")
    preferred_chunk_minutes: int = Field(default=60, ge=15, le=240)
    min_gap_buffer_minutes: int = Field(default=15, ge=0, le=60)
    protect_weekends: bool = False


class StudentConfigUpdate(BaseModel):
    max_daily_study_hours: float | None = Field(default=None, gt=0.0, le=16.0)
    wake_time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    sleep_time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    preferred_chunk_minutes: int | None = Field(default=None, ge=15, le=240)
    min_gap_buffer_minutes: int | None = Field(default=None, ge=0, le=60)
    protect_weekends: bool | None = None


class StudentConfigResponse(StudentConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
