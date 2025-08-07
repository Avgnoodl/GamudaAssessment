from datetime import datetime, timezone
from typing import List
import random   

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session, selectinload

from database import get_db
from models import Match as DBMatch, MatchEvent as DBMatchEvent  # ← rename alias

FrontendTestMode: bool = False  # Set to True for testing with mock data
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatchEventSchema(BaseModel):
    minute: int
    team: str
    player: str
    type: str
    sub_in: str | None = None
    class Config:
        orm_mode = True


class MatchSchema(BaseModel): 
    id: int
    league: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    kickoff_time: datetime
    status: str
    events: List[MatchEventSchema] = []

    class Config:
        orm_mode = True

MOCK_MATCHES: List[MatchSchema] = []

def _ensure_aware(dt: datetime) -> datetime:
    """
    Guarantee a UTC-aware datetime.

    • If `dt` already has tzinfo → convert to UTC.
    • If `dt` is naïve → assume it’s stored in UTC and attach tzinfo.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def current_minute(kickoff_time: datetime) -> int:
    """Return 0-90 based on UTC time, tolerant of naïve/aware mix."""
    delta = datetime.now(timezone.utc) - kickoff_time.astimezone(timezone.utc)
    return max(0, min(int(delta.total_seconds() // 60), 90))


EVENT_TYPES = ["goal", "yellow_card", "substitution"]

def maybe_add_event(match: DBMatch, db: Session) -> None:
    """
    30 % chance to create a random event and, if it’s a goal, bump the score.
    Called every time the frontend polls /api/matches.
    """
    # Only live games simulate
    if match.status != "live":
        return

    # Stop at 90'
    if current_minute(match.kickoff_time) >= 90:
        match.status = "finished"
        return

    # RNG: 70 % of the time we do nothing
    if random.random() > 0.50:  # 2 % chance to add an event at every polling event
        return

    evt_type = random.choice(EVENT_TYPES)

    # Avoid None if you forgot to seed players
    home_players = match.home_players or []
    away_players = match.away_players or []
    all_players  = home_players + away_players or ["Unknown"]

    player_out = random.choice(all_players)

    evt = DBMatchEvent(
        match_id=match.id,
        minute=current_minute(match.kickoff_time),
        team=match.home_team if player_out in home_players else match.away_team,
        player=player_out,
        type=evt_type,
        sub_in=random.choice(all_players) if evt_type == "substitution" else None,
    )
    match.events.append(evt)     # cascades, and match.events now contains it

    # Adjust score if it was a goal
    if evt_type == "goal":
        if player_out in home_players:
            match.home_score += 1
        else:
            match.away_score += 1


@app.get("/api/matches", response_model=List[MatchSchema])
def list_matches(db: Session = Depends(get_db)) -> List[MatchSchema]:
    """Return all matches, simulating live ones on-the-fly."""
    if FrontendTestMode:
        return MOCK_MATCHES

    matches: List[DBMatch] = (
        db.query(DBMatch)
        .options(selectinload(DBMatch.events))
        .all()
    )

    # 🔥 simulate for each live match
    for m in matches:
        maybe_add_event(m, db)

    db.commit()   # persist new events / score changes

    return matches     # thanks to orm_mode, Pydantic handles conversion


@app.get("/api/matches/{match_id}", response_model=MatchSchema)
def get_match(match_id: int, db: Session = Depends(get_db)) -> MatchSchema:
    """Return a single match by its identifier."""
    if FrontendTestMode:
        for match in MOCK_MATCHES:
            if match.id == match_id:
                return match
        raise HTTPException(status_code=404, detail="Match not found")
    match = (
        db.query(DBMatch)
        .options(selectinload(DBMatch.events))
        .filter(DBMatch.id == match_id)
        .first()
    )
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

