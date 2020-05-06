from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from .models import Calendar, Entry, Participant


def get_calendar(db: Session, calendar_id: int) -> Calendar:
    return db.query(Calendar).filter(Calendar.id == calendar_id).one()


def get_calendar_by_hash(db: Session, url_hash: str):
    return db.query(Calendar).filter(Calendar.url_hash == url_hash).one()


def create_calendar(db: Session, name: str) -> Calendar:
    if len(name) < 3:
        raise ValueError("Calendar name must be at least 3 characters long.")

    # TODO: Hash collision protection.
    db_calendar = Calendar(name=name, url_hash=uuid4().hex)
    db.add(db_calendar)
    db.flush()
    return db_calendar


def create_participant(db: Session, calendar_id: int, name: str) -> Participant:
    participant = Participant(calendar_id=calendar_id, name=name)

    db.add(participant)
    db.flush()

    return participant


def create_entry(db: Session, calendar_id: int, timestamp) -> Entry:
    entry = Entry(calendar_id=calendar_id, timestamp=timestamp)

    db.add(entry)
    db.flush()

    return entry


def delete_entry(db: Session, entry: Entry) -> None:
    db.delete(entry)
    db.flush()


def update_entry(db: Session, entry: Entry, timestamp: datetime) -> Entry:
    entry.timestamp = timestamp
    db.flush()
    return entry
