import tkinter as tk


class Rules(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)

        self.configure(background="#E5E5E5")
        self.user_id = user_id
        self.controller = parent

        self.title_label = tk.Label(self,
                                    text="Rules",
                                    bg="#E5E5E5", fg="black",
                                    width=0,
                                    font=("Arial", 25))
        self.rules_label = tk.Label(self, text="This will be the text", bg="#E5E5E5", fg="black")
        self.back_button = tk.Button(self, text="Back to homepage", bg="#E5E5E5", command=self.back_clicked)
        self.place_widgets()
    def place_widgets(self):
        self.title_label.place(x=300, y=0)
        self.rules_label.place(x=100, y=50)
        self.back_button.place(x=370, y=370)

    def back_clicked(self):
        self.controller.show_home_page(self.user_id)

