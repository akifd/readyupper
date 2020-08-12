import uuid
from datetime import datetime
from typing import List

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from readyupper import operations
from readyupper.models import Calendar, Entry, Participant, Participation


def test_get_calendar(db: Session, calendar: Calendar):
    found = operations.get_calendar(db, calendar_id=calendar.id)

    assert isinstance(calendar, Calendar)
    assert found.id == calendar.id


def test_get_non_existant_calendar(db: Session, calendar: Calendar):
    with pytest.raises(NoResultFound):
        operations.get_calendar(db, calendar_id=uuid.uuid4())


def test_create_calendar(db: Session):
    assert db.query(Calendar).count() == 0

    calendar = operations.create_calendar(db, name="New calendar")

    assert db.query(Calendar).count() == 1
    assert calendar.id
    assert calendar.name == "New calendar"
    assert calendar.created


def test_create_calendar_without_name(db: Session):
    with pytest.raises(ValueError):
        operations.create_calendar(db, name="")


def test_delete_calendar(db: Session, calendar: Calendar):
    assert db.query(Calendar).count() == 1
    operations.delete_calendar(db, calendar)
    assert db.query(Calendar).count() == 0


def test_get_participant(db: Session, participant: Participant):
    found = operations.get_participant(db, participant_id=participant.id)

    assert isinstance(found, Participant)
    assert found.id == participant.id


def test_get_participants(db: Session, calendar: Calendar,
                          participants: List[Participant]):
    results = operations.get_participants(db, calendar.id)

    assert results[0].id == participants[0].id
    assert results[0].calendar_id == participants[0].calendar_id
    assert results[0].name == participants[0].name
    assert results[0].created == participants[0].created
    assert results[1].id == participants[1].id
    assert results[1].calendar_id == participants[1].calendar_id
    assert results[1].name == participants[1].name
    assert results[1].created == participants[1].created


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


def test_update_participant(db: Session, participant: Participant):
    operations.update_participant(db, participant, "John")

    participant = db.query(Participant).one()
    assert participant.name == "John"


def test_get_entries(db: Session, calendar: Calendar, entries: List[Entry]):
    results = operations.get_entries(db, calendar.id)

    assert results[0].id == entries[0].id
    assert results[0].calendar_id == entries[0].calendar_id
    assert results[0].timestamp == entries[0].timestamp
    assert results[0].created == entries[0].created
    assert results[1].id == entries[1].id
    assert results[1].calendar_id == entries[1].calendar_id
    assert results[1].timestamp == entries[1].timestamp
    assert results[1].created == entries[1].created


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


def test_get_participations_not_existing(db: Session, calendar: Calendar, entry: Entry,
                                         participant: Participant):
    participations = operations.get_participations(db, calendar.id, entry.id,
                                                   participant.id)
    assert participations == []


def test_get_participations(db: Session, calendar: Calendar, entry: Entry,
                            participant: Participant, participation: Participation):
    participations = operations.get_participations(db, calendar.id, entry.id,
                                                   participant.id)
    assert participations == [participation]


def test_create_participation(db: Session, calendar: Calendar, entry: Entry,
                              participant: Participant):
    operations.create_participation(db, calendar.id, entry.id, participant.id)

    participation = db.query(Participation).one()
    assert participation.calendar_id == calendar.id
    assert participation.entry_id == entry.id
    assert participation.participant_id == participant.id


def test_delete_participation(db: Session, participation: Participation):
    assert db.query(Participation).count() == 1
    operations.delete_participation(db, participation)
    assert db.query(Participation).count() == 0
