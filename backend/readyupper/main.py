from typing import List

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import schemas, operations, models
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


@app.get("/calendar/{url_hash}/", response_model=schemas.Calendar)
def read_calendar(url_hash: str, db: Session = Depends(get_db)):
    return operations.get_calendar_by_hash(db, url_hash)


@app.post("/calendar/", response_model=schemas.Calendar)
def create_calendar(calendar: schemas.CalendarCreate, db: Session = Depends(get_db)):
    return operations.create_calendar(db, calendar.name)


@app.post("/calendar/{calendar_id}/participants/",
          response_model=List[schemas.Participant])
def set_participants(calendar_id: int, participants: List[str],
                     db: Session = Depends(get_db)):
    calendar = db.query(models.Calendar).filter(models.Calendar.id == calendar_id).one()
    return operations.set_participants(db, calendar, participants)


@app.post("/entries/", response_model=schemas.Entry)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    return operations.create_entry(db, entry.calendar_id, entry.timestamp)


@app.delete("/entries/{entry_id}/")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.Entry).one()
    operations.delete_entry(db, entry)
