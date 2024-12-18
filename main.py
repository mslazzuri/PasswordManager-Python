import tkinter as tk
from customtkinter import *
from gui.login_screen import LoginScreen

def main():
    root = CTk()
    app = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
