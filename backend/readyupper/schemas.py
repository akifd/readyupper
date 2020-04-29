from datetime import datetime
from pydantic import BaseModel


class Calendar(BaseModel):
    id: int
    name: str
    url_hash: str
    created: datetime = datetime.now

    class Config:
        orm_mode = True


class CalendarCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True
