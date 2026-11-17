"""Fixed commitment model representing immovable schedule anchors."""

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, SmallInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base
from backend.app.models.base import TimestampMixin

if TYPE_CHECKING:
    from backend.app.models.course import Course


class FixedCommitment(Base, TimestampMixin):
    """Immutable recurring calendar anchor (classes, work shifts, team athletics)."""

    __tablename__ = "fixed_commitments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    commitment_type: Mapped[str] = mapped_column(
        String(32),
        default="lecture",
        nullable=False,
    )  # 'lecture', 'lab', 'discussion', 'work', 'sport', 'personal'
    day_of_week: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 0 = Monday, 6 = Sunday
    start_time: Mapped[str] = mapped_column(String(5), nullable=False)  # "HH:MM" 24h
    end_time: Mapped[str] = mapped_column(String(5), nullable=False)    # "HH:MM" 24h
    location: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        default="scheduled",
        nullable=False,
    )  # 'scheduled', 'completed', 'missed'

    # Relationships
    course: Mapped["Course | None"] = relationship("Course", back_populates="commitments")

    def __repr__(self) -> str:
        return f"<FixedCommitment(id={self.id}, title='{self.title}', day={self.day_of_week}, time='{self.start_time}-{self.end_time}')>"
