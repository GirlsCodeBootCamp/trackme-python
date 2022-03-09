from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime
from .trackers import Tracker


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
