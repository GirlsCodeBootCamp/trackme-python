from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Tracker(BaseModel):
    name: Optional[str]
    url_address: str
    created_at: Optional[datetime] = datetime.now()
    is_offer: Optional[bool] = None
    deleted: Optional[bool] = False


trackers = {
    45: {
        "name": "Yandex",
        "url_address": "https://ya.ru"
    },
    723: {
        "url_address": "yahoo.com",
        "created_at": "2022-02-10T19:40:35.073346",
    },
    611: {
        "url_address": "mail.ru",
        "created_at": "2022-02-10T19:40:35.073346",
    },
    5908: {
        "url_address": "torba.com.ua",
        "created_at": "2022-02-10T19:40:35.073346",
        "is_offer": None
    }
}
