import tkinter as tk
from functools import partial
from GUI.vertical_scrolled_frame import VerticalScrolledFrame
class HomeScreen(tk.Frame):
    '''
    This class is used to show the home screen to the user once they have logged in. It has three seperate frames:
    Create league frame: used to create a league
    Join league frame: used to join a legaue
    View league frame: allows you to view the leagues you are currently part of
    '''
    def __init__(self, parent, user_id):
        '''
        This method is used to initialise all the widgets and attributes that are part of the screen

        Parameters
        ----------
        parent - parent class of the tkinter frame which is also used as the controller
        user_id: user_id of the user that is logged in
        '''
        super().__init__(parent)
        self.configure(background="#E5E5E5")

        self.join_league_tab = tk.Frame(self, width=320, height=150, bg="#E5E5E5", highlightbackground="black", highlightthickness=3)
        self.create_league_frame = tk.Frame(self, width=320, height=185, bg="#E5E5E5", highlightbackground="black", highlightthickness=3)
        self.view_leagues_frame = VerticalScrolledFrame(self, width=380, height=345, bg="#E5E5E5", highlightbackground="black", highlightthickness=3)

        self.title_label = tk.Label(self,
                                    text="Football survivor",
                                    bg="#E5E5E5", fg="black",
                                    width=0,
                                    font=("Arial", 20))
        self.user_id = user_id
        self.controller = parent
        self.join_league_var = tk.StringVar()

        # join league widgets
        self.join_league_title = tk.Label(self.join_league_tab, text="Join a league", bg="#E5E5E5", fg="black",font=("Arial", 17))
        self.join_league_entry = tk.Entry(self.join_league_tab, textvariable=self.join_league_var, width=48, bg="white", fg="black")
        self.join_league_button = tk.Button(self.join_league_tab, text="Join", command=self.join_league_clicked, highlightbackground="#E5E5E5", padx=131, pady=6, activebackground="#545354", relief="flat", bg="grey")
        self.join_league_text = tk.Label(self.join_league_tab, text="To join a league please enter a unique league id", bg="#E5E5E5", fg="black")
        self.join_message_label = tk.Label(self.join_league_tab, text='', foreground='red', bg="#E5E5E5")

        # user leagues widgets
        self.user_leagues = self.controller.get_user_league_info(self.user_id)
        self.league_id_label = tk.Label(self.view_leagues_frame, text="League ID", bg="#E5E5E5", fg="black")
        self.league_name_label = tk.Label(self.view_leagues_frame, text="League Name", bg="#E5E5E5", fg="black")
        self.start_gameweek_label = tk.Label(self.view_leagues_frame, text="Start Gameweek", bg="#E5E5E5", fg="black")
        self.league_id = [tk.Button(self.view_leagues_frame, text=name[0], command=partial(self.view_league_clicked, name[0]), highlightbackground="#E5E5E5", activebackground="#545354", relief="flat", bg="grey", width=2) for name in
                          self.user_leagues]
        self.league_name = [tk.Label(self.view_leagues_frame, text=name[1], fg='black', bg="#E5E5E5") for name in self.user_leagues]
        self.start_gameweek = [tk.Label(self.view_leagues_frame, text=name[2], fg='black', bg="#E5E5E5") for name in self.user_leagues]
        self.league_name_var = tk.StringVar()

        # Create league widgets
        self.create_league_title = tk.Label(self.create_league_frame, text="Create a League", bg="#E5E5E5", fg="black", font=("Arial", 14))
        self.create_league_label = tk.Label(self.create_league_frame, text="To create a league enter a league name and the starting \n gameweek (this is when the league will start from)", bg="#E5E5E5", fg="black")
        self.label_league_name = tk.Label(self.create_league_frame, text="League name:", bg="#E5E5E5", fg="black")
        self.league_name_entry = tk.Entry(self.create_league_frame, textvariable=self.league_name_var, width=48, bg="white", fg="black")
        self.create_league_button = tk.Button(self.create_league_frame, text="create", command=self.create_button_clicked, highlightbackground="#E5E5E5", padx=127, pady=2, activebackground="#545354", relief="flat", bg="grey")
        self.gameweek_timings_id = self.controller.get_gameweek_id()
        self.gameweek_timings = self.get_gameweek_dates(self.gameweek_timings_id)
        self.gameweek_label = tk.Label(self.create_league_frame, text="Start Gameweek: ", bg="#E5E5E5", fg="black")
        self.gameweek_var = tk.StringVar()
        self.gameweek_var.set(self.gameweek_timings[0])
        self.gameweek_drop_down_menu = tk.OptionMenu(self.create_league_frame, self.gameweek_var, *self.gameweek_timings)
        self.gameweek_drop_down_menu.config(bg="grey", fg="black", relief="flat", highlightbackground="#E5E5E5")
        self.create_message_label = tk.Label(self.create_league_frame, text='', foreground='red', bg="#E5E5E5")

        self.rules_button = tk.Button(self, text="Game Rules", command=self.rules_button_clicked, highlightbackground="#E5E5E5", relief="flat", bg="grey", activebackground="#545354")

        self.profile_image = tk.PhotoImage(file=r"GUI/images/profile.png").subsample(10,10)
        self.profile_button = tk.Button(self, image=self.profile_image, command=self.profile_clicked, highlightbackground="#545354", relief="flat", bg="#E5E5E5")

        self.place_widgets()

    def place_widgets(self):
        '''
        This subroutine is used to place all of the widgets that are initialised in the __init__ method.
        To do this either the .place or .grid command is used
        '''
        self.title_label.place(x=300, y=0)
        self.view_leagues_frame.place(x=380, y=40)
        self.join_league_tab.place(x=20, y=40)

        self.join_league_title.place(x=80, y=0)
        self.join_league_entry.place(x=10, y=56)
        self.join_league_button.place(x=10, y=100)
        self.join_league_text.place(x=10, y=30)
        self.join_message_label.place(x=10, y=77)


        self.league_id_label.grid(row=0, column =0)
        self.league_name_label.grid(row=0, column =1)
        self.start_gameweek_label.grid(row=0, column =2)
        for i in range(len(self.league_id)):
            self.league_id[i].grid(row=i+1, column =0)
            self.league_name[i].grid(row=i+1, column =1)
            self.start_gameweek[i].grid(row=i+1, column =2)


        self.create_league_frame.place(x=20, y=200)

        self.create_league_title.place(x=75, y=0)
        self.create_league_label.place(x=10, y=25)
        self.label_league_name.place(x=10, y=56)
        self.league_name_entry.place(x=10, y=76)
        self.gameweek_label.place(x=10, y=94)
        self.gameweek_drop_down_menu.place(x=10, y=113)
        self.create_league_button.place(x=10, y=146)
        self.create_message_label.place(x=170, y=105)

        self.profile_button.place(x=768, y=0)
        self.rules_button.place(x=10, y=10)

    def join_league_clicked(self):
        '''
        This function is run when the join_league_button is pressed
        It is used to show the league selection page if successful
        If not displays a suitable error message to the user through the show_join_league_error function
        '''
        try:
            current_gameweek = self.controller.get_league_starting_gameweek(self.join_league_var.get())
            self.controller.show_league_selection_page(self.user_id, self.join_league_var.get(), current_gameweek)
        except ValueError as error:
            self.show_join_league_error(error)

    def show_join_league_error(self, error):
        '''
        This subroutine is used to display a suitable error messge to the user which is removed after 3 seconds
        Parameters
        ----------
        error - the error that has arisen from joining a league
        '''
        self.join_message_label['text'] = error
        self.join_message_label['foreground'] = 'red'
        self.join_message_label.after(3000, self.hide_message)

    def hide_message(self):
        '''
        This subroutine is used to remove the error message that is shown to the user
        '''
        self.join_message_label['text'] = ''
        self.create_message_label["text"] = ""

    def show_create_league_error(self, error):
        '''
        This subroutine is used to display a suitable error message to the user
        Parameters
        ----------
        error - the error that has arisen from creating a league

        '''
        self.create_message_label['text'] = error
        self.create_message_label['foreground'] = 'red'
        self.create_message_label.after(3000, self.hide_message)

    def view_league_clicked(self, league_id):
        '''
        This subroutine is run when the league_id button is clicked using the league_id as a parameter specifying the league they would like to join
        It is used to show the view league page
        Parameters
        ----------
        league_id: the league_id of the league they would like to view
        '''
        self.controller.show_view_league_page(self.user_id, league_id)

    def get_gameweek_dates(self, lis):
        '''
        This subroutine is used to convert the gameweek_timings_id which is a two-dimensional list containing gameweek_id and start_date into a list with only start_date
        Parameters
        ----------
        lis

        Returns
        -------

        '''
        lis_new = []
        for i in lis:
            lis_new.append(i[1])
        return lis_new

    def get_gameweek_id_final(self):
        '''
        this subroutine is used to get the corresponding gameweek id from the gameweek date selected
        Returns
        -------
        the gameweek id
        '''
        for i in self.gameweek_timings:
            if i.strftime("%Y-%m-%d %H:%M:%S") == self.gameweek_var.get():
                gameweek = i

        for j in self.gameweek_timings_id:
            if j[1] == gameweek:
                return j[0]

    def rules_button_clicked(self):
        '''
        This subroutine is used to show the rules frame when the rules button is clicked
        '''
        self.controller.show_rules_page(self.user_id)
    def profile_clicked(self):
        '''
        This subroutine is used to show the sign out button when the profile button is clicked.
        The sign out button disappears after 3 seconds
        Returns
        -------

        '''
        self.sign_out_button = tk.Button(self, text="Sign Out", command=self.sign_out_clicked,  highlightbackground="#E5E5E5", relief="flat", bg="grey", activebackground="#545354")
        self.sign_out_button.place(x=700, y=10)
        self.sign_out_button.after(3000, self.hide_sign_out)
    def hide_sign_out(self):
        '''
        This subroutine is used to remove the sign out button
          '''
        self.sign_out_button.destroy()
    def create_button_clicked(self):
        '''
        This subroutine is used whent the create_league_button is clicked
        If successful it will show the league selection page to the user
        If not it will show the appropriate error to the user
        '''
        try:
            gameweek_id = self.get_gameweek_id_final()
            self.controller.add_league(gameweek_id, self.league_name_entry.get())
            league_gameweek = self.controller.get_final_league_gameweek()
            #self.controller.add_user_league(self.user_id, league_gameweek[0])
            self.controller.show_league_selection_page(self.user_id, league_gameweek[0], gameweek_id)
        except ValueError as error:
            self.show_create_league_error(error)

    def sign_out_clicked(self):
        '''
        This subroutine is used to return the user to the sign in frame
        '''
        self.controller.show_frame("sign_in_frame")