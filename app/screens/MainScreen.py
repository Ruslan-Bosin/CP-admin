from PyQt6.QtWidgets import QMainWindow, QPushButton
import app
from app import logger


class MainScreen(QMainWindow):

    def __init__(self):
        super().__init__()

        button = QPushButton("Main")
        button.clicked.connect(self.next)
        self.setCentralWidget(button)

    def next(self):
        print(app.storage.get_value("logged"))
