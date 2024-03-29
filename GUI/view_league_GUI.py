import tkinter as tk
from GUI.vertical_scrolled_frame import VerticalScrolledFrame


class ViewLeague(tk.Frame):
    """
    This class is used to view a league to a user
    """
    def __init__(self, parent, user_id, league_id):
        """
        This subroutine is used to initialise all the widgets and attributes
        Parameters
        ----------
        parent - parent class of the tkinter frame which is also used as the controller
        user_id - the user id of the user currently signed in
        league_id - the league id of the team they are making selections for
        """
        super().__init__(parent)
        self.images = {"view": tk.PhotoImage(file=r"GUI/images/view.png").subsample(19, 19),
                       "hide": tk.PhotoImage(file=r"GUI/images/hide.png").subsample(19, 19),
                       "back": tk.PhotoImage(file=r"GUI/images/back_button.png").subsample(19, 19)}

        self.players_frame = VerticalScrolledFrame(self, width=350, height=700, bg="#E5E5E5",
                                                   highlightbackground="black", highlightthickness=3)
        self.selections_frame = VerticalScrolledFrame(self, width=300, height=700, bg="#E5E5E5",
                                                      highlightbackground="black", highlightthickness=3)

        self.config(background="#E5E5E5")
        self.user_id = user_id
        self.league_id = league_id
        self.controller = parent

        self.user_ids = self.controller.get_user_ids(self.league_id)
        self.user_names = self.controller.get_user_name(self.user_ids)
        self.points = self.controller.check_points(self.user_ids, self.league_id)

        self.league_name = self.controller.get_league_name(self.league_id)
        self.league_title = tk.Label(self, text=f"{self.league_name}", bg="#E5E5E5", font=('Arial', 15))

        self.total_list = []
        for i in range(len(self.user_ids)):
            lis = []
            lis.append(self.user_ids[i][0])
            lis.append(self.user_names[i])
            lis.append(self.points[i])
            self.total_list.append(lis)
        self.total_list.sort(reverse=True, key=lambda x: x[2])
        self.position_label = tk.Label(self.players_frame, text="Positon", bg="#E5E5E5")
        self.user_label = tk.Label(self.players_frame, text="Name", bg="#E5E5E5")
        self.lives_label = tk.Label(self.players_frame, text="Number of Points", bg="#E5E5E5")

        self.positions = [tk.Label(self.players_frame, text=f"{position + 1}", bg="#E5E5E5") for position in
                          range(len(self.user_ids))]
        self.user_names = [tk.Label(self.players_frame, text=f"{name[1][0]} {name[1][1]}", bg="#E5E5E5") for name in self.total_list]
        self.back_button = tk.Button(self, image=self.images["back"], text="Back", bg="#E5E5E5", command=self.back_clicked, relief="flat")
        self.user_lives = [tk.Label(self.players_frame, text=f"{lives[2]}", bg="#E5E5E5") for lives in self.total_list]

        self.user_games = self.controller.get_games(self.user_id, self.league_id)
        self.selections_label = tk.Label(self, text=f"Your selections", bg="#E5E5E5", font=('Arial', 12))
        self.users_label = tk.Label(self, text="Leaderboard", bg="#E5E5E5", font=('Arial', 12))
        self.place_widgets()
        self.display_matches()

    def place_widgets(self):
        """
        This funciton is used to place the widgets
        """
        self.players_frame.place(x=20,y=60)
        self.selections_frame.place(x=350, y=60)

        self.position_label.grid(row=1, column=0)
        self.user_label.grid(row=1, column=1)
        self.lives_label.grid(row=1, column=2)
        self.back_button.grid(row=0, column=0)

        self.selections_label.place(x=460, y=35)
        self.users_label.place(x=110, y=35)
        self.league_title.place(x=300, y=0)

        for i in range(len(self.user_ids)):
            self.positions[i].grid(row=2 + i, column=0)
            self.user_names[i].grid(row=2 + i, column=1)
            self.user_lives[i].grid(row=2 + i, column=3)

    def display_matches(self):
        """
        This function is used to display the selections of the users through diplaying the matches and the scores if have been played
        """
        self.gameweek_label = tk.Label(self.selections_frame, text="Gameweek", bg="#E5E5E5", fg="black")
        self.user_selection_label = tk.Label(self.selections_frame, text="Your Selection", bg="#E5E5E5", fg="black")
        self.opp_team_label = tk.Label(self.selections_frame, text="Opposing team", bg="#E5E5E5", fg="black")
        self.gameweek = [
            tk.Label(self.selections_frame, text=match[0], fg="black", width=3, font=("Arial", 8), bg="#E5E5E5") for
            match in self.user_games]
        self.user_teams = [
            tk.Label(self.selections_frame, text=match[1], fg="black", bg=match[3], width=3, font=("Arial", 8)) for
            match in self.user_games]
        self.opp_teams = [
            tk.Label(self.selections_frame, text=match[4], fg="black", bg=match[6], width=3, font=("Arial", 8)) for
            match in self.user_games]
        self.user_teams_score = [
            tk.Label(self.selections_frame, text=match[2], fg="black", width=3, font=("Arial", 8), bg="#E5E5E5") for
            match in self.user_games]
        self.opp_teams_score = [
            tk.Label(self.selections_frame, text=match[5], fg="black", width=3, font=("Arial", 8), bg="#E5E5E5") for
            match in self.user_games]
        self.versus_label = [tk.Label(self.selections_frame, text="vs", fg="black", bg="#E5E5E5") for j in
                             range(len(self.user_games))]
        index = 0
        self.gameweek_label.grid(row=0, column=0)
        self.user_selection_label.grid(row=0, column=1)
        self.opp_team_label.grid(row=0, column=3)
        for i in range(len(self.user_games)):

            self.gameweek[i].grid(row=2*i+1, column=0)
            self.user_teams[i].grid(row=2*i+1, column=1)
            self.versus_label[i].grid(row=2*i+1, column=2)
            self.opp_teams[i].grid(row=2*i+1, column=3)
            self.user_teams_score[i].grid(row=2*i+2, column=1)
            self.opp_teams_score[i].grid(row=2*i+2, column=3)

    def back_clicked(self):
        """
        This function is used to return the user to the home page
        """
        self.controller.show_home_page(self.user_id)
