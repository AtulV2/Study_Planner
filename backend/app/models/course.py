"""Course model representation."""

from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.database import Base
from backend.app.models.base import TimestampMixin

if TYPE_CHECKING:
    from backend.app.models.commitment import FixedCommitment
    from backend.app.models.deadline import Deadline


class Course(Base, TimestampMixin):
    """Enrolled academic course entity."""

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    color: Mapped[str] = mapped_column(String(16), default="#3B82F6", nullable=False)
    instructor: Mapped[str | None] = mapped_column(String(128), nullable=True)

    # Relationships with strict cascade delete
    commitments: Mapped[List["FixedCommitment"]] = relationship(
        "FixedCommitment",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    deadlines: Mapped[List["Deadline"]] = relationship(
        "Deadline",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Course(id={self.id}, code='{self.code}', name='{self.name}')>"
