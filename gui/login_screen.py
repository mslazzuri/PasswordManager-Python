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
        
        self.root: CTk = root
        self.root.title("Login")
        
        # Calculate screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Window dimensions
        window_width = 700
        window_height = 650

        # Calculate position
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
        self.users: dict = load_users()

        ################################################################################

        # UI Colors
        navy_blue: str = "#05445e"
        blue_grotto: str = "#189ab4"
        blue_green: str = "#75e6da"
        baby_green: str = "#d4f1f4"
        white: str = "#ffffff"

        # UI Fonts
        helvetica_bold: tuple[str, int, str] = ("Helvetica", 20, "bold")
        goldman: tuple[str, int, str] = ("Goldman", 20, "bold")
        changa: tuple[str, int, str] = ("Changa", 20)
        changa_small: tuple[str, int, str] = ("Changa", 14)
        arial: tuple[str, int, str] = ("Arial", 10)

        ################################################################################

        # Set background color for the window
        self.root.config(bg=navy_blue)

         # Create a frame to center elements
        self.center_frame = tk.Frame(self.root, bg=navy_blue)
        self.center_frame.pack(expand=True, fill="both")

        # UI Elements

        # Logo
        logo_path = "/Users/matheussecco/PasswordManager/PasswordManagerApp/pictures/logo.png"

        original_image = Image.open(logo_path)
        new_width = 300
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
        logo_label.pack(pady=10)

        # Username
        self.username_entry = CTkEntry(
            master=self.root,
            placeholder_text="Username",
            placeholder_text_color=navy_blue,
            text_color=navy_blue,
            font=changa,
            bg_color=navy_blue,
            fg_color=baby_green,
            border_color=baby_green,
            width=200,
            height=50,
            corner_radius=50
        )
        self.username_entry.pack(pady=10)

        # Password Frame (to simulate the password entry with an embedded button)
        self.password_frame = tk.Frame(self.root, bg=navy_blue)
        self.password_frame.pack(pady=10)

        # Password Entry
        self.password_entry = CTkEntry(
            master=self.password_frame,
            placeholder_text="Password",
            placeholder_text_color=navy_blue,
            text_color=navy_blue,
            font=changa,
            bg_color=navy_blue,
            fg_color=baby_green,
            border_color=baby_green,
            width=200,
            height=50,
            corner_radius=50,
            show="*",
        )
        self.password_entry.pack(side="top", fill="x", expand=True)

        # Eye Button
        eye_image_path = "/Users/matheussecco/PasswordManager/PasswordManagerApp/pictures/eye.jpg"
        self.show_password = False

        # Load image with transparency
        eye_image = Image.open(eye_image_path).convert("RGBA")
        self.eye_icon = ImageTk.PhotoImage(eye_image.resize((20, 20)))

        # Transparent button with the same background color as the application
        self.eye_button = CTkButton(
            master=self.password_frame,
            image=self.eye_icon,
            width=30,
            height=30,
            fg_color="transparent",  # or match bg_color of the password_frame
            hover_color=baby_green,  # Optional: Set a hover color
            text="",
            command=self.toggle_password_visibility,
        )
        self.eye_button.pack(pady=10)

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
            font=changa_small,
            command=self.login,
        )
        self.login_button.pack(pady=10)

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
            font=changa_small,
            command=self.register,
        )
        self.register_button.pack(pady=10)

    def login(self) -> None:
        """
        Login method.
        Hashes password given by user and compares to the stored hash.
        """
        
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users:
            stored_hash = self.users[username]
            if verify_password(password, stored_hash):
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                self.root.destroy()
                self.launch_password_manager(username)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
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

    def toggle_password_visibility(self) -> None:
        """
        Changest the password visibility when user clicks on eye logo.
        """
        self.show_password = not self.show_password  # Toggle state

        if self.show_password:
            self.password_entry.configure(show="")  # Show plain text
        else:
            self.password_entry.configure(show="*")  # Mask the password        

# Import Guard
if __name__ == "__main__":  # pragma: no cover
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()