from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    league = Column(String, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_score = Column(Integer, nullable=False)
    away_score = Column(Integer, nullable=False)
    kickoff_time = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    events = relationship("MatchEvent", back_populates="match", cascade="all, delete-orphan")


class MatchEvent(Base):
    __tablename__ = "match_events"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    minute = Column(Integer, nullable=False)
    team = Column(String, nullable=False)
    player = Column(String, nullable=False)
    type = Column(String, nullable=False)

    match = relationship("Match", back_populates="events")
