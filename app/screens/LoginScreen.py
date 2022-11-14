from PyQt6.QtWidgets import QMainWindow
import app
from app import logger
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QMessageBox
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
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
        self.setStyleSheet("""
            * {
                border: none;
                background-color: '#F5F5F5';
            }
            QTableWidget::item:selected {
                background-color: red;
            }
            QTableWidget::item:selected {
                background-color: #F5F5F5;
                color: black;
            }
        """)
        self.form_layout = QVBoxLayout()
        inputs_layout = QVBoxLayout()
        lines_layout = QVBoxLayout()

        form_title = QLabel("Вход")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(600)
        font.setFamily("Arial Black")
        form_title.setFont(font)
        form_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.form_layout.addWidget(form_title)


        login_label = QLabel("Введите email:")
        login = QLineEdit(self)
        login.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border-radius: 3px;
            }
        """)
        login.setMinimumHeight(30)
        login.setTextMargins(5, 0, 5, 0)
        login.setMaximumWidth(230)
        lines_layout.addWidget(login_label)
        lines_layout.addWidget(login)
        lines_layout.setSpacing(0)
        inputs_layout.addLayout(lines_layout)

        lines_layout = QVBoxLayout()
        password = QLineEdit(self)
        password.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border-radius: 3px;
            }
        """)
        password.setEchoMode(QLineEdit.EchoMode.Password)
        password.setMaximumWidth(230)
        password.setMinimumHeight(30)
        password.setTextMargins(5, 0, 5, 0)
        password_label = QLabel("Введите пароль:")
        lines_layout.addWidget(password_label)
        lines_layout.addWidget(password)
        password.focusWidget()
        lines_layout.setSpacing(0)
        inputs_layout.addLayout(lines_layout)

        self.form_layout.addLayout(inputs_layout)
        accept = QPushButton("Войти", self)
        font = QFont()
        font.setFamily("Arial")
        accept.setFont(font)
        accept.setMinimumHeight(30)
        accept.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        accept.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 5px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
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

        if not check_server():

            messageBox = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if messageBox == QMessageBox.StandardButton.Abort:
                exit(-1)

        response = requests.post(
            f"{BASE_URL}/admin/login",
            json={'email': f'{self.login_edit.text()}',
                  'password': f'{self.password_edit.text()}'}
        )

        if (response.status_code == 200):

            response_json = response.json()
            app.storage.set_value("token", response_json['token'])

            from app.screens.MainScreen import MainScreen
            app.window.addWidget(MainScreen())
            app.window.setCurrentIndex(2)
        else:
            self.error_message.show()

    def mousePressEvent(self, event):
        self.error_message.hide()
