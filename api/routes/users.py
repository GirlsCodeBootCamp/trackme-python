from fastapi import APIRouter, Depends
from typing import Optional
# from models.users import User, users
# from sql_app.models import User
from sql_app.database import get_db
from sqlalchemy.orm import Session
from sql_app import crud, schemas
from sql_app.database import get_db

router = APIRouter()

user_id_gen = 0


def email_duplicates(email: str):
    users_values = list(users.values())
    for user in users_values:
        if user.email == email:
            return True
    return False

# Create user


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # db_user = crud.get_user_by_email(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User])
# def user_list_filtered(last_name: Optional[str] = None):
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def user_by_id(user_id: int, db: Session = Depends(get_db)):
    if user_id not in users:
        return {"Error": "User not found."}

    return users[user_id]


@router.post("/{user_id}/tracker", response_model=schemas.Tracker)
def create_tracker(tracker: schemas.TrackerCreate, db: Session = Depends(get_db)):
    db_tracker = crud.create_tracker(db, tracker)
    # connect to the user in user_tracker
    return db_tracker
