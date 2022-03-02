from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, func

from .database import Base, Table

user_tracker = Table("user_tracker", Base.metadata,
                       Column("user_id", ForeignKey("users.id"), primary_key=True),
                       Column("tracker_id", ForeignKey("trackers.id"), primary_key=True))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)

    trackers = relationship("Tracker", secondary=user_tracker, back_populates="owners")


class Tracker(Base):
    __tablename__ = "trackers"

    id = Column(Integer, primary_key=True, index=True)
    url_address = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_offer = Column(Boolean)
    deleted = Column(Boolean, default=False)
    
    owners = relationship("User", secondary=user_tracker, back_populates="trackers")

