import pytest
from sqlalchemy.orm.exc import NoResultFound

from . import operations
from .models import Calendar


@pytest.fixture
def calendar(db):
    calendar = Calendar(name="Test calendar", url_hash="abcdefg")
    db.add(calendar)
    db.flush()
    return calendar


def test_get_calendar(db, calendar):
    found = operations.get_calendar(db, calendar_id=calendar.id)

    assert isinstance(calendar, Calendar)
    assert found.id == calendar.id


def test_get_non_existant_calendar(db, calendar):
    with pytest.raises(NoResultFound):
        operations.get_calendar(db, calendar_id=-1)


def test_get_calendar_by_hash(db, calendar):
    found = operations.get_calendar_by_hash(db, url_hash="abcdefg")

    assert isinstance(calendar, Calendar)
    assert found.id == calendar.id


def test_get_calendar_by_invalid_hash(db, calendar):
    with pytest.raises(NoResultFound):
        operations.get_calendar_by_hash(db, url_hash="qwerty")


def test_create_calendar(db):
    assert db.query(Calendar).count() == 0

    calendar = operations.create_calendar(db, name="New calendar")

    assert db.query(Calendar).count() == 1
    assert calendar.id
    assert calendar.name == "New calendar"
    assert calendar.url_hash
    assert calendar.created
