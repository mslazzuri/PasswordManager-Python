import tkinter as tk
from tkinter import messagebox, scrolledtext
from password import PasswordManager

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        # Login Section
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=10)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.login_password_entry = tk.Entry(self.login_frame, show="*", width=30)
        self.login_password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Add New Password Section
        self.add_frame = tk.Frame(root)

        tk.Label(self.add_frame, text="Service:").grid(row=0, column=0, padx=5, pady=5)
        self.service_entry = tk.Entry(self.add_frame, width=30)
        self.service_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.add_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.add_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.add_frame, text="Add Password", command=self.add_password)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Verify Password Section
        self.verify_frame = tk.Frame(root)

        tk.Label(self.verify_frame, text="Service:").grid(row=0, column=0, padx=5, pady=5)
        self.verify_service_entry = tk.Entry(self.verify_frame, width=30)
        self.verify_service_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.verify_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.verify_password_entry = tk.Entry(self.verify_frame, show="*", width=30)
        self.verify_password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.verify_button = tk.Button(self.verify_frame, text="Verify Password", command=self.verify_password)
        self.verify_button.grid(row=2, column=0, columnspan=2, pady=10)

        # View All Passwords Section
        self.view_frame = tk.Frame(root)

        self.view_button = tk.Button(self.view_frame, text="View All Passwords", command=self.view_passwords)
        self.view_button.grid(row=0, column=0, pady=10)

        self.passwords_text = scrolledtext.ScrolledText(self.view_frame, width=50, height=10, state='disabled')
        self.passwords_text.grid(row=1, column=0, padx=5, pady=5)

        # Save to File Button
        self.save_button = tk.Button(root, text="Save to File", command=self.save_to_file)

        # Initialize the PasswordManager
        self.manager = PasswordManager()
        self.logged_in = False

    def login(self):
        username = self.username_entry.get().strip()
        password = self.login_password_entry.get().strip()

        # Example static credentials; replace with proper authentication logic as needed
        if username == "admin" and password == "admin123":
            self.logged_in = True
            self.login_frame.pack_forget()
            self.add_frame.pack(pady=10)
            self.verify_frame.pack(pady=10)
            self.view_frame.pack(pady=10)
            self.save_button.pack(pady=10)
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def add_password(self):
        if not self.logged_in:
            messagebox.showerror("Error", "You must log in first.")
            return

        service = self.service_entry.get().strip()
        password = self.password_entry.get().strip()

        if not service or not password:
            messagebox.showerror("Error", "Service and Password fields cannot be empty.")
            return

        if self.manager.add_new_password(service, password):
            messagebox.showinfo("Success", f"Password added for service '{service}'!")
            self.service_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Service '{service}' already exists.")

    def verify_password(self):
        if not self.logged_in:
            messagebox.showerror("Error", "You must log in first.")
            return

        service = self.verify_service_entry.get().strip()
        password = self.verify_password_entry.get().strip()

        if not service or not password:
            messagebox.showerror("Error", "Service and Password fields cannot be empty.")
            return

        if self.manager.verify_password(service, password):
            messagebox.showinfo("Success", "Password is correct!")
        else:
            messagebox.showerror("Error", "Incorrect password or service not found.")

    def view_passwords(self):
        if not self.logged_in:
            messagebox.showerror("Error", "You must log in first.")
            return

        self.passwords_text.configure(state='normal')
        self.passwords_text.delete(1.0, tk.END)

        passwords = self.manager.get_all_passwords()
        if passwords:
            for service, password in passwords.items():
                self.passwords_text.insert(tk.END, f"Service: {service}, Password: {password}\n")
        else:
            self.passwords_text.insert(tk.END, "No passwords stored.")

        self.passwords_text.configure(state='disabled')

    def save_to_file(self):
        if not self.logged_in:
            messagebox.showerror("Error", "You must log in first.")
            return

        try:
            self.manager.save_to_file()
            messagebox.showinfo("Success", "Passwords saved to file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save passwords: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
