"""Pydantic schemas for Course entity."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CourseBase(BaseModel):
    code: str = Field(..., max_length=32, description="Course identifier (e.g. CS 240)")
    name: str = Field(..., max_length=128, description="Full course title")
    color: str = Field(default="#3B82F6", max_length=16, description="Hex color token")
    instructor: str | None = Field(default=None, max_length=128)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    code: str | None = Field(default=None, max_length=32)
    name: str | None = Field(default=None, max_length=128)
    color: str | None = Field(default=None, max_length=16)
    instructor: str | None = Field(default=None, max_length=128)


class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
