from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from .models import Calendar, Entry, Participant, Participation


def get_calendar(db: Session, calendar_id: UUID) -> Calendar:
    return db.query(Calendar).filter(Calendar.id == calendar_id).one()


def create_calendar(db: Session, name: str) -> Calendar:
    if len(name) < 3:
        raise ValueError("Calendar name must be at least 3 characters long.")

    db_calendar = Calendar(name=name)
    db.add(db_calendar)
    db.flush()
    return db_calendar


def delete_calendar(db: Session, calendar: Calendar) -> None:
    db.delete(calendar)
    db.flush()


def get_participant(db: Session, participant_id: UUID) -> Participant:
    return db.query(Participant) \
        .filter(Participant.id == participant_id) \
        .one()


def create_participant(db: Session, calendar_id: UUID, name: str) -> Participant:
    participant = Participant(calendar_id=calendar_id, name=name)

    db.add(participant)
    db.flush()

    return participant


def delete_participant(db: Session, participant: Participant) -> None:
    db.delete(participant)
    db.flush()


def update_participant(db: Session, participant: Participant, name: str) -> Participant:
    participant.name = name
    db.flush()
    return participant


def create_entry(db: Session, calendar_id: UUID, timestamp) -> Entry:
    entry = Entry(calendar_id=calendar_id, timestamp=timestamp)

    db.add(entry)
    db.flush()

    return entry


def delete_entry(db: Session, entry: Entry) -> None:
    db.delete(entry)
    db.flush()


def update_entry(db: Session, entry: Entry, timestamp: datetime) -> Entry:
    entry.timestamp = timestamp
    db.flush()
    return entry


def create_participation(db: Session, calendar_id: UUID, entry_id: UUID,
                         participant_id: UUID) -> Participation:
    participation = Participation(calendar_id=calendar_id, entry_id=entry_id,
                                  participant_id=participant_id)

    db.add(participation)
    db.flush()

    return participation


def delete_participation(db: Session, participation: Participation) -> None:
    db.delete(participation)
    db.flush()
