import customtkinter as ctk

from password_manager import password_manager
from settings import login

class dashboard(ctk.CTk):
    WinWidth=532
    WinHeight=780
    StandardFont=("default", 18)

    def __init__(self):
        super().__init__()
        self.geometry(str(self.WinWidth)+"x"+str(self.WinHeight))
        self.title("MunCrypt Password Manager")

        self.titleLabel = ctk.CTkLabel(self, text="Welcome!", fg_color="transparent", font=("default", 40, "bold"), text_color="cyan")
        self.titleLabel.pack(padx=20, pady=20)

        # TODO add function to allow user to create login entry for database.
        # TODO add permanent pinned toolbar for adding and logging out.
        # TODO add functionality which polls database for all available logins and displays them for the user.