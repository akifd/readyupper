from uuid import UUID

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import schemas, operations
from .models import Entry, Participant
from .database import Session as SessionLocal


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


@app.get("/calendar/{calendar_id}/", response_model=schemas.Calendar)
def read_calendar(calendar_id: UUID, db: Session = Depends(get_db)):
    return operations.get_calendar(db, calendar_id)


@app.post("/calendar/", response_model=schemas.Calendar)
def create_calendar(calendar: schemas.CalendarCreate, db: Session = Depends(get_db)):
    return operations.create_calendar(db, calendar.name)


@app.post("/participants/", response_model=schemas.Participant)
def create_participant(participant: schemas.ParticipantCreate,
                       db: Session = Depends(get_db)):
    return operations.create_participant(db, participant.calendar_id, participant.name)


@app.delete("/participants/{participant_id}/")
def delete_participant(participant_id: UUID, db: Session = Depends(get_db)):
    participant = db.query(Participant) \
        .filter(Participant.id == participant_id) \
        .one()
    operations.delete_participant(db, participant)


@app.patch("/participants/{participant_id}/", response_model=schemas.Participant)
def update_participant(participant_id: UUID, data: schemas.ParticipantUpdate,
                       db: Session = Depends(get_db)):
    participant = db.query(Participant) \
        .filter(Participant.id == participant_id) \
        .one()
    return operations.update_participant(db, participant, name=data.name)


@app.post("/entries/", response_model=schemas.Entry)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    return operations.create_entry(db, entry.calendar_id, entry.timestamp)


@app.delete("/entries/{entry_id}/")
def delete_entry(entry_id: UUID, db: Session = Depends(get_db)):
    entry = db.query(Entry).filter(Entry.id == entry_id).one()
    operations.delete_entry(db, entry)


@app.patch("/entries/{entry_id}/", response_model=schemas.Entry)
def update_entry(entry_id: UUID, data: schemas.EntryUpdate,
                 db: Session = Depends(get_db)):
    entry = db.query(Entry).filter(Entry.id == entry_id).one()
    return operations.update_entry(db, entry, data.timestamp)
