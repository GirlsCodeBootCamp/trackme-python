from fastapi import APIRouter

from api.routes import trackers

router = APIRouter()

router.include_router(trackers.router, prefix="/trackers")