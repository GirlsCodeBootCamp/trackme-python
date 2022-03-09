from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


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
