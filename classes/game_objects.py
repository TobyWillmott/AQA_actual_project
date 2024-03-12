from database import queries as qry
import classes.api as api
from sqlalchemy import create_engine
from database.models import Base, User, Selection
from sqlalchemy.orm import Session
import hashlib
import re
from datetime import datetime

engine = create_engine("sqlite:///database/fantasy_football.sqlite", echo=True)
Base.metadata.create_all(engine)


class Game:

    def __init__(self):
        self.user = None
        # self.time = datetime(2023, 8, 11, 17, 30, 0)
        self.time = datetime.now()

    def add_user(self, first_name_, last_name_, username_, password_):
        '''
        adds a uer to the database by runnin the qry.qry_add_user() function
        validates whether first_name, last_name, username and password are all valid inputs
        '''
        username_pattern = "^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$"
        if not re.fullmatch(username_pattern, username_):
            raise ValueError("Username is invalid")
        if first_name_ == "":
            raise ValueError("First name is invalid")
        if last_name_ == "":
            raise ValueError("Surname is invalid")
        password_pattern = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.fullmatch(password_pattern, password_):
            raise ValueError(
                "Password is invalid, Must have minimum eight characters, at least one letter and one number")
        qry.qry_add_user(first_name_, last_name_, username_, password_)

    def add_league(self, gameweek_id_, league_name_):
        '''
        used to add a league to the database by running the qry.qry_add_league() function
        validates whether the league name is valid
        '''
        if league_name_ == "":
            raise ValueError("You must enter \n a league name")
        if len(league_name_) > 20:
            raise ValueError("League name too long")
        qry.qry_add_league(gameweek_id_, league_name_)

    def set_user(self, id):
        '''
        Parameters
        ----------
        id - user id of the user

        instantiating the player class
        '''
        self.player = Player(id)

    def add_user_selections(self, selection_lis):
        '''

        Parameters
        ----------
        selection_lis - list of the users selections

        Returns
        The output of player.set_user_selections() - this is a message that notifies whether was successful

        '''
        return self.player.set_user_selections(selection_lis)

    def get_gameweek_id(self):
        '''

        Returns
        a list of all the gameweek ids and the corresponding date

        filters the list only showing dates that are in the future
        used to display the possible starting gameweeks in the dropbox
        '''
        timings = qry.qry_get_gameweek_id()
        updated_timings = []
        for gameweek in timings:
            if gameweek[1] > self.time:
                updated_timings.append(gameweek)
        return updated_timings

    def get_username_details(self, username_entry):
        '''

        Parameters
        ----------
        username_entry - username

        Returns
        a list containing the user_id, username, password
        '''
        return qry.qry_get_username_details(username_entry)

    def get_teams(self):
        '''

        Returns
        a list containing team id and corresponding team name

        '''
        return qry.qry_get_teams()

    def get_league_starting_gameweek(self, league_id_):
        '''

        Parameters
        ----------
        league_id_ - league_id of the league you would like the starting gameweeek of

        Returns
        the starting_date of the leauge with league id, league_id

        '''
        return qry.qry_get_league_starting_gameweek(league_id_)

    def get_final_league_gameweek(self):
        '''

        Returns
        -------
        the league id of the last league added

        '''
        return qry.qry_get_final_league_gameweek()

    def get_user_league_info(self, user_id_):
        '''

        Parameters
        ----------
        user_id_ - user id of the user

        Returns
        -------
        A  list containing the current leagues the user is part of
        '''
        return qry.qry_get_user_league_info(user_id_)

    def id_to_team(self, team_id_):
        '''

        Parameters
        ----------
        team_id_

        Returns
        -------
        the team abbreviation for the team id
        '''
        return qry.qry_id_to_team(team_id_)

    def get_user_name(self, user_ids):
        '''

        Parameters
        ----------
        user_ids - a list of user ids

        Returns
        -------
        the usernames of the list of user ids
        '''
        return qry.qry_get_user_name(user_ids)

    def get_user_ids(self, league_id_):
        '''

        Parameters
        ----------
        league_id_

        Returns
        -------
        a list of the user_ids that are in a league
        '''
        return qry.qry_get_user_ids(league_id_)

    def get_selection(self, league_id_, user_id_):
        '''

        Parameters
        ----------
        league_id_
        user_id_

        Returns
        -------
        a list of user_ids that contain are part of the league with league id: league_id
        '''
        return qry.qry_get_selection(league_id_, user_id_)

    def match_info(self, game_week_id):
        '''

        Parameters
        ----------
        game_week_id - gameweek_id of the gameweek you would like information from

        Returns
        -------
        a list of the match data for a given gameweek (team_id of teams playing, and difficulty for each team)
        '''
        return api.api_match_info(game_week_id)

    def check_points(self, user_ids, league_id):
        '''

        Parameters
        ----------
        user_ids - a list of all the users in a legue which require the points for
        league_id

        Returns
        -------
        a list containing the number of points for each user

        '''
        selection_lis = []
        for user in user_ids:
            selection = self.get_selection(league_id, user[0])
            selection_lis.append(selection)
        return api.api_check_points(selection_lis)

    def hash_password(self, password):
        '''

        Parameters
        ----------
        password

        Returns
        -------
        the hashed password
        '''
        if password == "":
            return False
        else:
            hasher = hashlib.sha256()
            hasher.update(bytes(password, 'utf-8'))
            return hasher.hexdigest()

    def get_games(self, user_id, league_id):
        '''

        Parameters
        ----------
        user_id
        league_id

        Returns
        -------
        a list of all a users selections including a score(if match has been played) and the difficulty
        '''
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
        return games

    def id_to_colour(self, difficulty):
        '''

        Parameters
        ----------
        difficulty - the difficulty of a match - (a number 1 to 5)

        Returns
        -------
        a hex colour that is used in the GUI to display the difficulty

        '''
        if difficulty == 1:
            colour = "#2cba00"
        elif difficulty == 2:
            colour = "#a3ff00"
        elif difficulty == 3:
            colour = "#fff400"
        elif difficulty == 4:
            colour = "#ffa700"
        elif difficulty == 5:
            colour = "#ff0000"
        return colour

    def check_error_joining(self, user_id, league_id, gameweek_id):
        '''

        Parameters
        ----------
        user_id
        league_id
        gameweek_id

        Returns
        -------
        a ValueError if there is an error joining a league

        this subroutine is used to check whether a user is able to join a league by checking whether the user is already in this league
        '''
        if qry.qry_check_in_league(user_id, league_id) != []:
            # qry.qry_check in league returns a list containing the user_league_id if the user is part of the league
            raise ValueError("Already in league")
        starting_time = qry.qry_get_league_starting_datetime(gameweek_id)
        if starting_time < self.time:
            raise ValueError("League has already started")

    def get_league_name(self, league_id):
        '''

        Parameters
        ----------
        league_id

        Returns
        -------
        The name of the given league id
        '''
        return qry.qry_get_league_name(league_id)


class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_selections = None
        self.user_selections_db = []
        self.add_user_league = []
        self.current_gameweek = None
        self.end_gameweek = None
        self.finished = None

    def add_all(self):
        '''
        adds all the selections to the database once all selections have been made
        Adds a value to the user_league table which in the linked table
        '''
        qry.qry_add_user_league(self.add_user_league[0], self.add_user_league[1])
        self.add_user_league = []

        qry.qry_add_selection_list(self.user_selections_db)
        self.user_selections_db = []
        self.user_selections = None
        self.current_gameweek = None
        self.end_gameweek = None

    def set_user_selections(self, selection_lis):
        self.current_gameweek = selection_lis[0]
        if self.user_selections == None:
            if selection_lis[0] + 20 > 38:
                self.end_gameweek = 38
            else:
                self.end_gameweek = self.current_gameweek + 19
            if selection_lis[0] > self.end_gameweek:
                raise ValueError("Gameweek has finished")
            if self.team_playing(self.current_gameweek, selection_lis[2]) == False:
                raise ValueError("Team is not playing \n in this gameweek")
            self.user_selections = [selection_lis]
            self.set_user_league(selection_lis[1], selection_lis[3])
            self.user_selections_db.append(
                Selection(gameweek_id=selection_lis[0], outcome=None, user_id=selection_lis[1],
                          team_id=selection_lis[2],
                          league_id=selection_lis[3]))
        else:
            if selection_lis[0] > self.end_gameweek:
                raise ValueError("League has finished")
            elif selection_lis[0] == self.end_gameweek:
                self.user_selections_db.append(
                    Selection(gameweek_id=selection_lis[0], outcome=None, user_id=selection_lis[1],
                              team_id=selection_lis[2],
                              league_id=selection_lis[3]))
                self.user_selections.append(selection_lis)
                self.add_all()
                return "finished"
            else:
                if self.team_playing(self.current_gameweek, selection_lis[2]) == False:
                    raise ValueError("Team is not playing in this gameweek")
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

    def team_playing(self, game_week_id, team_id):
        return api.team_playing(game_week_id, team_id)
