import tkinter as tk

class ViewLeague(tk.Frame):
    def __init__(self, parent, user_id, league_id):
        super().__init__(parent)

        self.config(background="#E5E5E5")
        self.user_id = user_id
        self.league_id = league_id
        self.controller = parent

        self.user_ids = self.controller.get_user_ids(self.league_id)
        self.user_names = self.controller.get_user_name(self.user_ids)
        self.lives = self.controller.check_lives(self.user_ids, self.league_id)
        print("lives", self.lives)
        self.total_list = []
        for i in range(len(self.user_ids)):
            lis=[]
            lis.append(self.user_ids[i][0])
            lis.append(self.user_names[i])
            lis.append(self.lives[i])
            self.total_list.append(lis)
        self.total_list.sort(reverse=True, key=lambda x:x[2])
        self.position_label = tk.Label(self, text="Positon", bg="#E5E5E5")
        self.user_label = tk.Label(self, text="Name", bg="#E5E5E5")
        self.lives_label = tk.Label(self, text="Number of lives", bg="#E5E5E5")

        self.positions = [tk.Label(self, text=f"{position+1}", bg="#E5E5E5") for position in range(len(self.user_ids))]
        self.user_names = [tk.Label(self, text=f"{name[1][0]} {name[1][1]}", bg="#E5E5E5") for name in self.total_list]
        self.back_button = tk.Button(self, text="Back", bg="#E5E5E5", command=self.back_clicked)
        self.user_lives = [tk.Label(self, text=f"{lives[2]}", bg="#E5E5E5") for lives in self.total_list]

        self.user_games = self.controller.get_games(self.user_id, self.league_id)
        self.selections_label = tk.Label(self, text=f"Your selections")
        self.place_widgets()
        self.display_matches()

    def place_widgets(self):
        self.position_label.grid(row=1, column=0)
        self.user_label.grid(row=1, column=1)
        self.lives_label.grid(row=1, column=2)
        self.back_button.grid(row=0, column=0)

        self.selections_label.place(x=600, y=0)

        for i in range(len(self.user_ids)):
            self.positions[i].grid(row=2+i, column=0)
            self.user_names[i].grid(row=2+i, column=1)
            self.user_lives[i].grid(row=2+i, column=3)

    def display_matches(self):
        self.gameweek =  [tk.Label(self, text=match[0], fg="black", width=3, font=("Arial", 8), bg="#E5E5E5") for match in self.user_games]
        self.user_teams = [tk.Label(self, text=match[1], fg="black", bg=match[3], width=3, font=("Arial", 8)) for match in self.user_games]
        self.opp_teams = [tk.Label(self, text=match[4], fg="black", bg=match[6], width=3, font=("Arial", 8)) for match in self.user_games]
        self.user_teams_score = [tk.Label(self, text=match[2], fg="black", width=3, font=("Arial", 8), bg="#E5E5E5") for match in self.user_games]
        self.opp_teams_score = [tk.Label(self, text=match[5], fg="black", width=3, font=("Arial", 8),  bg="#E5E5E5") for match in self.user_games]
        print(self.opp_teams_score)
        self.versus_label = [tk.Label(self, text="vs", fg="black", bg="#E5E5E5") for j in range(len(self.user_games))]
        index = 0
        for i in range(len(self.user_games)):
            if i< 10:
                self.gameweek[i].place(x=400, y=20+index*37)
                self.user_teams[i].place(x=425, y=20+index*37)
                self.versus_label[i].place(x=453, y=20+index*37)
                self.opp_teams[i].place(x=475, y=20+index*37)
                self.user_teams_score[i].place(x=425, y=35+index*37)
                self.opp_teams_score[i].place(x=475, y=35 + index * 37)
                index += 1
            else:
                self.gameweek[i].place(x=600, y=20 + (index-10) * 37)
                self.user_teams[i].place(x=625, y=20 + (index-10) * 37)
                self.versus_label[i].place(x=653, y=20 + (index-10) * 37)
                self.opp_teams[i].place(x=675, y=20 + (index-10) * 37)
                self.user_teams_score[i].place(x=625, y=35 + (index-10) * 37)
                self.opp_teams_score[i].place(x=675, y=35 + (index-10) * 37)
                index += 1




    def back_clicked(self):
        self.controller.show_home_page(self.user_id)