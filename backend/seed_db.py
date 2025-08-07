from datetime import datetime, timedelta, timezone

from database import SessionLocal, create_tables, drop_tables
from models import Match, MatchEvent


def seed() -> None:
    """Reset the database and insert extensive mock football data with diverse events."""
    # Start fresh
    drop_tables()
    create_tables()

    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)   # aware datetime in UTC         # reference for dynamic kick-offs

        # ---------- Premier League ----------
        arsenal_vs_chelsea_live = Match(
            league="Premier League",
            home_team="Arsenal",
            away_team="Chelsea",
            home_score=2,
            away_score=1,
            kickoff_time=now - timedelta(minutes=15),   # 15’ gone
            status="live",
            home_players=[
                "Bukayo Saka", "Gabriel Jesus", "Martin Ødegaard",
                "Declan Rice", "Ben White", "Kai Havertz"
            ],
            away_players=[
                "Raheem Sterling", "Cole Palmer", "Enzo Fernández",
                "Reece James", "Ben Chilwell", "Moisés Caicedo"
            ],
            events=[
                MatchEvent(minute=5,  team="Chelsea",  player="Ben Chilwell",        type="corner"),
                MatchEvent(minute=8,  team="Arsenal",  player="William Saliba",      type="handball"),
                MatchEvent(minute=10, team="Chelsea",  player="Enzo Fernández",      type="offside"),
                
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
            home_players=["Erling Haaland", "Phil Foden", "Rodri"],
            away_players=["Mohamed Salah", "Darwin Núñez", "Trent Alexander-Arnold"],
            events=[
                MatchEvent(minute=5,  team="Manchester City", player="Rodri",              type="corner"),
                MatchEvent(minute=9,  team="Liverpool",       player="Trent Alexander-Arnold", type="throw_in"),
                MatchEvent(minute=11, team="Manchester City", player="Erling Haaland",     type="goal"),
                MatchEvent(minute=27, team="Liverpool",       player="Darwin Núñez",       type="goal"),
                MatchEvent(minute=30, team="Manchester City", player="Jack Grealish",      type="foul"),
                MatchEvent(minute=33, team="Liverpool",       player="Andrew Robertson",   type="handball"),
                MatchEvent(minute=42, team="Manchester City", player="Phil Foden",         type="goal"),
                MatchEvent(minute=47, team="Manchester City", player="Ibrahima Konaté",    type="own_goal"),
                MatchEvent(minute=56, team="Liverpool",       player="Mohamed Salah",      type="goal"),
                MatchEvent(minute=65, team="Manchester City", player="Rúben Dias",         type="var"),
                MatchEvent(minute=69, team="Liverpool",       player="Alisson Becker",     type="penalty_saved"),
                MatchEvent(minute=74, team="Liverpool",       player="Virgil van Dijk",    type="yellow_card"),
                MatchEvent(minute=77, team="Manchester City", player="Bernardo Silva",     type="injury"),
                MatchEvent(minute=82, team="Manchester City", player="Phil Foden", type="substitution", sub_in="Jérémy Doku"),
                MatchEvent(minute=89, team="Manchester City", player="Kevin De Bruyne",    type="goal"),
                MatchEvent(minute=90, team="Liverpool",       player="Darwin Núñez",       type="var_overturned"),
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
            home_players=["Robert Lewandowski", "Pedri", "Frenkie de Jong"],
            away_players=["Vinícius Júnior", "Jude Bellingham", "Luka Modrić"],
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
            home_players=["Takefusa Kubo", "Robin Le Normand"],
            away_players=["Álvaro Morata", "Antoine Griezmann"],
            events=[
                MatchEvent(minute=5,  team="Atlético Madrid", player="Álvaro Morata",     type="goal"),
                MatchEvent(minute=12, team="Real Sociedad",   player="Brais Méndez",      type="corner"),
                MatchEvent(minute=22, team="Atlético Madrid", player="Antoine Griezmann", type="free_kick"),
                MatchEvent(minute=48, team="Real Sociedad",   player="Robin Le Normand",  type="handball"),
                MatchEvent(minute=61, team="Real Sociedad",   player="Takefusa Kubo",     type="goal"),
                MatchEvent(minute=70, team="Atlético Madrid", player="José María Giménez",type="injury"),
                MatchEvent(minute=75, team="Real Sociedad",   player="Mikel Merino",      type="yellow_card"),
                MatchEvent(minute=79, team="Real Sociedad",   player="Takefusa Kubo",     type="substitution", sub_in="Umar Sadiq"),
            ],
        )

        # ---------- Serie A ----------
        inter_vs_milan_live = Match(
            league="Serie A",
            home_team="Inter",
            away_team="AC Milan",
            home_score=0,
            away_score=0,
            kickoff_time=now - timedelta(minutes=25),   # 25' gone
            status="live",
            home_players=["Lautaro Martínez", "Hakan Çalhanoğlu", "Federico Dimarco"],
            away_players=["Rafael Leão", "Theo Hernández", "Christian Pulisic"],
            events=[
                MatchEvent(minute=5,  team="Inter",   player="Federico Dimarco", type="corner"),
                MatchEvent(minute=14, team="Inter",   player="Lautaro Martínez", type="yellow_card"),
                MatchEvent(minute=22, team="AC Milan",player="Theo Hernández",   type="throw_in"),
               
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
            home_players=["Dušan Vlahović", "Federico Chiesa"],
            away_players=["Paulo Dybala", "Romelu Lukaku"],
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
            home_players=["Harry Kane", "Jamal Musiala"],
            away_players=["Marco Reus", "Niclas Füllkrug"],
            events=[
                MatchEvent(minute=3,  team="Bayern Munich",   player="Joshua Kimmich", type="free_kick"),
                MatchEvent(minute=7,  team="Bayern Munich",   player="Harry Kane",     type="goal"),
                MatchEvent(minute=16, team="Borussia Dortmund", player="Gregor Kobel", type="goal_kick"),
                MatchEvent(minute=20, team="Borussia Dortmund", player="Mats Hummels", type="yellow_card"),
                MatchEvent(minute=22, team="Borussia Dortmund", player="Marco Reus",   type="goal"),
                MatchEvent(minute=28, team="Bayern Munich",   player="Alphonso Davies",type="handball"),
                MatchEvent(minute=35, team="Bayern Munich",   player="Jamal Musiala",  type="goal"),
                MatchEvent(minute=45, team="Bayern Munich",   player="Julian Ryerson", type="own_goal"),
                MatchEvent(minute=50, team="Bayern Munich",   player="Kingsley Coman", type="goal"),
                MatchEvent(minute=59, team="Bayern Munich",   player="Leroy Sané",     type="injury"),
                MatchEvent(minute=63, team="Bayern Munich",   player="Joshua Kimmich", type="foul"),
                MatchEvent(minute=68, team="Borussia Dortmund", player="Niklas Süle",  type="penalty_saved"),
                MatchEvent(minute=70, team="Borussia Dortmund", player="Julian Brandt",type="substitution", sub_in="Karim Adeyemi"),
                MatchEvent(minute=78, team="Borussia Dortmund", player="Niclas Füllkrug", type="goal"),
                MatchEvent(minute=82, team="Bayern Munich",   player="Dayot Upamecano", type="var_overturned"),
                MatchEvent(minute=85, team="Borussia Dortmund", player="Marco Reus",   type="substitution", sub_in="Youssoufa Moukoko"),
                MatchEvent(minute=90, team="Bayern Munich",   player="Thomas Müller",  type="goal"),
            ],
        )

        leverkusen_vs_leipzig_live = Match(
            league="Bundesliga",
            home_team="Bayer Leverkusen",
            away_team="RB Leipzig",
            home_score=1,
            away_score=1,
            kickoff_time= now - timedelta(minutes=70),   # 15’ gone
            status="live",
            home_players=["Florian Wirtz", "Granit Xhaka"],
            away_players=["Loïs Openda", "Dani Olmo"],
            events=[
                MatchEvent(minute=7,  team="Bayer Leverkusen", player="Piero Hincapié", type="corner"),
                MatchEvent(minute=17, team="RB Leipzig",      player="Loïs Openda",    type="goal"),
                MatchEvent(minute=23, team="RB Leipzig",      player="Dani Olmo",      type="free_kick"),
                MatchEvent(minute=44, team="Bayer Leverkusen", player="Florian Wirtz", type="goal"),
                MatchEvent(minute=55, team="Bayer Leverkusen", player="Granit Xhaka",  type="yellow_card"),
                MatchEvent(minute=60, team="RB Leipzig",      player="Willi Orbán",    type="injury"),
                MatchEvent(minute=68, team="Bayer Leverkusen", player="Jonas Hofmann", type="throw_in"),
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
            home_players=["Kylian Mbappé", "Ousmane Dembélé"],
            away_players=["Pierre-Emerick Aubameyang", "Jordan Veretout"],
            events=[
                MatchEvent(minute=4,  team="Marseille",            player="Jordan Veretout",   type="corner"),
                MatchEvent(minute=12, team="Marseille",            player="Pierre-Emerick Aubameyang", type="offside"),
                MatchEvent(minute=25, team="Paris Saint-Germain",  player="Sergio Ramos",      type="handball"),
                MatchEvent(minute=31, team="Paris Saint-Germain",  player="Kylian Mbappé",     type="goal"),
                MatchEvent(minute=45, team="Paris Saint-Germain",  player="Gianluigi Donnarumma", type="penalty_saved"),
                MatchEvent(minute=61, team="Paris Saint-Germain",  player="Ousmane Dembélé",   type="goal"),
                MatchEvent(minute=68, team="Paris Saint-Germain",  player="Achraf Hakimi",     type="foul"),
                MatchEvent(minute=70, team="Marseille",            player="Pau López",         type="goal_kick"),
                MatchEvent(minute=75, team="Marseille",            player="Jonathan Clauss",   type="red_card"),
                MatchEvent(minute=82, team="Paris Saint-Germain",  player="Marco Asensio",     type="injury"),
                # PSG swap Dembélé → Randal Kolo Muani
                MatchEvent(minute=85, team="Paris Saint-Germain",  player="Ousmane Dembélé",   type="substitution", sub_in="Randal Kolo Muani"),
                MatchEvent(minute=88, team="Paris Saint-Germain",  player="Lucas Hernández",   type="var_check"),
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
            home_players=["Alexandre Lacazette"],
            away_players=["Terem Moffi"],
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
