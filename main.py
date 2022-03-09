from fastapi import FastAPI

from api.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

from sql_app import models
from sql_app.database import engine


def get_application():
    application = FastAPI()
    application.include_router(api_router)
    origins = [
        "http://localhost:3000",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


print("This is test message")
models.Base.metadata.create_all(bind=engine)

app = get_application()
