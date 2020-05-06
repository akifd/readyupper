from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session

from . import models


def get_calendar(db: Session, calendar_id: int) -> models.Calendar:
    return db.query(models.Calendar).filter(models.Calendar.id == calendar_id).one()


def get_calendar_by_hash(db: Session, url_hash: str):
    return db.query(models.Calendar).filter(models.Calendar.url_hash == url_hash).one()


def create_calendar(db: Session, name: str) -> models.Calendar:
    if len(name) < 3:
        raise ValueError("Calendar name must be at least 3 characters long.")

    # TODO: Hash collision protection.
    db_calendar = models.Calendar(name=name, url_hash=uuid4().hex)
    db.add(db_calendar)
    db.flush()
    return db_calendar


def set_participants(db: Session, calendar: models.Calendar, participants: List[str]) \
        -> List[models.Participant]:
    db.query(models.Participant) \
        .filter(models.Participant.calendar_id == calendar.id) \
        .delete()

    participants = [models.Participant(calendar_id=calendar.id, name=name)
                    for name in participants]

    db.add_all(participants)
    db.flush()

    return participants


def create_entry(db: Session, calendar_id: int, timestamp) -> models.Entry:
    entry = models.Entry(calendar_id=calendar_id, timestamp=timestamp)

    db.add(entry)
    db.flush()

    return entry


def delete_entry(db: Session, entry: models.Entry) -> None:
    db.delete(entry)
    db.flush()


def update_entry(db: Session, entry: models.Entry, timestamp: datetime) -> models.Entry:
    entry.timestamp = timestamp
    db.flush()
    return entry
