from fastapi import APIRouter
from typing import Optional
from models.users import User, users

router = APIRouter()

user_id_gen = 0


def email_duplicates(email: str):
    users_values = list(users.values())
    for user in users_values:
        if user.email == email:
            return True
    return False


@router.post("/")
def create_user(user: User):
    if email_duplicates(user.email):
        return {"Error": "Email address has already been used."}
    global user_id_gen
    user_id_gen += 1
    users[user_id_gen] = user
    return users[user_id_gen]


@router.get("/")
def user_list_filtered(last_name: Optional[str] = None):
    users_filtered = {}
    for user_id, user in users.items():
        if user['last_name'] == last_name:
            users_filtered[user_id] = user
    return {"size": len(users_filtered), "data": users_filtered}


@router.get("/{user_id}")
def user_by_id(user_id: int):
    if user_id not in users:
        return {"Error": "User not found."}

    return users[user_id]
