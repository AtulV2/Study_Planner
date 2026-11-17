"""Application configuration module.

Loads environment variables using Pydantic Settings, providing strongly-typed
runtime configurations for database connections and default student boundaries.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings and constraints."""

    # Project metadata
    PROJECT_NAME: str = "AutoPace"
    API_V1_PREFIX: str = "/api/v1"

    # Database configuration: defaults to local SQLite with WAL mode
    DATABASE_URL: str = "sqlite:///./autopace.db"

    # Default student cognitive boundaries
    DEFAULT_MAX_DAILY_STUDY_HOURS: float = 5.5
    DEFAULT_WAKE_TIME: str = "08:00"
    DEFAULT_SLEEP_TIME: str = "23:00"
    DEFAULT_PREFERRED_CHUNK_MINUTES: int = 60
    DEFAULT_MIN_GAP_BUFFER_MINUTES: int = 15
    DEFAULT_PROTECT_WEEKENDS: bool = False

    # Meal buffer specifications (HH:MM)
    LUNCH_START: str = "12:30"
    LUNCH_END: str = "13:15"
    DINNER_START: str = "18:30"
    DINNER_END: str = "19:15"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
