from api.routes.utils import VerifyToken
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import trackers, users
from sql_app import crud
from sql_app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
token_auth_scheme = HTTPBearer()


def validate_token(token):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        raise HTTPException(status_code=400, detail=result)
    return result


# Create user
@router.post("/", response_model=users.User)
def create_user(
    user: users.UserCreate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
):
    db_user = crud.get_user(db, user.id)
    if db_user:
        print(f"user exists, {user.username}, skipping creation")
    return crud.create_user(db, user)


@router.get("/", response_model=list[users.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=users.User)
def read_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
):
    validate_token(token)

    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/tracker", response_model=trackers.Tracker)
def create_user_tracker(
    user_id: int, tracker: trackers.TrackerCreate, db: Session = Depends(get_db)
):
    db_tracker = crud.create_user_tracker(db, tracker, user_id)
    if not db_tracker:
        raise HTTPException(status_code=404, detail="User not found")
    # connect to the user in user_tracker
    return db_tracker
