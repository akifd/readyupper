from datetime import datetime
from pydantic import BaseModel, validator


class Calendar(BaseModel):
    id: int
    name: str
    url_hash: str
    created: datetime = datetime.now

    class Config:
        orm_mode = True


class CalendarCreate(BaseModel):
    name: str

    @validator("name")
    def name_minimum_length(cls, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long.")

        return value

    class Config:
        orm_mode = True


class Participant(BaseModel):
    id: int
    calendar_id: int
    name: str
    created: datetime = datetime.now

    class Config:
        orm_mode = True


class Entry(BaseModel):
    id: int
    calendar_id: int
    timestamp: datetime
    created: datetime = datetime.now

    class Config:
        orm_mode = True


class EntryCreate(BaseModel):
    calendar_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
