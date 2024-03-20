import tkinter as tk


class Rules(tk.Frame):
    '''
    This class is used to show the rules page to the user
    '''
    def __init__(self, parent, user_id):
        '''
        this method is used to initialise any widgets and attributes that are shown
        Parameters
        ----------
        parent - parent class of the tkinter frame which is also used as the controller
        user_id - user id of the user currently signed in
        '''
        super().__init__(parent)

        self.configure(background="#E5E5E5")
        self.user_id = user_id
        self.controller = parent
        self.text = (
            "Hello welcome to football survivor\n\n We believe this should be a fun and entertaining game for \n"
            "anyone to play. The game is an example of a fantasy football game consisting of leagues. A \n"
            "league is a period of 20 or less gameweeks where you must pick a premier legue team every \n"
            "gameweek. After making your selections as the games are played in real life your will be \n"
            "awarded points based on the number of points the team received in real life. You can create a \n"
            "league by selecting the start gameweek and entering a name. Or you can join a league by having \n"
            "a friend or family member tell you the unique league id. However you can only join a league \n"
            "when the league starting date is in the future as some of the matches will already have been \n"
            "played.\n\n To start we suggest you join a league. To do so return to the homepage and select a \n"
            "league starting gameweek and a name and press create. You will then be shown to a league \n"
            "selection page, you should pick a team for every gameweek, you can only pick a team once.")
        self.title_label = tk.Label(self,
                                    text="Rules",
                                    bg="#E5E5E5", fg="black",
                                    width=0,
                                    font=("Arial", 25))
        self.rules_label = tk.Label(self, text=self.text, bg="#E5E5E5", fg="black")
        self.back_button = tk.Button(self, text="Back to homepage", bg="grey", command=self.back_clicked, highlightbackground="#E5E5E5", padx=70, pady=10, relief="flat")
        self.place_widgets()
    def place_widgets(self):
        '''
        This subroutine is used to place all the widgets
        '''
        self.title_label.place(x=360, y=0)
        self.rules_label.place(x=150, y=50)
        self.back_button.place(x=280, y=340)

    def back_clicked(self):
        '''
        This subroutine returns the user back to the home page
        '''
        self.controller.show_home_page(self.user_id)