"""Student configuration model holding boundary and preference constraints."""

from sqlalchemy import Integer, Float, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.core.database import Base
from backend.app.models.base import TimestampMixin


class StudentConfig(Base, TimestampMixin):
    """Student boundary preferences, daily capacity limits, and rest rules."""

    __tablename__ = "student_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    max_daily_study_hours: Mapped[float] = mapped_column(Float, default=5.5, nullable=False)
    wake_time: Mapped[str] = mapped_column(String(5), default="08:00", nullable=False)
    sleep_time: Mapped[str] = mapped_column(String(5), default="23:00", nullable=False)
    preferred_chunk_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    min_gap_buffer_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    protect_weekends: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<StudentConfig(id={self.id}, max_hours={self.max_daily_study_hours}, wake='{self.wake_time}', sleep='{self.sleep_time}')>"
