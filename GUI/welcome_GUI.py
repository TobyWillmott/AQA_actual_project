import tkinter as tk


class WelcomeScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(background="white")
        self.controller = parent
        self.welcome_label = tk.Label(self, text="Username:")
        self.sign_in_button = tk.Button(self, text="Sign in", command=self.sign_in_clicked)
        self.register_button = tk.Button(self, text="Register", command=self.register_clicked)

        self.place_widgets()

    def place_widgets(self):
        self.welcome_label.grid(row=1, column=0)
        self.sign_in_button.grid(row=2, column=0)
        self.register_button.grid(row=2, column=1)

    def sign_in_clicked(self):
        self.controller.show_frame("sign_in_frame")

    def register_clicked(self):
        self.controller.show_frame("register_frame")



