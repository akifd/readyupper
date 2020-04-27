from pydantic import BaseModel


class Calendar(BaseModel):
    id: int
    name: str
    url_hash: str
    password: str = ""

    class Config:
        orm_mode = True


class CalendarCreate(BaseModel):
    name: str
    url_hash: str
    password: str = ""

    class Config:
        orm_mode = True
