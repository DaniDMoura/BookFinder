import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from tkinter import *
from .db_connection import cursor
import os
import re
import bcrypt

class Authentication:
    def __init__(self):
        self.root = ttk.Window(themename="darkly")

        self.sign_up_window = None  
        self.loginwindow = None

        self.username_entry = None
        self.password_entry = None
        self.user_id = None

        self.icon_path = os.path.join("assets", "Icons", "images.png")
        try:
            icon = ttk.PhotoImage(file=self.icon_path)
            self.root.iconphoto(False, icon)
        except Exception as e:
            Messagebox.show_error(f"Icon error: {e}","Error",parent=self.loginwindow)

        self.style = self.root.style
        self.style.configure("little.TLabel",font=("Raleway",4))
        self.style.configure("TLabel", font=("Raleway", 9),foreground="white")
        self.style.configure("TButton", font=("Raleway", 9),foreground="white")
        self.style.configure("TEntry", font=("Raleway", 9),foreground="white")
        self.style.configure("Link.TButton", font=("Raleway", 9),foreground="white")
        self.style.map(
            "Link.TButton",
            foreground=[("active", "#87CEFA")],
            focuscolor=[("focus", "")],
        )
        self.style.map("TButton", focuscolor=[("focus", "")])
        self.style.configure(
            "TButton",
            relief="flat",
            highlightthickness=0,
            borderwidth=0,
            focuscolor="none",
        )

        cursor.execute("USE SelectedBooks;")

    def authentication_sign_up_window(self):
        if self.sign_up_window is None or not self.sign_up_window.winfo_exists():
            self.sign_up_window = Toplevel(self.loginwindow)
            self.sign_up_window.title("Sign-up")
            self.sign_up_window.resizable(False, False)

            framesignup = ttk.Frame(self.sign_up_window)
            framesignup.grid(padx=10, pady=10)

            signup_username_label = ttk.Label(framesignup, text="Username")
            signup_password_label = ttk.Label(framesignup, text="Password")
            signup_confirm_label = ttk.Label(framesignup, text="Confirm?")

            signup_username_entry = ttk.Entry(framesignup, bootstyle="dark")
            signup_password_entry = ttk.Entry(
                framesignup, bootstyle="dark", show="*"
            )
            signup_confirm_entry = ttk.Entry(framesignup, bootstyle="dark", show="*")

            signup_button = ttk.Button(
                framesignup,
                text="Sign Up",
                bootstyle="dark",
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
        self.loginwindow = ttk.Toplevel(self.root)
        self.loginwindow.title("Sign-in")
        self.loginwindow.resizable(False, False)

        self.loginwindow.iconphoto(True, PhotoImage(file=self.icon_path))

        framelogin = ttk.Frame(self.loginwindow)
        framelogin.grid(padx=10, pady=10)

        username_label = ttk.Label(framelogin, text="Username")
        password_label = ttk.Label(framelogin, text="Password")

        self.username_entry = ttk.Entry(framelogin, bootstyle="dark")
        self.password_entry = ttk.Entry(framelogin, bootstyle="dark", show="*")

        submit_button = ttk.Button(
            framelogin, bootstyle="dark", text="Submit", command=self.submit_login
        )

        signup_button = ttk.Button(
            framelogin,
            text="Sign Up",
            bootstyle="link",
            command=self.authentication_sign_up_window,
        )

        username_label.grid(row=0, column=0, padx=5, pady=5)
        password_label.grid(row=1, column=0, padx=5, pady=5)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        submit_button.grid(row=2, column=0, columnspan=2, pady=7)
        signup_button.grid(row=3, column=0, columnspan=2)

        self.root.withdraw()
        self.loginwindow.protocol("WM_DELETE_WINDOW", self.root.quit)

        self.root.mainloop()

    def authentication_validate_sign_up(
        self, signup_username_entry, signup_password_entry, signup_confirm_entry
    ):
        if signup_password_entry.get() != signup_confirm_entry.get():
            Messagebox.show_error(
                "Passwords do not match.", "Error", parent=self.sign_up_window
            )
        elif not re.match("^[a-zA-Z0-9._]*$", signup_username_entry.get()):
            Messagebox.show_error(
                'Username can only contain letters, numbers, "." and "_".',
                "Error",
                parent=self.sign_up_window,
            )
        elif not re.match("^[a-zA-Z0-9._]*$", signup_password_entry.get()):
            Messagebox.show_error(
                'Password can only contain letters, numbers, "." and "_".',
                "Error",
                parent=self.sign_up_window,
            )
        elif len(signup_username_entry.get()) < 8:
            Messagebox.show_error(
                "Username must be at least 8 characters.",
                "Error",
                parent=self.sign_up_window,
            )
        elif len(signup_username_entry.get()) > 50:
            Messagebox.show_error(
                "Username cannot be longer than 50 characters.",
                "Error",
                parent=self.sign_up_window,
            )
        elif len(signup_password_entry.get()) < 8:
            Messagebox.show_error(
                "Password must be at least 8 characters.",
                "Error",
                parent=self.sign_up_window,
            )
        elif len(signup_password_entry.get()) > 255:
            Messagebox.show_error(
                "Password cannot be longer than 255 characters.",
                "Error",
                parent=self.sign_up_window,
            )
        else:
            self.authentication_insert_user(
                signup_username_entry, signup_password_entry
            )

    def authentication_insert_user(self, signup_username_entry, signup_password_entry):
        senha = signup_password_entry.get()
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'),salt).decode('utf-8')
        try:
            cursor.execute(
                "INSERT INTO Users (Login, Password) VALUES (?,?)",
                (signup_username_entry.get(), senha_hash),
            )
            self.sign_up_window.destroy()
            self.sign_up_window = None
        except Exception as e:
            Messagebox.show_error(
                f"Sign-up failed: {str(e)}", "Error", parent=self.sign_up_window
            )

    def submit_login(self):
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()

            if self.authentication_login_validation(username, password):
                cursor.execute(
                    "SELECT UserID FROM Users WHERE Login = ?",
                    (username,)
                )
                result = cursor.fetchone()
                
                if result:
                    self.user_id = result[0]  
                    from .requestdata import main_window
                    self.loginwindow.destroy()
                    main_window(self.root, self.user_id, username, password)
            else:
                Messagebox.show_error(
                    "Login or Password Incorrect.", 
                    "Error", 
                    parent=self.loginwindow
                )

        except Exception as e:
            Messagebox.show_error(
            f"Login error: {str(e)}", 
            "Fatal Error", 
            parent=self.loginwindow
            )

    def authentication_login_validation(self, username, password):
        try:

            cursor.execute("SELECT Password FROM Users WHERE Login = ?",(username,))
            result = cursor.fetchone()

            if not result:
                return False

            senha_hash = result[0].encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'), senha_hash):
                return True
            else:
                return False

        except Exception as e:
            Messagebox.show_error(f"Database error: {str(e)}", "Error", parent=self.loginwindow)
            return False

    def authentication_get_userID(self, username, password):
        try:
            cursor.execute(
                "SELECT UserID FROM Users WHERE Login = ? and Password = ?",
                (username.strip(), password.strip()),
            )
            result = cursor.fetchone()
            if result:
                self.user_id = result[0]
                return True
            return False
        except Exception as e:
            print(f"Erro ao buscar UserID: {e}")
            return False

    def get_userID(self):
        return self.user_id
