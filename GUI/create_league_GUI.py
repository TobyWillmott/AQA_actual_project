import tkinter as tk
from datetime import datetime as dt


class CreateLeague(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)

        # create widgets
        self.controller = parent
        self.label_league_name = tk.Label(self, text="League name:")
        self.user_id = user_id
        self.league_name_var = tk.StringVar()
        self.league_name_entry = tk.Entry(self, textvariable=self.league_name_var, width=30)
        self.create_league_button = tk.Button(self, text="create", command=self.create_button_clicked)
        self.back_button = tk.Button(self, text="Back", command=self.back_clicked)
        self.gameweek_timings_id = self.controller.get_gameweek_id()
        self.gameweek_timings = self.get_gameweek_dates(self.gameweek_timings_id)
        self.gameweek_label = tk.Label(self, text="Start Gameweek: ")
        self.gameweek_var = tk.StringVar()
        self.gameweek_var.set(self.gameweek_timings[0])
        self.gameweek_drop_down_menu = tk.OptionMenu(self, self.gameweek_var, *self.gameweek_timings)
        self.place_widgets()

    def get_gameweek_dates(self, lis):
        lis_new = []
        for i in lis:
            lis_new.append(i[1])
        return lis_new

    def place_widgets(self):
        self.back_button.grid(row=0, column=0)
        self.label_league_name.grid(row=1, column=0)
        self.league_name_entry.grid(row=1, column=1)
        self.create_league_button.grid(row=2, column=2)
        self.gameweek_label.grid(row=2, column=0)
        self.gameweek_drop_down_menu.grid(row=2, column=1)

    def get_gameweek_id_final(self):
        for i in self.gameweek_timings:
            if i.strftime("%Y-%m-%d %H:%M:%S") == self.gameweek_var.get():
                gameweek = i

        for j in self.gameweek_timings_id:
            if j[1] == gameweek:
                return j[0]

    def create_button_clicked(self):
        gameweek_id = self.get_gameweek_id_final()
        self.controller.add_league(gameweek_id, self.league_name_entry.get())
        league_gameweek = self.controller.get_final_league_gameweek()
        self.controller.add_user_league(self.user_id, league_gameweek[0])
        self.controller.show_league_selection_page(self.user_id, league_gameweek[0], gameweek_id)

    def back_clicked(self):
        self.controller.show_home_page(self.user_id)
