# password_manager.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from customtkinter import *
from utils.file_utils import load_passwords, save_passwords
from utils.crypto_utils import decrypt_password, encrypt_password

class PasswordManagerApp:
    def __init__(self, root: tk, username: str) -> None:
        self.root = root
        self.root.title("Password Manager")

        # Calculate screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Window dimensions
        window_width = 650
        window_height = 570

        # Calculate position
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

        self.username = username
        self.passwords = load_passwords()
        if username not in self.passwords:
            self.passwords[username] = {}

        # UI Elements

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

        # Other button attributes
        button_width = 200

        ################################################################################

        # Background color for the window
        self.root.configure(bg=navy_blue)

        # Center frame to center everything
        self.center_frame = tk.Frame(self.root, bg=navy_blue)
        self.center_frame.pack(expand=True, fill="both")

        # Logout button
        self.logout_button = CTkButton(
            master=self.root,
            text="Logout",
            font=changa_small,
            text_color="orange",
            fg_color=navy_blue, 
            bg_color=navy_blue,  # Background color
            command=self.logout_screen
        )
        self.logout_button.pack(pady=8)

        # Frame to hold the listbox and scrollbar
        self.listbox_frame = tk.Frame(master=self.center_frame, bg=navy_blue)
        self.listbox_frame.pack(pady=10, padx=10)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Passwords listbox
        self.password_listbox = tk.Listbox(
            master=self.listbox_frame,
            font=changa_small,
            background=baby_green,
            foreground=navy_blue,
            selectmode=tk.SINGLE,  # Allow only one selection at a time
            yscrollcommand=self.scrollbar.set,  # Link listbox scrolling to scrollbar
            width=30,
            height=10
        )
        self.password_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Configure the scrollbar to work with the listbox
        self.scrollbar.config(command=self.password_listbox.yview)

        # Buttons grid (frame)
        self.buttons_frame = tk.Frame(self.root, bg=navy_blue)
        self.buttons_frame.pack(expand=True, fill="both")

        # Buttons frame
        self.buttons_frame = tk.Frame(master=self.center_frame, bg=navy_blue)
        self.buttons_frame.pack(pady=10)

        # Add Button
        self.add_button = CTkButton(
            master=self.buttons_frame,
            text="Add Password",
            corner_radius=32,
            font=changa,
            text_color=baby_green,
            fg_color="orange",
            width=button_width,
            hover=True, 
            hover_color=navy_blue,
            command=self.add_password
        )
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        # View Button
        self.view_button = CTkButton(
            master=self.buttons_frame,
            text="View Password",
            corner_radius=32,
            font=changa,
            text_color=baby_green,
            fg_color="orange",
            width=button_width,
            hover=True, 
            hover_color=navy_blue,
            command=self.view_password
        )
        self.view_button.grid(row=0, column=1, padx=5, pady=5)

        # Modify Button
        self.modify_button = CTkButton(
            master=self.buttons_frame,
            text="Modify password",
            corner_radius=32,
            font=changa,
            text_color=baby_green,
            fg_color="orange",
            width=button_width,
            hover=True, 
            hover_color=navy_blue,
            command=self.modify_password
        )
        self.modify_button.grid(row=1, column=0, padx=5, pady=5)

        # Delete Button
        self.delete_button = CTkButton(
            master=self.buttons_frame,
            text="Delete password",
            corner_radius=32,
            font=changa,
            text_color=baby_green,
            fg_color="orange",
            width=button_width,
            hover=True, 
            hover_color=navy_blue,
            command=self.delete_password
        )
        self.delete_button.grid(row=1, column=1, padx=5, pady=5)

        self.update_listbox()

    def update_listbox(self):
        """
        Update the listbox with the current user's services.
        """
        # Clear all items in the listbox
        self.password_listbox.delete(0, tk.END)
        
        # Populate the listbox with services
        for service in self.passwords[self.username]:
            self.password_listbox.insert(tk.END, service)

    def add_password(self):
        service = simpledialog.askstring("Service", "Enter the service name:")
        if service:
            password = simpledialog.askstring("Password", "Enter the password:", show="*")
            if password:
                encrypted = encrypt_password(password)
                self.passwords[self.username][service] = encrypted
                save_passwords(self.passwords)
                self.update_listbox()
                messagebox.showinfo("Success", "Password added successfully.")

    def view_password(self):
        selected = self.password_listbox.curselection()
        if selected:
            service = self.password_listbox.get(selected)
            encrypted = self.passwords[self.username][service]
            decrypted = decrypt_password(encrypted)
            messagebox.showinfo("Password", f"The password for {service} is: {decrypted}")
        else:
            messagebox.showerror("Error", "Please select a service.")

    def delete_password(self):
        selected = self.password_listbox.curselection()
        if selected:
            service = self.password_listbox.get(selected)
            del self.passwords[self.username][service]
            save_passwords(self.passwords)
            self.update_listbox()
            messagebox.showinfo("Success", "Password deleted successfully.")
        else:
            messagebox.showerror("Error", "Please select a service.")

    def modify_password(self):
        selected = self.password_listbox.curselection()
        if selected:
            service = self.password_listbox.get(selected)
            new_password = simpledialog.askstring("Modify Password", f"Enter a new password for {service}:", show="*")
            if new_password:
                encrypted = encrypt_password(new_password)
                self.passwords[self.username][service] = encrypted
                save_passwords(self.passwords)
                messagebox.showinfo("Success", "Password modified successfully.")
        else:
            messagebox.showerror("Error", "Please select a service.")
    
    def logout_screen(self):
        """
        Handles logout functionality.
        Returns the user to the login screen.
        """
        # Destroy the current password manager screen
        self.root.destroy()


if __name__ == "__main__":
    root = CTk()
    app = PasswordManagerApp(root, "example_user")
    root.mainloop()
