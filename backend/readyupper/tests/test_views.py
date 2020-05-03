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
