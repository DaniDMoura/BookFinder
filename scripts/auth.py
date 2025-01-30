import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from tkinter import *
from .db_connection import cursor
import re


class Authentication():
    def __init__(self):
        self.sign_up_window = None
        self.loginwindow = None
        self.username_entry = None
        self.password_entry = None
        cursor.execute("USE SelectedBooks;")

    def authentication_sign_up_window(self):
        if self.sign_up_window is None or not self.sign_up_window.winfo_exists():
            self.sign_up_window = Toplevel(self.loginwindow)
            self.sign_up_window.title("Sign-up")
            self.sign_up_window.resizable(False, False)

            style = ttk.Style()
            style.theme_use("cyborg")
            style.configure("TLabel", font=("Raleway", 8))
            style.configure("TButton", font=("Raleway", 8))

            framesignup = ttk.Frame(self.sign_up_window)
            framesignup.grid(padx=10, pady=10)

            signup_username_label = ttk.Label(framesignup, text="Username", style="TLabel")
            signup_password_label = ttk.Label(framesignup, text="Password", style="TLabel")
            signup_confirm_label = ttk.Label(framesignup, text="Confirm?", style="TLabel")

            signup_username_entry = ttk.Entry(framesignup, bootstyle="success")
            signup_password_entry = ttk.Entry(framesignup, bootstyle="success", show="*")
            signup_confirm_entry = ttk.Entry(framesignup, bootstyle="success", show="*")

            signup_button = ttk.Button(
                framesignup,
                text="Sign Up",
                bootstyle="success",
                command=lambda: self.authentication_validate_sign_up(
                    signup_username_entry, signup_password_entry, signup_confirm_entry
                ),
            )

            signup_username_label.grid(row=0, column=0, padx=5, pady=5)
            signup_password_label.grid(row=1, column=0, padx=5, pady=5)
            signup_confirm_label.grid(row=2, column=0, padx=5, pady=5)
            signup_username_entry.grid(row=0, column=1, padx=5, pady=5)
            signup_password_entry.grid(row=1, column=1, padx=5, pady=5)
            signup_confirm_entry.grid(row=2, column=1, padx=5, pady=5)
            signup_button.grid(row=3, column=0, columnspan=2, pady=10)

            self.sign_up_window.protocol("WM_DELETE_WINDOW", self.fechar_sign_up_window)


    def fechar_sign_up_window(self):
        if self.sign_up_window is not None:
            self.sign_up_window.destroy()
            self.sign_up_window = None


    def authentication_sign_in_window(self):
        self.loginwindow = Tk()
        self.loginwindow.title("Sign-in")
        self.loginwindow.iconphoto(True, PhotoImage(file="assets/Icons/images.png"))
        self.loginwindow.resizable(False, False)

        style = ttk.Style()
        style.theme_use("cyborg")
        style.configure("TLabel", font=("Raleway", 8))
        style.configure("Link.TButton", font=("Raleway", 8))
        style.map(
            "Link.TButton", foreground=[("active", "#87CEFA")], focuscolor=[("focus", "")]
        )
        style.map("TButton", focuscolor=[("focus", "")])
        style.configure(
            "TButton", relief="flat", highlightthickness=0, borderwidth=0, focuscolor="none"
        )

        framelogin = ttk.Frame(self.loginwindow)
        framelogin.grid(padx=10, pady=10)

        username_label = ttk.Label(framelogin, text="Username")
        password_label = ttk.Label(framelogin, text="Password")

        self.username_entry = ttk.Entry(framelogin, bootstyle="success")
        self.password_entry = ttk.Entry(framelogin, bootstyle="success", show="*")

        submit_button = ttk.Button(framelogin, bootstyle="success", text="Submit",command=self.submit_login)

        signup_button = ttk.Button(
            framelogin,
            text="Sign Up",
            bootstyle="link",
            command=self.authentication_sign_up_window
        )

        username_label.grid(row=0, column=0, padx=5, pady=5)
        password_label.grid(row=1, column=0, padx=5, pady=5)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        submit_button.grid(row=2, column=0, columnspan=2, pady=7)
        signup_button.grid(row=3, column=0, columnspan=2)

        self.loginwindow.mainloop()


    def authentication_validate_sign_up(
        self,signup_username_entry, signup_password_entry, signup_confirm_entry
    ):
        if signup_password_entry.get() != signup_confirm_entry.get():
            Messagebox.show_error("Passwords do not match.", "Error")
        elif not re.match("^[a-zA-Z0-9._]*$", signup_username_entry.get()):
            Messagebox.show_error('Username can only contain letters, numbers, "." and "_".', "Error")
        elif not re.match("^[a-zA-Z0-9._]*$", signup_password_entry.get()):
            Messagebox.show_error('Password can only contain letters, numbers, "." and "_".', "Error")
        elif len(signup_username_entry.get()) < 8:
            Messagebox.show_error("Username must be at least 8 characters.", "Error")
        elif len(signup_username_entry.get()) > 50:
            Messagebox.show_error("Username cannot be longer than 50 characters.", "Error")
        elif len(signup_password_entry.get()) < 8:
            Messagebox.show_error("Password must be at least 8 characters.", "Error")
        elif len(signup_password_entry.get()) > 255:
            Messagebox.show_error("Password cannot be longer than 255 characters.", "Error")
        else:
            self.authentication_insert_user(signup_username_entry, signup_password_entry)


    def authentication_insert_user(self,signup_username_entry, signup_password_entry):
        try:
            cursor.execute("INSERT INTO Users VALUES (?,?)",(signup_username_entry.get(), signup_password_entry.get()))
            print(f"User {signup_username_entry.get()} is logged")
            self.sign_up_window.destroy()
            self.sign_up_window = None
        except Exception as e:
            Messagebox.show_error(f"Sign-up failed: {str(e)}","Error")

    def submit_login(self):
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()

            if not username or not password:
                Messagebox.show_error("Username or Password cannot be empty.", "Error")
                return
            
            if self.authentication_login_validation(username,password):
                from .requestdata import main_window
                print("antes de chamar main_window")
                main_window()
                print("depois de chamar main_window")
                self.loginwindow.after(100, self.loginwindow.destroy)
                
                
        except Exception as e:
            Messagebox.show_error(f"Login failed: {str(e)}","Error")


    def authentication_login_validation(self,username,password):
        cursor.execute("SELECT * FROM Users WHERE Login = ? and Password = ?",(username,password))            
                    
        result = cursor.fetchall()

        if not result:
            Messagebox.show_error("Login or Password Incorrect.", "Error")
            return False
        else:
            return True
    
