import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database import models as m

engine = create_engine('sqlite:///:memory:')

@pytest.fixture
def session():
    Session = sessionmaker(bind=engine)
    db_session = Session()
    yield db_session
    db_session.rollback()
    db_session.close()


@pytest.fixture(autouse=True)
def setup_db(session, request):
    def teardown():
        m.Base.metadata.drop_all(engine)

    m.Base.metadata.create_all(engine)

    teams = [m.Team(team_name="Arsenal"),
             m.Team(team_name="Aston Villa"),
             m.Team(team_name="Bournemouth"),
             m.Team(team_name="Brentford"),
             m.Team(team_name="Brighton & Hove Albion"),
             m.Team(team_name="Burnley"),
             m.Team(team_name="Chelsea"),
             m.Team(team_name="Crystal Palace"),
             m.Team(team_name="Everton"),
             m.Team(team_name="Fulham"),
             m.Team(team_name="Liverpool"),
             m.Team(team_name="Luton Town"),
             m.Team(team_name="Manchester City"),
             m.Team(team_name="Manchester United"),
             m.Team(team_name="Newcastle United"),
             m.Team(team_name="Nottingham Forest"),
             m.Team(team_name="Sheffield United"),
             m.Team(team_name="Tottenham Hotspur"),
             m.Team(team_name="West Ham United"),
             m.Team(team_name="Wolverhampton Wanderers")]

    users = [m.User(first_name="Toby", last_name="Willmott", username="tobywillmott", password="P@ssword123"),
             m.User(first_name="James", last_name="Smith", username="jamessmith", password="p@rdhE123"),
             m.User(first_name="John", last_name="Dixon", username="tomdixon", password="Th@$$or99od"), ]

    gameweek = [m.Gameweek(start_date=datetime(2023, 8, 11, 17, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 8, 19, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 8, 26, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 9, 2, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 9, 16, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 9, 23, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 9, 30, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 10, 7, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 10, 21, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 10, 28, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 11, 4, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 11, 11, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 11, 25, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 12, 2, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 12, 5, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 12, 9, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 12, 16, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 12, 23, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 12, 26, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2023, 12, 30, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 1, 13, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 1, 30, 17, 15, 0)),
                m.Gameweek(start_date=datetime(2024, 2, 3, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 2, 10, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 2, 17, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 2, 24, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 3, 2, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 3, 9, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 3, 16, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 3, 30, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 4, 2, 17, 15, 0)),
                m.Gameweek(start_date=datetime(2024, 4, 6, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 4, 13, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 4, 20, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 4, 27, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 5, 4, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 5, 11, 12, 30, 0)),
                m.Gameweek(start_date=datetime(2024, 5, 19, 13, 30, 0))]

    leagues = [m.League(gameweek_id=1, league_name="The best league"),
               m.League(gameweek_id=2, league_name="Tottenham Fans")]

    user_leagues = [m.UserLeague(user_id=4, league_id=1),
                    m.UserLeague(user_id=2, league_id=2)]
    # Add changes to the database and commit
    session.add_all(users)
    session.add_all(teams)
    session.add_all(leagues)
    session.add_all(gameweek)
    session.add_all(user_leagues)
    session.commit()

    request.addfinalizer(teardown)

class TestSetup:
    def test_query_teams(self, session):
        teams = session.query(m.Team).all()
        assert len(teams) == 20
        assert teams[0].team_name == "Arsenal"
        assert teams[1].team_name == "Aston Villa"

    def test_query_users(self, session):
        users = session.query(m.User).all()
        assert len(users) == 3
        assert users[0] == {"first_name": "Toby",
                            "last_name": "Willmott",
                            "username": "tobywillmott",
                            "Password": "P@ssword123"
                            }
class TestQueries:
    def test_db(self, session):
        teams = session.query(m.Team).all()
        assert len(teams) == 20
