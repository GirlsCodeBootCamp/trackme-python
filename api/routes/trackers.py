#from typing import List
from fastapi import APIRouter, Depends, HTTPException
import random

# from models.trackers import Tracker, trackers
from sql_app.models import Tracker
from sql_app.database import get_db
from sqlalchemy.orm import Session
from sql_app import crud, schemas

router = APIRouter()

# Dependency

# /trackers/

@router.get("/", response_model=list[schemas.Tracker])
def read_trackers_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trackers = crud.get_trackers(db, skip=skip, limit=limit)
    return trackers

@router.get("/{tracker_id}", response_model=schemas.Tracker)
def read_tracker_by_id(tracker_id: int, db: Session = Depends(get_db)):
    db_tracker = crud.get_tracker(db, tracker_id=tracker_id)
    if db_tracker is None:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return db_tracker

# create orphan tracker without user ownership


@router.post("/", response_model=schemas.Tracker)
def create_tracker(tracker: schemas.TrackerCreate, db: Session = Depends(get_db)):
    db_tracker = crud.get_tracker_by_url(db, url_address=tracker.url_address)
    if db_tracker is not None:
        raise HTTPException(status_code=400, detail="URL address already registered")
    return crud.create_tracker(db, tracker)


@router.put("/{tracker_id}/", response_model=schemas.Tracker)
def update_tracker(tracker_id: str, tracker: schemas.TrackerBase, db: Session = Depends(get_db)):
    db_tracker = crud.update_tracker(db, tracker_id, tracker)
    if db_tracker is None:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return crud.delete_tracker_by_id(db, tracker_id=tracker_id)



@router.delete("/{tracker_id}", response_model=schemas.Tracker)
def delete_tracker_by_id(tracker_id: str, db: Session = Depends(get_db)):
    db_tracker = crud.delete_tracker_by_id(db, tracker_id=tracker_id)
    if db_tracker is None:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return crud.delete_tracker_by_id(db, tracker_id=tracker_id)
