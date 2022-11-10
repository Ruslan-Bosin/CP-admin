from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QPushButton
import app
from app import logger
from app.screens.LoginScreen import LoginScreen

class LoadingScreen(QMainWindow):

    def __init__(self):
        super().__init__()

        button = QPushButton("Go")
        button.clicked.connect(self.next)
        self.setCentralWidget(button)

    def next(self):
        app.storage.set_value("logged", "True")
        app.window.addWidget(LoginScreen())
        app.window.setCurrentIndex(app.window.currentIndex() + 1)
