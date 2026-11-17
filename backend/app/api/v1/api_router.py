"""Master API v1 router combining all sub-routers."""

from fastapi import APIRouter
from backend.app.api.v1.courses import router as courses_router
from backend.app.api.v1.commitments import router as commitments_router
from backend.app.api.v1.deadlines import router as deadlines_router
from backend.app.api.v1.study_blocks import router as study_blocks_router
from backend.app.api.v1.recovery import router as recovery_router
from backend.app.api.v1.config import router as config_router
from backend.app.api.v1.seed import router as diagnostics_router
from backend.app.api.v1.calendar_sync import router as calendar_router

api_router = APIRouter()

api_router.include_router(diagnostics_router)
api_router.include_router(courses_router)
api_router.include_router(commitments_router)
api_router.include_router(deadlines_router)
api_router.include_router(study_blocks_router)
api_router.include_router(recovery_router)
api_router.include_router(config_router)
api_router.include_router(calendar_router)
