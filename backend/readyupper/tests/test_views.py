import json
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from readyupper import schemas
from readyupper.models import Calendar, Entry, Participant


def test_view_read_calendar(test_client: TestClient, calendar: Calendar):
    response = test_client.get(f"/calendar/{calendar.url_hash}/")

    assert response.status_code == 200
    data = response.json()
    assert data.keys() == {"id", "name", "url_hash", "created"}
    assert data == json.loads(schemas.Calendar(**data).json())


def test_view_create_calendar(db: Session, test_client: TestClient):
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


def test_view_create_calendar_with_short_name(db: Session, test_client: TestClient):
    response = test_client.post("/calendar/", json={"name": "AB"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{
            "loc": ["body", "calendar", "name"],
            "msg": "Name must be at least 3 characters long.",
            "type": "value_error",
        }]
    }


def test_view_create_participant(db: Session, test_client: TestClient,
                                 calendar: Calendar):
    response = test_client.post("/participants/",
                                json={"calendar_id": calendar.id, "name": "Jack"})

    assert response.status_code == 200

    data = response.json()
    assert data.keys() == {"id", "calendar_id", "name", "created"}
    assert data == json.loads(schemas.Participant(**data).json())

    assert db.query(Participant).count() == 1
    participant = db.query(Participant).one()
    assert participant.calendar_id == calendar.id
    assert participant.name == "Jack"
    assert participant.created


def test_view_create_participant_with_short_name(db: Session, test_client: TestClient,
                                                 calendar: Calendar):
    response = test_client.post("/participants/",
                                json={"calendar_id": calendar.id, "name": ""})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{
            "loc": ["body", "participant", "name"],
            "msg": "Name must be at least 3 characters long.",
            "type": "value_error",
        }]
    }


def test_view_delete_participant(db: Session, test_client: TestClient,
                                 participant: Participant):
    assert db.query(Participant).count() == 1

    response = test_client.delete(f"/participants/{participant.id}/")

    assert response.status_code == 200
    assert db.query(Participant).count() == 0


def test_view_update_participant(db: Session, test_client: TestClient,
                                 calendar: Calendar, participant: Participant):
    response = test_client.patch(f"/participants/{participant.id}/",
                                 json={"name": "John"})

    assert response.status_code == 200

    participant = db.query(Participant).one()
    assert participant.name == "John"

    data = response.json()
    assert data.keys() == {"id", "calendar_id", "name", "created"}
    assert data["id"] is not None
    assert data["calendar_id"] == calendar.id
    assert data["name"] == "John"
    assert data["created"] is not None


def test_view_create_entry(db: Session, test_client: TestClient,
                           calendar: Calendar):
    assert db.query(Entry).count() == 0

    response = test_client.post("/entries/", json={"calendar_id": calendar.id,
                                                   "timestamp": "2020-05-18 10:30:00"})

    assert response.status_code == 200

    data = response.json()

    assert data.keys() == {"id", "calendar_id", "timestamp", "created"}
    assert data["id"] is not None
    assert data["calendar_id"] == calendar.id
    assert data["timestamp"] == "2020-05-18T10:30:00"
    assert data["created"] is not None


def test_view_delete_entry(db: Session, test_client: TestClient, entry: Entry):
    assert db.query(Entry).count() == 1

    response = test_client.delete(f"/entries/{entry.id}/")

    assert response.status_code == 200
    assert db.query(Entry).count() == 0


def test_view_update_entry(db: Session, test_client: TestClient, calendar: Calendar,
                           entry: Entry):
    response = test_client.patch(f"/entries/{entry.id}/",
                                 json={"timestamp": "2020-12-22 09:25:00"})

    assert response.status_code == 200

    entry = db.query(Entry).one()
    assert entry.timestamp == datetime(2020, 12, 22, 9, 25, 0)

    data = response.json()
    assert data.keys() == {"id", "calendar_id", "timestamp", "created"}
    assert data["id"] is not None
    assert data["calendar_id"] == calendar.id
    assert data["timestamp"] == "2020-12-22T09:25:00"
    assert data["created"] is not None
