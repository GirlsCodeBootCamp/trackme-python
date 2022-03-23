from fastapi import APIRouter, Depends, HTTPException
from sql_app.database import get_db
from sqlalchemy.orm import Session
from sql_app import crud, schemas

router = APIRouter()

# Create user

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/tracker", response_model=schemas.Tracker)
def create_user_tracker(user_id: int, tracker: schemas.TrackerCreate, db: Session = Depends(get_db)):
    db_tracker = crud.create_user_tracker(db, tracker, user_id)
    if not db_tracker:       
        raise HTTPException(status_code=404, detail="User not found")
    # connect to the user in user_tracker
    return db_tracker
