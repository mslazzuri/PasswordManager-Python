# login_screen.py
import tkinter as tk
from tkinter import messagebox
from customtkinter import *
from utils.file_utils import load_users, save_users
from utils.crypto_utils import hash_password, verify_password
from gui.password_manager import PasswordManagerApp
from PIL import Image, ImageTk

class LoginScreen:
    """Defines the Login Screen UI and its functions."""

    def __init__(self, root: CTk) -> None:
        """
        Initialize the Login Screen Window

        Params:
            root (CTk): The CTk main object for the program.
        """
        
        self.root = root
        self.root.title("Login")
        self.users = load_users()

        ################################################################################

        # UI Colors
        navy_blue = "#05445e"
        blue_grotto = "#189ab4"
        blue_green = "#75e6da"
        baby_green = "#d4f1f4"
        white = "#ffffff"

        # UI Fonts
        helvetica_bold = ("Helvetica", 20, "bold")
        goldman = ("Goldman", 20, "bold")
        changa = ("Changa", 20)
        changa_small = ("Changa", 14)
        arial = ("Arial", 10)

        ################################################################################

        # Set background color for the window
        self.root.config(bg=navy_blue)

        # UI Elements

        # Logo
        logo_path = "/Users/matheussecco/PasswordManager/PasswordManagerApp/pictures/logo.png"

        original_image = Image.open(logo_path)
        new_width = 400
        ratio = original_image.height / original_image.width
        new_height = int(new_width * ratio)
        resized_image = original_image.resize((new_width, new_height), None)

        logo = ImageTk.PhotoImage(resized_image)
    
        logo_label = tk.Label(
            self.root,
            image=logo,
            background=navy_blue
        )
        logo_label.image = logo
        logo_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Username
        tk.Label(
            self.root,
            text="Username:",
            background=navy_blue,
            foreground=baby_green,
            font=changa
        ).grid(row=1, column=0, pady=8, padx=8)

        # Username box (user)
        self.username_entry = tk.Entry(self.root, background=baby_green, foreground=navy_blue, font=changa_small)
        self.username_entry.grid(row=1, column=1, pady=8, padx=8)

        # Password
        password_label = CTkLabel(
            master=self.root,
            text="Password:",
            font=changa,
            fg_color=navy_blue,
            bg_color=navy_blue,
            text_color=baby_green
        )
        password_label.grid(row=2, column=0, pady=5, padx=5)

        # Password box (user)
        self.password_entry = tk.Entry(self.root, show="*", background=baby_green, foreground=navy_blue, font=changa_small)
        self.password_entry.grid(row=2, column=1, pady=8, padx=8)

        # Login Button
        self.login_button = CTkButton(
            master=self.root,
            text="Login",
            corner_radius=32,
            fg_color="orange",
            bg_color=navy_blue,
            text_color=baby_green,
            hover=True,
            hover_color=navy_blue,
            font=changa,
            command=self.login,
        )
        self.login_button.grid(row=4, column=0, pady=10)

        # Register User Button
        self.register_button = CTkButton(
            master=self.root,
            text="Register",
            corner_radius=32,
            fg_color=baby_green,
            bg_color=navy_blue,
            text_color="orange",
            hover=True,
            hover_color=navy_blue,
            font=changa,
            command=self.register,
        )
        self.register_button.grid(row=4, column=1)

    def login(self) -> None:
        """
        Login method.
        Hashes password given by user and compares to the stored hash.
        """
        
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hash_password(password)

        if username in self.users and verify_password(password, hashed_password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.root.destroy()
            self.launch_password_manager(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self) -> None:
        """
        Registers user in the user database.
        Hashes password and stores it with the corresponding username.
        """
        
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users:
            messagebox.showerror("Error", "Username already exists.")
        elif not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
        else:
            self.users[username] = hash_password(password)
            save_users(self.users)
            messagebox.showinfo("Success", "User registered successfully.")


    def launch_password_manager(self, username: str) -> None:
        """
        Launches the password manager after login.
        """
        
        manager_root = tk.Tk()
        PasswordManagerApp(manager_root, username)
        manager_root.mainloop()


# Import Guard
if __name__ == "__main__":  # pragma: no cover
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()