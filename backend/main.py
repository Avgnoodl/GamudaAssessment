from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session, selectinload

from database import get_db
from models import Match as DBMatch


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatchEvent(BaseModel):
    minute: int
    team: str
    player: str
    type: str

    class Config:
        orm_mode = True


class Match(BaseModel):
    id: int
    league: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    kickoff_time: datetime
    status: str
    events: List[MatchEvent] = []

    class Config:
        orm_mode = True


@app.get("/api/matches", response_model=List[Match])
def list_matches(db: Session = Depends(get_db)) -> List[DBMatch]:
    """Return all available matches."""
    return db.query(DBMatch).options(selectinload(DBMatch.events)).all()


@app.get("/api/matches/{match_id}", response_model=Match)
def get_match(match_id: int, db: Session = Depends(get_db)) -> DBMatch:
    """Return a single match by its identifier."""
    match = (
        db.query(DBMatch)
        .options(selectinload(DBMatch.events))
        .filter(DBMatch.id == match_id)
        .first()
    )
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

