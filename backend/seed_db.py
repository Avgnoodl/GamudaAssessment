from datetime import datetime

from database import SessionLocal, create_tables, drop_tables
from models import Match, MatchEvent


def seed():
    """Reset the database and insert mock match data."""
    drop_tables()
    create_tables()

    db = SessionLocal()
    try:
        match1 = Match(
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
        )
        match2 = Match(
            league="La Liga",
            home_team="Barcelona",
            away_team="Real Madrid",
            home_score=0,
            away_score=0,
            kickoff_time=datetime(2024, 10, 27, 18, 0),
            status="scheduled",
            events=[],
        )

        db.add_all([match1, match2])
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Database seeded with mock data.")
