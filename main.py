from typing import Optional
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

trackers = {
    "45": {
        "name": "Yandex",
        "url_address": "https://ya.ru"
    },
    "723": {
        "url_address": "yahoo.com",
        "created_at": "2022-02-10T19:40:35.073346",
    },
    "611": {
        "url_address": "mail.ru",
        "created_at": "2022-02-10T19:40:35.073346",
    },
    "5908": {
        "url_address": "torba.com.ua",
        "created_at": "2022-02-10T19:40:35.073346",
        "is_offer": None
    }
}


class Tracker(BaseModel):
    name: Optional[str]
    url_address: str
    created_at: Optional[datetime] = datetime.now()
    is_offer: Optional[bool] = None


class User(BaseModel):
    name: str
    email: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/trackers/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if item_id in trackers.keys():
        return trackers[item_id]
    return {"message": "Tracker not found"}


# @app.get("/trackers/")
# def read_items():
#     return trackers
@app.post("/trackers/")
def create_item(item: Tracker):
    item_id = random.randint(1, 9999)
    trackers[item_id] = item
    return {"item_name": item.name, "item_id": item_id}


@app.put("/trackers/{item_id}")
def update_item(item_id: int, item: Tracker):
    if item_id in trackers.keys():
        trackers[item_id] = item
        return {"item_name": item.name, "item_id": item_id}
    return {"message": "Tracker not found"}
