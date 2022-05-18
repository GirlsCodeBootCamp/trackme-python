from typing import List

from pydantic import BaseModel

from .trackers import Tracker


class UserBase(BaseModel):
    id: str
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    trackers: List[Tracker] = []

    class Config:
        orm_mode = True
