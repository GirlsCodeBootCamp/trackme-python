from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


class TrackerBase(BaseModel):
    url_address: str
    name: Optional[str] = None
    frequency: Optional[int] = 24


class TrackerCreate(TrackerBase):
    pass


class Tracker(TrackerBase):
    id: int
    created_at: datetime

    deleted: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    trackers: List[Tracker] = []

    class Config:
        orm_mode = True


'''
class UserOut(User):
    trackers: List[Tracker]


class TrackerOut(Tracker):
    users: List[User]
'''
