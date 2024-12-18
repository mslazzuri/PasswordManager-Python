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
        button_width = 10

        ################################################################################

        # Background color for the window
        self.root.configure(bg=navy_blue)

        # Logout button
        self.logout_button = tk.Button(
            root,
            text="Logout",
            font=changa_small,
            foreground=navy_blue, 
            background=blue_green,  # Background color
            activebackground=navy_blue,  # Active background when clicked
            activeforeground=blue_green,  # Active text color when clicked
            relief='flat',  # Makes the button flat without borders
            borderwidth=0,  # Removes the border width
            highlightthickness=0,  # Removes the highlight border
            width=button_width,
            command=self.logout_screen
        )
        self.logout_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Passwords list box
        self.password_listbox = tk.Listbox(
            root,
            font=changa_small,
            background=baby_green,
            foreground=navy_blue,
            width=50
        )
        self.password_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Add Button
        self.add_button = tk.Button(
            root,
            text="Add Password",
            font=changa_small,
            foreground=navy_blue, 
            background=blue_green,  # Background color
            activebackground=navy_blue,  # Active background when clicked
            activeforeground=blue_green,  # Active text color when clicked
            relief='flat',  # Makes the button flat without borders
            borderwidth=0,  # Removes the border width
            width=button_width,
            highlightthickness=0,  # Removes the highlight border
            
            command=self.add_password
        )
        self.add_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        # View Button
        self.view_button = tk.Button(
            root,
            text="View Password",
            font=changa_small,
            foreground=navy_blue, 
            background=blue_green,  # Background color
            activebackground=navy_blue,  # Active background when clicked
            activeforeground=blue_green,  # Active text color when clicked
            relief='flat',  # Makes the button flat without borders
            borderwidth=0,  # Removes the border width
            highlightthickness=0,  # Removes the highlight border
            width=button_width,
            command=self.view_password
        )
        self.view_button.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        # Delete Button
        self.delete_button = tk.Button(
            root,
            text="Delete Password",
            font=changa_small,
            foreground=navy_blue, 
            background=blue_green,  # Background color
            activebackground=navy_blue,  # Active background when clicked
            activeforeground=blue_green,  # Active text color when clicked
            relief='flat',  # Makes the button flat without borders
            borderwidth=0,  # Removes the border width
            highlightthickness=0,  # Removes the highlight border
            width=button_width,
            command=self.delete_password
        )
        self.delete_button.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        # Modify Button
        self.modify_button = tk.Button(
            root,
            text="Modify Password",
            font=changa_small,
            foreground=navy_blue, 
            background=blue_green,  # Background color
            activebackground=navy_blue,  # Active background when clicked
            activeforeground=blue_green,  # Active text color when clicked
            relief='flat',  # Makes the button flat without borders
            borderwidth=0,  # Removes the border width
            highlightthickness=0,  # Removes the highlight border
            width=button_width,
            command=self.modify_password
        )
        self.modify_button.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        self.update_listbox()

    def update_listbox(self):
        self.password_listbox.delete(0, tk.END)
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
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root, "example_user")
    root.mainloop()
