import tkinter as tk
from functools import partial
from GUI.verticle_scrolled_frame import VerticalScrolledFrame
class HomeScreen(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.configure(background="#E5E5E5")

        self.join_league_tab = tk.Frame(self, width=320, height=150, bg="#E5E5E5", highlightbackground="black", highlightthickness=3)
        self.create_league_frame = tk.Frame(self, width=320, height=185, bg="#E5E5E5", highlightbackground="black", highlightthickness=3)
        #self.view_leagues_frame = tk.Frame(self, width=380, height=345, bg="#E5E5E5", highlightbackground="black", highlightthickness=3)
        self.view_leagues_frame = VerticalScrolledFrame(self, width=380, height=345, bg="#E5E5E5", highlightbackground="black", highlightthickness=3)

        self.title_label = tk.Label(self,
                                    text="Football survivor",
                                    bg="#E5E5E5", fg="black",
                                    width=0,
                                    font=("Arial", 25))
        self.user_id = user_id
        self.controller = parent
        self.join_league_var = tk.StringVar()

        # join league widgets
        self.join_league_title = tk.Label(self.join_league_tab, text="Join a league", bg="#E5E5E5", fg="black",font=("Arial", 17))
        self.join_league_entry = tk.Entry(self.join_league_tab, textvariable=self.join_league_var, width=30, bg="white", fg="black")
        self.join_league_button = tk.Button(self.join_league_tab, text="Join", command=self.join_league_clicked, highlightbackground="#E5E5E5")
        self.join_league_text = tk.Label(self.join_league_tab, text="To join a league please enter a unique league id", bg="#E5E5E5", fg="black")
        self.message_label = tk.Label(self.join_league_tab, text='', foreground='red', bg="#E5E5E5")

        # user leagues widgets
        self.user_leagues = self.controller.get_user_league_info(self.user_id)
        self.league_id_label = tk.Label(self.view_leagues_frame, text="League ID", bg="#E5E5E5", fg="black")
        self.league_name_label = tk.Label(self.view_leagues_frame, text="League Name", bg="#E5E5E5", fg="black")
        self.start_gameweek_label = tk.Label(self.view_leagues_frame, text="Start Gameweek", bg="#E5E5E5", fg="black")
        self.league_id = [tk.Button(self.view_leagues_frame, text=name[0], command=partial(self.view_league_clicked, name[0]), highlightbackground="#E5E5E5") for name in
                          self.user_leagues]
        self.league_name = [tk.Label(self.view_leagues_frame, text=name[1], fg='black', bg="#E5E5E5") for name in self.user_leagues]
        self.start_gameweek = [tk.Label(self.view_leagues_frame, text=name[2], fg='black', bg="#E5E5E5") for name in self.user_leagues]
        self.league_name_var = tk.StringVar()

        # Create league widgets
        self.create_league_title = tk.Label(self.create_league_frame, text="Create a League", bg="#E5E5E5", fg="black", font=("Arial", 17))
        self.create_league_label = tk.Label(self.create_league_frame, text="To create a league enter a league name and the starting gameweek", bg="#E5E5E5", fg="black")
        self.label_league_name = tk.Label(self.create_league_frame, text="League name:", bg="#E5E5E5", fg="black")
        self.league_name_entry = tk.Entry(self.create_league_frame, textvariable=self.league_name_var, width=30, fg="black", bg="white")
        self.create_league_button = tk.Button(self.create_league_frame, text="create", command=self.create_button_clicked, highlightbackground="#E5E5E5")
        self.gameweek_timings_id = self.controller.get_gameweek_id()
        self.gameweek_timings = self.get_gameweek_dates(self.gameweek_timings_id)
        self.gameweek_label = tk.Label(self.create_league_frame, text="Start Gameweek: ", bg="#E5E5E5", fg="black")
        self.gameweek_var = tk.StringVar()
        self.gameweek_var.set(self.gameweek_timings[0])
        self.gameweek_drop_down_menu = tk.OptionMenu(self.create_league_frame, self.gameweek_var, *self.gameweek_timings)
        self.gameweek_drop_down_menu.config(bg="#E5E5E5", fg="black")

        self.rules_button = tk.Button(self, text="Game Rules", command=self.rules_button_clicked, highlightbackground="#E5E5E5")

        self.profile_image = tk.PhotoImage(file=r"GUI/images/profile.png").subsample(10,10)
        self.profile_button = tk.Button(self, image=self.profile_image, command=self.rules_button_clicked, highlightbackground="#E5E5E5", relief="flat", bg="#E5E5E5")

        self.place_widgets()

    def place_widgets(self):

        self.title_label.place(x=300, y=0)
        self.view_leagues_frame.place(x=380, y=40)
        self.join_league_tab.place(x=20, y=40)

        self.join_league_title.place(x=40, y=0)
        self.join_league_entry.place(x=10, y=60)
        self.join_league_button.place(x=10, y=110)
        self.join_league_text.place(x=10, y=30)
        self.message_label.place(x=10, y=90)


        self.league_id_label.grid(row=0, column =0)
        self.league_name_label.grid(row=0, column =1)
        self.start_gameweek_label.grid(row=0, column =2)
        for i in range(len(self.league_id)):
            self.league_id[i].grid(row=i+1, column =0)
            self.league_name[i].grid(row=i+1, column =1)
            self.start_gameweek[i].grid(row=i+1, column =2)


        self.create_league_frame.place(x=20, y=200)

        self.create_league_title.place(x=50, y=0)
        self.create_league_label.place(x=10, y=25)
        self.label_league_name.place(x=10, y=45)
        self.league_name_entry.place(x=10, y=65)
        self.gameweek_label.place(x=10, y=100)
        self.gameweek_drop_down_menu.place(x=10, y=125)
        self.create_league_button.place(x=10, y=145)

        self.profile_button.place(x=768, y=0)
        self.rules_button.place(x=0, y=0)

    def join_league_clicked(self):
        try:
            current_gameweek = self.controller.get_league_starting_gameweek(self.join_league_var.get())
            self.controller.show_league_selection_page(self.user_id, self.join_league_var.get(), current_gameweek)
        except ValueError as error:
            self.show_join_league_error(error)

    def show_join_league_error(self, error):
        self.message_label['text'] = error
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def hide_message(self):
        self.message_label['text'] = ''
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

    def rules_button_clicked(self):
        self.controller.show_rules_page(self.user_id)
    def profile_clicked(self):
        self.sign_out_button = tk.Button(self, text="Sign Out", command=self.sign_out_clicked, highlightbackground="#E5E5E5")
        self.sign_out_button.place(x=700, y=20)
    def create_button_clicked(self):
        gameweek_id = self.get_gameweek_id_final()
        self.controller.add_league(gameweek_id, self.league_name_entry.get())
        league_gameweek = self.controller.get_final_league_gameweek()
        #self.controller.add_user_league(self.user_id, league_gameweek[0])
        self.controller.show_league_selection_page(self.user_id, league_gameweek[0], gameweek_id)

    def sign_out_clicked(self):
        self.controller.show_frame("sign_in_frame")