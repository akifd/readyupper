import json
import pytest
from sqlalchemy.orm.exc import NoResultFound

from . import operations, schemas
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


def test_view_read_calendar(test_client, calendar):
    response = test_client.get(f"/calendar/{calendar.url_hash}/")

    assert response.status_code == 200
    data = response.json()
    assert data.keys() == {"id", "name", "url_hash", "created"}
    assert data == json.loads(schemas.Calendar(**data).json())


def test_view_create_calendar(test_client, db):
    assert db.query(Calendar).count() == 0

    response = test_client.post("/calendar/", json={"name": "New calendar"})

    assert response.status_code == 200

    data = response.json()
    assert data.keys() == {"id", "name", "url_hash", "created"}
    assert data == json.loads(schemas.Calendar(**data).json())

    assert db.query(Calendar).count() == 1
    calendar = db.query(Calendar).one()
    assert calendar.name == "New calendar"
    assert calendar.url_hash
    assert calendar.created
