from GUI.registration_GUI import Registration
from GUI.sign_in_GUI import SignIn
import tkinter as tk
from sqlalchemy import create_engine
from GUI.rules_GUI import Rules
from GUI.home_screen_GUI import HomeScreen
from GUI.select_teams_GUI import SelectTeams
from GUI.view_league_GUI import ViewLeague
from classes.game_objects import Game


class TkApplication(tk.Tk):
    """
    This class initialises the game and a Tk instance (window)
    The window includes a sets up frames with the different views on the game
    The class also acts as a controller between the model and user interface
    """

    def __init__(self):
        """
        This method initialised all the attributes ot the class
        """
        super().__init__()
        self.geometry("800x400")
        self.configure(background="#E5E5E5")
        self.game = Game()

        self.resizable(False, False)
        #self.engine = create_engine("sqlite:///database/fantasy_football.sqlite", echo=True)
        self.frames = {
            "sign_in_frame": SignIn(self),
            "register_frame": Registration(self)
        }

        self.show_frame("sign_in_frame")

    def show_frame(self, current_frame: str):
        """
        This function is used to show the frames that don't take any parameters

        Parameters
        ----------
        current_frame - the frame that you would like to show
        """
        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()

        frame_to_show = self.frames[current_frame]
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def show_home_page(self, user_id):
        """
        This functino is used to show the home page frame

        Parameters
        ----------
        user_id - user_id of the user
        """
        self.geometry("800x400")
        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()
        self.game.set_user(user_id)
        frame_to_show = HomeScreen(self, user_id)
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def show_rules_page(self, user_id):
        """
        This function is used to show the rules page to the user
        Parameters
        ----------
        user_id - user_id of the user
        """
        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()
        frame_to_show = Rules(self, user_id)
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def show_league_selection_page(self, user_id, league_id, gameweek_id):
        """
        This function is used to show the league selection page to the user

        Parameters
        ----------
        user_id - the user_id of the user signed in and making selections
        league_id - the league_id of the league you are making selections for
        gameweek_id - the starting gameweek of the league
        """
        self.game.check_error_joining(user_id, league_id, gameweek_id)

        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()

        frame_to_show = SelectTeams(self, user_id, league_id, gameweek_id)
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def show_view_league_page(self, user_id, league_id):
        """
        This function is used to show the view league page to the user

        Parameters
        ----------
        user_id - user_id of the user signing in
        league_id - league_id of the league the user wants to view
        """
        self.geometry("700x800")
        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()

        frame_to_show = ViewLeague(self, user_id, league_id)
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def add_user(self, first_name_, last_name_, username_, password_):
        """
        adds a user to the database by running add_user function in the game object
        """
        self.game.add_user(first_name_, last_name_, username_, password_)

    def add_league(self, gameweek_id_, league_name_):
        """
        adds a league to the database by running the add_league function in the game object
        """
        self.game.add_league(gameweek_id_, league_name_)

    #    def add_user_league(self, user_id_, league_id_):
    #        self.game.add_user_league(user_id_, league_id_)
    def get_username_details(self, username_entry):
        """
        gets the users username details to check the sign in details by running the get_username_details function in
        the game object
        """
        return self.game.get_username_details(username_entry)

    # def get_gameweek_timings(self):
    #    return self.game.get_gameweek_timings()

    def get_gameweek_id(self):
        """
        gets a list of all the gameweek_id's and the corresponding start_date's by running the get_gameweek_id
        function in the game object
        """
        return self.game.get_gameweek_id()

    def add_user_selections(self, lis):
        """
        adds the user selections to the player object by running the add_user_selection file of the game object
        """
        return self.game.add_user_selections(lis)

    def get_teams(self):
        """
        Returns a list containing team id and corresponding team name by running the get_teams function of the game
        object
        """
        return self.game.get_teams()

    def get_league_starting_gameweek(self, league_id_):
        """
        Returns the league starting gameweek from the league id through the get_league_starting_gameweek from the
        game object
        """
        return self.game.get_league_starting_gameweek(league_id_)

    def get_final_league_gameweek(self):
        """
        Returns the league id of the last league added through the get_final_league_gameweek function from the game
        object
        """
        return self.game.get_final_league_gameweek()

    def get_user_league_info(self, user_id_):
        """
        Returns a list of the current leagues the user is part of by running the get_user_league_info function from
        the game object
        """
        return self.game.get_user_league_info(user_id_)

    def match_info(self, game_week_id):
        """
        Returns a list of the match data for a given gameweek by running the match_info function from the game object
        """
        return self.game.match_info(game_week_id)

    def id_to_team(self, team_id_):
        """
        Returns a team abbreviation name from the team_id by running the id_to_team function from the game object
        """
        return self.game.id_to_team(team_id_)

    def get_user_name(self, user_ids):
        """
        converts a list of user_id's into a list of corresponding username's by running the get_user_names function
        from the game object
        """
        return self.game.get_user_name(user_ids)

    def get_user_ids(self, league_id_):
        """
        returns a list of users that are part of the league with league_id: league_id by running the function
        get_user_ids from the game object
        """
        return self.game.get_user_ids(league_id_)

    def check_points(self, user_ids, league_id):
        """
        Returns the number of points each user has in the league with league_id: league_id by running the function
        check_points from the game object
        """
        return self.game.check_points(user_ids, league_id)

    def hash_password(self, password):
        """
        converts a normal password into a hashed password by running the hash_password function from the game object
        """
        return self.game.hash_password(password)

    def get_games(self, user_id, league_id):
        """
        returns a list of all user selections in a league and the score and difficulty by running the function
        get_games from the game object
        """
        return self.game.get_games(user_id, league_id)

    def get_league_name(self, league_id):
        """
        gets the league name from the league_id by running the functino get_league_name function from the game object
        """
        return self.game.get_league_name(league_id)


if __name__ == "__main__":
    app = TkApplication()
    app.mainloop()
