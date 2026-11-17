"""iCalendar (RFC 5545) generation service."""

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.app.models.study_block import StudyBlock
from backend.app.models.commitment import FixedCommitment


class ICalService:
    """Generates standard iCalendar (.ics) subscription feeds."""

    @staticmethod
    def _format_datetime(dt: datetime) -> str:
        """Formats datetime to iCal UTC format: YYYYMMDDTHHMMSSZ."""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt.strftime("%Y%m%dT%H%M%SZ")

    @classmethod
    def generate_feed(cls, db: Session) -> str:
        """Generates RFC 5545 calendar string for all active study blocks."""
        now_stamp = cls._format_datetime(datetime.now(timezone.utc))

        blocks = db.execute(
            select(StudyBlock).where(
                StudyBlock.status.in_(["scheduled", "completed", "recovered"])
            ).order_by(StudyBlock.start_datetime.asc())
        ).scalars().all()

        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//AutoPace//Resilient Academic Workload OS//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:AutoPace Academic Schedule",
            "X-WR-TIMEZONE:UTC",
        ]

        for block in blocks:
            lines.extend(
                [
                    "BEGIN:VEVENT",
                    f"UID:autopace-studyblock-{block.id}@autopace.app",
                    f"DTSTAMP:{now_stamp}",
                    f"DTSTART:{cls._format_datetime(block.start_datetime)}",
                    f"DTEND:{cls._format_datetime(block.end_datetime)}",
                    f"SUMMARY:{block.title}",
                    f"DESCRIPTION:AutoPace Focus Session ({block.duration_minutes}m) - Status: {block.status}",
                    f"STATUS:{'CONFIRMED' if block.status != 'missed' else 'CANCELLED'}",
                    "END:VEVENT",
                ]
            )

        lines.append("END:VCALENDAR")
        return "\r\n".join(lines) + "\r\n"
