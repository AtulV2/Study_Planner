"""Recovery event model recording audit logs of dynamic schedule adaptations."""

from datetime import datetime, timezone
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.core.database import Base
from backend.app.models.base import UTCDateTime


class RecoveryEvent(Base):
    """Audit log tracking automatic healing, shift, or triage interventions."""

    __tablename__ = "recovery_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        UTCDateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    trigger_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )  # 'auto_heal', 'triage_mvp', 'shift_today', 'micro_action'
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_blocks_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    details_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)

    def __repr__(self) -> str:
        return f"<RecoveryEvent(id={self.id}, type='{self.trigger_type}', affected={self.affected_blocks_count})>"
