from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QPushButton
import app
from app import logger


class LoginScreen(QMainWindow):

    def __init__(self):
        super().__init__()

        button = QPushButton("Back")
        button.clicked.connect(self.next)
        self.setCentralWidget(button)

    def next(self):
        print(app.storage.get_value("logged"))
