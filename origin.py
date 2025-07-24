"""Origin point for password manager application. Handles creation of individual applications
    each application serves it's own defined purpose, including login, and the main dashboard."""

from password_manager import password_manager
from dashboard import dashboard
import settings

if settings.login == False:
    app2=password_manager()
    app2.mainloop()

if settings.login == True:
    mainApp = dashboard()
    mainApp.mainloop()