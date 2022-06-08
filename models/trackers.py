from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TrackerBase(BaseModel):
    url_address: str
    name: Optional[str] = None


class TrackerCreate(TrackerBase):
    user_id: str


class Tracker(TrackerBase):
    id: int
    created_at: datetime

    deleted: bool

    class Config:
        orm_mode = True
