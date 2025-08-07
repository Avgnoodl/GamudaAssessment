from datetime import datetime
import asyncio
import random
from typing import List

from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session, selectinload

from apscheduler.schedulers.background import BackgroundScheduler

from database import get_db, SessionLocal
from models import Match as DBMatch, MatchEvent as DBMatchEvent

FrontendTestMode: bool = False  # Set to True for testing with mock data
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
    sub_in: str | None = None
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
    current_minute: int | None = None

    class Config:
        orm_mode = True

MOCK_MATCHES: List[Match] = [
    Match(
        id=1,
        league="Premier League",
        home_team="Arsenal",
        away_team="Chelsea",
        home_score=2,
        away_score=1,
        kickoff_time=datetime(2024, 10, 26, 15, 0),
        status="live",
        events=[
            MatchEvent(minute=23, team="Arsenal", player="Saka", type="goal"),
            MatchEvent(minute=45, team="Chelsea", player="Sterling", type="goal"),
            MatchEvent(minute=70, team="Arsenal", player="Martinelli", type="goal"),
        ],
    ),
    Match(
        id=2,
        league="La Liga",
        home_team="Barcelona",
        away_team="Real Madrid",
        home_score=0,
        away_score=0,
        kickoff_time=datetime(2024, 10, 27, 18, 0),
        status="scheduled",
        events=[],
    ),
]

def compute_current_minute(match: DBMatch) -> int | None:
    """Return the current minute for a live match."""
    if match.status != "live":
        return None
    diff = datetime.utcnow() - match.kickoff_time
    minute = int(diff.total_seconds() // 60)
    return max(0, min(90, minute))


def to_schema(db_match: DBMatch) -> Match:
    match = Match.from_orm(db_match)
    match.current_minute = compute_current_minute(db_match)
    return match


def get_matches(db: Session) -> List[Match]:
    db_matches = db.query(DBMatch).options(selectinload(DBMatch.events)).all()
    return [to_schema(m) for m in db_matches]


@app.get("/api/matches", response_model=List[Match])
def list_matches(db: Session = Depends(get_db)) -> List[Match]:
    """Return all available matches."""
    if FrontendTestMode:
        return MOCK_MATCHES
    return get_matches(db)


@app.get("/api/matches/{match_id}", response_model=Match)
def get_match(match_id: int, db: Session = Depends(get_db)) -> Match:
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
    return to_schema(match)


def simulate_events() -> None:
    """Randomly insert events for live matches."""
    db = SessionLocal()
    try:
        live_matches = db.query(DBMatch).filter(DBMatch.status == "live").all()
        for match in live_matches:
            current_minute = compute_current_minute(match)
            if current_minute is None or current_minute >= 90:
                continue
            if random.random() >= 0.3:
                continue
            event_type = random.choice(["goal", "yellow_card", "substitution"])
            team_choice = random.choice(["home", "away"])
            team_name = match.home_team if team_choice == "home" else match.away_team
            player_out = f"Player {random.randint(1,99)}"
            if event_type == "goal":
                if team_choice == "home":
                    match.home_score += 1
                else:
                    match.away_score += 1
                event = DBMatchEvent(
                    match_id=match.id,
                    minute=current_minute,
                    team=team_name,
                    player=player_out,
                    type="goal",
                )
            elif event_type == "yellow_card":
                event = DBMatchEvent(
                    match_id=match.id,
                    minute=current_minute,
                    team=team_name,
                    player=player_out,
                    type="yellow_card",
                )
            else:  # substitution
                player_in = f"Player {random.randint(100,199)}"
                event = DBMatchEvent(
                    match_id=match.id,
                    minute=current_minute,
                    team=team_name,
                    player=player_out,
                    type="substitution",
                    sub_in=player_in,
                )
            db.add(event)
        db.commit()
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(simulate_events, "interval", seconds=10)


@app.on_event("startup")
def start_scheduler() -> None:
    scheduler.start()


@app.websocket("/ws/matches")
async def ws_matches(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            with SessionLocal() as db:
                matches = get_matches(db)
            await websocket.send_json([m.dict() for m in matches])
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass

