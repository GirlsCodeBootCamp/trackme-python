from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

user_tracker = Table(
    "user_tracker",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("tracker_id", ForeignKey("trackers.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)

    trackers = relationship("Tracker", secondary=user_tracker, back_populates="owners")


class Tracker(Base):
    __tablename__ = "trackers"

    id = Column(Integer, primary_key=True, index=True)
    url_address = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted = Column(Boolean, default=False)
    content = Column(String)

    owners = relationship("User", secondary=user_tracker, back_populates="trackers")
