from fastapi import APIRouter

from api.routes import trackers

from api.routes import users

router = APIRouter()

router.include_router(trackers.router, prefix="/trackers")

router.include_router(users.router, prefix="/users")
