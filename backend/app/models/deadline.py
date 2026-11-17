"""Deadline deliverable model representing academic assignments and exams."""

from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base
from backend.app.models.base import TimestampMixin, UTCDateTime

if TYPE_CHECKING:
    from backend.app.models.course import Course
    from backend.app.models.study_block import StudyBlock


class Deadline(Base, TimestampMixin):
    """Academic deadline or exam deliverable requiring allocated study time."""

    __tablename__ = "deadlines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    due_datetime: Mapped[datetime] = mapped_column(UTCDateTime, nullable=False)
    estimated_hours: Mapped[float] = mapped_column(Float, nullable=False)
    completed_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    priority: Mapped[str] = mapped_column(
        String(20),
        default="medium",
        nullable=False,
    )  # 'high', 'medium', 'low'
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
    )  # 'pending', 'completed', 'at_risk'
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    course: Mapped["Course"] = relationship("Course", back_populates="deadlines")
    study_blocks: Mapped[List["StudyBlock"]] = relationship(
        "StudyBlock",
        back_populates="deadline",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Deadline(id={self.id}, title='{self.title}', due='{self.due_datetime}', priority='{self.priority}')>"
