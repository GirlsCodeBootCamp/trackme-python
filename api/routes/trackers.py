from typing import Optional
from email.mime.text import MIMEText

from api.routes.utils import VerifyToken
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import trackers
from sql_app import crud
from sql_app.database import get_db
from sqlalchemy.orm import Session
import time
import difflib
import smtplib
import ssl
import urllib3
from bs4 import BeautifulSoup as bs
import re


router = APIRouter()
token_auth_scheme = HTTPBearer()


def validate_token(token):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        raise HTTPException(status_code=400, detail=result)
    return result


@router.get("/", response_model=Optional[list[trackers.Tracker]])
def read_trackers_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
):
    result = validate_token(token)
    result = crud.get_trackers(db, skip=skip, limit=limit)
    return result


@router.get("/{tracker_id}", response_model=trackers.Tracker)
def read_tracker_by_id(
    tracker_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
):
    validate_token(token)
    db_tracker = crud.get_tracker(db, tracker_id=tracker_id)
    if not db_tracker:
        raise HTTPException(status_code=404, detail="Tracker not found")
    return db_tracker


# create orphan tracker without user ownership
@router.post("/", response_model=trackers.Tracker)
def create_tracker(tracker: trackers.TrackerCreate, db: Session = Depends(get_db)):
    db_tracker = crud.get_tracker_by_url(db, url_address=tracker.url_address)
    if not db_tracker:
        db_tracker = crud.create_tracker(db, tracker)
    db_tracker = crud.create_user_tracker(db, tracker, tracker.user_id)
    return db_tracker


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


def send_email(receiver_email, message):
    sender_email = "info@trackme.ninja"
    password = "9tur!W4jJzrM"
    smtp_server = "smtp.zoho.com"
    port = 465  # For starttls
    msg = MIMEText(message)
    msg["Subject"] = "Content changed"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(msg.get("From"), msg["To"], msg.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    print(f"{message} sent to {receiver_email}")


def check_tracker(tracker: str, db):
    print(tracker.id, tracker.url_address)
    if not tracker.owners:
        return

    old_content = tracker.content

    http = urllib3.PoolManager()
    try:
        resp = http.request("GET", tracker.url_address)
        root = resp.data
        soup = bs(root)  # make BeautifulSoup
        output = soup.get_text()
        new_content = re.sub(r"\n+", "\n", output)
        changed = False
        if tracker.content:
            i = 0
            for text in difflib.unified_diff(
                new_content.split("\n"), old_content.split("\n")
            ):
                if text[:3] not in ("+++", "---", "@@ "):
                    changed = True
                    # print(text)
                    i += 1
        if changed or not tracker.content:
            tracker.content = new_content
            crud.update_tracker(db, tracker.id, tracker)
            # TODO Add timestamp when changed
            # TODO send an email, add task to background task?
            message = f"Subject: New changes on website \n \n the tracker {tracker.url_address} has been changed"
            for user in tracker.owners:
                print(user.email, message)
                send_email(user.email, message)
            # TODO add to UI and/or API validation of the URL when creating a tracker
    except Exception:
        print("URL not valid")


# testing endpoint
@router.post("/track")
async def send_notification(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    result = crud.get_trackers(db)

    for tr in result:
        background_tasks.add_task(check_tracker, tr, db)
    print("all trackers have been checked")
    return result
