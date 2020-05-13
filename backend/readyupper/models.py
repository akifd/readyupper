import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class Calendar(Base):
    __tablename__ = "calendars"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,
                nullable=False)
    name = Column(String(255), nullable=False)
    created = Column(DateTime, nullable=False, server_default=func.now())

    participants = relationship("Participant", order_by=lambda: Participant.id,
                                back_populates="calendar",
                                cascade="all, delete, delete-orphan")
    entries = relationship("Entry", order_by=lambda: Entry.id,
                           back_populates="calendar",
                           cascade="all, delete, delete-orphan")


class Entry(Base):
    __tablename__ = "entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,
                nullable=False)
    calendar_id = Column(UUID(as_uuid=True), ForeignKey("calendars.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created = Column(DateTime, nullable=False, server_default=func.now())

    calendar = relationship("Calendar", back_populates="entries")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,
                nullable=False)
    calendar_id = Column(UUID(as_uuid=True), ForeignKey("calendars.id"), nullable=False)
    name = Column(String(255), nullable=False)
    created = Column(DateTime, nullable=False, server_default=func.now())

    calendar = relationship("Calendar", back_populates="participants")
