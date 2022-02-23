from pydantic import BaseModel
import pydantic.types

users = {
    45: {
        "first_name": "Simon",
        "last_name": "Bandoor",
        "email": "simon.b@gmail.com"
    },
    46: {
        "first_name": "Teresa",
        "last_name": "Bandoor",
        "email": "teresa.b@gmail.com"
    },
    47: {
        "first_name": "Tyler",
        "last_name": "Johns",
        "email": "tyler.tyler@yahoo.com",
    },
}


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
