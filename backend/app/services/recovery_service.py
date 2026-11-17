"""Dynamic recovery engine providing auto-heal, triage downscaling, and schedule shifts.

Implements Algorithm B from System Architecture specifications:
- Auto-heal missed study blocks into nearest viable gaps before deadline.
- Triage / MVP mode reducing low-priority hours by 30% and medium-priority by 20%.
- Shift-today with graceful bedtime overflow cascading to tomorrow.
- Micro-action starter task recommendation.
- Comprehensive RecoveryEvent audit logging with before/after diffs.
"""

import json
from datetime import datetime, date, timedelta, timezone, time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.models.study_block import StudyBlock
from backend.app.models.deadline import Deadline
from backend.app.models.recovery_event import RecoveryEvent
from backend.app.models.student_config import StudentConfig
from backend.app.services.capacity_service import CapacityService
from backend.app.services.scheduler_service import SchedulerService


class RecoveryService:
    """Provides resilient self-healing scheduling algorithms and audit logging."""

    @classmethod
    def preview_recovery(cls, db: Session, current_time: datetime | None = None) -> List[Dict[str, Any]]:
        """Calculates non-destructive before/after recovery preview diff."""
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        missed_blocks = db.execute(
            select(StudyBlock).where(StudyBlock.status == "missed").order_by(StudyBlock.start_datetime.asc())
        ).scalars().all()

        diffs: List[Dict[str, Any]] = []
        config = CapacityService.get_or_create_config(db)
        eval_date = current_time.date()

        for block in missed_blocks:
            deadline = db.get(Deadline, block.deadline_id) if block.deadline_id else None
            max_bound = deadline.due_datetime if deadline else current_time + timedelta(days=7)

            # Search forward for free gap
            search_date = eval_date
            assigned_slot = None

            while search_date <= max_bound.date() and not assigned_slot:
                free_gaps = SchedulerService.find_free_gaps(
                    db,
                    search_date,
                    min_duration_minutes=block.duration_minutes,
                    config=config,
                )
                for gap in free_gaps:
                    gap_start = max(gap.start, current_time)
                    if gap_start + timedelta(minutes=block.duration_minutes) <= min(gap.end, max_bound):
                        assigned_slot = (gap_start, gap_start + timedelta(minutes=block.duration_minutes))
                        break
                search_date += timedelta(days=1)

            diffs.append(
                {
                    "block_id": block.id,
                    "title": block.title,
                    "original_start": block.start_datetime.isoformat(),
                    "original_end": block.end_datetime.isoformat(),
                    "proposed_start": assigned_slot[0].isoformat() if assigned_slot else None,
                    "proposed_end": assigned_slot[1].isoformat() if assigned_slot else None,
                    "status_change": "missed -> recovered" if assigned_slot else "unresolvable",
                    "resolvable": assigned_slot is not None,
                }
            )

        return diffs

    @classmethod
    def auto_heal(cls, db: Session, current_time: datetime | None = None) -> Dict[str, Any]:
        """Commits reallocation of missed study blocks into upcoming buffer gaps."""
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        missed_blocks = db.execute(
            select(StudyBlock).where(StudyBlock.status == "missed").order_by(StudyBlock.start_datetime.asc())
        ).scalars().all()

        if not missed_blocks:
            return {"status": "no_op", "message": "No missed blocks requiring recovery", "affected_count": 0}

        config = CapacityService.get_or_create_config(db)
        eval_date = current_time.date()
        diff_records: List[Dict[str, Any]] = []
        healed_count = 0

        for block in missed_blocks:
            deadline = db.get(Deadline, block.deadline_id) if block.deadline_id else None
            max_bound = deadline.due_datetime if deadline else current_time + timedelta(days=7)

            search_date = eval_date
            assigned_start = None
            assigned_end = None

            while search_date <= max_bound.date() and not assigned_start:
                free_gaps = SchedulerService.find_free_gaps(
                    db,
                    search_date,
                    min_duration_minutes=block.duration_minutes,
                    config=config,
                )
                for gap in free_gaps:
                    gap_start = max(gap.start, current_time)
                    gap_candidate_end = gap_start + timedelta(minutes=block.duration_minutes)
                    if gap_candidate_end <= min(gap.end, max_bound):
                        assigned_start = gap_start
                        assigned_end = gap_candidate_end
                        break
                search_date += timedelta(days=1)

            if assigned_start and assigned_end:
                diff_records.append(
                    {
                        "block_id": block.id,
                        "title": block.title,
                        "old_start": block.start_datetime.isoformat(),
                        "old_end": block.end_datetime.isoformat(),
                        "new_start": assigned_start.isoformat(),
                        "new_end": assigned_end.isoformat(),
                    }
                )
                block.start_datetime = assigned_start
                block.end_datetime = assigned_end
                block.status = "recovered"
                block.notes = (block.notes or "") + " [Auto-healed into future buffer]"
                healed_count += 1

        # Record audit event
        recovery_event = RecoveryEvent(
            trigger_type="auto_heal",
            description=f"Auto-healed {healed_count} missed study sessions into future buffers.",
            affected_blocks_count=healed_count,
            details_json=json.dumps(diff_records),
        )
        db.add(recovery_event)
        db.commit()

        return {
            "status": "success",
            "healed_count": healed_count,
            "recovery_event_id": recovery_event.id,
            "details": diff_records,
        }

    @classmethod
    def triage_mvp(cls, db: Session) -> Dict[str, Any]:
        """Reduces scope for lower priority deliverables: 30% reduction on low, 20% on medium."""
        deadlines = db.execute(
            select(Deadline).where(Deadline.status.in_(["pending", "at_risk"]))
        ).scalars().all()

        affected_deadlines: List[Dict[str, Any]] = []
        total_blocks_adjusted = 0

        for dl in deadlines:
            original_hours = dl.estimated_hours
            reduction_factor = 0.0

            if dl.priority == "low":
                reduction_factor = 0.30  # 30% reduction
            elif dl.priority == "medium":
                reduction_factor = 0.20  # 20% reduction

            if reduction_factor > 0:
                new_hours = round(original_hours * (1.0 - reduction_factor), 2)
                dl.estimated_hours = new_hours

                # Adjust remaining scheduled study blocks if allocated exceeds new estimate
                scheduled_blocks = db.execute(
                    select(StudyBlock).where(
                        StudyBlock.deadline_id == dl.id,
                        StudyBlock.status.in_(["scheduled", "recovered"]),
                    ).order_by(StudyBlock.start_datetime.desc())
                ).scalars().all()

                target_minutes = int(new_hours * 60)
                current_minutes = sum(b.duration_minutes for b in scheduled_blocks)
                excess_minutes = max(0, current_minutes - target_minutes)

                for block in scheduled_blocks:
                    if excess_minutes <= 0:
                        break
                    if block.duration_minutes <= excess_minutes:
                        excess_minutes -= block.duration_minutes
                        db.delete(block)
                        total_blocks_adjusted += 1
                    else:
                        block.duration_minutes -= excess_minutes
                        block.end_datetime = block.start_datetime + timedelta(minutes=block.duration_minutes)
                        excess_minutes = 0
                        total_blocks_adjusted += 1

                affected_deadlines.append(
                    {
                        "deadline_id": dl.id,
                        "title": dl.title,
                        "priority": dl.priority,
                        "original_hours": original_hours,
                        "triage_hours": new_hours,
                    }
                )

        recovery_event = RecoveryEvent(
            trigger_type="triage_mvp",
            description=f"Triage MVP downscaled {len(affected_deadlines)} deadlines, pruning {total_blocks_adjusted} blocks.",
            affected_blocks_count=total_blocks_adjusted,
            details_json=json.dumps(affected_deadlines),
        )
        db.add(recovery_event)
        db.commit()

        return {
            "status": "success",
            "deadlines_triaged": len(affected_deadlines),
            "blocks_adjusted": total_blocks_adjusted,
            "details": affected_deadlines,
        }

    @classmethod
    def shift_today(
        cls,
        db: Session,
        shift_minutes: int = 60,
        current_time: datetime | None = None,
    ) -> Dict[str, Any]:
        """Pushes today's remaining blocks forward, overflowing past bedtime into tomorrow."""
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        target_date = current_time.date()
        config = CapacityService.get_or_create_config(db)
        sleep_t = SchedulerService.parse_time_str(config.sleep_time)
        sleep_dt = SchedulerService.make_aware_datetime(target_date, sleep_t)

        start_of_day = SchedulerService.make_aware_datetime(target_date, time(0, 0))
        end_of_day = SchedulerService.make_aware_datetime(target_date, time(23, 59, 59))

        blocks = db.execute(
            select(StudyBlock).where(
                StudyBlock.start_datetime >= current_time,
                StudyBlock.start_datetime <= end_of_day,
                StudyBlock.status == "scheduled",
            ).order_by(StudyBlock.start_datetime.asc())
        ).scalars().all()

        shifted_records: List[Dict[str, Any]] = []

        for block in blocks:
            old_start = block.start_datetime
            old_end = block.end_datetime
            proposed_start = old_start + timedelta(minutes=shift_minutes)
            proposed_end = old_end + timedelta(minutes=shift_minutes)

            # Check if shifts past bedtime
            if proposed_end > sleep_dt:
                # Overflow into tomorrow's first available window
                tomorrow = target_date + timedelta(days=1)
                tomorrow_wake_t = SchedulerService.parse_time_str(config.wake_time)
                tomorrow_wake_dt = SchedulerService.make_aware_datetime(tomorrow, tomorrow_wake_t)

                block.start_datetime = tomorrow_wake_dt
                block.end_datetime = tomorrow_wake_dt + timedelta(minutes=block.duration_minutes)
                block.notes = (block.notes or "") + f" [Shifted today past bedtime into tomorrow morning]"
            else:
                block.start_datetime = proposed_start
                block.end_datetime = proposed_end

            shifted_records.append(
                {
                    "block_id": block.id,
                    "title": block.title,
                    "old_start": old_start.isoformat(),
                    "new_start": block.start_datetime.isoformat(),
                    "new_end": block.end_datetime.isoformat(),
                }
            )

        recovery_event = RecoveryEvent(
            trigger_type="shift_today",
            description=f"Shifted today's schedule forward by {shift_minutes} minutes for {len(blocks)} blocks.",
            affected_blocks_count=len(blocks),
            details_json=json.dumps(shifted_records),
        )
        db.add(recovery_event)
        db.commit()

        return {
            "status": "success",
            "shifted_count": len(blocks),
            "details": shifted_records,
        }

    @classmethod
    def get_micro_action(cls, db: Session, current_time: datetime | None = None) -> Dict[str, Any] | None:
        """Finds a 30-45 min starter focus task to overcome inertia."""
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        # First check immediate scheduled blocks
        next_block = db.execute(
            select(StudyBlock).where(
                StudyBlock.start_datetime >= current_time,
                StudyBlock.status.in_(["scheduled", "recovered"]),
            ).order_by(StudyBlock.start_datetime.asc())
        ).scalars().first()

        if next_block:
            starter_duration = min(35, next_block.duration_minutes)
            return {
                "type": "study_block",
                "title": f"Quick Start: {next_block.title}",
                "duration_minutes": starter_duration,
                "suggested_prompt": f"Dedicate just {starter_duration} minutes right now to make first progress.",
                "deadline_id": next_block.deadline_id,
                "block_id": next_block.id,
            }

        # Otherwise check urgent pending deadline
        urgent_deadline = db.execute(
            select(Deadline).where(
                Deadline.status.in_(["pending", "at_risk"]),
                Deadline.due_datetime >= current_time,
            ).order_by(Deadline.due_datetime.asc())
        ).scalars().first()

        if urgent_deadline:
            return {
                "type": "deadline",
                "title": f"Sprint Setup: {urgent_deadline.title}",
                "duration_minutes": 30,
                "suggested_prompt": "Set a 30-minute timer and complete the first sub-problem or reading passage.",
                "deadline_id": urgent_deadline.id,
                "block_id": None,
            }

        return None
