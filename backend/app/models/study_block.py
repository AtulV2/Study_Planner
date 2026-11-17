"""StudyBlock model representing flexible focus sessions."""

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base
from backend.app.models.base import TimestampMixin, UTCDateTime

if TYPE_CHECKING:
    from backend.app.models.deadline import Deadline


class StudyBlock(Base, TimestampMixin):
    """Flexible study or focus block allocated dynamically on the calendar."""

    __tablename__ = "study_blocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    deadline_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("deadlines.id", ondelete="CASCADE"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    start_datetime: Mapped[datetime] = mapped_column(UTCDateTime, nullable=False)
    end_datetime: Mapped[datetime] = mapped_column(UTCDateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        default="scheduled",
        nullable=False,
    )  # 'scheduled', 'completed', 'missed', 'recovered', 'skipped'
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    deadline: Mapped["Deadline | None"] = relationship("Deadline", back_populates="study_blocks")

    def __repr__(self) -> str:
        return f"<StudyBlock(id={self.id}, title='{self.title}', start='{self.start_datetime}', status='{self.status}')>"
