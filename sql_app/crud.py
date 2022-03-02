from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_tracker(db: Session, item: schemas.TrackerCreate, user_id: int):
    db_tracker = models.Tracker(**item.dict(), owner_id=user_id)
    db.add(db_tracker)
    db.commit()
    db.refresh(db_tracker)
    return db_tracker


def get_tracker(db: Session, tracker_id: int):
    return db.query(models.Tracker).filter(models.Tracker.id == tracker_id).first()


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


def update_tracker():
    return


def delete_tracker_by_id():
    # set deleted to True
    return
