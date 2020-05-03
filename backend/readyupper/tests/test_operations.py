import pytest
from sqlalchemy.orm.exc import NoResultFound

from readyupper import operations
from readyupper.models import Calendar, Participant


def test_get_calendar(db, calendar):
    found = operations.get_calendar(db, calendar_id=calendar.id)

    assert isinstance(calendar, Calendar)
    assert found.id == calendar.id


def test_get_non_existant_calendar(db, calendar):
    with pytest.raises(NoResultFound):
        operations.get_calendar(db, calendar_id=-1)


def test_get_calendar_by_hash(db, calendar):
    found = operations.get_calendar_by_hash(db, url_hash=calendar.url_hash)

    assert isinstance(calendar, Calendar)
    assert found.id == calendar.id


def test_get_calendar_by_invalid_hash(db, calendar):
    with pytest.raises(NoResultFound):
        operations.get_calendar_by_hash(db, url_hash=calendar.url_hash + "zxc")


def test_create_calendar(db):
    assert db.query(Calendar).count() == 0

    calendar = operations.create_calendar(db, name="New calendar")

    assert db.query(Calendar).count() == 1
    assert calendar.id
    assert calendar.name == "New calendar"
    assert calendar.url_hash
    assert calendar.created


def test_create_calendar_without_name(db):
    with pytest.raises(ValueError):
        operations.create_calendar(db, name="")


def test_set_participants(db, calendar):
    assert db.query(Participant).count() == 0
    operations.set_participants(db, calendar, ["Jack", "John"])
    assert db.query(Participant).count() == 2

    participants = db.query(Participant).order_by(Participant.id).all()
    assert participants[0].calendar_id == calendar.id
    assert participants[0].name == "Jack"
    assert participants[1].calendar_id == calendar.id
    assert participants[1].name == "John"


def test_set_participants_with_existing_rows(db, calendar):
    calendar.participants = [Participant(calendar=calendar, name="Jack"),
                             Participant(calendar=calendar, name="John")]
    db.flush()

    assert db.query(Participant).count() == 2
    operations.set_participants(db, calendar, ["Jack", "Mat"])
    assert db.query(Participant).count() == 2

    participants = db.query(Participant).order_by(Participant.id).all()
    assert participants[0].calendar_id == calendar.id
    assert participants[0].name == "Jack"
    assert participants[1].calendar_id == calendar.id
    assert participants[1].name == "Mat"


def test_set_participants_to_empty(db, calendar):
    calendar.participants = [Participant(calendar=calendar, name="Jack"),
                             Participant(calendar=calendar, name="John")]
    db.flush()

    assert db.query(Participant).count() == 2
    operations.set_participants(db, calendar, [])
    assert db.query(Participant).count() == 0
