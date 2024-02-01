import tkinter as tk
from functools import partial

class HomeScreen(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.configure(background="#E5E5E5")

        self.title_label = tk.Label(self,
                                    text="Football survivor",
                                    bg="#E5E5E5", fg="black",
                                    width=0,
                                    font=("Arial", 25))
        self.user_id = user_id
        self.controller = parent
        self.join_league_var = tk.StringVar()
        self.join_league_entry = tk.Entry(self, textvariable=self.join_league_var, width=30, bg="white", fg="black")
        self.join_league_button = tk.Button(self, text="Join", command=self.join_league_clicked, highlightbackground="#E5E5E5")
        self.join_league_text = tk.Label(self, text="To join league enter unique id", bg="#E5E5E5", fg="black")
        self.user_leagues = self.controller.get_user_league_info(self.user_id)
        print(self.user_leagues)
        self.league_id_label = tk.Label(self, text="League ID", bg="#E5E5E5", fg="black")
        self.league_name_label = tk.Label(self, text="League Name", bg="#E5E5E5", fg="black")
        self.start_gameweek_label = tk.Label(self, text="Start Gameweek", bg="#E5E5E5", fg="black")
        self.league_id = [tk.Button(self, text=name[0], command=partial(self.view_league_clicked, name[0]), highlightbackground="#E5E5E5") for name in
                          self.user_leagues]
        self.league_name = [tk.Label(self, text=name[1], fg='black', bg="#E5E5E5") for name in self.user_leagues]
        self.start_gameweek = [tk.Label(self, text=name[2], fg='black', bg="#E5E5E5") for name in self.user_leagues]

        self.label_league_name = tk.Label(self, text="League name:", bg="#E5E5E5", fg="black")
        self.league_name_var = tk.StringVar()
        self.league_name_entry = tk.Entry(self, textvariable=self.league_name_var, width=30, fg="black", bg="white")
        self.create_league_button = tk.Button(self, text="create", command=self.create_button_clicked, highlightbackground="#E5E5E5")

        self.gameweek_timings_id = self.controller.get_gameweek_id()
        self.gameweek_timings = self.get_gameweek_dates(self.gameweek_timings_id)
        self.gameweek_label = tk.Label(self, text="Start Gameweek: ", bg="#E5E5E5", fg="black")
        self.gameweek_var = tk.StringVar()
        self.gameweek_var.set(self.gameweek_timings[0])
        self.gameweek_drop_down_menu = tk.OptionMenu(self, self.gameweek_var, *self.gameweek_timings)
        self.gameweek_drop_down_menu.config(bg="#E5E5E5", fg="black")

        self.profile_image = tk.PhotoImage(file=r"GUI/images/profile.png").subsample(10,10)
        self.profile_button = tk.Button(self, image=self.profile_image, command=self.profile_clicked, highlightbackground="#E5E5E5", relief="flat", bg="#E5E5E5")

        self.place_widgets()

    def place_widgets(self):
        self.title_label.place(x=300, y=0)

        self.join_league_entry.place(x=20, y=80)
        self.join_league_button.place(x=20, y=110)
        self.join_league_text.place(x=20, y=50)

        self.league_id_label.place(x=400, y=50)
        self.league_name_label.place(x=500, y=50)
        self.start_gameweek_label.place(x=600, y=50)
        for i in range(len(self.league_id)):
            self.league_id[i].place(x=400, y=100+i*30)
            self.league_name[i].place(x=500, y=100+i*30)
            self.start_gameweek[i].place(x=600, y=100+i*30)

        self.label_league_name.place(x=20, y=200)
        self.league_name_entry.place(x=20, y=225)
        self.create_league_button.place(x=20, y=350)
        self.gameweek_label.place(x=20, y=275)
        self.gameweek_drop_down_menu.place(x=20, y=300)
        self.profile_button.place(x=768, y=0)

    def join_league_clicked(self):
        self.controller.add_user_league(self.user_id, self.join_league_var.get())
        current_gameweek = self.controller.get_league_starting_gameweek(self.join_league_var.get())
        self.controller.show_league_selection_page(self.user_id, self.join_league_var.get(), current_gameweek)

    def create_league_clicked(self):
        self.controller.show_create_league_page(self.user_id)

    def view_league_clicked(self, league_id):
        self.controller.show_view_league_page(self.user_id, league_id)

    def get_gameweek_dates(self, lis):
        lis_new = []
        for i in lis:
            lis_new.append(i[1])
        return lis_new

    def get_gameweek_id_final(self):
        for i in self.gameweek_timings:
            if i.strftime("%Y-%m-%d %H:%M:%S") == self.gameweek_var.get():
                gameweek = i

        for j in self.gameweek_timings_id:
            if j[1] == gameweek:
                return j[0]

    def profile_clicked(self):
        self.sign_out_button = tk.Button(self, text="Sign Out", command=self.sign_out_clicked, highlightbackground="#E5E5E5")
        self.sign_out_button.place(x=700, y=20)
    def create_button_clicked(self):
        gameweek_id = self.get_gameweek_id_final()
        self.controller.add_league(gameweek_id, self.league_name_entry.get())
        league_gameweek = self.controller.get_final_league_gameweek()
        self.controller.add_user_league(self.user_id, league_gameweek[0])
        self.controller.show_league_selection_page(self.user_id, league_gameweek[0], gameweek_id)

    def sign_out_clicked(self):
        self.controller.show_frame("sign_in_frame")