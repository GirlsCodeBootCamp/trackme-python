from fastapi import FastAPI

from api.api import router as api_router
import uvicorn
import os


def get_application():
    application = FastAPI()
    application.include_router(api_router)
    return application


app = get_application()

if __name__ == "__main__":
    server_port = os.getenv("PORT") or 8000
    uvicorn.run("main:app", host="0.0.0.0", port=server_port)
