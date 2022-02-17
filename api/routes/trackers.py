from fastapi import APIRouter
import random

from models.trackers import Tracker, trackers

router = APIRouter()


@router.get("/")
def read_trackers_all():
    return trackers


@router.get("/{tracker_id}")
def read_tracker_by_id(tracker_id: int):
    if tracker_id in trackers.keys():
        return trackers[tracker_id]
    return {"message": "Tracker not found"}


@router.post("/")
def create_tracker(tracker: Tracker):
    tracker_id = random.randint(1, 9999)
    trackers[tracker_id] = tracker
    return {"tracker_name": tracker.name, "tracker_id": tracker_id}


@router.put("/{tracker_id}")
def update_tracker(tracker_id: str, tracker: Tracker):
    if tracker_id in trackers.keys():
        trackers[tracker_id] = tracker
        return {"tracker_name": tracker.name, "tracker_id": tracker_id}
    return {"message": "Tracker not found"}


@router.delete("/{tracker_id}")
def delete_tracker_by_id(tracker_id: str):
    if tracker_id in trackers.keys():
        trackers[tracker_id]["deleted"] = True
        return {"message": "Tracker has been deleted"}
    return {"message": "Tracker not found"}