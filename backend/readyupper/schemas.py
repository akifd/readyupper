from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class Calendar(BaseModel):
    id: UUID
    name: str
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
    id: UUID
    calendar_id: UUID
    name: str
    created: datetime = datetime.now

    class Config:
        orm_mode = True


class ParticipantCreate(BaseModel):
    calendar_id: UUID
    name: str

    @validator("name")
    def name_minimum_length(cls, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long.")

        return value

    class Config:
        orm_mode = True


class ParticipantUpdate(BaseModel):
    name: str

    @validator("name")
    def name_minimum_length(cls, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long.")

        return value

    class Config:
        orm_mode = True


class Entry(BaseModel):
    id: UUID
    calendar_id: UUID
    timestamp: datetime
    created: datetime = datetime.now

    class Config:
        orm_mode = True


class EntryCreate(BaseModel):
    calendar_id: UUID
    timestamp: datetime

    class Config:
        orm_mode = True


class EntryUpdate(BaseModel):
    timestamp: datetime

    class Config:
        orm_mode = True


class ParticipationCreate(BaseModel):
    calendar_id: UUID
    entry_id: UUID
    participant_id: UUID

    class Config:
        orm_mode = True
