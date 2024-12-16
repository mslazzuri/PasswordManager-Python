# login_screen.py
import tkinter as tk
from tkinter import messagebox
from utils.file_utils import load_users, save_users
from utils.crypto_utils import hash_password, verify_password
from gui.password_manager import PasswordManagerApp

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Screen")

        self.users = load_users()

        # UI Colors
        navy_blue = "#05445e"
        blue_grotto = "#189ab4"
        blue_green = "#75e6da"
        baby_green = "#d4f1f4"
        white = "#ffffff"

        # UI Fonts
        helvetica_bold = ("Helvetica", 12, "bold")
        arial = ("Arial", 10)

        # Set background color for the window
        self.root.configure(bg=navy_blue)

        # UI Elements
        tk.Label(root, text="Username:").grid(row=0, column=0, pady=5, padx=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(root, text="Password:").grid(row=1, column=0, pady=5, padx=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, pady=10)

        self.register_button = tk.Button(root, text="Register", command=self.register)
        self.register_button.grid(row=2, column=1, pady=10)

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