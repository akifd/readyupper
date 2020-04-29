from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import schemas, operations
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
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/calendar/{url_hash}/", response_model=schemas.Calendar)
def read_calendar(url_hash: str, db: Session = Depends(get_db)):
    return operations.get_calendar_by_hash(db, url_hash)


@app.post("/calendar/", response_model=schemas.Calendar)
def create_calendar(calendar: schemas.CalendarCreate, db: Session = Depends(get_db)):
    return operations.create_calendar(db, calendar.name)
