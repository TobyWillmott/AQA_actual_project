import tkinter as tk


class Registration(tk.Frame):
    '''
    This class is used to show the registration page to the user
    '''
    def __init__(self, parent):
        '''
        This method is used to initialise all the widgets and attributes that are part of the screen
        Parameters
        ----------
        parent - parent class of the tkinter frame which is also used as the controller
        '''
        super().__init__(parent)
        self.configure(background="#E5E5E5")

        self.images = {"view": tk.PhotoImage(file=r"GUI/images/view.png").subsample(19, 19),
                       "hide": tk.PhotoImage(file=r"GUI/images/hide.png").subsample(19, 19),
                       "back": tk.PhotoImage(file=r"GUI/images/back_button.png").subsample(19,19)}

        self.view_button = tk.Button(self, image=self.images["view"], command=self.view_clicked, relief="flat", bg="white")
        self.title_label = tk.Label(self,
                                    text="Welcome to football survivor",
                                    bg="#e7e6ed", fg="black",
                                    width=0,
                                    font=("Arial", 25))

        self.controller = parent
        self.label_first_name = tk.Label(self, text="First Name:", bg="#E5E5E5", fg="black")

        self.label_second_name = tk.Label(self, text="Second Name:", bg="#E5E5E5", fg="black")

        # label
        self.label_username = tk.Label(self, text="Username:", bg="#E5E5E5", fg="black")

        self.label_password = tk.Label(self, text='Password: ', bg="#E5E5E5", fg="black")

        self.first_name_var = tk.StringVar()
        self.first_name_entry = tk.Entry(self, textvariable=self.first_name_var, width=25, fg="black", font=('Arial', 20), bg="white")

        self.second_name_var = tk.StringVar()
        self.second_name_entry = tk.Entry(self, textvariable=self.second_name_var, width=25, fg="black", font=('Arial', 20), bg="white")

        # username entry
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(self, textvariable=self.username_var, width=25, fg="black", font=('Arial', 20), bg="white")

        # password entry
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self, textvariable=self.password_var, width=25, fg="black",font=('Arial', 20), bg="white", show="*")

        # save button
        self.save_button = tk.Button(self, text='Create Account', command=self.save_button_clicked, highlightbackground="#E5E5E5", padx=144, pady=10, relief="flat")

        # message
        self.message_label = tk.Label(self, text='', foreground='red', bg="#E5E5E5")

        self.back_button = tk.Button(self, image=self.images["back"] , command=self.back_clicked, highlightbackground="#E5E5E5", relief="flat", bg="#E5E5E5")



        self.place_widgets()

    def place_widgets(self):
        '''
        This subroutine is used to place all the widgets
        '''
        self.back_button.place(x=0, y=0)
        self.title_label.place(x=200, y=0)
        self.label_first_name.place(x=200, y=40)
        self.first_name_entry.place(x=200, y=65)
        self.label_second_name.place(x=200, y=110)
        self.second_name_entry.place(x=200, y=135)
        self.label_username.place(x=200, y=180)
        self.username_entry.place(x=200, y=205)
        self.label_password.place(x=200, y=250)
        self.password_entry.place(x=200, y=275)
        self.message_label.place(x=200, y=315)
        self.save_button.place(x=200, y=345)
        self.view_button.place(x=538, y=277)
        self.view_button.lift()


    def view_clicked(self):
        '''
        This subroutine converts the password text from asteriks to text or text to asteriks (allows the user to hide or show the password)
        '''
        if self.view_button.cget('image')==str(self.images["view"]):
            self.view_button.configure(image=self.images["hide"])
            self.password_entry.configure(show="")

        elif self.view_button.cget('image') == str(self.images["hide"]):
            self.view_button.configure(image=self.images["view"])
            self.password_entry.configure(show="*")

    def save_button_clicked(self):
        '''
        This subroutine is run when the save_button is clicked and either shows the home_page to the user if successful or displays an appropiate error message
        '''
        try:
            if self.controller:
                clicked = self.controller.add_user(self.first_name_var.get(), self.second_name_var.get(),
                                                   self.username_var.get(), self.password_var.get())
                self.show_home_page()
        except ValueError as error:
            self.show_error(error)

    def show_home_page(self):
        '''
        This subroutine is used to show the home page once the user has successfully created an account
        '''
        self.user_list = self.controller.get_username_details(self.username_var.get())
        id = self.user_list[0]
        self.password_var.set("")
        self.username_var.set("")
        self.first_name_var.set("")
        self.second_name_var.set("")
        self.controller.show_home_page(id)

    def show_error(self, message):
        '''
        This subroutine is used to show the appropriate error message to the user
        Parameters
        ----------
        message
        '''
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def hide_message(self):
        '''
        This subroutine is used to hide the error message that is displayed to the user
        '''
        self.message_label['text'] = ''


    def back_clicked(self):
        '''
        This subroutine is when the back_button is clicked and the user is returned to the sign_in_frame
        '''
        self.username_var.set("")
        self.password_var.set("")
        self.first_name_var.set("")
        self.second_name_var.set("")
        self.controller.show_frame("sign_in_frame")
