from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
users = {}


def email_duplicates(email: str):
    users_values = list(users.values())
    for user in users_values:
        if user.email == email:
            return True
    return False


class User(BaseModel):
    first_name: str
    last_name: str
    email: str


@router.post("/create-user/{user_id}")
def create_user(user_id: str, user: User):
    if user_id in users:
        return {"Error": "User id has already been used."}
    if email_duplicates(user.email):
        return {"Error": "Email address has already been used."}
    users[user_id] = user

    return users[user_id]
