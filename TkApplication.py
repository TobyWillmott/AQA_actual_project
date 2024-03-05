from GUI.registration_GUI import Registration
from GUI.welcome_GUI import WelcomeScreen
from GUI.sign_in_GUI import SignIn
import tkinter as tk
from sqlalchemy import create_engine
from GUI.rules_GUI import Rules
from GUI.home_screen_GUI import HomeScreen
from GUI.select_teams_GUI import SelectTeams
from GUI.view_league_GUI import ViewLeague
from classes.game_objects import Game


class TkApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        self.configure(background="#E5E5E5")
        self.game = Game()

        title_string = "Fantasy football"
        self.resizable(False, False)
        self.engine = create_engine("sqlite:///database/fantasy_football.sqlite", echo=True)
        self.frames = {
            "welcome_frame": WelcomeScreen(self),
            "sign_in_frame": SignIn(self),
            "register_frame": Registration(self)
        }

        self.show_frame("sign_in_frame")

    def show_frame(self, current_frame: str):
        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()

        frame_to_show = self.frames[current_frame]
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def show_home_page(self, user_id):
        #self.geometry("800x800")
        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()
        self.game.set_user(user_id)
        frame_to_show = HomeScreen(self, user_id)
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def show_rules_page(self, user_id):
        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()
        frame_to_show = Rules(self, user_id)
        frame_to_show.pack(expand=True, fill=tk.BOTH)
    def show_league_selection_page(self, user_id, league_id, gameweek_id):
        self.game.check_in_league(user_id, league_id)

        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()

        frame_to_show = SelectTeams(self, user_id, league_id, gameweek_id)
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def show_view_league_page(self, user_id, league_id):
        widgets = self.winfo_children()
        for w in widgets:
            if w.winfo_class() == "Frame":
                w.pack_forget()

        frame_to_show = ViewLeague(self, user_id, league_id)
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def add_user(self, first_name_, last_name_, username_, password_):
        self.game.add_user(first_name_, last_name_, username_, password_)

    def add_league(self, gameweek_id_, league_name_):
        self.game.add_league(gameweek_id_, league_name_)

#    def add_user_league(self, user_id_, league_id_):
#        self.game.add_user_league(user_id_, league_id_)
    def get_username_details(self, username_entry):
        return self.game.get_username_details(username_entry)

    def get_gameweek_timings(self):
        return self.game.get_gameweek_timings()

    def get_gameweek_id(self):
        return self.game.get_gameweek_id()

    def add_selection_list(self, user_selections):
        self.game.add_selection_list(user_selections)

    def add_user_selections(self, lis):
        return self.game.add_user_selections(lis)
    #def add_selection(self, gameweek_id_, user_id_, team_id_, league_id_):
    #    self.game.add_selection(gameweek_id_, user_id_, team_id_, league_id_)
    def get_teams(self):
        return self.game.get_teams()

    def get_league_starting_gameweek(self, league_id_):
        return self.game.get_league_starting_gameweek(league_id_)

    def get_final_league_gameweek(self):
        return self.game.get_final_league_gameweek()

    def get_user_league_info(self, user_id_):
        return self.game.get_user_league_info(user_id_)

    def match_info(self, game_week_id):
        return self.game.match_info(game_week_id)

    def id_to_team(self, team_id_):
        return self.game.id_to_team(team_id_)

    def get_user_name(self, user_ids):
        return self.game.get_user_name(user_ids)

    def get_user_ids(self, league_id_):
        return self.game.get_user_ids(league_id_)

    def check_lives(self, user_ids, league_id):
        return self.game.check_lives(user_ids, league_id)
    def hash_password(self, password):
        return self.game.hash_password(password)

    def get_games(self, user_id, league_id):
        return self.game.get_games(user_id, league_id)

if __name__ == "__main__":
    app = TkApplication()
    app.mainloop()
