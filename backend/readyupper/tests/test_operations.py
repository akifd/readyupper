from datetime import datetime

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from readyupper import operations
from readyupper.models import Calendar, Participant, Entry


def test_get_calendar(db: Session, calendar: Calendar):
    found = operations.get_calendar(db, calendar_id=calendar.id)

    assert isinstance(calendar, Calendar)
    assert found.id == calendar.id


def test_get_non_existant_calendar(db: Session, calendar: Calendar):
    with pytest.raises(NoResultFound):
        operations.get_calendar(db, calendar_id=-1)


def test_get_calendar_by_hash(db: Session, calendar: Calendar):
    found = operations.get_calendar_by_hash(db, url_hash=calendar.url_hash)

    assert isinstance(calendar, Calendar)
    assert found.id == calendar.id


def test_get_calendar_by_invalid_hash(db: Session, calendar: Calendar):
    with pytest.raises(NoResultFound):
        operations.get_calendar_by_hash(db, url_hash=calendar.url_hash + "zxc")


def test_create_calendar(db: Session):
    assert db.query(Calendar).count() == 0

    calendar = operations.create_calendar(db, name="New calendar")

    assert db.query(Calendar).count() == 1
    assert calendar.id
    assert calendar.name == "New calendar"
    assert calendar.url_hash
    assert calendar.created


def test_create_calendar_without_name(db: Session):
    with pytest.raises(ValueError):
        operations.create_calendar(db, name="")


def test_create_participant(db: Session, calendar: Calendar):
    assert db.query(Participant).count() == 0
    operations.create_participant(db, calendar.id, "Jack")
    assert db.query(Participant).count() == 1

    participant = db.query(Participant).one()
    assert participant.calendar_id == calendar.id
    assert participant.name == "Jack"


def test_delete_participant(db: Session, participant: Participant):
    assert db.query(Participant).count() == 1
    operations.delete_participant(db, participant)
    assert db.query(Participant).count() == 0


def test_create_entry(db: Session, calendar: Calendar):
    timestamp = datetime(2020, 5, 18, 10, 30, 0)

    operations.create_entry(db, calendar.id, timestamp)

    entry = db.query(Entry).one()
    assert entry.calendar_id == calendar.id
    assert entry.timestamp == timestamp


def test_delete_entry(db: Session, entry: Entry):
    assert db.query(Entry).count() == 1
    operations.delete_entry(db, entry)
    assert db.query(Entry).count() == 0


def test_update_entry(db: Session, entry: Entry):
    timestamp = datetime(2020, 5, 10, 18, 45, 0)

    operations.update_entry(db, entry, timestamp)

    entry = db.query(Entry).one()
    assert entry.timestamp == datetime(2020, 5, 10, 18, 45, 0)
