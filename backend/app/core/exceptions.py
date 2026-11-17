"""Domain-specific exceptions for AutoPace."""


class AutoPaceError(Exception):
    """Base exception for all AutoPace domain errors."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class CapacityExceededError(AutoPaceError):
    """Raised when scheduling study blocks exceeds the student's daily cognitive limit."""
    pass


class ZeroGapsAvailableError(AutoPaceError):
    """Raised when no viable free gap can be found before a deadline."""
    pass


class ScheduleConflictError(AutoPaceError):
    """Raised when an immovable commitment conflicts with an existing anchor."""
    pass


class EntityNotFoundError(AutoPaceError):
    """Raised when a requested database entity does not exist."""
    pass
