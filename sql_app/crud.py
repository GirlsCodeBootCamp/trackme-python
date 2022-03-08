from sqlalchemy.orm import Session, joinedload

from . import models, schemas

def get_tracker(db: Session, tracker_id: int):
    return db.query(models.Tracker).filter(models.Tracker.id == tracker_id).one_or_none()

def get_tracker_by_url(db: Session, url_address: str):
    return db.query(models.Tracker).filter(models.Tracker.url_address == url_address).one_or_none()

def get_trackers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tracker).offset(skip).limit(limit).all()


def create_tracker(db: Session, tracker: schemas.TrackerCreate):
    db_tracker = models.Tracker(
        url_address=tracker.url_address,
        name=tracker.name
    )
    db.add(db_tracker)
    db.commit()
    db.refresh(db_tracker)
    return db_tracker


def update_tracker(db: Session, tracker_id: int, tracker: schemas.TrackerBase):
    # get the existing data
    db_tracker = db.query(models.Tracker).filter(models.Tracker.id == tracker_id).one_or_none()
    if db_tracker is None:
        return None
    
    # Update model class variable from requested fields 
    db_tracker.name = tracker.name
    for var, value in vars(tracker).items():
        setattr(db_tracker, var, value) if value else None
    db.add(db_tracker)
    db.commit()
    db.refresh(db_tracker)
    return db_tracker


def delete_tracker_by_id(db: Session, tracker_id: int):
    # get the existing data
    db_tracker = db.query(models.Tracker).filter(models.Tracker.id == tracker_id).one_or_none()
    if db_tracker is None:
        return None

    # set deleted to True
    db_tracker.deleted = True
    db.commit()
    db.refresh(db_tracker)
    return db_tracker

def get_user(db: Session, user_id: int):
    return db.query(models.User).options(joinedload(models.User.trackers)).filter(models.User.id == user_id).one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).options(joinedload(models.User.trackers)).filter(models.User.email == email).one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).options(joinedload(models.User.trackers)).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_tracker(db: Session, item: schemas.TrackerCreate, user_id: int):
    # check if user exist, get its data
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    db_tracker = db.query(models.Tracker).filter(models.Tracker.url_address == item.url_address).one_or_none()

    # create tracker if tracker with given url doesn't exist
    if db_tracker is None:
        db_tracker = models.Tracker(**item.dict())

    # connect tracker to user
    db_tracker.owners.append(db_user)
    db_tracker.deleted = False
    db.add(db_tracker)
    db.commit()
    db.refresh(db_tracker)
    return db_tracker


