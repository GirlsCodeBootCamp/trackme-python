from typing import Optional

from datetime import datetime
from pydantic import BaseModel


class TrackerBase(BaseModel):
    url_address: str
    name: Optional[str] = None


class TrackerCreate(TrackerBase):
    pass


class Tracker(TrackerBase):
    id: int
    created_at: datetime

    deleted: bool

    class Config:
        orm_mode = True
