import customtkinter as ctk
import keyring
import sqlite3

from database import create_database
from settings import service_name
from encryption import set_master_key, check_masterKey
import settings

class password_manager(ctk.CTk):
    WinWidth=532
    WinHeight=780
    StandardFont=("default", 18)

    def __init__(self):
        super().__init__()
        create_database()
        self.geometry(str(self.WinWidth)+"x"+str(self.WinHeight))
        self.title("MunCrypt Password Manager")

        """Title for the app"""
        self.titleLabel = ctk.CTkLabel(self, text="MunCrypt", fg_color="transparent", font=("default", 40, "bold"), text_color="cyan")
        self.titleLabel.pack(padx=20, pady=20)

        """Master password entry box, displays * by default"""
        self.mPw = ctk.CTkEntry(self, placeholder_text="Master Vault Password", width=self.WinWidth - 20, height = self.WinWidth/5, show="*")
        self.mPw.bind("<Button>", self.masterCheck)
        self.mPw.bind("<Return>", self.unlockEvent)
        self.mPw.pack()

        self.entryButton = ctk.CTkButton(self, width = self.WinWidth/2, height = self.WinHeight/10, text="Unlock", command=self.unlockEvent,
                                         font=self.StandardFont)
        self.entryButton.pack(padx=50, pady=50)

    def unlockEvent(self, *args):
        if check_masterKey(self.mPw.get()):
            settings.login = True
            settings.mpwTemp = self.mPw.get()
            print(settings.login)
            self.destroy()
        return None
    
    """Checks to see if password already exists in local keyring, if it doesn't, repeatedly prompts user for master password."""
    def masterCheck(self, event):
        submitted = False
        while(keyring.get_password(service_name, service_name) == None) and submitted == False:
            self.setupDialog = ctk.CTkInputDialog(text="Please set a master password to unlock the application.", title="First Time Setup")
            input = self.setupDialog.get_input()
            if input != None:
                set_master_key(input)
                submitted = True
        return