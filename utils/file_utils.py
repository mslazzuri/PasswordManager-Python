import json
import os

USERS_FILE = "passwords.txt"
PASSWORDS_FILE = "user.txt"

# Load users from a file
def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        return json.load(file)

# Save users to a file
def save_users(users: dict):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

#################################################

# Load passwords from a file
def load_passwords() -> dict:
    if not os.path.exists(PASSWORDS_FILE):
        return {}
    with open(PASSWORDS_FILE, "r") as file:
        return json.load(file)

# Save passwords to a file
def save_passwords(passwords: dict):
    with open(PASSWORDS_FILE, "w") as file:
        json.dump(passwords, file, indent=4)
