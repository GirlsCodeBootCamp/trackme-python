from models import trackers, users
from sqlalchemy.orm import Session, joinedload

from . import models


def get_tracker(data_base: Session, tracker_id: int):
    return (
        data_base.query(models.Tracker)
        .filter(models.Tracker.id == tracker_id)
        .one_or_none()
    )


def get_tracker_by_url(data_base: Session, url_address: str):
    return (
        data_base.query(models.Tracker)
        .filter(models.Tracker.url_address == url_address)
        .one_or_none()
    )


def get_trackers(data_base: Session, skip: int = 0, limit: int = 100):
    return data_base.query(models.Tracker).offset(skip).limit(limit).all()


def create_tracker(data_base: Session, tracker: trackers.TrackerCreate):
    db_tracker = models.Tracker(url_address=tracker.url_address, name=tracker.name)
    data_base.add(db_tracker)
    data_base.commit()
    data_base.refresh(db_tracker)
    return db_tracker


def update_tracker(data_base: Session, tracker_id: int, tracker: trackers.TrackerBase):
    # get the existing data
    db_tracker = (
        data_base.query(models.Tracker)
        .filter(models.Tracker.id == tracker_id)
        .one_or_none()
    )
    if db_tracker is None:
        return None

    # Update model class variable from requested fields
    db_tracker.name = tracker.name
    for var, value in vars(tracker).items():
        if value:
            setattr(db_tracker, var, value)
    data_base.add(db_tracker)
    data_base.commit()
    data_base.refresh(db_tracker)
    return db_tracker


def delete_tracker_by_id(data_base: Session, tracker_id: int):
    # get the existing data
    db_tracker = (
        data_base.query(models.Tracker)
        .filter(models.Tracker.id == tracker_id)
        .one_or_none()
    )
    if db_tracker is None:
        return None

    # set deleted to True
    db_tracker.deleted = True
    data_base.commit()
    data_base.refresh(db_tracker)
    return db_tracker


def get_user(data_base: Session, user_id: int):
    return (
        data_base.query(models.User)
        .options(joinedload(models.User.trackers))
        .filter(models.User.id == user_id)
        .one_or_none()
    )


def get_user_by_email(data_base: Session, email: str):
    return (
        data_base.query(models.User)
        .options(joinedload(models.User.trackers))
        .filter(models.User.email == email)
        .one_or_none()
    )


def get_users(data_base: Session, skip: int = 0, limit: int = 100):
    result = data_base.query(models.User).offset(skip).limit(limit).all()
    return result


def create_user(data_base: Session, user: users.UserCreate):
    db_user = models.User(email=user.email, username=user.username)
    data_base.add(db_user)
    data_base.commit()
    data_base.refresh(db_user)
    return db_user


def create_user_tracker(data_base: Session, item: trackers.TrackerCreate, user_id: int):
    # check if user exist, get its data
    db_user = get_user(data_base, user_id)
    if db_user is None:
        return None
    db_tracker = (
        data_base.query(models.Tracker)
        .filter(models.Tracker.url_address == item.url_address)
        .one_or_none()
    )

    # create tracker if tracker with given url doesn't exist
    if db_tracker is None:
        db_tracker = models.Tracker(**item.dict())

    # connect tracker to user
    db_tracker.owners.append(db_user)
    db_tracker.deleted = False
    data_base.add(db_tracker)
    data_base.commit()
    data_base.refresh(db_tracker)
    return db_tracker
