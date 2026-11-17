"""Scheduler service handling interval arithmetic, gap-finding, and cap enforcement.

Implements Algorithm A from System Architecture specifications:
- Fixed commitment ingestion with 15m post-activity transit buffer.
- Mandatory physiological pauses (lunch 12:30-13:15, dinner 18:30-19:15).
- Contiguous interval merging.
- Free window inversion within student waking hours [wake_time, sleep_time].
- Strict cognitive cap enforcement (max 5.5 hours daily study limit).
"""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.models.course import Course
from backend.app.models.commitment import FixedCommitment
from backend.app.models.deadline import Deadline
from backend.app.models.study_block import StudyBlock
from backend.app.models.student_config import StudentConfig
from backend.app.services.capacity_service import CapacityService
from backend.app.core.config import settings
from backend.app.core.exceptions import CapacityExceededError, ZeroGapsAvailableError


@dataclass
class TimeInterval:
    """Represents a time interval defined by start and end datetimes."""

    start: datetime
    end: datetime

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)

    def overlaps_or_touches(self, other: "TimeInterval") -> bool:
        return self.start <= other.end and other.start <= self.end

    def merge(self, other: "TimeInterval") -> "TimeInterval":
        return TimeInterval(
            start=min(self.start, other.start),
            end=max(self.end, other.end),
        )


class SchedulerService:
    """Pure domain scheduling and mathematical interval engine."""

    @staticmethod
    def parse_time_str(time_str: str) -> time:
        """Parses 'HH:MM' string into datetime.time object."""
        parts = time_str.strip().split(":")
        return time(hour=int(parts[0]), minute=int(parts[1]))

    @classmethod
    def make_aware_datetime(cls, target_date: date, time_obj: time) -> datetime:
        """Constructs UTC timezone-aware datetime for a specific date and time."""
        return datetime(
            target_date.year,
            target_date.month,
            target_date.day,
            time_obj.hour,
            time_obj.minute,
            0,
            tzinfo=timezone.utc,
        )

    @classmethod
    def merge_intervals(cls, intervals: List[TimeInterval]) -> List[TimeInterval]:
        """Merges overlapping or contiguous intervals into unified busy spans."""
        if not intervals:
            return []

        sorted_intervals = sorted(intervals, key=lambda x: x.start)
        merged: List[TimeInterval] = [sorted_intervals[0]]

        for current in sorted_intervals[1:]:
            last = merged[-1]
            if current.start <= last.end:
                # Merge overlapping or touching intervals
                merged[-1] = TimeInterval(
                    start=last.start,
                    end=max(last.end, current.end),
                )
            else:
                merged.append(current)

        return merged

    @classmethod
    def get_day_busy_intervals(
        cls,
        db: Session,
        target_date: date,
        config: StudentConfig | None = None,
    ) -> List[TimeInterval]:
        """Gathers all fixed commitments, existing study blocks, and mandatory buffers."""
        if config is None:
            config = CapacityService.get_or_create_config(db)

        busy: List[TimeInterval] = []

        # 1. Non-waking hours buffer: before wake_time and after sleep_time
        wake_t = cls.parse_time_str(config.wake_time)
        sleep_t = cls.parse_time_str(config.sleep_time)

        day_start = datetime(target_date.year, target_date.month, target_date.day, 0, 0, tzinfo=timezone.utc)
        wake_dt = cls.make_aware_datetime(target_date, wake_t)
        sleep_dt = cls.make_aware_datetime(target_date, sleep_t)
        day_end = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, tzinfo=timezone.utc)

        if wake_dt > day_start:
            busy.append(TimeInterval(start=day_start, end=wake_dt))
        if day_end > sleep_dt:
            busy.append(TimeInterval(start=sleep_dt, end=day_end))

        # 2. Mandatory physiological meal buffers
        lunch_start_t = cls.parse_time_str(settings.LUNCH_START)
        lunch_end_t = cls.parse_time_str(settings.LUNCH_END)
        busy.append(
            TimeInterval(
                start=cls.make_aware_datetime(target_date, lunch_start_t),
                end=cls.make_aware_datetime(target_date, lunch_end_t),
            )
        )

        dinner_start_t = cls.parse_time_str(settings.DINNER_START)
        dinner_end_t = cls.parse_time_str(settings.DINNER_END)
        busy.append(
            TimeInterval(
                start=cls.make_aware_datetime(target_date, dinner_start_t),
                end=cls.make_aware_datetime(target_date, dinner_end_t),
            )
        )

        # 3. Fixed commitments for the day of week (Monday=0, Sunday=6)
        day_of_week = target_date.weekday()
        commitments = db.execute(
            select(FixedCommitment).where(
                FixedCommitment.day_of_week == day_of_week,
                FixedCommitment.status != "missed",
            )
        ).scalars().all()

        for comm in commitments:
            comm_start_t = cls.parse_time_str(comm.start_time)
            comm_end_t = cls.parse_time_str(comm.end_time)
            comm_start_dt = cls.make_aware_datetime(target_date, comm_start_t)
            comm_end_dt = cls.make_aware_datetime(target_date, comm_end_t)

            # Inject transit / cognitive reset buffer (15m default) after fixed commitments
            transit_buffer = timedelta(minutes=config.min_gap_buffer_minutes)
            busy.append(TimeInterval(start=comm_start_dt, end=comm_end_dt + transit_buffer))

        # 4. Existing active study blocks scheduled on this day
        start_of_day = cls.make_aware_datetime(target_date, time(0, 0))
        end_of_day = cls.make_aware_datetime(target_date, time(23, 59, 59))
        study_blocks = db.execute(
            select(StudyBlock).where(
                StudyBlock.start_datetime >= start_of_day,
                StudyBlock.start_datetime <= end_of_day,
                StudyBlock.status.in_(["scheduled", "completed", "recovered"]),
            )
        ).scalars().all()

        for block in study_blocks:
            busy.append(TimeInterval(start=block.start_datetime, end=block.end_datetime))

        return cls.merge_intervals(busy)

    @classmethod
    def find_free_gaps(
        cls,
        db: Session,
        target_date: date,
        min_duration_minutes: int = 45,
        config: StudentConfig | None = None,
    ) -> List[TimeInterval]:
        """Calculates free study windows by inverting busy spans against waking window."""
        if config is None:
            config = CapacityService.get_or_create_config(db)

        # Check weekend protection
        if config.protect_weekends and target_date.weekday() in (5, 6):
            return []

        wake_t = cls.parse_time_str(config.wake_time)
        sleep_t = cls.parse_time_str(config.sleep_time)
        waking_start = cls.make_aware_datetime(target_date, wake_t)
        waking_end = cls.make_aware_datetime(target_date, sleep_t)

        busy_spans = cls.get_day_busy_intervals(db, target_date, config)

        free_gaps: List[TimeInterval] = []
        current_cursor = waking_start

        for busy in busy_spans:
            # Only consider intervals that intersect the waking period
            busy_start = max(waking_start, busy.start)
            busy_end = min(waking_end, busy.end)

            if busy_start > current_cursor:
                slot_duration = int((busy_start - current_cursor).total_seconds() // 60)
                if slot_duration >= min_duration_minutes:
                    free_gaps.append(TimeInterval(start=current_cursor, end=busy_start))

            if busy_end > current_cursor:
                current_cursor = busy_end

        # Check trailing window between last busy span and bedtime
        if waking_end > current_cursor:
            slot_duration = int((waking_end - current_cursor).total_seconds() // 60)
            if slot_duration >= min_duration_minutes:
                free_gaps.append(TimeInterval(start=current_cursor, end=waking_end))

        return free_gaps

    @classmethod
    def auto_schedule_deadline(
        cls,
        db: Session,
        deadline_id: int,
        start_from_date: date | None = None,
    ) -> List[StudyBlock]:
        """Allocates study blocks for an individual deadline respecting cognitive caps."""
        deadline = db.get(Deadline, deadline_id)
        if not deadline:
            raise ZeroGapsAvailableError(f"Deadline with id {deadline_id} not found.")

        config = CapacityService.get_or_create_config(db)
        chunk_minutes = config.preferred_chunk_minutes
        max_daily_minutes = int(config.max_daily_study_hours * 60)

        # Calculate needed study minutes
        remaining_hours = max(0.0, deadline.estimated_hours - deadline.completed_hours)
        total_minutes_needed = int(round(remaining_hours * 60))

        if total_minutes_needed <= 0:
            return []

        if start_from_date is None:
            start_from_date = datetime.now(timezone.utc).date()

        due_date = deadline.due_datetime.date()
        current_date = start_from_date
        allocated_blocks: List[StudyBlock] = []

        minutes_allocated = 0

        # Traverse calendar days towards due date
        while current_date <= due_date and minutes_allocated < total_minutes_needed:
            # Skip weekend if protected
            if config.protect_weekends and current_date.weekday() in (5, 6):
                current_date += timedelta(days=1)
                continue

            current_day_load = CapacityService.get_daily_study_minutes(db, current_date)
            available_daily_budget = max(0, max_daily_minutes - current_day_load)

            if available_daily_budget < 30:
                # Cap reached for this day; move to next
                current_date += timedelta(days=1)
                continue

            free_gaps = cls.find_free_gaps(db, current_date, min_duration_minutes=30, config=config)

            for gap in free_gaps:
                gap_start = gap.start
                # Ensure we don't schedule past deadline due_datetime on the due date
                gap_end = min(gap.end, deadline.due_datetime)

                while gap_start < gap_end and minutes_allocated < total_minutes_needed and available_daily_budget >= 30:
                    remaining_gap_minutes = int((gap_end - gap_start).total_seconds() // 60)
                    needed_minutes = total_minutes_needed - minutes_allocated

                    # Determine block duration
                    block_duration = min(chunk_minutes, remaining_gap_minutes, needed_minutes, available_daily_budget)
                    if block_duration < 30:
                        break

                    block_end = gap_start + timedelta(minutes=block_duration)

                    new_block = StudyBlock(
                        deadline_id=deadline.id,
                        title=f"{deadline.title} - Focus Session",
                        start_datetime=gap_start,
                        end_datetime=block_end,
                        duration_minutes=block_duration,
                        status="scheduled",
                        notes=f"Auto-scheduled session ({block_duration}m)",
                    )
                    db.add(new_block)
                    allocated_blocks.append(new_block)

                    minutes_allocated += block_duration
                    available_daily_budget -= block_duration
                    gap_start = block_end

                if minutes_allocated >= total_minutes_needed or available_daily_budget < 30:
                    break

            current_date += timedelta(days=1)

        db.commit()
        for block in allocated_blocks:
            db.refresh(block)

        # Check if full requirement was fulfilled
        if minutes_allocated < total_minutes_needed:
            deadline.status = "at_risk"
            db.commit()

        return allocated_blocks

    @classmethod
    def auto_fit_all(cls, db: Session) -> Dict[str, Any]:
        """Global allocator fitting all unfulfilled deadlines into available gaps."""
        # Prioritize: high priority first, then earliest due date
        deadlines = db.execute(
            select(Deadline)
            .where(Deadline.status.in_(["pending", "at_risk"]))
            .order_by(
                # High priority first
                Deadline.priority.desc(),
                Deadline.due_datetime.asc(),
            )
        ).scalars().all()

        total_blocks_created = 0
        at_risk_count = 0

        for dl in deadlines:
            blocks = cls.auto_schedule_deadline(db, dl.id)
            total_blocks_created += len(blocks)
            if dl.status == "at_risk":
                at_risk_count += 1

        return {
            "status": "success",
            "deadlines_processed": len(deadlines),
            "study_blocks_created": total_blocks_created,
            "at_risk_deadlines": at_risk_count,
        }
