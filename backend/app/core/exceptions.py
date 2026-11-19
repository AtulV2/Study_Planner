"""Domain-specific exceptions for Study Planner."""


class StudyPlannerError(Exception):
    """Base exception for all Study Planner domain errors."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


# Backwards compatibility alias
AutoPaceError = StudyPlannerError


class CapacityExceededError(StudyPlannerError):
    """Raised when scheduling study blocks exceeds the student's daily cognitive limit."""
    pass


class ZeroGapsAvailableError(StudyPlannerError):
    """Raised when no viable free gap can be found before a deadline."""
    pass


class ScheduleConflictError(StudyPlannerError):
    """Raised when an immovable commitment conflicts with an existing anchor."""
    pass


class EntityNotFoundError(StudyPlannerError):
    """Raised when a requested database entity does not exist."""
    pass
