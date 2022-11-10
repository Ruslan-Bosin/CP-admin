from PyQt6.QtWidgets import QMainWindow
import app
from app import logger


class LoginScreen(QMainWindow):

    def __init__(self):
        super().__init__()


    def next(self):
        print(app.storage.get_value("logged"))
