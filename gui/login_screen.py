# login_screen.py
import tkinter as tk
from tkinter import messagebox
from utils.file_utils import load_users, save_users
from utils.crypto_utils import hash_password, verify_password
from gui.password_manager import PasswordManagerApp
from PIL import Image, ImageTk

class LoginScreen:
    def __init__(self, root):
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
        self.root.configure(bg=navy_blue)

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
        tk.Label(
            self.root,
            text="Password:",
            background=navy_blue,
            foreground=baby_green,
            font=changa
        ).grid(row=2, column=0, pady=5, padx=5)
        
        # Password box (user)
        self.password_entry = tk.Entry(self.root, show="*", background=baby_green, foreground=navy_blue, font=changa_small)
        self.password_entry.grid(row=2, column=1, pady=8, padx=8)

        # Login Button
        self.login_button = tk.Button(
            self.root,
            text="Login",
            font=changa,
            foreground=navy_blue, 
            background=blue_green,  # Background color
            activebackground=navy_blue,  # Active background when clicked
            activeforeground=blue_green,  # Active text color when clicked
            relief='flat',  # Makes the button flat without borders
            borderwidth=0,  # Removes the border width
            highlightthickness=0,  # Removes the highlight border
            command=self.login
        )
        self.login_button.grid(row=4, column=0, pady=10)

        # Register User Button
        self.register_button = tk.Button(
        self.root, 
        text="Register", 
        font=changa, 
        foreground=navy_blue, 
        background=blue_green,  # Background color
        activebackground=navy_blue,  # Active background when clicked
        activeforeground=blue_green,  # Active text color when clicked
        relief='flat',  # Makes the button flat without borders
        borderwidth=0,  # Removes the border width
        highlightthickness=0,  # Removes the highlight border
        command=self.register
    )

        self.register_button.grid(row=4, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hash_password(password)

        if username in self.users and verify_password(password, hashed_password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.root.destroy()
            self.launch_password_manager(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
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


    def launch_password_manager(self, username):
        manager_root = tk.Tk()
        PasswordManagerApp(manager_root, username)
        manager_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()