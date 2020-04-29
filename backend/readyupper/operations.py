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
    db.commit()
    return db_calendar
