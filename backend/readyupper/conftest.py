from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models
from .database import DATABASE_SETTINGS, Base, database_url
from .main import app, get_db


@pytest.fixture(scope="session")
def engine():
    # Create the test engine.
    TEST_DATABASE_SETTINGS = DATABASE_SETTINGS.copy()
    TEST_DATABASE_SETTINGS["NAME"] = "test_" + DATABASE_SETTINGS["NAME"]
    TEST_DATABASE_URL = database_url(**TEST_DATABASE_SETTINGS)

    test_engine = create_engine(TEST_DATABASE_URL)

    # Create tables.
    Base.metadata.create_all(test_engine)

    yield test_engine

    # Drop tables.
    Base.metadata.drop_all(test_engine)


@pytest.fixture(scope="session")
def session_maker(engine):
    return sessionmaker(bind=engine)


@pytest.fixture(scope="session")
def session(session_maker):
    session = session_maker()
    yield session
    session.close()


@pytest.fixture
def db(session):
    yield session
    session.rollback()


@pytest.fixture
def test_client(db, mocker):
    def get_test_db():
        yield db

    app.dependency_overrides[get_db] = get_test_db

    return TestClient(app)


@pytest.fixture
def calendar(db):
    calendar = models.Calendar(name="Test calendar")
    db.add(calendar)
    db.flush()
    return calendar


@pytest.fixture
def entry(db, calendar):
    entry = models.Entry(timestamp=datetime(2020, 10, 19, 14, 30, 0))
    calendar.entries = [entry]
    db.flush()
    return entry


@pytest.fixture
def entries(db, calendar):
    entries = [
        models.Entry(calendar_id=calendar.id,
                     timestamp=datetime(2020, 10, 19, 14, 30, 0)),
        models.Entry(calendar_id=calendar.id,
                     timestamp=datetime(2020, 10, 20, 12, 15, 0)),
    ]
    db.add_all(entries)
    db.flush()
    return entries


@pytest.fixture
def participant(db, calendar):
    participant = models.Participant(name="Jack")
    calendar.participants = [participant]
    db.flush()
    return participant


@pytest.fixture
def participants(db, calendar):
    participants = [
        models.Participant(calendar_id=calendar.id, name="Jack"),
        models.Participant(calendar_id=calendar.id, name="John"),
    ]
    db.add_all(participants)
    db.flush()
    return participants


@pytest.fixture
def participation(db, calendar, entry, participant):
    participation = models.Participation(calendar_id=calendar.id,
                                         entry_id=entry.id,
                                         participant_id=participant.id)
    db.add(participation)
    db.flush()
    return participation
