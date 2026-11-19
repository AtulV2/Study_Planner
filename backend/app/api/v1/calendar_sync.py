"""Calendar export and synchronization endpoint."""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.services.ical_service import ICalService

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/feed.ics")
def get_ical_feed(db: Session = Depends(get_db)):
    """Standard iCalendar subscription feed for Apple/Google Calendar."""
    ical_content = ICalService.generate_feed(db)
    return Response(
        content=ical_content,
        media_type="text/calendar",
        headers={
            "Content-Disposition": 'attachment; filename="study_planner_schedule.ics"',
            "Cache-Control": "no-cache, no-store, must-revalidate",
        },
    )
