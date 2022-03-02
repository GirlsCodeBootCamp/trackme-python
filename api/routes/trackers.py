from fastapi import APIRouter, Depends
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

# /trackers/611


@router.get("/{tracker_id}", response_model=schemas.Tracker)
def read_tracker_by_id(tracker_id: int, db: Session = Depends(get_db)):
    # if tracker_id in trackers.keys():
    #     return trackers[tracker_id]
    # return {"message": "Tracker not found"}
    return crud.get_tracker(tracker_id=tracker_id)

# create orphan tracker without user ownership


@router.post("/", response_model=schemas.Tracker)
def create_tracker(tracker: schemas.TrackerCreate, db: Session = Depends(get_db)):
    return crud.create_tracker(db, tracker)


# @router.put("/{tracker_id}")
# def update_tracker(tracker_id: str, tracker: Tracker, db: Session = Depends(get_db)):
#     if tracker_id in trackers.keys():
#         trackers[tracker_id] = tracker
#         return {"tracker_name": tracker.name, "tracker_id": tracker_id}
#     return {"message": "Tracker not found"}


# @router.delete("/{tracker_id}")
# def delete_tracker_by_id(tracker_id: str, db: Session = Depends(get_db)):
#     if tracker_id in trackers.keys():
#         trackers[tracker_id]["deleted"] = True
#         return {"message": "Tracker has been deleted"}
#     return {"message": "Tracker not found"}
