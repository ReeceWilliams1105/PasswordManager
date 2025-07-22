import customtkinter as ctk
import keyring
import sqlite3

from database import create_database
from settings import service_name
from encryption import set_master_key

class FirstTimeWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.geometry("400x300")

        self.Toplabel = ctk.CTkLabel(self, text="First Time Setup")
        self.Toplabel.pack(padx=20, pady=20)

        self.LowerLabel = ctk.CTkLabel(self, text="Please set a master password to unlock the application.")        
        self.LowerLabel.pack()

        self.mPwSet = ctk.CTkEntry(self, placeholder_text="Master Vault Password", width=380, height=40)
        self.mPwSet.pack()

class password_manager(ctk.CTk):
    WinWidth=532
    WinHeight=780
    StandardFont=("default", 18)

    def __init__(self):
        super().__init__()
        create_database()
        self.geometry(str(self.WinWidth)+"x"+str(self.WinHeight))
        self.firstTimeWindow = None
        self.title("MunCrypt Password Manager")

        """Title for the app"""
        self.titleLabel = ctk.CTkLabel(self, text="MunCrypt", fg_color="transparent", font=("default", 40, "bold"), text_color="cyan")
        self.titleLabel.pack(padx=20, pady=20)

        """Master password entry box, displays * by default"""
        self.mPw = ctk.CTkEntry(self, placeholder_text="Master Vault Password", width=self.WinWidth - 20, height = self.WinWidth/5, show="*")
        self.mPw.pack()

        self.entryButton = ctk.CTkButton(self, width = self.WinWidth/2, height = self.WinHeight/10, text="Unlock", command=self.unlockEvent,
                                         font=self.StandardFont)
        self.entryButton.pack(padx=50, pady=50)
        """ https://www.askpython.com/python-modules/tkinter/bind-in-tkinter - To use when clicking on entry box to solve focus problem."""
        self.masterCheck()

    def unlockEvent(self):
        print(keyring.get_password(service_name, service_name))
        return None
    
    def masterCheck(self):
        if keyring.get_password(service_name, service_name) != None:
            return
        else:
            self.firstTimeSetup()
            self.firstTimeWindow.focus()

    def firstTimeSetup(self):
        if self.firstTimeWindow is None or not self.firstTimeWindow.winfo_exists():
            self.firstTimeWindow = FirstTimeWindow(self)
        else:
            self.firstTimeWindow.focus()
        

app=password_manager()
app.mainloop()