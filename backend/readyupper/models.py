from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class Calendar(Base):
    __tablename__ = "calendars"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url_hash = Column(String(32), nullable=False, unique=True)
    created = Column(DateTime, nullable=False, server_default="NOW()")
