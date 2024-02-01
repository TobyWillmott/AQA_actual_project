from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.models import League, Team, Gameweek, User
from datetime import datetime

teams = [Team(team_name="Arsenal", team_abb="ARS"),
         Team(team_name="Aston Villa", team_abb="AVL"),
         Team(team_name="Bournemouth", team_abb="BOU"),
         Team(team_name="Brentford", team_abb="BRE"),
         Team(team_name="Brighton & Hove Albion", team_abb="BHA"),
         Team(team_name="Burnley", team_abb="BUR"),
         Team(team_name="Chelsea", team_abb="CHE"),
         Team(team_name="Crystal Palace", team_abb="CRY"),
         Team(team_name="Everton", team_abb="EVE"),
         Team(team_name="Fulham", team_abb="FUL"),
         Team(team_name="Liverpool", team_abb="LIV"),
         Team(team_name="Luton Town", team_abb="LUT"),
         Team(team_name="Manchester City", team_abb="MCI"),
         Team(team_name="Manchester United", team_abb="MNU"),
         Team(team_name="Newcastle United", team_abb="NEW"),
         Team(team_name="Nottingham Forest", team_abb="NFO"),
         Team(team_name="Sheffield United", team_abb="SHU"),
         Team(team_name="Tottenham Hotspur", team_abb="TOT"),
         Team(team_name="West Ham United", team_abb="WHU"),
         Team(team_name="Wolverhampton Wanderers", team_abb="WOL")]

users = [User(first_name="Toby", last_name="Willmott", username="tobywillmott", password="ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"),
         User(first_name="James", last_name="Smith", username="jamessmith", password="ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"),
         User(first_name="John", last_name="Dixon", username="tomdixon", password="ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"), ]

gameweek = [Gameweek(start_date=datetime(2023, 8, 11, 17, 30, 0)),
            Gameweek(start_date=datetime(2023, 8, 19, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 8, 26, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 9, 2, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 9, 16, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 9, 23, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 9, 30, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 10, 7, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 10, 21, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 10, 28, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 11, 4, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 11, 11, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 11, 25, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 12, 2, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 12, 5, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 12, 9, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 12, 16, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 12, 23, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 12, 26, 12, 30, 0)),
            Gameweek(start_date=datetime(2023, 12, 30, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 1, 13, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 1, 30, 17, 15, 0)),
            Gameweek(start_date=datetime(2024, 2, 3, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 2, 10, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 2, 17, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 2, 24, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 3, 2, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 3, 9, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 3, 16, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 3, 30, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 4, 2, 17, 15, 0)),
            Gameweek(start_date=datetime(2024, 4, 6, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 4, 13, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 4, 20, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 4, 27, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 5, 4, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 5, 11, 12, 30, 0)),
            Gameweek(start_date=datetime(2024, 5, 19, 13, 30, 0))]

leagues = [League(gameweek_id=1, league_name="The best league"),
           League(gameweek_id=2, league_name="Tottenham Fans")]


engine = create_engine("sqlite:///fantasy_football.sqlite", echo=True)

with Session(engine) as sess:
    sess.add_all(users)
    sess.add_all(teams)
    sess.add_all(leagues)
    sess.add_all(gameweek)
    sess.commit()


