from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@app.get("/api/matches", response_model=List[Match])
def list_matches() -> List[Match]:
    """Return all available matches."""
    return MOCK_MATCHES


@app.get("/api/matches/{match_id}", response_model=Match)
def get_match(match_id: int) -> Match:
    """Return a single match by its identifier."""
    for match in MOCK_MATCHES:
        if match.id == match_id:
            return match
    raise HTTPException(status_code=404, detail="Match not found")
