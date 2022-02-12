from fastapi import FastAPI

from api.api import router as api_router


def get_application():
    application = FastAPI()
    application.include_router(api_router)
    return application


app = get_application()
