"""Study Planner FastAPI Application Factory and ASGI Entrypoint.

Configures:
- Global CORS middleware supporting Vite/React local dev.
- RFC 7807 standardized error response handlers.
- Declarative schema initialization and pre-seeding on startup.
- Full API v1 routing under /api/v1.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.database import Base, engine, SessionLocal
from backend.app.core.exceptions import (
    AutoPaceError,
    CapacityExceededError,
    ZeroGapsAvailableError,
    ScheduleConflictError,
    EntityNotFoundError,
)
from backend.app.services.capacity_service import CapacityService
from backend.app.api.v1.api_router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle startup and shutdown handler."""
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    # Ensure default student configuration is seeded
    db = SessionLocal()
    try:
        CapacityService.get_or_create_config(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Capacity-Aware, Self-Healing Academic Workload Management System",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits frontend dev server on any port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# RFC 7807 Standardized Error Handlers
@app.exception_handler(CapacityExceededError)
async def capacity_exceeded_handler(request: Request, exc: CapacityExceededError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": {
                "code": "CAPACITY_EXCEEDED",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.exception_handler(ZeroGapsAvailableError)
async def zero_gaps_handler(request: Request, exc: ZeroGapsAvailableError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "ZERO_GAPS_AVAILABLE",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": "NOT_FOUND",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.exception_handler(AutoPaceError)
async def autopace_generic_handler(request: Request, exc: AutoPaceError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "BAD_REQUEST",
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


# Attach API v1 Router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root_redirect():
    """Root redirect to API documentation."""
    return {
        "name": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "api_v1": settings.API_V1_PREFIX,
    }
