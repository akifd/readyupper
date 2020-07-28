import json
import uuid
from datetime import datetime
from typing import List

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from readyupper import schemas
from readyupper.models import Calendar, Entry, Participant, Participation


def test_get_calendar(test_client: TestClient, calendar: Calendar):
    response = test_client.get(f"/calendars/{calendar.id}/")

    assert response.status_code == 200
    data = response.json()
    assert data.keys() == {"id", "name", "created"}
    assert data == json.loads(schemas.Calendar(**data).json())


def test_get_inexistant_calendar(test_client: TestClient):
    random_uuid = uuid.uuid4()
    response = test_client.get(f"/calendars/{random_uuid}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Calendar not found."}


def test_create_calendar(db: Session, test_client: TestClient):
    assert db.query(Calendar).count() == 0

    response = test_client.post("/calendars/", json={"name": "New calendar"})

    assert response.status_code == 200

    data = response.json()
    assert data.keys() == {"id", "name", "created"}
    assert data == json.loads(schemas.Calendar(**data).json())

    assert db.query(Calendar).count() == 1
    calendar = db.query(Calendar).one()
    assert calendar.name == "New calendar"
    assert calendar.created


def test_create_calendar_with_short_name(db: Session, test_client: TestClient):
    response = test_client.post("/calendars/", json={"name": "AB"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{
            "loc": ["body", "calendar", "name"],
            "msg": "Name must be at least 3 characters long.",
            "type": "value_error",
        }]
    }


def test_delete_calendar(db: Session, test_client: TestClient, calendar: Calendar):
    response = test_client.delete(f"/calendars/{calendar.id}/")
    assert response.status_code == 200
    assert db.query(Calendar).count() == 0


def test_delete_inexistant_calendar(db: Session, test_client: TestClient):
    random_uuid = uuid.uuid4()
    response = test_client.delete(f"/calendars/{random_uuid}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Calendar not found."}


def test_create_participant(db: Session, test_client: TestClient, calendar: Calendar):
    response = test_client.post("/participants/",
                                json={"calendar_id": str(calendar.id), "name": "Jack"})

    assert response.status_code == 200

    data = response.json()
    assert data.keys() == {"id", "calendar_id", "name", "created"}
    assert data == json.loads(schemas.Participant(**data).json())

    assert db.query(Participant).count() == 1
    participant = db.query(Participant).one()
    assert participant.calendar_id == calendar.id
    assert participant.name == "Jack"
    assert participant.created


def test_create_participant_with_short_name(db: Session, test_client: TestClient,
                                            calendar: Calendar):
    response = test_client.post("/participants/",
                                json={"calendar_id": str(calendar.id), "name": ""})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{
            "loc": ["body", "participant", "name"],
            "msg": "Name must be at least 3 characters long.",
            "type": "value_error",
        }]
    }


def test_delete_participant(db: Session, test_client: TestClient,
                            participant: Participant):
    assert db.query(Participant).count() == 1

    response = test_client.delete(f"/participants/{participant.id}/")

    assert response.status_code == 200
    assert db.query(Participant).count() == 0


def test_delete_inexistant_participant(test_client: TestClient):
    random_uuid = uuid.uuid4()
    response = test_client.delete(f"/participants/{random_uuid}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found."}


def test_update_participant(db: Session, test_client: TestClient, calendar: Calendar,
                            participant: Participant):
    response = test_client.patch(f"/participants/{participant.id}/",
                                 json={"name": "John"})

    assert response.status_code == 200

    participant = db.query(Participant).one()
    assert participant.name == "John"

    data = response.json()
    assert data.keys() == {"id", "calendar_id", "name", "created"}
    assert data["id"] is not None
    assert data["calendar_id"] == str(calendar.id)
    assert data["name"] == "John"
    assert data["created"] is not None


def test_update_inexistant_participant(test_client: TestClient):
    random_uuid = uuid.uuid4()
    response = test_client.patch(f"/participants/{random_uuid}/",
                                 json={"name": "John"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found."}


def test_get_entries(db: Session, test_client: TestClient, calendar: Calendar,
                     entries: List[Entry]):
    response = test_client.get("/entries/", params={"calendar_id": calendar.id})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    assert data[0].keys() == {"id", "calendar_id", "timestamp", "created"}
    assert data[0]["id"] == str(entries[0].id)
    assert data[0]["calendar_id"] == str(entries[0].calendar_id)
    assert data[0]["timestamp"] == entries[0].timestamp.isoformat()
    assert data[0]["created"] == entries[0].created.isoformat()

    assert data[1].keys() == {"id", "calendar_id", "timestamp", "created"}
    assert data[1]["id"] == str(entries[1].id)
    assert data[1]["calendar_id"] == str(entries[1].calendar_id)
    assert data[1]["timestamp"] == entries[1].timestamp.isoformat()
    assert data[1]["created"] == entries[1].created.isoformat()


def test_create_entry(db: Session, test_client: TestClient, calendar: Calendar):
    assert db.query(Entry).count() == 0

    response = test_client.post("/entries/", json={"calendar_id": str(calendar.id),
                                                   "timestamp": "2020-05-18 10:30:00"})

    assert response.status_code == 200

    data = response.json()

    assert data.keys() == {"id", "calendar_id", "timestamp", "created"}
    assert data["id"] is not None
    assert data["calendar_id"] == str(calendar.id)
    assert data["timestamp"] == "2020-05-18T10:30:00"
    assert data["created"] is not None


def test_delete_entry(db: Session, test_client: TestClient, entry: Entry):
    assert db.query(Entry).count() == 1

    response = test_client.delete(f"/entries/{entry.id}/")

    assert response.status_code == 200
    assert db.query(Entry).count() == 0


def test_delete_inexistant_entry(test_client: TestClient):
    random_uuid = uuid.uuid4()
    response = test_client.delete(f"/entries/{random_uuid}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Entry not found."}


def test_update_entry(db: Session, test_client: TestClient, calendar: Calendar,
                      entry: Entry):
    response = test_client.patch(f"/entries/{entry.id}/",
                                 json={"timestamp": "2020-12-22 09:25:00"})

    assert response.status_code == 200

    entry = db.query(Entry).one()
    assert entry.timestamp == datetime(2020, 12, 22, 9, 25, 0)

    data = response.json()
    assert data.keys() == {"id", "calendar_id", "timestamp", "created"}
    assert data["id"] is not None
    assert data["calendar_id"] == str(calendar.id)
    assert data["timestamp"] == "2020-12-22T09:25:00"
    assert data["created"] is not None


def test_update_inexistant_entry(test_client: TestClient):
    random_uuid = uuid.uuid4()
    response = test_client.patch(f"/entries/{random_uuid}/",
                                 json={"timestamp": "2020-12-22 09:25:00"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Entry not found."}


def test_create_participation(db: Session, test_client: TestClient, calendar: Calendar,
                              entry: Entry, participant: Participant):
    response = test_client.post(
        "/participations/",
        json={"calendar_id": str(calendar.id),
              "entry_id": str(entry.id),
              "participant_id": str(participant.id)}
    )

    assert response.status_code == 200
    assert response.json() == {}

    participation = db.query(Participation).one()
    assert participation.calendar_id == calendar.id
    assert participation.entry_id == entry.id
    assert participation.participant_id == participant.id
    assert participation.created is not None


def test_delete_participation(db: Session, test_client: TestClient,
                              participation: Participation):
    assert db.query(Participation).count() == 1

    response = test_client.delete(f"/participations/{participation.id}/")

    assert response.status_code == 200
    assert db.query(Participation).count() == 0


def test_delete_inexistant_participation(test_client: TestClient):
    random_uuid = uuid.uuid4()
    response = test_client.delete(f"/participations/{random_uuid}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Participation not found."}
