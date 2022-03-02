from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

class TrackerBase(BaseModel):
    url_address: str
    name: str
    created_at: Optional[datetime] = None
    is_offer: Optional[bool] = None
    deleted: Optional[bool] = False

class TrackerCreate(TrackerBase):
    pass

class Tracker(TrackerBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    
    trackers: List[Tracker] = []

    class Config:
        orm_mode = True


class UserOut(User):
    trackers: List[Tracker]


class TrackerOut(Tracker):
    users: List[User]


