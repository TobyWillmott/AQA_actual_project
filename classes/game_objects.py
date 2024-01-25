from database import queries as qry
import classes.api as api
from sqlalchemy import create_engine
from database.models import Base, User
from sqlalchemy.orm import Session
import hashlib

engine = create_engine("sqlite:///database/fantasy_football.sqlite", echo=True)
Base.metadata.create_all(engine)


class Game:

    def __init__(self):
        self.user = None

    def add_user(self, first_name_, last_name_, username_, password_):
        qry.qry_add_user(first_name_, last_name_, username_, password_)

    def get_gameweek_timings(self):
        return qry.qry_get_gameweek_timings()

    def add_league(self, gameweek_id_, league_name_):
        qry.qry_add_league(gameweek_id_, league_name_)

    def add_user_league(self, user_id_, league_id_):
        qry.qry_add_user_league(user_id_, league_id_)

    def add_selection_list(self, user_selections):
        qry.qry_add_selection_list(user_selections)

    def get_gameweek_id(self):
        return qry.qry_get_gameweek_id()

    def get_username_details(self, username_entry):
        return qry.qry_get_username_details(username_entry)

    def add_selection(self, gameweek_id_, user_id_, team_id_, league_id_):
        qry.qry_add_selection(gameweek_id_, user_id_, team_id_, league_id_)

    def get_teams(self):
        return qry.qry_get_teams()

    def get_league_starting_gameweek(self, league_id_):
        return qry.qry_get_league_starting_gameweek(league_id_)

    def get_final_league_gameweek(self):
        return qry.qry_get_final_league_gameweek()

    def get_user_league_info(self, user_id_):
        return qry.qry_get_user_league_info(user_id_)

    def id_to_team(self, team_id_):
        return qry.qry_id_to_team(team_id_)

    def get_user_name(self, user_ids):
        return qry.qry_get_user_name(user_ids)

    def get_user_ids(self, league_id_):
        return qry.qry_get_user_ids(league_id_)

    def get_selection(self, league_id_, user_id_):
        return qry.qry_get_selection(league_id_, user_id_)

    def match_info(self, game_week_id):
        return api.api_match_info(game_week_id)

    def check_lives(self, user_ids, league_id):
        selection_lis = []
        for user in user_ids:
            selection = self.get_selection(league_id, user)
            selection_lis.append(selection)
        return api.api_check_lives(user_ids, league_id, selection_lis)
    def hash_password(self, password):
        hasher = hashlib.sha256()
        hasher.update(bytes(password, 'utf-8'))
        return hasher.hexdigest()

    def get_games(self, user_id, league_id):
        user_selections = qry.qry_get_games(user_id, league_id)
        games = api.get_games(user_selections)
        for gameweek in games:
            user_team = qry.qry_id_to_team(gameweek[1])
            opp_team = qry.qry_id_to_team(gameweek[4])
            user_difficulty = self.id_to_colour(gameweek[3])
            opp_difficulty = self.id_to_colour(gameweek[6])
            gameweek[1] = user_team
            gameweek[4] = opp_team
            gameweek[3] = user_difficulty
            gameweek[6] = opp_difficulty
        print("games: ",games)
        return games

    def id_to_colour(self, difficulty):
        if difficulty==1:
            colour="#2cba00"
        elif difficulty==2:
            colour="#a3ff00"
        elif difficulty==3:
            colour="#fff400"
        elif difficulty==4:
            colour="#ffa700"
        elif difficulty==5:
            colour="#ff0000"
        return colour



class User:
    def __init__(self):
        self.sess = Session(engine)
        self.my_user = None

    def set_my_user(self, user_id):
        self.my_user = self.sess.get(User, user_id)

    def remove_my_user(self):
        self.my_user = None

