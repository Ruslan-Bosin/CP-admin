import requests
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLabel
from config import BASE_URL
import app
from app import logger
from app.utils.check_server import check_server

class LoadingScreen(QMainWindow):

    def __init__(self):
        super().__init__()

        label = QLabel("Загрузка")
        self.setCentralWidget(label)

        self.on_load()

    def on_load(self):

        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        if app.storage.key_exists("token"):

            response = requests.get(
                f"{BASE_URL}/admin/verify_token",
                headers={"x-access-token": app.storage.get_value(key="token")}
            )

            if response.status_code == 200:
                from app.screens.MainScreen import MainScreen
                app.window.addWidget(MainScreen())
                app.window.setCurrentIndex(1)
            else:
                QMessageBox.information(
                    self,
                    "Уведомление",
                    "Срок действия сессии истёк"
                )
                from app.screens.LoginScreen import LoginScreen
                app.window.addWidget(LoginScreen())
                app.window.setCurrentIndex(1)
        else:
            from app.screens.LoginScreen import LoginScreen
            app.window.addWidget(LoginScreen())
            app.window.setCurrentIndex(1)
