from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session

from . import models


def get_calendar(db: Session, calendar_id: int):
    return db.query(models.Calendar).filter(models.Calendar.id == calendar_id).one()


def get_calendar_by_hash(db: Session, url_hash: str):
    return db.query(models.Calendar).filter(models.Calendar.url_hash == url_hash).one()


def create_calendar(db: Session, name: str):
    # TODO: Hash collision protection.
    db_calendar = models.Calendar(name=name, url_hash=uuid4().hex)
    db.add(db_calendar)
    db.flush()
    return db_calendar


def set_participants(db: Session, calendar: models.Calendar, participants: List[str]):
    db.query(models.Participant) \
        .filter(models.Participant.calendar_id == calendar.id) \
        .delete()

    participants = [models.Participant(calendar_id=calendar.id, name=name)
                    for name in participants]

    db.add_all(participants)
    db.flush()

    return participants
