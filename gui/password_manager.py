# password_manager.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from utils.file_utils import load_passwords, save_passwords
from utils.crypto_utils import decrypt_password, encrypt_password

class PasswordManagerApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Password Manager")

        self.username = username
        self.passwords = load_passwords()
        if username not in self.passwords:
            self.passwords[username] = {}

        # UI Elements
        self.password_listbox = tk.Listbox(root, width=50)
        self.password_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Password", command=self.add_password)
        self.add_button.grid(row=1, column=0, padx=5, pady=5)

        self.view_button = tk.Button(root, text="View Password", command=self.view_password)
        self.view_button.grid(row=1, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(root, text="Delete Password", command=self.delete_password)
        self.delete_button.grid(row=2, column=0, padx=5, pady=5)

        self.modify_button = tk.Button(root, text="Modify Password", command=self.modify_password)
        self.modify_button.grid(row=2, column=1, padx=5, pady=5)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root, "example_user")
    root.mainloop()
