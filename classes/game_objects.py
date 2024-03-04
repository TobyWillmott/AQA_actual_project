from database import queries as qry
import classes.api as api
from sqlalchemy import create_engine
from database.models import Base, User, Selection
from sqlalchemy.orm import Session
import hashlib
import re

engine = create_engine("sqlite:///database/fantasy_football.sqlite", echo=True)
Base.metadata.create_all(engine)


class Game:

    def __init__(self):
        self.user = None
        self.user_selections = None
        self.user_selections_db = []
        self.add_league_lis = []
        self.add_user_league = []
        self.start_gameweek = None
        self.end_gameweek = None
        self.finished = None

    def add_user(self, first_name_, last_name_, username_, password_):
        username_pattern = "^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$"
        if not re.fullmatch(username_pattern, username_):
            raise ValueError("Username is invalid")
        if first_name_ == "":
            raise ValueError("First name is invalid")
        if last_name_ == "":
            raise ValueError("Surname is invalid")
        password_pattern = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.fullmatch(password_pattern, password_):
            raise ValueError("Password is invalid, Must have minimum eight characters, at least one letter and one number")
        qry.qry_add_user(first_name_, last_name_, username_, password_)
    def add_league(self, gameweek_id_, league_name_):
        qry.qry_add_league(gameweek_id_, league_name_)
    def set_user(self, id):
        self.player = Player(id)
    def get_gameweek_timings(self):
        return qry.qry_get_gameweek_timings()

    def add_user_selections(self, selection_lis):
        return self.player.set_user_selections(selection_lis)

    def get_gameweek_id(self):
        return qry.qry_get_gameweek_id()

    def get_username_details(self, username_entry):
        return qry.qry_get_username_details(username_entry)

#    def add_selection(self, gameweek_id_, user_id_, team_id_, league_id_):
#        qry.qry_add_selection(gameweek_id_, user_id_, team_id_, league_id_)

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
        if password == "":
            return False
        else:
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



class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_selections = None
        self.user_selections_db = []
        self.add_user_league = []
        self.start_gameweek = None
        self.end_gameweek = None
        self.finished = None
    def add_all(self):
        print("this is the user_league", self.add_user_league)
        print(self.user_selections)
        qry.qry_add_user_league(self.add_user_league[0], self.add_user_league[1])
        self.add_user_league = []

        qry.qry_add_selection_list(self.user_selections_db)
        self.user_selections_db = []
        self.user_selections = None
        self.start_gameweek = None
        self.end_gameweek = None
    def set_user_selections(self, selection_lis):
        print("this is the selection lis ", selection_lis)
        print("this is the total lis", self.user_selections)
        if self.user_selections == None:
            print("true")
            self.user_selections = [selection_lis]
            self.start_gameweek = selection_lis[0]
            self.set_user_league(selection_lis[1], selection_lis[3])
            self.user_selections_db.append(
                Selection(gameweek_id=selection_lis[0], outcome=None, user_id=selection_lis[1],
                          team_id=selection_lis[2],
                          league_id=selection_lis[3]))
            if selection_lis[0] + 20 > 40:
                self.end_gameweek = 40
            else:
                self.end_gameweek = self.start_gameweek + 19
            print(self.user_selections)
        else:
            print(self.end_gameweek)
            if selection_lis[0] >= self.end_gameweek:
                print("gamweek has finished")
                for gameweek in self.user_selections:
                    if gameweek[2] == selection_lis[2]:
                        print("team has been selected")
                        return "Team has already been selected"
                self.user_selections_db.append(
                    Selection(gameweek_id=selection_lis[0], outcome=None, user_id=selection_lis[1],
                              team_id=selection_lis[2],
                              league_id=selection_lis[3]))
                self.user_selections.append(selection_lis)
                self.add_all()
                return "finished"
            else:
                print(self.user_selections, "\n")
                for gameweek in self.user_selections:
                    if gameweek[2] == selection_lis[2]:
                        return "Team has already been selected"
                self.user_selections_db.append(
                    Selection(gameweek_id=selection_lis[0], outcome=None, user_id=selection_lis[1],
                              team_id=selection_lis[2],
                              league_id=selection_lis[3]))
                self.user_selections.append(selection_lis)
    def set_user_league(self, user_id_, league_id_):
        self.add_user_league = [user_id_, league_id_]
    def remove_my_user(self):
        self.my_user = None

