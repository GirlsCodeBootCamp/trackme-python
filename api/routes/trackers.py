from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPBearer
from models import trackers
from sql_app import crud
from sql_app.database import get_db
from sqlalchemy.orm import Session
from .utils import VerifyToken

router = APIRouter()
token_auth_scheme = HTTPBearer()


@router.get("/", response_model=list[trackers.Tracker])
def read_trackers_all(
    response: Response,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: str = Depends(token_auth_scheme),
):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # return result
    return crud.get_trackers(db, skip=skip, limit=limit)


@router.get("/{tracker_id}", response_model=trackers.Tracker)
def read_tracker_by_id(
    response: Response,
    tracker_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(token_auth_scheme),
):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    db_tracker = crud.get_tracker(db, tracker_id=tracker_id)
    if not db_tracker:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return db_tracker


# create orphan tracker without user ownership
@router.post("/", response_model=trackers.Tracker)
def create_tracker(tracker: trackers.TrackerCreate, db: Session = Depends(get_db)):
    db_tracker = crud.get_tracker_by_url(db, url_address=tracker.url_address)
    if db_tracker:
        raise HTTPException(status_code=400, detail="URL address already registered")
    return crud.create_tracker(db, tracker)


@router.put("/{tracker_id}/", response_model=trackers.Tracker)
def update_tracker(
    tracker_id: int, tracker: trackers.TrackerBase, db: Session = Depends(get_db)
):
    db_tracker = crud.update_tracker(db, tracker_id, tracker)
    if not db_tracker:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return crud.delete_tracker_by_id(db, tracker_id=tracker_id)


@router.delete("/{tracker_id}", response_model=trackers.Tracker)
def delete_tracker_by_id(tracker_id: int, db: Session = Depends(get_db)):
    db_tracker = crud.delete_tracker_by_id(db, tracker_id=tracker_id)
    if not db_tracker:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return crud.delete_tracker_by_id(db, tracker_id=tracker_id)
