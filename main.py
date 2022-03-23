import os

import uvicorn
from api.api import router as api_router
from fastapi import FastAPI
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


models.Base.metadata.create_all(bind=engine)

app = get_application()

if __name__ == "__main__":
    server_port = os.getenv("PORT") or 8000
    uvicorn.run("main:app", host="0.0.0.0", port=server_port)
