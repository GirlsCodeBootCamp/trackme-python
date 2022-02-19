from pydantic import BaseModel
import pydantic.types

users = {}


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
