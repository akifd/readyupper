import json

from readyupper import schemas, models


def test_view_read_calendar(test_client, calendar):
    response = test_client.get(f"/calendar/{calendar.url_hash}/")

    assert response.status_code == 200
    data = response.json()
    assert data.keys() == {"id", "name", "url_hash", "created"}
    assert data == json.loads(schemas.Calendar(**data).json())


def test_view_create_calendar(test_client, db):
    assert db.query(models.Calendar).count() == 0

    response = test_client.post("/calendar/", json={"name": "New calendar"})

    assert response.status_code == 200

    data = response.json()
    assert data.keys() == {"id", "name", "url_hash", "created"}
    assert data == json.loads(schemas.Calendar(**data).json())

    assert db.query(models.Calendar).count() == 1
    calendar = db.query(models.Calendar).one()
    assert calendar.name == "New calendar"
    assert calendar.url_hash
    assert calendar.created


def test_view_create_calendar_with_short_name(test_client, db):
    response = test_client.post("/calendar/", json={"name": "AB"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{
            "loc": ["body", "calendar", "name"],
            "msg": "Name must be at least 3 characters long.",
            "type": "value_error",
        }]
    }


def test_view_set_participants(test_client, db, calendar):
    assert db.query(models.Participant).count() == 0

    response = test_client.post(f"/calendar/{calendar.id}/participants/",
                                json=["Jack", "John"])

    assert response.status_code == 200

    data = response.json()

    assert data[0].keys() == {"id", "calendar_id", "name", "created"}
    assert data[0]["id"] is not None
    assert data[0]["calendar_id"] == calendar.id
    assert data[0]["name"] == "Jack"
    assert data[0]["created"] is not None

    assert data[1].keys() == {"id", "calendar_id", "name", "created"}
    assert data[1]["id"] is not None
    assert data[1]["calendar_id"] == calendar.id
    assert data[1]["name"] == "John"
    assert data[1]["created"] is not None


def test_view_create_entry(test_client, db, calendar):
    assert db.query(models.Entry).count() == 0

    response = test_client.post(f"/calendar/{calendar.id}/entries/",
                                json={"timestamp": "2020-05-18 10:30:00"})

    assert response.status_code == 200

    data = response.json()

    assert data.keys() == {"id", "calendar_id", "timestamp", "created"}
    assert data["id"] is not None
    assert data["calendar_id"] == calendar.id
    assert data["timestamp"] == "2020-05-18T10:30:00"
    assert data["created"] is not None
