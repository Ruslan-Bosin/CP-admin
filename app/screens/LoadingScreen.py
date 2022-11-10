import requests
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from config import BASE_URL
import app
from app import logger
from app.screens.LoginScreen import LoginScreen
from app.screens.MainScreen import MainScreen
from app.utils.check_server import check_server

class LoadingScreen(QMainWindow):

    def __init__(self):
        super().__init__()

        self.on_load()

    def on_load(self):

        if not check_server():

            messageBox = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if messageBox == QMessageBox.StandardButton.Abort:
                exit(-1)

        if app.storage.key_exists("token"):

            response = requests.get(
                f"{BASE_URL}/admin/verify_token",
                headers={"x-access-token": app.storage.get_value(key="token")}
            )

            if response.status_code == 200:
                app.window.addWidget(MainScreen())
                app.window.setCurrentIndex(app.window.currentIndex() + 1)
            else:
                QMessageBox.information(
                    self,
                    "Уведомление",
                    "Срок действия сессии истёк"
                )
                app.window.addWidget(LoginScreen())
                app.window.setCurrentIndex(app.window.currentIndex() + 1)
        else:
            app.window.addWidget(LoginScreen())
            app.window.setCurrentIndex(app.window.currentIndex() + 1)
