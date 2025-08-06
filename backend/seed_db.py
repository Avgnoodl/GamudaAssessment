# seed_db.py
from datetime import datetime

from database import SessionLocal, create_tables, drop_tables
from models import Match, MatchEvent


def seed() -> None:
    """Reset the database and insert extensive mock football data."""
    # Start fresh
    drop_tables()
    create_tables()

    db = SessionLocal()
    try:
        # ---------- Premier League ----------
        arsenal_vs_chelsea_live = Match(
            league="Premier League",
            home_team="Arsenal",
            away_team="Chelsea",
            home_score=2,
            away_score=1,
            kickoff_time=datetime(2024, 10, 26, 15, 0),
            status="live",
            events=[
                MatchEvent(minute=23, team="Arsenal", player="Bukayo Saka", type="goal"),
                MatchEvent(minute=45, team="Chelsea", player="Raheem Sterling", type="goal"),
                MatchEvent(minute=53, team="Arsenal", player="Declan Rice", type="yellow_card"),
                MatchEvent(minute=70, team="Arsenal", player="Gabriel Martinelli", type="goal"),
                MatchEvent(minute=75, team="Chelsea", player="Moisés Caicedo", type="substitution"),
            ],
        )
        man_city_vs_liverpool_finished = Match(
            league="Premier League",
            home_team="Manchester City",
            away_team="Liverpool",
            home_score=3,
            away_score=2,
            kickoff_time=datetime(2024, 10, 19, 17, 30),
            status="finished",
            events=[
                MatchEvent(minute=11, team="Manchester City", player="Erling Haaland", type="goal"),
                MatchEvent(minute=27, team="Liverpool", player="Darwin Núñez", type="goal"),
                MatchEvent(minute=42, team="Manchester City", player="Phil Foden", type="goal"),
                MatchEvent(minute=56, team="Liverpool", player="Mohamed Salah", type="goal"),
                MatchEvent(minute=89, team="Manchester City", player="Kevin De Bruyne", type="goal"),
            ],
        )

        # ---------- La Liga ----------
        barca_vs_madrid_scheduled = Match(
            league="La Liga",
            home_team="Barcelona",
            away_team="Real Madrid",
            home_score=0,
            away_score=0,
            kickoff_time=datetime(2024, 10, 27, 18, 0),
            status="scheduled",
            events=[],
        )
        sociedad_vs_atletico_finished = Match(
            league="La Liga",
            home_team="Real Sociedad",
            away_team="Atlético Madrid",
            home_score=1,
            away_score=1,
            kickoff_time=datetime(2024, 10, 20, 20, 0),
            status="finished",
            events=[
                MatchEvent(minute=5, team="Atlético Madrid", player="Álvaro Morata", type="goal"),
                MatchEvent(minute=61, team="Real Sociedad", player="Takefusa Kubo", type="goal"),
                MatchEvent(minute=75, team="Real Sociedad", player="Mikel Merino", type="yellow_card"),
            ],
        )

        # ---------- Serie A ----------
        inter_vs_milan_live = Match(
            league="Serie A",
            home_team="Inter",
            away_team="AC Milan",
            home_score=0,
            away_score=0,
            kickoff_time=datetime(2024, 10, 26, 21, 45),
            status="live",
            events=[
                MatchEvent(minute=14, team="Inter", player="Lautaro Martínez", type="yellow_card"),
                MatchEvent(minute=33, team="AC Milan", player="Rafael Leão", type="goal"),
            ],
        )
        juve_vs_roma_scheduled = Match(
            league="Serie A",
            home_team="Juventus",
            away_team="Roma",
            home_score=0,
            away_score=0,
            kickoff_time=datetime(2024, 11, 3, 20, 45),
            status="scheduled",
            events=[],
        )

        # ---------- Bundesliga ----------
        bayern_vs_dortmund_finished = Match(
            league="Bundesliga",
            home_team="Bayern Munich",
            away_team="Borussia Dortmund",
            home_score=4,
            away_score=2,
            kickoff_time=datetime(2024, 10, 18, 19, 30),
            status="finished",
            events=[
                MatchEvent(minute=7, team="Bayern Munich", player="Harry Kane", type="goal"),
                MatchEvent(minute=22, team="Borussia Dortmund", player="Marco Reus", type="goal"),
                MatchEvent(minute=35, team="Bayern Munich", player="Jamal Musiala", type="goal"),
                MatchEvent(minute=50, team="Bayern Munich", player="Kingsley Coman", type="goal"),
                MatchEvent(minute=78, team="Borussia Dortmund", player="Niclas Füllkrug", type="goal"),
                MatchEvent(minute=90, team="Bayern Munich", player="Thomas Müller", type="goal"),
            ],
        )
        leverkusen_vs_leipzig_live = Match(
            league="Bundesliga",
            home_team="Bayer Leverkusen",
            away_team="RB Leipzig",
            home_score=1,
            away_score=1,
            kickoff_time=datetime(2024, 10, 26, 21, 30),
            status="live",
            events=[
                MatchEvent(minute=17, team="RB Leipzig", player="Loïs Openda", type="goal"),
                MatchEvent(minute=44, team="Bayer Leverkusen", player="Florian Wirtz", type="goal"),
            ],
        )

        # ---------- Ligue 1 ----------
        psg_vs_marseille_finished = Match(
            league="Ligue 1",
            home_team="Paris Saint-Germain",
            away_team="Marseille",
            home_score=2,
            away_score=0,
            kickoff_time=datetime(2024, 10, 17, 21, 0),
            status="finished",
            events=[
                MatchEvent(minute=31, team="Paris Saint-Germain", player="Kylian Mbappé", type="goal"),
                MatchEvent(minute=61, team="Paris Saint-Germain", player="Ousmane Dembélé", type="goal"),
                MatchEvent(minute=75, team="Marseille", player="Jonathan Clauss", type="red_card"),
            ],
        )
        lyon_vs_nice_scheduled = Match(
            league="Ligue 1",
            home_team="Lyon",
            away_team="Nice",
            home_score=0,
            away_score=0,
            kickoff_time=datetime(2024, 11, 1, 20, 0),
            status="scheduled",
            events=[],
        )

        # ---------- Commit ----------
        db.add_all(
            [
                arsenal_vs_chelsea_live,
                man_city_vs_liverpool_finished,
                barca_vs_madrid_scheduled,
                sociedad_vs_atletico_finished,
                inter_vs_milan_live,
                juve_vs_roma_scheduled,
                bayern_vs_dortmund_finished,
                leverkusen_vs_leipzig_live,
                psg_vs_marseille_finished,
                lyon_vs_nice_scheduled,
            ]
        )
        db.commit()
        print("Database seeded with extended mock data.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
