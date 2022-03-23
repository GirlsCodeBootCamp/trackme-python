from api.routes import trackers, users
from fastapi import APIRouter

router = APIRouter()

router.include_router(trackers.router, prefix="/trackers")

router.include_router(users.router, prefix="/users")
