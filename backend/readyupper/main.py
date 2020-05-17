from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from . import operations, schemas
from .database import Session as SessionLocal
from .models import Entry, Participation


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    try:
        db = SessionLocal()
        yield db
        db.commit()
    finally:
        db.close()


# TODO: Change to /calendars/{calendar_id}/.
@app.get("/calendar/{calendar_id}/", response_model=schemas.Calendar)
def get_calendar(calendar_id: UUID, db: Session = Depends(get_db)):
    try:
        return operations.get_calendar(db, calendar_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Calendar not found.")


# TODO: Change to /calendars/.
@app.post("/calendar/", response_model=schemas.Calendar)
def create_calendar(calendar: schemas.CalendarCreate, db: Session = Depends(get_db)):
    return operations.create_calendar(db, calendar.name)


@app.delete("/calendars/{calendar_id}/")
def delete_calendar(calendar_id: UUID, db: Session = Depends(get_db)):
    try:
        calendar = operations.get_calendar(db, calendar_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Calendar not found.")

    operations.delete_calendar(db, calendar)


@app.post("/participants/", response_model=schemas.Participant)
def create_participant(participant: schemas.ParticipantCreate,
                       db: Session = Depends(get_db)):
    return operations.create_participant(db, participant.calendar_id, participant.name)


@app.delete("/participants/{participant_id}/")
def delete_participant(participant_id: UUID, db: Session = Depends(get_db)):
    try:
        participant = operations.get_participant(db, participant_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Participant not found.")

    operations.delete_participant(db, participant)


@app.patch("/participants/{participant_id}/", response_model=schemas.Participant)
def update_participant(participant_id: UUID, data: schemas.ParticipantUpdate,
                       db: Session = Depends(get_db)):
    try:
        participant = operations.get_participant(db, participant_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Participant not found.")

    return operations.update_participant(db, participant, name=data.name)


@app.post("/entries/", response_model=schemas.Entry)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    return operations.create_entry(db, entry.calendar_id, entry.timestamp)


@app.delete("/entries/{entry_id}/")
def delete_entry(entry_id: UUID, db: Session = Depends(get_db)):
    try:
        entry = db.query(Entry).filter(Entry.id == entry_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Entry not found.")

    operations.delete_entry(db, entry)


@app.patch("/entries/{entry_id}/", response_model=schemas.Entry)
def update_entry(entry_id: UUID, data: schemas.EntryUpdate,
                 db: Session = Depends(get_db)):
    try:
        entry = db.query(Entry).filter(Entry.id == entry_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Entry not found.")

    return operations.update_entry(db, entry, data.timestamp)


@app.post("/participations/")
def create_participation(data: schemas.ParticipationCreate,
                         db: Session = Depends(get_db)):
    operations.create_participation(db, data.calendar_id, data.entry_id,
                                    data.participant_id)
    return {}


@app.delete("/participations/{participation_id}/")
def delete_participation(participation_id: UUID, db: Session = Depends(get_db)):
    try:
        participation = db.query(Participation) \
            .filter(Participation.id == participation_id) \
            .one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Participation not found.")

    operations.delete_entry(db, participation)
