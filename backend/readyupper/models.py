from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class Calendar(Base):
    __tablename__ = "calendars"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url_hash = Column(String(32), nullable=False, unique=True)
    created = Column(DateTime, nullable=False, server_default=func.now())

    participants = relationship("Participant", order_by=lambda: Participant.id,
                                back_populates="calendar",
                                cascade="all, delete, delete-orphan")
    entries = relationship("Entry", order_by=lambda: Entry.id,
                           back_populates="calendar",
                           cascade="all, delete, delete-orphan")


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created = Column(DateTime, nullable=False, server_default=func.now())

    calendar = relationship("Calendar", back_populates="entries")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
    name = Column(String(255), nullable=False)
    created = Column(DateTime, nullable=False, server_default=func.now())

    calendar = relationship("Calendar", back_populates="participants")
