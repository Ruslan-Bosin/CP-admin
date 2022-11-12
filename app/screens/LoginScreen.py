from PyQt6.QtWidgets import QMainWindow
import app
from app import logger
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QMessageBox
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt
import sys
import requests
from config import BASE_URL
from app.utils.check_server import check_server


class LoginScreen(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.setGeometry(100, 100, 400, 400)
        self.form_layout = QVBoxLayout()
        inputs_layout = QVBoxLayout()
        lines_layout = QVBoxLayout()

        form_title = QLabel("Вход")
        font = QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(600)
        form_title.setFont(font)
        form_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.form_layout.addWidget(form_title)


        login_label = QLabel("Введите email:")
        login = QLineEdit(self)
        login.setMaximumWidth(230)
        lines_layout.addWidget(login_label)
        lines_layout.addWidget(login)
        lines_layout.setSpacing(0)
        inputs_layout.addLayout(lines_layout)

        lines_layout = QVBoxLayout()
        password = QLineEdit(self)
        password.setEchoMode(QLineEdit.EchoMode.Password)
        password.setMaximumWidth(230)
        password_label = QLabel("Введите пароль:")
        lines_layout.addWidget(password_label)
        lines_layout.addWidget(password)
        password.focusWidget()
        lines_layout.setSpacing(0)
        inputs_layout.addLayout(lines_layout)

        self.form_layout.addLayout(inputs_layout)
        accept = QPushButton("Войти", self)
        accept.setMaximumWidth(230)
        self.form_layout.addWidget(accept)

        self.login_edit, self.password_edit = login, password

        self.error_message = QLabel("Неправильный email или пароль")
        self.form_layout.addWidget(self.error_message)
        self.error_message.hide()
        self.error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        accept.clicked.connect(self.OnClick)
        widget = QWidget()
        # form_layout.setContentsMargins(200, 200, 200, 200)
        self.form_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        widget.setLayout(self.form_layout)
        self.setCentralWidget(widget)

    def OnClick(self):
        if check_server():
            response = requests.post(
                f"{BASE_URL}/admin/login",
                json={'email': f'{self.login_edit.text()}',
                      'password': f'{self.password_edit.text()}'}
            )
            if (response.status_code == 200):
                print("1")
                response_json = response.json()
                app.storage.set_value("token", response_json['token'])
            else:
                self.error_message.show()

        if not check_server():

            messageBox = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if messageBox == QMessageBox.StandardButton.Abort:
                exit(-1)


    def mousePressEvent(self, event):
        self.error_message.hide()


# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#     app.setStyle("""""")
#     win = LoginScreen()
#     win.show()
#     app.exec()