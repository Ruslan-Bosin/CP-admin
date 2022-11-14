import requests
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog
from PyQt6.QtCore import QPropertyAnimation
from PyQt6 import QtCore, QtGui, QtWidgets
from config import BASE_URL, BASE_URL_IMAGE
import app
from app import logger
from app.utils.check_server import check_server
from app.utils.exception_hook import exception_hook
import csv
import sqlite3


class MainScreen(QMainWindow):

    def __init__(self):
        super().__init__()

        self.clients_data: list[dict[str: object]] = list()
        self.organizations_data: list[dict[str: object]] = list()
        self.records_data: list[dict[str: object]] = list()
        self.has_access = False
        self.has_access_text = "Данное поле не рекомендовано к изменению"
        self.has_no_access_text = "У вас нет прав менять это поле"

        self.export_table_name: str = "organizations"

        self.current_table_name = "organizations"

        self.current_client_id = -1
        self.clients_table_current_selection = (-1, -1)
        self.clients_table_can_edit = False

        self.current_organization_id = -1
        self.organizations_table_current_selection = (-1, -1)
        self.organizations_table_can_edit = False

        self.current_record_id = -1
        self.records_table_current_selection = (-1, -1)
        self.records_table_can_edit = False

        self.in_table_cell_alignment = QtCore.Qt.AlignmentFlag.AlignCenter

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
        self.font_name = ""

        # Central widget
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")

        # Horizontal Layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Left Menu Container
        self.left_menu_container = QtWidgets.QFrame(self.central_widget)
        self.left_menu_container.setEnabled(True)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                            QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.left_menu_container.sizePolicy().hasHeightForWidth())
        self.left_menu_container.setSizePolicy(size_policy)
        self.left_menu_container.setMaximumSize(QtCore.QSize(0, 16777215))
        self.left_menu_container.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.left_menu_container.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.left_menu_container.setLineWidth(0)
        self.left_menu_container.setObjectName("left_menu_container")

        # Layout - 2
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.left_menu_container)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Left Menu
        self.left_menu = QtWidgets.QFrame(self.left_menu_container)
        self.left_menu.setMinimumSize(QtCore.QSize(250, 0))
        self.left_menu.setAutoFillBackground(False)
        self.left_menu.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.left_menu.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.left_menu.setStyleSheet("""
            .QFrame {
                border-right: 1px solid #575F6E;
            }
            QPushButton {
                background-color: white;
                border-radius: 5px;
                border: 1px solid #DBDBDB;
            }
            QPushButton:hover {
                background-color: #F8F8F8;
            }
            QPushButton:pressed {
                border: 1px solid #CFCFCF;
                background-color: #F1F1F1;
            }
            QPushButton:checked {
                border: 1px solid #CFCFCF;
                background-color: #F1F1F1;
            }
        """)
        self.left_menu.setObjectName("left_menu")

        # Layout - 4
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.left_menu)
        self.verticalLayout_4.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # Left Menu Title
        self.left_menu_title = QtWidgets.QLabel(self.left_menu)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.left_menu_title.sizePolicy().hasHeightForWidth())
        self.left_menu_title.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.left_menu_title.setFont(font)
        self.left_menu_title.setObjectName("left_menu_title")

        self.verticalLayout_4.addWidget(self.left_menu_title)

        spacer_item = QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_4.addItem(spacer_item)

        # Page 1 Button
        self.page_1_button = QtWidgets.QPushButton(self.left_menu)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.page_1_button.sizePolicy().hasHeightForWidth())
        self.page_1_button.setSizePolicy(size_policy)
        self.page_1_button.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.page_1_button.setFont(font)
        self.page_1_button.setObjectName("page_1_button")

        self.verticalLayout_4.addWidget(self.page_1_button)

        # Page 2 Button
        self.page_2_button = QtWidgets.QPushButton(self.left_menu)
        self.page_2_button.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.page_2_button.setFont(font)
        self.page_2_button.setObjectName("page_2_button")

        self.verticalLayout_4.addWidget(self.page_2_button)

        # Page 3 Button
        self.page_3_button = QtWidgets.QPushButton(self.left_menu)
        self.page_3_button.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.page_3_button.setFont(font)
        self.page_3_button.setObjectName("page_3_button")

        self.verticalLayout_4.addWidget(self.page_3_button)

        spacer_item1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacer_item1)

        # Exit Button
        self.exit_button = QtWidgets.QPushButton(self.left_menu)
        self.exit_button.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("exit_button")

        self.verticalLayout_4.addWidget(self.exit_button)

        self.verticalLayout_2.addWidget(self.left_menu)

        self.horizontalLayout.addWidget(self.left_menu_container)

        # Main Body
        self.main_body = QtWidgets.QFrame(self.central_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                            QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(2)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.main_body.sizePolicy().hasHeightForWidth())
        self.main_body.setSizePolicy(size_policy)
        self.main_body.setMinimumSize(QtCore.QSize(400, 0))
        self.main_body.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.main_body.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.main_body.setLineWidth(0)
        self.main_body.setObjectName("main_body")

        # Vertical Layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_body)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Header
        self.header = QtWidgets.QFrame(self.main_body)
        self.header.setMinimumSize(QtCore.QSize(0, 40))
        self.header.setMaximumSize(QtCore.QSize(16777215, 40))
        self.header.setStyleSheet("")
        self.header.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.header.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.header.setLineWidth(0)
        self.header.setObjectName("header")

        # Horizontal Layout 2
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Open Left Menu Button
        self.open_left_menu_button = QtWidgets.QPushButton(self.header)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.open_left_menu_button.sizePolicy().hasHeightForWidth())
        self.open_left_menu_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.open_left_menu_button.setFont(font)
        self.open_left_menu_button.setObjectName("open_left_menu_button")

        self.horizontalLayout_2.addWidget(self.open_left_menu_button)

        spacer_item2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacer_item2)

        # Page Title
        self.page_title = QtWidgets.QLabel(self.header)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.page_title.sizePolicy().hasHeightForWidth())
        self.page_title.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.page_title.setFont(font)
        self.page_title.setObjectName("page_title")

        self.horizontalLayout_2.addWidget(self.page_title)

        spacer_item3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacer_item3)

        # Open Right Menu Button
        self.open_right_menu_button = QtWidgets.QPushButton(self.header)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.open_right_menu_button.sizePolicy().hasHeightForWidth())
        self.open_right_menu_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.open_right_menu_button.setFont(font)
        self.open_right_menu_button.setObjectName("open_right_menu_button")

        self.horizontalLayout_2.addWidget(self.open_right_menu_button)

        self.verticalLayout.addWidget(self.header)

        # Main Body
        self.body = QtWidgets.QFrame(self.main_body)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(size_policy)
        self.body.setStyleSheet("background: white;")
        self.body.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.body.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.body.setLineWidth(0)
        self.body.setObjectName("body")

        # Horizontal Layout 3
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.body)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # Body Stack
        self.body_stack = QtWidgets.QStackedWidget(self.body)
        self.body_stack.setObjectName("body_stack")

        # Page 1
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")

        # HorizontalLayout 4
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.page_1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        spacer_item4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacer_item4)

        # Forme layout
        self.forme_layout = QtWidgets.QFrame(self.page_1)
        self.forme_layout.setObjectName("forme_layout")

        # Form Layout
        self.form_layout = QtWidgets.QVBoxLayout(self.forme_layout)
        self.form_layout.setSpacing(15)
        self.form_layout.setObjectName("form_layout")

        spacer_item5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.form_layout.addItem(spacer_item5)

        # Account Label
        self.account_label = QtWidgets.QLabel(self.forme_layout)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.account_label.sizePolicy().hasHeightForWidth())
        self.account_label.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.account_label.setFont(font)
        self.account_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.account_label.setObjectName("account_label")

        self.form_layout.addWidget(self.account_label)

        # Line 1 Layout
        self.line_1_layout = QtWidgets.QHBoxLayout()
        self.line_1_layout.setObjectName("line_1_layout")

        # Email Label
        self.email_label = QtWidgets.QLabel(self.forme_layout)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.email_label.setFont(font)
        self.email_label.setObjectName("email_label")

        self.line_1_layout.addWidget(self.email_label)

        # Email Field
        self.email_field = QtWidgets.QLineEdit(self.forme_layout)
        self.email_field.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.email_field.setFont(font)
        self.email_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.email_field.setMinimumHeight(30)
        self.email_field.setTextMargins(5, 0, 5, 0)
        self.email_field.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                border-radius: 3px;
            }
        """)
        self.email_field.setObjectName("email_field")

        self.line_1_layout.addWidget(self.email_field)

        self.form_layout.addLayout(self.line_1_layout)

        # Line 2 Layout
        self.line_2_layout = QtWidgets.QHBoxLayout()
        self.line_2_layout.setObjectName("line_2_layout")
        self.password_label = QtWidgets.QLabel(self.forme_layout)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")

        self.line_2_layout.addWidget(self.password_label)

        # Password Field
        self.password_field = QtWidgets.QLineEdit(self.forme_layout)
        self.password_field.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.password_field.setFont(font)
        self.password_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.password_field.setMinimumHeight(30)
        self.password_field.setTextMargins(5, 0, 5, 0)
        self.password_field.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                border-radius: 3px;
            }
        """)
        self.password_field.setObjectName("password_field")

        self.line_2_layout.addWidget(self.password_field)

        self.form_layout.addLayout(self.line_2_layout)

        # Line 2 Layout
        self.line_3_layout = QtWidgets.QHBoxLayout()
        self.line_3_layout.setObjectName("line_3_layout")

        # Editing Label
        self.editing_label = QtWidgets.QLabel(self.forme_layout)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.editing_label.setFont(font)
        self.editing_label.setObjectName("editing_label")

        self.line_3_layout.addWidget(self.editing_label)

        # Editing Layout
        self.editing_layout = QtWidgets.QHBoxLayout()
        self.editing_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.editing_layout.setObjectName("editing_layout")

        # Editing
        self.editing = QtWidgets.QCheckBox(self.forme_layout)
        self.editing.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.editing.setFont(font)
        self.editing.setObjectName("editing")

        self.editing_layout.addWidget(self.editing)

        # Editing Button
        self.editing_button = QtWidgets.QPushButton(self.forme_layout)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.editing_button.setFont(font)
        self.editing_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.editing_button.setStyleSheet("""
            QPushButton {
                color: #007AFF;
            }
            QPushButton:hover {
                color: #2C91FF;
            }
            QPushButton:pressed {
                color: #77B8FF;
            }
            QPushButton:disabled {
                color: grey;
            }
        """)
        self.editing_button.setObjectName("editing_button")

        self.editing_layout.addWidget(self.editing_button)

        spacer_item6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.editing_layout.addItem(spacer_item6)

        # Line 3 Layout
        self.line_3_layout.addLayout(self.editing_layout)
        self.form_layout.addLayout(self.line_3_layout)

        # Logout Button
        self.logout_button = QtWidgets.QPushButton(self.forme_layout)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.logout_button.sizePolicy().hasHeightForWidth())
        self.logout_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.logout_button.setFont(font)
        self.logout_button.setMinimumHeight(30)
        self.logout_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.logout_button.setObjectName("logout_button")

        self.form_layout.addWidget(self.logout_button)

        spacer_item7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.form_layout.addItem(spacer_item7)

        self.horizontalLayout_4.addWidget(self.forme_layout)

        spacer_item8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacer_item8)

        self.body_stack.addWidget(self.page_1)

        # Page 2
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")

        # HorizontalLayout 6
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        # Tab widget
        self.tabWidget = QtWidgets.QTabWidget(self.page_2)
        self.tabWidget.setObjectName("tabWidget")

        # Organizations Layout
        self.organizations_layout = QtWidgets.QWidget()
        self.organizations_layout.setObjectName("organizations_layout")

        # VerticalLayout 5
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.organizations_layout)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # HorizontalLayout 5
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        # Search Bar Layout
        self.search_bar_layout = QtWidgets.QHBoxLayout()
        self.search_bar_layout.setObjectName("search_bar_layout")

        # Search Line Edit
        self.search_line_edit = QtWidgets.QLineEdit(self.organizations_layout)
        self.search_line_edit.setStyleSheet("""
            QLineEdit {
                background: #F5F5F5;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
            }
            QLineEdit:focus {
                background: #F0F0F0;
            }
            QLineEdit:hover {
                background: #F0F0F0;
            }
        """)
        self.search_line_edit.setObjectName("search_line_edit")

        self.search_bar_layout.addWidget(self.search_line_edit)

        # Search Button
        self.search_button = QtWidgets.QPushButton(self.organizations_layout)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.search_button.sizePolicy().hasHeightForWidth())
        self.search_button.setSizePolicy(size_policy)
        self.search_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.search_button.setMinimumHeight(self.search_line_edit.height() - 7)
        self.search_button.setMinimumWidth(50)
        self.search_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1987FE;
            }
            QPushButton:pressed {
                background-color: #62ABFB;
            }
            QPushButton:disabled {
                background-color: #F5F5F5;
                color: grey;
            }
        """)
        self.search_button.setObjectName("search_button")

        self.search_bar_layout.addWidget(self.search_button)

        self.horizontalLayout_5.addLayout(self.search_bar_layout)

        spacer_item9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacer_item9)

        # Sort Button
        self.add_organization_button = QtWidgets.QPushButton(self.organizations_layout)
        self.add_organization_button.setMinimumHeight(self.search_line_edit.height() - 7)
        self.add_organization_button.setMinimumWidth(80)
        self.add_organization_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_organization_button.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.add_organization_button.setObjectName("add_organization_button")

        self.horizontalLayout_5.addWidget(self.add_organization_button)

        # Save button
        self.save_button = QtWidgets.QPushButton(self.organizations_layout)
        self.save_button.setMinimumHeight(self.search_line_edit.height() - 7)
        self.save_button.setMinimumWidth(80)
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.save_button.setObjectName("save_button")

        self.horizontalLayout_5.addWidget(self.save_button)

        # Refuse button
        self.refresh_button = QtWidgets.QPushButton(self.organizations_layout)
        self.refresh_button.setMinimumHeight(self.search_line_edit.height() - 7)
        self.refresh_button.setMinimumWidth(80)
        self.refresh_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.refresh_button.setObjectName("refresh_button")

        self.horizontalLayout_5.addWidget(self.refresh_button)

        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        # Organizations Table
        self.organizations_table = QtWidgets.QTableWidget(self.organizations_layout)
        self.organizations_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.organizations_table.setObjectName("organizations_table")
        self.organizations_table.setColumnCount(0)
        self.organizations_table.setRowCount(0)

        self.verticalLayout_5.addWidget(self.organizations_table)

        self.tabWidget.addTab(self.organizations_layout, "")

        # Clients Layout
        self.clients_layout = QtWidgets.QWidget()
        self.clients_layout.setObjectName("clients_layout")

        # Vertical Layout 6
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.clients_layout)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.top_panel_clients = QtWidgets.QHBoxLayout()

        # Top Panel Clients
        self.top_panel_clients.setObjectName("top_panel_clients")

        # Search Bar Layout Clients
        self.search_bar_layout_clients = QtWidgets.QHBoxLayout()
        self.search_bar_layout_clients.setObjectName("search_bar_layout_clients")

        # Search Line Edit 2
        self.search_line_edit_clients = QtWidgets.QLineEdit(self.clients_layout)
        self.search_line_edit_clients.setStyleSheet("""
            QLineEdit {
                background: #F5F5F5;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
            }
            QLineEdit:focus {
                background: #F0F0F0;
            }
            QLineEdit:hover {
                background: #F0F0F0;
            }
        """)
        self.search_line_edit_clients.setObjectName("search_line_edit_2")

        self.search_bar_layout_clients.addWidget(self.search_line_edit_clients)

        # Search Button Clients
        self.search_button_clients = QtWidgets.QPushButton(self.clients_layout)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.search_button_clients.sizePolicy().hasHeightForWidth())
        self.search_button_clients.setSizePolicy(size_policy)
        self.search_button_clients.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.search_button_clients.setMinimumHeight(self.search_line_edit_clients.height() - 7)
        self.search_button_clients.setMinimumWidth(50)
        self.search_button_clients.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.search_button_clients.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1987FE;
            }
            QPushButton:pressed {
                background-color: #62ABFB;
            }
            QPushButton:disabled {
                background-color: #F5F5F5;
                color: grey;
            }
        """)
        self.search_button_clients.setObjectName("search_button_clients")

        self.search_bar_layout_clients.addWidget(self.search_button_clients)

        self.top_panel_clients.addLayout(self.search_bar_layout_clients)

        spacer_item10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                              QtWidgets.QSizePolicy.Policy.Minimum)
        self.top_panel_clients.addItem(spacer_item10)

        # Sort Button Clients
        self.add_client_button = QtWidgets.QPushButton(self.clients_layout)
        self.add_client_button.setMinimumHeight(self.search_line_edit_clients.height() - 7)
        self.add_client_button.setMinimumWidth(80)
        self.add_client_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_client_button.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.add_client_button.setObjectName("add_client_button")

        self.top_panel_clients.addWidget(self.add_client_button)

        # Save Button Clients
        self.save_button_clients = QtWidgets.QPushButton(self.clients_layout)
        self.save_button_clients.setMinimumHeight(self.search_line_edit_clients.height() - 7)
        self.save_button_clients.setMinimumWidth(80)
        self.save_button_clients.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.save_button_clients.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.save_button_clients.setObjectName("save_button_clients")

        self.top_panel_clients.addWidget(self.save_button_clients)

        # Refresh Button Clients
        self.refresh_button_clients = QtWidgets.QPushButton(self.clients_layout)
        self.refresh_button_clients.setMinimumHeight(self.search_line_edit_clients.height() - 7)
        self.refresh_button_clients.setMinimumWidth(80)
        self.refresh_button_clients.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.refresh_button_clients.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.refresh_button_clients.setObjectName("refresh_button_clients")

        self.top_panel_clients.addWidget(self.refresh_button_clients)

        self.verticalLayout_6.addLayout(self.top_panel_clients)

        # Clients Table
        self.clients_table = QtWidgets.QTableWidget(self.clients_layout)
        self.clients_table.setObjectName("clients_table")
        self.clients_table.setColumnCount(0)
        self.clients_table.setRowCount(0)
        self.clients_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout_6.addWidget(self.clients_table)

        self.tabWidget.addTab(self.clients_layout, "")

        # Records Layout
        self.records_layout = QtWidgets.QWidget()
        self.records_layout.setObjectName("records_layout")

        # VerticalLayout 7
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.records_layout)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        # Top Panel Records
        self.top_panel_records = QtWidgets.QHBoxLayout()
        self.top_panel_records.setObjectName("top_panel_records")

        # Search Bar Layout Records
        self.search_bar_layout_records = QtWidgets.QHBoxLayout()
        self.search_bar_layout_records.setObjectName("search_bar_layout_records")

        # Search Line Edit Records
        self.search_line_edit_records = QtWidgets.QLineEdit(self.records_layout)
        self.search_line_edit_records.setStyleSheet("""
            QLineEdit {
                background: #F5F5F5;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
            }
            QLineEdit:focus {
                background: #F0F0F0;
            }
            QLineEdit:hover {
                background: #F0F0F0;
            }
        """)
        self.search_line_edit_records.setObjectName("search_line_edit_records")

        self.search_bar_layout_records.addWidget(self.search_line_edit_records)

        # Search Button Records
        self.search_button_records = QtWidgets.QPushButton(self.records_layout)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.search_button_records.sizePolicy().hasHeightForWidth())
        self.search_button_records.setSizePolicy(size_policy)
        self.search_button_records.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.search_button_records.setMinimumHeight(self.search_line_edit_records.height() - 7)
        self.search_button_records.setMinimumWidth(50)
        self.search_button_records.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.search_button_records.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1987FE;
            }
            QPushButton:pressed {
                background-color: #62ABFB;
            }
            QPushButton:disabled {
                background-color: #F5F5F5;
                color: grey;
            }
        """)
        self.search_button_records.setObjectName("search_button_records")

        self.search_bar_layout_records.addWidget(self.search_button_records)

        self.top_panel_records.addLayout(self.search_bar_layout_records)

        spacer_item11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                              QtWidgets.QSizePolicy.Policy.Minimum)
        self.top_panel_records.addItem(spacer_item11)

        # Sort Button Records
        self.add_record_button = QtWidgets.QPushButton(self.records_layout)
        self.add_record_button.setMinimumHeight(self.search_line_edit_records.height() - 7)
        self.add_record_button.setMinimumWidth(80)
        self.add_record_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_record_button.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.add_record_button.setObjectName("add_record_button")

        self.top_panel_records.addWidget(self.add_record_button)

        # Save Button Records
        self.save_button_records = QtWidgets.QPushButton(self.records_layout)
        self.save_button_records.setMinimumHeight(self.search_line_edit_records.height() - 7)
        self.save_button_records.setMinimumWidth(80)
        self.save_button_records.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.save_button_records.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.save_button_records.setObjectName("save_button_records")

        self.top_panel_records.addWidget(self.save_button_records)

        # Refresh Button Records
        self.refresh_button_records = QtWidgets.QPushButton(self.records_layout)
        self.refresh_button_records.setMinimumHeight(self.search_line_edit_records.height() - 7)
        self.refresh_button_records.setMinimumWidth(80)
        self.refresh_button_records.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.refresh_button_records.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
        """)
        self.refresh_button_records.setObjectName("refresh_button_records")

        self.top_panel_records.addWidget(self.refresh_button_records)

        self.verticalLayout_7.addLayout(self.top_panel_records)

        # Table Widget
        self.records_table = QtWidgets.QTableWidget(self.records_layout)
        self.records_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.records_table.setObjectName("records_table")
        self.records_table.setColumnCount(0)
        self.records_table.setRowCount(0)

        self.verticalLayout_7.addWidget(self.records_table)

        self.tabWidget.addTab(self.records_layout, "")

        self.horizontalLayout_6.addWidget(self.tabWidget)

        self.body_stack.addWidget(self.page_2)

        # Page 1
        self.page_3 = QtWidgets.QWidget()

        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.page_3)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")

        self.page_3_Logs_View = QtWidgets.QPlainTextEdit()
        self.page_3_Logs_View.isReadOnly()
        self.page_3_Logs_View.setStyleSheet("""
                background-color: #575F6E;
                border: none;
        """)

        self.horizontalLayout_9.addWidget(self.page_3_Logs_View)

        self.page_3.setObjectName("page_3")

        self.body_stack.addWidget(self.page_3)

        self.horizontalLayout_3.addWidget(self.body_stack)

        self.verticalLayout.addWidget(self.body)

        self.horizontalLayout.addWidget(self.main_body)

        # Right Menu Container
        self.right_menu_container = QtWidgets.QFrame(self.central_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                            QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.right_menu_container.sizePolicy().hasHeightForWidth())
        self.right_menu_container.setSizePolicy(size_policy)
        self.right_menu_container.setMaximumSize(QtCore.QSize(0, 16777215))
        self.right_menu_container.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.right_menu_container.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.right_menu_container.setLineWidth(0)
        self.right_menu_container.setObjectName("right_menu_container")

        # VerticalLayout 3
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.right_menu_container)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # Right Menu
        self.right_menu = QtWidgets.QFrame(self.right_menu_container)
        self.right_menu.setMinimumSize(QtCore.QSize(250, 0))
        self.right_menu.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.right_menu.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.right_menu.setStyleSheet("""
            .QFrame {
                border-left: 1px solid #575F6E;
            }
        """)
        self.right_menu.setObjectName("right_menu")

        self.right_menu_stack_layout = QtWidgets.QVBoxLayout(self.right_menu)
        self.right_menu_stack_layout.setObjectName("right_menu_stack_layout")
        self.right_menu_stack = QtWidgets.QStackedWidget(self.right_menu)
        self.right_menu_stack.setObjectName("right_menu_stack")
        self.page_1_right_menu = QtWidgets.QWidget()
        self.page_1_right_menu.setObjectName("page_1_right_menu")
        self.right_menu_vertical_layout_page_1 = QtWidgets.QVBoxLayout(self.page_1_right_menu)
        self.right_menu_vertical_layout_page_1.setObjectName("right_menu_vertical_layout_page_2")
        self.right_menu_not_working_label = QtWidgets.QLabel(self.page_1_right_menu)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                            QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.right_menu_not_working_label.sizePolicy().hasHeightForWidth())
        self.right_menu_not_working_label.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_not_working_label.setFont(font)
        self.right_menu_not_working_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.right_menu_not_working_label.setObjectName("right_menu_not_working_label")
        self.right_menu_vertical_layout_page_1.addWidget(self.right_menu_not_working_label)
        self.right_menu_stack.addWidget(self.page_1_right_menu)
        self.page_2_right_menu = QtWidgets.QWidget()
        self.page_2_right_menu.setObjectName("page_2_right_menu")
        self.right_menu_vertical_layout_page_2 = QtWidgets.QVBoxLayout(self.page_2_right_menu)
        self.right_menu_vertical_layout_page_2.setSpacing(10)
        self.right_menu_vertical_layout_page_2.setObjectName("right_menu_vertical_layout_page_2")
        spacer_item = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_2.addItem(spacer_item)
        self.right_menu_title_page_2 = QtWidgets.QLabel(self.page_2_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_2.setFont(font)
        self.right_menu_title_page_2.setObjectName("right_menu_title_page_2")
        self.right_menu_vertical_layout_page_2.addWidget(self.right_menu_title_page_2)
        self.complex_layout_page_2 = QtWidgets.QHBoxLayout()
        self.complex_layout_page_2.setObjectName("complex_layout_page_2")
        self.right_menu_input_page_2 = QtWidgets.QLineEdit(self.page_2_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_2.setFont(font)
        self.right_menu_input_page_2.setObjectName("right_menu_input_page_2")
        self.complex_layout_page_2.addWidget(self.right_menu_input_page_2)
        self.right_menu_button_page_2 = QtWidgets.QPushButton(self.page_2_right_menu)
        self.right_menu_button_page_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_button_page_2.setObjectName("right_menu_button_page_2")
        self.complex_layout_page_2.addWidget(self.right_menu_button_page_2)
        self.right_menu_vertical_layout_page_2.addLayout(self.complex_layout_page_2)
        self.right_menu_sub_text_page_2 = QtWidgets.QLabel(self.page_2_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_sub_text_page_2.setFont(font)
        self.right_menu_sub_text_page_2.setObjectName("right_menu_sub_text_page_2")
        self.right_menu_vertical_layout_page_2.addWidget(self.right_menu_sub_text_page_2)
        spacer_item1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_2.addItem(spacer_item1)
        self.right_menu_main_button_page_2 = QtWidgets.QPushButton(self.page_2_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_main_button_page_2.setFont(font)
        self.right_menu_main_button_page_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_main_button_page_2.setObjectName("right_menu_main_button_page_2")
        self.right_menu_vertical_layout_page_2.addWidget(self.right_menu_main_button_page_2)
        self.right_menu_stack.addWidget(self.page_2_right_menu)
        self.page_3_right_menu = QtWidgets.QWidget()
        self.page_3_right_menu.setObjectName("page_3_right_menu")
        self.right_menu_vertical_layout_page_3 = QtWidgets.QVBoxLayout(self.page_3_right_menu)
        self.right_menu_vertical_layout_page_3.setSpacing(10)
        self.right_menu_vertical_layout_page_3.setObjectName("right_menu_vertical_layout_page_3")
        spacer_item2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_3.addItem(spacer_item2)
        self.right_menu_title_page_3 = QtWidgets.QLabel(self.page_3_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_3.setFont(font)
        self.right_menu_title_page_3.setObjectName("right_menu_title_page_3")
        self.right_menu_vertical_layout_page_3.addWidget(self.right_menu_title_page_3)
        self.complex_layout_page_3 = QtWidgets.QHBoxLayout()
        self.complex_layout_page_3.setObjectName("complex_layout_page_3")
        self.check_box_page_3 = QtWidgets.QCheckBox(self.page_3_right_menu)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.check_box_page_3.sizePolicy().hasHeightForWidth())
        self.check_box_page_3.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.check_box_page_3.setFont(font)
        self.check_box_page_3.setObjectName("check_box_page_3")
        self.complex_layout_page_3.addWidget(self.check_box_page_3)
        self.right_menu_button_page_3 = QtWidgets.QPushButton(self.page_3_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_button_page_3.setFont(font)
        self.right_menu_button_page_3.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_button_page_3.setObjectName("right_menu_button_page_3")
        self.complex_layout_page_3.addWidget(self.right_menu_button_page_3)
        self.right_menu_vertical_layout_page_3.addLayout(self.complex_layout_page_3)
        self.right_menu_sub_text_page_3 = QtWidgets.QLabel(self.page_3_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_sub_text_page_3.setFont(font)
        self.right_menu_sub_text_page_3.setObjectName("right_menu_sub_text_page_3")
        self.right_menu_vertical_layout_page_3.addWidget(self.right_menu_sub_text_page_3)
        spacer_item3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_3.addItem(spacer_item3)
        self.right_menu_main_button_page_3 = QtWidgets.QPushButton(self.page_3_right_menu)
        self.right_menu_main_button_page_3.setObjectName("right_menu_main_button_page_3")
        self.right_menu_vertical_layout_page_3.addWidget(self.right_menu_main_button_page_3)
        self.right_menu_stack.addWidget(self.page_3_right_menu)
        self.page_4_right_menu = QtWidgets.QWidget()
        self.page_4_right_menu.setObjectName("page_4_right_menu")
        self.right_menu_vertical_layout_page_4 = QtWidgets.QVBoxLayout(self.page_4_right_menu)
        self.right_menu_vertical_layout_page_4.setSpacing(10)
        self.right_menu_vertical_layout_page_4.setObjectName("right_menu_vertical_layout_page_4")
        spacer_item4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_4.addItem(spacer_item4)
        self.right_menu_title_page_4 = QtWidgets.QLabel(self.page_4_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_4.setFont(font)
        self.right_menu_title_page_4.setObjectName("right_menu_title_page_4")
        self.right_menu_vertical_layout_page_4.addWidget(self.right_menu_title_page_4)
        self.complex_layout_page_4 = QtWidgets.QHBoxLayout()
        self.complex_layout_page_4.setObjectName("complex_layout_page_4")
        self.right_menu_main_button_page_4 = QtWidgets.QPushButton(self.page_4_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_main_button_page_4.setFont(font)
        self.right_menu_main_button_page_4.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_main_button_page_4.setObjectName("change_data_button_page_4")
        self.complex_layout_page_4.addWidget(self.right_menu_main_button_page_4)
        self.right_menu_vertical_layout_page_4.addLayout(self.complex_layout_page_4)
        self.right_menu_sub_text_page_4 = QtWidgets.QLabel(self.page_4_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_sub_text_page_4.setFont(font)
        self.right_menu_sub_text_page_4.setObjectName("right_menu_sub_text_page_4")
        self.right_menu_vertical_layout_page_4.addWidget(self.right_menu_sub_text_page_4)
        spacer_item5 = QtWidgets.QSpacerItem(20, 462, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_4.addItem(spacer_item5)
        self.right_menu_stack.addWidget(self.page_4_right_menu)
        self.page_5_right_menu = QtWidgets.QWidget()
        self.page_5_right_menu.setObjectName("page_5_right_menu")
        self.right_menu_vertical_layout_page_5 = QtWidgets.QVBoxLayout(self.page_5_right_menu)
        self.right_menu_vertical_layout_page_5.addSpacing(10)
        self.right_menu_vertical_layout_page_5.setObjectName("right_menu_vertical_layout_page_5")
        spacer_item6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_5.addItem(spacer_item6)
        self.right_menu_title_page_5_1 = QtWidgets.QLabel(self.page_5_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_5_1.setFont(font)
        self.right_menu_title_page_5_1.setObjectName("right_menu_title_page_5_1")
        self.right_menu_vertical_layout_page_5.addWidget(self.right_menu_title_page_5_1)
        self.right_menu_input_page_5_1 = QtWidgets.QLineEdit(self.page_5_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_5_1.setFont(font)
        self.right_menu_input_page_5_1.setObjectName("right_menu_input_page_5_1")
        self.right_menu_vertical_layout_page_5.addWidget(self.right_menu_input_page_5_1)
        spacer_item7 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_5.addItem(spacer_item7)
        self.right_menu_title_page_5_2 = QtWidgets.QLabel(self.page_5_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_5_2.setFont(font)
        self.right_menu_title_page_5_2.setObjectName("right_menu_title_page_5_2")
        self.right_menu_vertical_layout_page_5.addWidget(self.right_menu_title_page_5_2)
        self.complex_layout_page_5 = QtWidgets.QHBoxLayout()
        self.complex_layout_page_5.setObjectName("complex_layout_page_5")
        self.right_menu_input_page_5_2 = QtWidgets.QLineEdit(self.page_5_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_5_2.setFont(font)
        self.right_menu_input_page_5_2.setObjectName("right_menu_input_page_5_2")
        self.complex_layout_page_5.addWidget(self.right_menu_input_page_5_2)
        self.right_menu_button_page_5 = QtWidgets.QPushButton(self.page_5_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_button_page_5.setFont(font)
        self.right_menu_button_page_5.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_button_page_5.setObjectName("right_menu_button_page_5")
        self.complex_layout_page_5.addWidget(self.right_menu_button_page_5)
        self.right_menu_vertical_layout_page_5.addLayout(self.complex_layout_page_5)
        spacer_item8 = QtWidgets.QSpacerItem(20, 432, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_5.addItem(spacer_item8)
        self.right_menu_stack.addWidget(self.page_5_right_menu)
        self.page_6_right_menu = QtWidgets.QWidget()
        self.page_6_right_menu.setObjectName("page_6_right_menu")
        self.right_menu_vertical_layout_page_6 = QtWidgets.QVBoxLayout(self.page_6_right_menu)
        self.right_menu_vertical_layout_page_6.addSpacing(10)
        self.right_menu_vertical_layout_page_6.setObjectName("right_menu_vertical_layout_page_6")
        spacer_item9 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_6.addItem(spacer_item9)
        self.right_menu_title_page_6_1 = QtWidgets.QLabel(self.page_6_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_6_1.setFont(font)
        self.right_menu_title_page_6_1.setObjectName("right_menu_title_page_6_1")
        self.right_menu_vertical_layout_page_6.addWidget(self.right_menu_title_page_6_1)
        self.right_menu_input_page_6_1 = QtWidgets.QLineEdit(self.page_6_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_6_1.setFont(font)
        self.right_menu_input_page_6_1.setObjectName("right_menu_input_page_6_1")
        self.right_menu_vertical_layout_page_6.addWidget(self.right_menu_input_page_6_1)
        spacer_item10 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_6.addItem(spacer_item10)
        self.right_menu_title_page_6_2 = QtWidgets.QLabel(self.page_6_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_6_2.setFont(font)
        self.right_menu_title_page_6_2.setObjectName("right_menu_title_page_6_2")
        self.right_menu_vertical_layout_page_6.addWidget(self.right_menu_title_page_6_2)
        self.complex_layout_page_6 = QtWidgets.QHBoxLayout()
        self.complex_layout_page_6.setObjectName("complex_layout_page_6")
        self.right_menu_input_page_6_2 = QtWidgets.QLineEdit(self.page_6_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_6_2.setFont(font)
        self.right_menu_input_page_6_2.setObjectName("right_menu_input_page_6_2")
        self.complex_layout_page_6.addWidget(self.right_menu_input_page_6_2)
        self.right_menu_button_page_6 = QtWidgets.QPushButton(self.page_6_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_button_page_6.setFont(font)
        self.right_menu_button_page_6.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_button_page_6.setObjectName("right_menu_button_page_6")
        self.complex_layout_page_6.addWidget(self.right_menu_button_page_6)
        self.right_menu_vertical_layout_page_6.addLayout(self.complex_layout_page_6)
        spacer_item11 = QtWidgets.QSpacerItem(20, 429, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_6.addItem(spacer_item11)
        self.right_menu_stack.addWidget(self.page_6_right_menu)
        self.page_7_right_menu = QtWidgets.QWidget()
        self.page_7_right_menu.setObjectName("page_7_right_menu")
        self.right_menu_vertical_layout_page_7 = QtWidgets.QVBoxLayout(self.page_7_right_menu)
        self.right_menu_vertical_layout_page_7.setSpacing(10)
        self.right_menu_vertical_layout_page_7.setObjectName("right_menu_vertical_layout_page_7")
        spacer_item12 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_7.addItem(spacer_item12)
        self.right_menu_title_page_7 = QtWidgets.QLabel(self.page_7_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_7.setFont(font)
        self.right_menu_title_page_7.setObjectName("right_menu_title_page_7")
        self.right_menu_vertical_layout_page_7.addWidget(self.right_menu_title_page_7)
        self.complex_layout_page_7 = QtWidgets.QHBoxLayout()
        self.complex_layout_page_7.setObjectName("complex_layout_page_7")
        self.right_menu_input_page_7_1 = QtWidgets.QLineEdit(self.page_7_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_7_1.setFont(font)
        self.right_menu_input_page_7_1.setObjectName("right_menu_input_page_7_1")
        self.complex_layout_page_7.addWidget(self.right_menu_input_page_7_1)
        self.right_menu_text_mid_page_7 = QtWidgets.QLabel(self.page_7_right_menu)
        self.right_menu_text_mid_page_7.hide()
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_text_mid_page_7.setFont(font)
        self.right_menu_text_mid_page_7.setObjectName("right_menu_text_mid_page_7")
        self.complex_layout_page_7.addWidget(self.right_menu_text_mid_page_7)
        self.right_menu_input_page_7_2 = QtWidgets.QLineEdit(self.page_7_right_menu)
        self.right_menu_input_page_7_2.hide()
        self.right_menu_input_page_7_2.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_7_2.setFont(font)
        self.right_menu_input_page_7_2.setObjectName("right_menu_input_page_7_2")
        self.complex_layout_page_7.addWidget(self.right_menu_input_page_7_2)
        self.right_menu_button_page_7 = QtWidgets.QPushButton(self.page_7_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_button_page_7.setFont(font)
        self.right_menu_button_page_7.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_button_page_7.setObjectName("right_menu_button_page_7")
        self.complex_layout_page_7.addWidget(self.right_menu_button_page_7)
        self.right_menu_vertical_layout_page_7.addLayout(self.complex_layout_page_7)
        self.right_menu_progress_bar_page_7 = QtWidgets.QProgressBar(self.page_7_right_menu)
        self.right_menu_progress_bar_page_7.setTextVisible(False)
        self.right_menu_progress_bar_page_7.hide()
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_progress_bar_page_7.setFont(font)
        self.right_menu_progress_bar_page_7.setProperty("value", 24)
        self.right_menu_progress_bar_page_7.setTextVisible(True)
        self.right_menu_progress_bar_page_7.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.right_menu_progress_bar_page_7.setInvertedAppearance(False)
        self.right_menu_progress_bar_page_7.setObjectName("right_menu_progress_bar_page_7")
        self.right_menu_vertical_layout_page_7.addWidget(self.right_menu_progress_bar_page_7)
        self.right_menu_sub_text_page_7 = QtWidgets.QLabel(self.page_7_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_sub_text_page_7.setFont(font)
        self.right_menu_sub_text_page_7.setObjectName("right_menu_sub_text_page_7")
        self.right_menu_vertical_layout_page_7.addWidget(self.right_menu_sub_text_page_7)
        spacer_item13 = QtWidgets.QSpacerItem(20, 396, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_7.addItem(spacer_item13)
        self.right_menu_main_button_page_7 = QtWidgets.QPushButton(self.page_7_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_main_button_page_7.setFont(font)
        self.right_menu_main_button_page_7.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_main_button_page_7.setObjectName("right_menu_main_button_page_7")
        self.right_menu_vertical_layout_page_7.addWidget(self.right_menu_main_button_page_7)
        self.right_menu_stack.addWidget(self.page_7_right_menu)
        self.page_8_right_menu = QtWidgets.QWidget()
        self.page_8_right_menu.setObjectName("page_8_right_menu")
        self.right_menu_vertical_layout_page_8 = QtWidgets.QVBoxLayout(self.page_8_right_menu)
        self.right_menu_vertical_layout_page_8.addSpacing(10)
        self.right_menu_vertical_layout_page_8.setObjectName("right_menu_vertical_layout_page_8")
        spacer_item14 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_8.addItem(spacer_item14)
        self.right_menu_title_page_8 = QtWidgets.QLabel(self.page_8_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_8.setFont(font)
        self.right_menu_title_page_8.setObjectName("right_menu_title_page_8")
        self.right_menu_vertical_layout_page_8.addWidget(self.right_menu_title_page_8)
        self.right_menu_calendar_page_8 = QtWidgets.QCalendarWidget(self.page_8_right_menu)
        self.right_menu_calendar_page_8.setEnabled(True)
        self.right_menu_calendar_page_8.setObjectName("right_menu_calendar_page_8")
        self.right_menu_vertical_layout_page_8.addWidget(self.right_menu_calendar_page_8)
        self.complex_layout_page_8 = QtWidgets.QHBoxLayout()
        self.complex_layout_page_8.setObjectName("complex_layout_page_8")
        self.right_menu_input_page_8 = QtWidgets.QLineEdit(self.page_8_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_8.setFont(font)
        self.right_menu_input_page_8.setObjectName("right_menu_input_page_8")
        self.complex_layout_page_8.addWidget(self.right_menu_input_page_8)
        self.change_data_button_page_8 = QtWidgets.QPushButton(self.page_8_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.change_data_button_page_8.setFont(font)
        self.change_data_button_page_8.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.change_data_button_page_8.setObjectName("change_data_button_page_8")
        self.complex_layout_page_8.addWidget(self.change_data_button_page_8)
        self.right_menu_vertical_layout_page_8.addLayout(self.complex_layout_page_8)
        self.right_menu_sub_text_page_8 = QtWidgets.QLabel(self.page_8_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_sub_text_page_8.setFont(font)
        self.right_menu_sub_text_page_8.setObjectName("right_menu_sub_text_page_8")
        self.right_menu_vertical_layout_page_8.addWidget(self.right_menu_sub_text_page_8)
        spacer_item15 = QtWidgets.QSpacerItem(20, 218, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_8.addItem(spacer_item15)
        self.right_menu_main_button_page_8 = QtWidgets.QPushButton(self.page_8_right_menu)
        self.right_menu_main_button_page_8.setObjectName("right_menu_main_button_page_8")
        self.right_menu_vertical_layout_page_8.addWidget(self.right_menu_main_button_page_8)
        self.right_menu_stack.addWidget(self.page_8_right_menu)
        self.page_9_right_menu = QtWidgets.QWidget()
        self.page_9_right_menu.setObjectName("page_9_right_menu")
        self.right_menu_vertical_layout_page_9 = QtWidgets.QVBoxLayout(self.page_9_right_menu)
        self.right_menu_vertical_layout_page_9.addSpacing(10)
        self.right_menu_vertical_layout_page_9.setObjectName("right_menu_vertical_layout_page_9")
        spacer_item16 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_9.addItem(spacer_item16)
        self.right_menu_title_page_9 = QtWidgets.QLabel(self.page_9_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_9.setFont(font)
        self.right_menu_title_page_9.setObjectName("right_menu_title_page_9")
        self.right_menu_vertical_layout_page_9.addWidget(self.right_menu_title_page_9)
        self.image = QtWidgets.QLabel(self.page_9_right_menu)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum,
                                            QtWidgets.QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(size_policy)
        self.image.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.image.setText("")
        self.image.setScaledContents(True)
        self.image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image.setWordWrap(True)
        self.image.setObjectName("image")
        self.right_menu_vertical_layout_page_9.addWidget(self.image)
        self.complex_layout_page_9 = QtWidgets.QHBoxLayout()
        self.complex_layout_page_9.setObjectName("complex_layout_page_9")
        self.right_menu_button_page_9_1 = QtWidgets.QPushButton(self.page_9_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_button_page_9_1.setFont(font)
        self.right_menu_button_page_9_1.setObjectName("right_menu_button_page_9_1")
        self.complex_layout_page_9.addWidget(self.right_menu_button_page_9_1)
        self.right_menu_button_page_9_2 = QtWidgets.QPushButton(self.page_9_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_button_page_9_2.setFont(font)
        self.right_menu_button_page_9_2.setObjectName("right_menu_button_page_9_2")
        self.complex_layout_page_9.addWidget(self.right_menu_button_page_9_2)
        self.right_menu_vertical_layout_page_9.addLayout(self.complex_layout_page_9)
        self.right_menu_sub_text_page_9 = QtWidgets.QLabel(self.page_9_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_sub_text_page_9.setFont(font)
        self.right_menu_sub_text_page_9.setObjectName("right_menu_sub_text_page_9")
        self.right_menu_vertical_layout_page_9.addWidget(self.right_menu_sub_text_page_9)
        spacer_item17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_9.addItem(spacer_item17)
        self.right_menu_stack.addWidget(self.page_9_right_menu)
        self.page_10_right_menu = QtWidgets.QWidget()
        self.page_10_right_menu.setObjectName("page_10_right_menu")
        self.right_menu_vertical_layout_page_10 = QtWidgets.QVBoxLayout(self.page_10_right_menu)
        self.right_menu_vertical_layout_page_10.setSpacing(10)
        self.right_menu_vertical_layout_page_10.setObjectName("right_menu_vertical_layout_page_10")
        spacer_item18 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_10.addItem(spacer_item18)
        self.right_menu_title_page_10 = QtWidgets.QLabel(self.page_10_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_10.setFont(font)
        self.right_menu_title_page_10.setObjectName("right_menu_title_page_10")
        self.right_menu_vertical_layout_page_10.addWidget(self.right_menu_title_page_10)
        self.complex_layout_page_10 = QtWidgets.QHBoxLayout()
        self.complex_layout_page_10.setObjectName("complex_layout_page_10")
        self.right_menu_button_page_10_1 = QtWidgets.QPushButton(self.page_10_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_button_page_10_1.setFont(font)
        self.right_menu_button_page_10_1.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_button_page_10_1.setObjectName("right_menu_button_page_10_1")
        self.complex_layout_page_10.addWidget(self.right_menu_button_page_10_1)
        self.right_menu_button_page_10_2 = QtWidgets.QPushButton(self.page_10_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_button_page_10_2.setFont(font)
        self.right_menu_button_page_10_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_button_page_10_2.setObjectName("right_menu_button_page_10_2")
        self.complex_layout_page_10.addWidget(self.right_menu_button_page_10_2)
        self.right_menu_vertical_layout_page_10.addLayout(self.complex_layout_page_10)
        spacer_item19 = QtWidgets.QSpacerItem(20, 494, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_10.addItem(spacer_item19)
        self.right_menu_stack.addWidget(self.page_10_right_menu)
        self.page_11_right_menu = QtWidgets.QWidget()
        self.page_11_right_menu.setObjectName("page_11_right_menu")
        self.right_menu_vertical_layout_page_11 = QtWidgets.QVBoxLayout(self.page_11_right_menu)
        self.right_menu_vertical_layout_page_11.addSpacing(10)
        self.right_menu_vertical_layout_page_11.setObjectName("right_menu_vertical_layout_page_11")
        spacer_item20 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_11.addItem(spacer_item20)
        self.right_menu_title_page_11 = QtWidgets.QLabel(self.page_11_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_11.setFont(font)
        self.right_menu_title_page_11.setObjectName("right_menu_title_page_11")
        self.right_menu_vertical_layout_page_11.addWidget(self.right_menu_title_page_11)
        self.right_menu_input_page_11_1 = QtWidgets.QLineEdit(self.page_11_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_11_1.setFont(font)
        self.right_menu_input_page_11_1.setObjectName("right_menu_input_page_11_1")
        self.right_menu_vertical_layout_page_11.addWidget(self.right_menu_input_page_11_1)
        self.right_menu_input_page_11_2 = QtWidgets.QLineEdit(self.page_11_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_11_2.setFont(font)
        self.right_menu_input_page_11_2.setObjectName("right_menu_input_page_11_2")
        self.right_menu_vertical_layout_page_11.addWidget(self.right_menu_input_page_11_2)
        self.right_menu_input_page_11_3 = QtWidgets.QLineEdit(self.page_11_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_11_3.setFont(font)
        self.right_menu_input_page_11_3.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.right_menu_input_page_11_3.setObjectName("right_menu_input_page_11_3")
        self.right_menu_vertical_layout_page_11.addWidget(self.right_menu_input_page_11_3)
        spacer_item21 = QtWidgets.QSpacerItem(20, 418, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_11.addItem(spacer_item21)
        self.right_menu_main_button_page_11 = QtWidgets.QPushButton(self.page_11_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_main_button_page_11.setFont(font)
        self.right_menu_main_button_page_11.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_main_button_page_11.setObjectName("right_menu_main_button_page_11")
        self.right_menu_vertical_layout_page_11.addWidget(self.right_menu_main_button_page_11)
        self.right_menu_stack.addWidget(self.page_11_right_menu)
        self.page_12_right_menu = QtWidgets.QWidget()
        self.page_12_right_menu.setObjectName("page_12_right_menu")
        self.right_menu_vertical_layout_page_12 = QtWidgets.QVBoxLayout(self.page_12_right_menu)
        self.right_menu_vertical_layout_page_12.addSpacing(10)
        self.right_menu_vertical_layout_page_12.setObjectName("right_menu_vertical_layout_page_12")
        spacer_item22 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_12.addItem(spacer_item22)
        self.right_menu_title_page_12 = QtWidgets.QLabel(self.page_12_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_12.setFont(font)
        self.right_menu_title_page_12.setObjectName("right_menu_title_page_12")
        self.right_menu_vertical_layout_page_12.addWidget(self.right_menu_title_page_12)
        self.right_menu_input_page_12_1 = QtWidgets.QLineEdit(self.page_12_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_12_1.setFont(font)
        self.right_menu_input_page_12_1.setObjectName("right_menu_input_page_12_1")
        self.right_menu_vertical_layout_page_12.addWidget(self.right_menu_input_page_12_1)
        self.right_menu_input_page_12_2 = QtWidgets.QLineEdit(self.page_12_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_12_2.setFont(font)
        self.right_menu_input_page_12_2.setObjectName("right_menu_input_page_12_2")
        self.right_menu_vertical_layout_page_12.addWidget(self.right_menu_input_page_12_2)
        self.right_menu_input_page_12_3 = QtWidgets.QLineEdit(self.page_12_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_12_3.setFont(font)
        self.right_menu_input_page_12_3.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.right_menu_input_page_12_3.setObjectName("right_menu_input_page_12_3")
        self.right_menu_vertical_layout_page_12.addWidget(self.right_menu_input_page_12_3)
        spacer_item23 = QtWidgets.QSpacerItem(20, 418, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_12.addItem(spacer_item23)
        self.right_menu_main_button_page_12 = QtWidgets.QPushButton(self.page_12_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_main_button_page_12.setFont(font)
        self.right_menu_main_button_page_12.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_main_button_page_12.setObjectName("right_menu_main_button_page_12")
        self.right_menu_vertical_layout_page_12.addWidget(self.right_menu_main_button_page_12)
        self.right_menu_stack.addWidget(self.page_12_right_menu)
        self.page_13_right_menu = QtWidgets.QWidget()
        self.page_13_right_menu.setObjectName("page_13_right_menu")
        self.right_menu_vertical_layout_page_13 = QtWidgets.QVBoxLayout(self.page_13_right_menu)
        self.right_menu_vertical_layout_page_13.setSpacing(10)
        self.right_menu_vertical_layout_page_13.setObjectName("right_menu_vertical_layout_page_13")
        spacer_item24 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_13.addItem(spacer_item24)
        self.right_menu_title_page_13 = QtWidgets.QLabel(self.page_13_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.right_menu_title_page_13.setFont(font)
        self.right_menu_title_page_13.setObjectName("right_menu_title_page_13")
        self.right_menu_vertical_layout_page_13.addWidget(self.right_menu_title_page_13)
        self.right_menu_input_page_13_1 = QtWidgets.QLineEdit(self.page_13_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_13_1.setFont(font)
        self.right_menu_input_page_13_1.setObjectName("right_menu_input_page_13_1")
        self.right_menu_vertical_layout_page_13.addWidget(self.right_menu_input_page_13_1)
        self.right_menu_input_page_13_2 = QtWidgets.QLineEdit(self.page_13_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_13_2.setFont(font)
        self.right_menu_input_page_13_2.setObjectName("right_menu_input_page_13_2")
        self.right_menu_vertical_layout_page_13.addWidget(self.right_menu_input_page_13_2)
        spacer_item25 = QtWidgets.QSpacerItem(20, 444, QtWidgets.QSizePolicy.Policy.Minimum,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_13.addItem(spacer_item25)
        self.right_menu_main_button_page_13 = QtWidgets.QPushButton(self.page_13_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_main_button_page_13.setFont(font)
        self.right_menu_main_button_page_13.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_main_button_page_13.setObjectName("right_menu_main_button_page_13")
        self.right_menu_vertical_layout_page_13.addWidget(self.right_menu_main_button_page_13)
        self.right_menu_stack.addWidget(self.page_13_right_menu)
        self.right_menu_stack_layout.addWidget(self.right_menu_stack)

        self.verticalLayout_3.addWidget(self.right_menu)

        self.horizontalLayout.addWidget(self.right_menu_container)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)

        self.setCentralWidget(self.central_widget)

        self.animation_left_menu = QPropertyAnimation(self.left_menu_container, b"maximumWidth")
        self.animation_right_menu = QPropertyAnimation(self.right_menu_container, b"maximumWidth")

        QtCore.QMetaObject.connectSlotsByName(self)

        self.setup_connects()
        self.setup_text()
        self.setup_tables("clients")
        self.setup_tables("records")
        self.setup_tables("organizations")
        self.setup_stacks_and_tabs()
        self.setup_admin_info()
        self.setup_ui()

        # self.refresh_clients()
        # self.refresh_organizations()
        # self.refresh_records()

    # Настройка ui
    def setup_ui(self):

        self.page_1_button.setCheckable(True)
        self.page_1_button.setChecked(True)
        self.page_1_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.page_1_button.setIcon(QtGui.QIcon("app/static/icons/database.svg"))

        self.page_2_button.setCheckable(True)
        self.page_2_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.page_2_button.setIcon(QtGui.QIcon("app/static/icons/user.svg"))

        self.page_3_button.setCheckable(True)
        self.page_3_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.page_3_button.hide()
        self.page_3_button.setIcon(QtGui.QIcon("app/static/icons/logs.svg"))

        self.exit_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.exit_button.setIcon(QtGui.QIcon("app/static/icons/logout.svg"))
        self.exit_button.setIconSize(QtCore.QSize(12, 12))

        self.search_button.setEnabled(False)
        self.search_button_clients.setEnabled(False)
        self.search_button_records.setEnabled(False)

        self.open_left_menu_button.setIcon(QtGui.QIcon("app/static/icons/menu.svg"))
        self.open_left_menu_button.setIconSize(QtCore.QSize(25, 25))
        self.open_left_menu_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.open_left_menu_button.setStyleSheet("""
            QPushButton {
                background-color: none;
            }
        """)

        self.open_right_menu_button.setIcon(QtGui.QIcon("app/static/icons/menu.svg"))
        self.open_right_menu_button.setIconSize(QtCore.QSize(25, 25))
        self.open_right_menu_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.open_right_menu_button.setStyleSheet("""
            QPushButton {
                background-color: none;
            }
        """)

        self.right_menu_stack.setStyleSheet("""
            QPushButton {
                background-color: #E7E7E7;
                border: 2px solid #D4D4D4;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                border: 2px solid #BABABA;
            }
            QPushButton:pressed {
                background-color: #DBDBDB;
            }
            QLineEdit {
                background-color: white;
                border-radius: 3px;
                border: 1px solid #575F6E;
            }
            QLineEdit:disabled {
                border: 2px solid #D4D4D4;
                background-color: #E8E8E8;
            }
            QLineEdit:hover {
                background-color: #F6F6F6;
            }
            QLineEdit:focus {
                background-color: #F2F2F2;
            }
        """)

        self.right_menu_button_page_10_1.setMinimumHeight(30)
        self.right_menu_button_page_10_1.setText("SCV")
        self.right_menu_button_page_10_2.setMinimumHeight(30)
        self.right_menu_button_page_10_2.setText("DB")

        button_stylesheet = """                                                 
            QPushButton {                                                                            
                background-color: #007AFF;                                                           
                color: white;                                                                        
                border-radius: 3px;
                border: none;                                                                  
            }                                                                                        
            QPushButton:hover {                                                                      
                background-color: #1987FE;                                                           
            }                                                                                        
            QPushButton:pressed {                                                                    
                background-color: #62ABFB;                                                           
            }                                                                                        
            QPushButton:disabled {                                                                   
                background-color: #F5F5F5;                                                           
                color: grey;
                border: 2px solid #D4D4D4;                                                                         
            }                                                                                        
        """

        self.right_menu_main_button_page_2.setMinimumHeight(40)
        self.right_menu_main_button_page_2.setStyleSheet(button_stylesheet)

        self.right_menu_main_button_page_3.setMinimumHeight(40)
        self.right_menu_main_button_page_3.setStyleSheet(button_stylesheet)

        self.right_menu_main_button_page_4.setMinimumHeight(40)
        self.right_menu_main_button_page_4.setStyleSheet("""                                                 
            QPushButton {                                                                            
                background-color: #FF4545;                                                           
                color: white;                                                                        
                border-radius: 3px;
                border: none;                                                                  
            }                                                                                        
            QPushButton:hover {                                                                      
                background-color: #FF6363;                                                           
            }                                                                                        
            QPushButton:pressed {                                                                    
                background-color: #FF7676;                                                           
            }                                                                                        
            QPushButton:disabled {                                                                   
                background-color: #FFA6A6;                                                           
                color: grey;
                border: 2px solid #D4D4D4;                                                                         
            }                                                                                        
        """)

        self.right_menu_main_button_page_7.setMinimumHeight(40)
        self.right_menu_main_button_page_7.setStyleSheet(button_stylesheet)

        self.right_menu_main_button_page_8.setMinimumHeight(40)
        self.right_menu_main_button_page_8.setStyleSheet(button_stylesheet)

        self.right_menu_main_button_page_11.setMinimumHeight(40)
        self.right_menu_main_button_page_11.setStyleSheet(button_stylesheet)

        self.right_menu_main_button_page_12.setMinimumHeight(40)
        self.right_menu_main_button_page_12.setStyleSheet(button_stylesheet)

        self.right_menu_main_button_page_13.setMinimumHeight(40)
        self.right_menu_main_button_page_13.setStyleSheet(button_stylesheet)

        self.right_menu_input_page_13_1.setMinimumHeight(25)
        self.right_menu_input_page_13_2.setMinimumHeight(25)

        self.right_menu_input_page_12_1.setMinimumHeight(25)
        self.right_menu_input_page_12_2.setMinimumHeight(25)
        self.right_menu_input_page_12_3.setMinimumHeight(25)

        self.right_menu_input_page_11_1.setMinimumHeight(25)
        self.right_menu_input_page_11_2.setMinimumHeight(25)
        self.right_menu_input_page_11_3.setMinimumHeight(25)

        self.right_menu_input_page_2.setMinimumHeight(25)
        self.right_menu_input_page_2.setTextMargins(5, 0, 5, 0)
        self.right_menu_button_page_2.setMinimumHeight(25)
        self.right_menu_button_page_2.setMinimumWidth(100)

        self.right_menu_button_page_7.setMinimumHeight(25)
        self.right_menu_button_page_7.setMinimumWidth(100)
        self.right_menu_input_page_7_1.setMinimumHeight(25)
        self.right_menu_input_page_7_2.setMinimumHeight(25)

        self.right_menu_button_page_3.setMinimumHeight(25)
        self.right_menu_button_page_3.setMinimumWidth(100)

        self.right_menu_input_page_13_1.setTextMargins(5, 0, 5, 0)
        self.right_menu_input_page_13_2.setTextMargins(5, 0, 5, 0)
        self.right_menu_input_page_12_1.setTextMargins(5, 0, 5, 0)
        self.right_menu_input_page_12_2.setTextMargins(5, 0, 5, 0)
        self.right_menu_input_page_12_3.setTextMargins(5, 0, 5, 0)
        self.right_menu_input_page_11_1.setTextMargins(5, 0, 5, 0)
        self.right_menu_input_page_11_2.setTextMargins(5, 0, 5, 0)
        self.right_menu_input_page_11_3.setTextMargins(5, 0, 5, 0)

        if not self.has_access:
            self.add_client_button.setEnabled(False)
            self.add_organization_button.setEnabled(False)
            self.add_record_button.setEnabled(False)

    # Настройка подключений
    def setup_connects(self):
        self.refresh_button_clients.clicked.connect(self.refresh_clients)
        self.refresh_button_records.clicked.connect(self.refresh_records)
        self.refresh_button.clicked.connect(self.refresh_organizations)
        self.search_button_clients.clicked.connect(self.search_clients_clicked)
        self.search_button.clicked.connect(self.search_organizations_clicked)
        self.search_button_records.clicked.connect(self.search_records_clicked)

        self.page_1_button.clicked.connect(self.page_1_button_clicked)
        self.page_2_button.clicked.connect(self.page_2_button_clicked)
        self.page_3_button.clicked.connect(self.page_3_button_clicked)
        self.exit_button.clicked.connect(self.exit_button_clicked)
        self.logout_button.clicked.connect(self.exit_button_clicked)
        self.editing_button.clicked.connect(self.request_editing_clicked)

        self.open_left_menu_button.clicked.connect(self.slide_left_menu)
        self.open_right_menu_button.clicked.connect(self.slide_right_menu)

        self.tabWidget.currentChanged.connect(self.tab_changed)

        def search_button_when_text_changed():
            if self.search_line_edit.text() == "":
                self.search_button.setEnabled(False)
            else:
                self.search_button.setEnabled(True)

        self.search_line_edit.textChanged.connect(search_button_when_text_changed)

        def search_button_clients_when_text_changed():
            if self.search_line_edit_clients.text() == "":
                self.search_button_clients.setEnabled(False)
            else:
                self.search_button_clients.setEnabled(True)

        self.search_line_edit_clients.textChanged.connect(search_button_clients_when_text_changed)

        def search_button_records_when_text_changed():
            if self.search_line_edit_records.text() == "":
                self.search_button_records.setEnabled(False)
            else:
                self.search_button_records.setEnabled(True)

        self.search_line_edit_records.textChanged.connect(search_button_records_when_text_changed)

        self.save_button.clicked.connect(lambda _: self.right_menu_export_clicked("organizations"))
        self.save_button_clients.clicked.connect(lambda _: self.right_menu_export_clicked("clients"))
        self.save_button_records.clicked.connect(lambda _: self.right_menu_export_clicked("records"))

        self.right_menu_button_page_10_1.clicked.connect(self.export_as_csv_clicked)
        self.right_menu_button_page_10_2.clicked.connect(self.export_as_db_clicked)

        self.add_client_button.clicked.connect(lambda _: self.right_menu_add_clicked("clients"))
        self.add_organization_button.clicked.connect(lambda _: self.right_menu_add_clicked("organizations"))
        self.add_record_button.clicked.connect(lambda _: self.right_menu_add_clicked("records"))

        self.right_menu_main_button_page_12.clicked.connect(self.right_menu_create_client_clicked)
        self.right_menu_main_button_page_11.clicked.connect(self.right_menu_create_organization_clicked)
        self.right_menu_main_button_page_13.clicked.connect(self.right_menu_create_record_clicked)

        self.clients_table.itemSelectionChanged.connect(self.right_menu_clients_selection_changed)
        self.organizations_table.itemSelectionChanged.connect(self.right_menu_organizations_selection_changed)
        self.records_table.itemSelectionChanged.connect(self.right_menu_records_selection_changed)

        self.right_menu_button_page_2.clicked.connect(self.update_input_data_page_2)
        self.right_menu_input_page_2.textChanged.connect(self.input_data_changed_page_2)
        self.right_menu_input_page_7_1.textChanged.connect(self.input_data_changed_page_7)
        self.right_menu_main_button_page_2.clicked.connect(self.update_data_main_button_page_2_clicked)
        self.right_menu_main_button_page_7.clicked.connect(self.update_data_main_button_page_7_clicked)

        self.right_menu_button_page_3.clicked.connect(self.update_input_data_page_3)
        self.check_box_page_3.stateChanged.connect(self.input_data_changed_page_3)
        self.right_menu_main_button_page_3.clicked.connect(self.update_data_main_button_page_3_clicked)

        self.right_menu_main_button_page_4.clicked.connect(self.update_data_main_button_page_4_clicked)

        self.right_menu_button_page_7.clicked.connect(self.update_input_data_page_7)

    # Настройка текста
    def setup_text(self):
        self.left_menu_title.setText("Страницы:")
        self.page_1_button.setText("Главная")
        self.page_2_button.setText("Аккаунт")
        self.page_3_button.setText("Логи")
        self.exit_button.setText("Выйти")
        self.page_title.setText("Название")
        self.search_line_edit.setPlaceholderText("Поиск")
        self.search_button.setText("Поиск")
        self.add_organization_button.setText("Добавить")
        self.save_button.setText("Экспорт")
        self.refresh_button.setText("Обновить")
        self.search_line_edit_clients.setPlaceholderText("Поиск")
        self.search_button_clients.setText("Поиск")
        self.add_client_button.setText("Добавить")
        self.save_button_clients.setText("Экспорт")
        self.refresh_button_clients.setText("Обновить")
        self.search_line_edit_records.setPlaceholderText("Поиск")
        self.search_button_records.setText("Поиск")
        self.add_record_button.setText("Добавить")
        self.save_button_records.setText("Экспорт")
        self.refresh_button_records.setText("Обновить")
        self.account_label.setText("Профиль")
        self.email_label.setText("Почта:")
        self.password_label.setText("Пароль:")
        self.password_field.setText("123123123")
        self.editing_label.setText("Редактирование:")
        self.editing.setText("Разрешено")
        self.editing_button.setText("Запросить доступ")
        self.logout_button.setText("Выйти")
        self.tabWidget.setTabText(0, "Организации")
        self.tabWidget.setTabText(1, "Клиенты")
        self.tabWidget.setTabText(2, "Записи")
        self.right_menu_not_working_label.setText("Боковое меню недоступно")
        self.right_menu_title_page_2.setText("Поле:")
        self.right_menu_title_page_3.setText("Поле:")
        self.right_menu_title_page_4.setText("Поле:")

        self.right_menu_button_page_2.setText("Редактировать")
        self.right_menu_button_page_3.setText("Редактировать")
        self.right_menu_button_page_7.setText("Редактировать")
        self.change_data_button_page_8.setText("Редактировать")
        self.right_menu_sub_text_page_2.setText("У вас нет прав на редактирование этого поля")
        self.right_menu_sub_text_page_3.setText("У вас нет прав на редактирование этого поля")
        self.right_menu_sub_text_page_4.setText("У вас нет прав на редактирование этого поля")
        self.right_menu_sub_text_page_7.setText("У вас нет прав на редактирование этого поля")
        self.right_menu_sub_text_page_8.setText("У вас нет прав на редактирование этого поля")
        self.right_menu_sub_text_page_9.setText("У вас нет прав на редактирование этого поля")
        self.right_menu_main_button_page_2.setText("Сохранить изменения")
        self.right_menu_main_button_page_3.setText("Сохранить изменения")
        self.right_menu_main_button_page_7.setText("Сохранить изменения")
        self.right_menu_main_button_page_8.setText("Сохранить изменения")
        self.check_box_page_3.setText("Приватный")
        self.page_title.setText("Главная")

        self.right_menu_main_button_page_11.setText("Создать")
        self.right_menu_main_button_page_12.setText("Создать")
        self.right_menu_main_button_page_13.setText("Создать")

        self.right_menu_title_page_13.setText("Создать запись:")
        self.right_menu_title_page_12.setText("Создать клиента:")
        self.right_menu_title_page_11.setText("Создать организацию:")

        self.right_menu_input_page_13_1.setPlaceholderText("id клиента")
        self.right_menu_input_page_13_2.setPlaceholderText("id организации")
        self.right_menu_input_page_13_1.setPlaceholderText("id клиента")
        self.right_menu_input_page_13_2.setPlaceholderText("id организации")
        self.right_menu_input_page_12_1.setPlaceholderText("Имя")
        self.right_menu_input_page_12_2.setPlaceholderText("Email")
        self.right_menu_input_page_12_3.setPlaceholderText("Пароль")
        self.right_menu_input_page_11_1.setPlaceholderText("Название")
        self.right_menu_input_page_11_2.setPlaceholderText("Email")
        self.right_menu_input_page_11_3.setPlaceholderText("Пароль")
        self.right_menu_text_mid_page_7.setText("из")

        self.right_menu_main_button_page_4.setText("Удалить")

    # Настройка header-ов таблиц
    def setup_tables(self, table_name: str):
        if table_name == "clients":
            self.clients_table.setColumnCount(5)
            self.clients_table.setHorizontalHeaderLabels([
                "id",
                "имя",
                "email",
                "пароль",
                "приватный"
            ])
            self.resize_columns(self.clients_table)
        if table_name == "records":
            self.records_table.setColumnCount(5)
            self.records_table.setHorizontalHeaderLabels([
                "id",
                "организация",
                "пользователь",
                "количество накопленных купонов",
                "дата последней записи"
            ])
            self.resize_columns(self.records_table)
        if table_name == "organizations":
            self.organizations_table.setColumnCount(7)
            self.organizations_table.setHorizontalHeaderLabels([
                "id",
                "название организации",
                "email",
                "пароль",
                "максимум купонов",
                "стикер",
                "изображение"
            ])
            self.resize_columns(self.organizations_table)

    # Настройка default-ных страниц и вкладок
    def setup_stacks_and_tabs(self):
        self.body_stack.setCurrentIndex(1)
        self.right_menu_stack.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)

    # Анимация - левое меню
    def slide_left_menu(self):
        width = self.left_menu_container.width()

        if width == 0:
            new_width = 250
            self.open_left_menu_button.setIcon(QtGui.QIcon("app/static/icons/left_arrow.svg"))
        else:
            new_width = 0
            self.open_left_menu_button.setIcon(QtGui.QIcon("app/static/icons/menu.svg"))

        self.animation_left_menu.setDuration(250)
        self.animation_left_menu.setStartValue(width)
        self.animation_left_menu.setEndValue(new_width)
        self.animation_left_menu.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation_left_menu.start()

    # Получения информации о состоянии левого меню
    def left_menu_is_open(self) -> bool:
        if self.left_menu_container.width() == 0:
            return False
        return True

    # Анимация - правое меню
    def slide_right_menu(self):
        width = self.right_menu_container.width()

        if width == 0:
            new_width = 500
            self.open_right_menu_button.setIcon(QtGui.QIcon("app/static/icons/right_arrow.svg"))
        else:
            new_width = 0
            self.open_right_menu_button.setIcon(QtGui.QIcon("app/static/icons/menu.svg"))

        self.animation_right_menu.setDuration(250)
        self.animation_right_menu.setStartValue(width)
        self.animation_right_menu.setEndValue(new_width)
        self.animation_right_menu.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation_right_menu.start()

    # Получения информации о состоянии правого меню
    def right_menu_is_open(self) -> bool:
        if self.right_menu_container.width() == 0:
            return False
        return True

    # Отображения таблицы - выравнивание столбцов
    def resize_columns(self, table: QtWidgets.QTableWidget) -> None:
        column_width = table.width() // table.columnCount() - 3
        for i in range(table.columnCount()):
            table.setColumnWidth(i, column_width)

    # Заполнить записи
    def fill_table_from_dict_clients(self, values_list: list[dict[str: object]]) -> None:

        self.clients_table.setRowCount(len(values_list))
        k = 0

        for client in values_list:
            client_id = QTableWidgetItem(str(client["id"]))
            client_id.setTextAlignment(self.in_table_cell_alignment)
            name = QTableWidgetItem(client["name"])
            name.setTextAlignment(self.in_table_cell_alignment)
            email = QTableWidgetItem(client["email"])
            email.setTextAlignment(self.in_table_cell_alignment)
            password = QTableWidgetItem(client["password"])
            password.setTextAlignment(self.in_table_cell_alignment)
            is_private = QTableWidgetItem("Да" if client["is_private"] else "Нет")
            is_private.setTextAlignment(self.in_table_cell_alignment)

            self.clients_table.setItem(k, 0, client_id)
            self.clients_table.setItem(k, 1, name)
            self.clients_table.setItem(k, 2, email)
            self.clients_table.setItem(k, 3, password)
            self.clients_table.setItem(k, 4, is_private)

            k += 1

    # Заполнить записи
    def fill_table_from_dict_organizations(self, values_list: list[dict[str: object]]) -> None:

        self.organizations_table.setRowCount(len(values_list))

        k = 0
        for record in values_list:

            organization_id = QTableWidgetItem(str(record["id"]))
            organization_id.setTextAlignment(self.in_table_cell_alignment)
            organization_title = QTableWidgetItem(str(record["title"]))
            organization_title.setTextAlignment(self.in_table_cell_alignment)
            email = QTableWidgetItem(str(record["email"]))
            email.setTextAlignment(self.in_table_cell_alignment)
            password = QTableWidgetItem(str(record["password"]))
            password.setTextAlignment(self.in_table_cell_alignment)
            coupons_limit = QTableWidgetItem(str(record["limit"]))
            coupons_limit.setTextAlignment(self.in_table_cell_alignment)
            sticker = QTableWidgetItem(str(record["sticker"]))
            sticker.setTextAlignment(self.in_table_cell_alignment)
            image_url = BASE_URL_IMAGE + str(record["image"])

            if record["image"]:
                image_label = QtWidgets.QLabel()
                image_label.setScaledContents(True)
                pillow_image = Image.open(requests.get(image_url, stream=True).raw)
                qt_image = ImageQt(pillow_image)
                pixmap = QtGui.QPixmap.fromImage(qt_image)
                image_label.setPixmap(pixmap)
            else:
                image_label = QtWidgets.QLabel()
                image_label.setText("Нет")
                image_label.setAlignment(self.in_table_cell_alignment)

            self.organizations_table.setItem(k, 0, organization_id)
            self.organizations_table.setItem(k, 1, organization_title)
            self.organizations_table.setItem(k, 2, email)
            self.organizations_table.setItem(k, 3, password)
            self.organizations_table.setItem(k, 4, coupons_limit)
            self.organizations_table.setItem(k, 5, sticker)
            self.organizations_table.setCellWidget(k, 6, image_label)

            k += 1

    # Заполнить записи
    def fill_table_from_dict_records(self, values_list: list[dict[str: object]]) -> None:

        self.records_table.setRowCount(len(values_list))

        k = 0
        for record in values_list:
            record_id = QTableWidgetItem((str(record["id"])))
            record_id.setTextAlignment(self.in_table_cell_alignment)
            organization = (str(record["organization"]))
            # organization.setTextAlignment(self.in_table_cell_alignment)
            organization_title = (str(record["organization_title"]))
            # organization_title.setTextAlignment(self.in_table_cell_alignment)
            organization_and_id = QTableWidgetItem(f"{organization_title} ({organization})")
            organization_and_id.setTextAlignment(self.in_table_cell_alignment)
            user_id = (str(record["client"]))
            # user_id.setTextAlignment(self.in_table_cell_alignment)
            user_name = (str(record["client_name"]))
            # user_name.setTextAlignment(self.in_table_cell_alignment)
            user = QTableWidgetItem(f"{user_name} ({user_id})")
            user.setTextAlignment(self.in_table_cell_alignment)
            accumulated = QTableWidgetItem(str(record["accumulated"]))
            accumulated.setTextAlignment(self.in_table_cell_alignment)
            last_record_date = QTableWidgetItem(str(record["last_record_date"]))
            last_record_date.setTextAlignment(self.in_table_cell_alignment)

            self.records_table.setItem(k, 0, record_id)
            self.records_table.setItem(k, 1, organization_and_id)
            self.records_table.setItem(k, 2, user)
            self.records_table.setItem(k, 3, accumulated)
            self.records_table.setItem(k, 4, last_record_date)

            k += 1

    # Обновить
    def refresh_clients(self) -> None:

        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        response = requests.get(
            f"{BASE_URL}/admin/clients",
            headers={"x-access-token": app.storage.get_value(key="token")}
        )

        if response.status_code != 200:
            QMessageBox.information(
                self,
                "Уведомление",
                "Срок действия сессии истёк"
            )
            app.window.addWidget(app.screens.LoginScreen.LoginScreen())
            app.window.setCurrentIndex(app.window.currentIndex() + 1)
        else:
            self.clients_data = response.json()
            self.fill_table_from_dict_clients(self.clients_data)

            self.resize_columns(self.clients_table)

    # Обновить
    def refresh_organizations(self) -> None:

        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        response = requests.get(
            f"{BASE_URL}/admin/organizations",
            headers={"x-access-token": app.storage.get_value(key="token")}
        )

        if response.status_code != 200:
            QMessageBox.information(
                self,
                "Уведомление",
                "Срок действия сессии истёк"
            )
            app.window.addWidget(app.screens.LoginScreen.LoginScreen())
            app.window.setCurrentIndex(app.window.currentIndex() + 1)
        else:
            self.organizations_data = response.json()
            self.fill_table_from_dict_organizations(self.organizations_data)

            self.resize_columns(self.organizations_table)

    # Обновить
    def refresh_records(self) -> None:

        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        response = requests.get(
            f"{BASE_URL}/admin/records",
            headers={"x-access-token": app.storage.get_value(key="token")}
        )

        print(response.status_code)

        if response.status_code != 200:
            QMessageBox.information(
                self,
                "Уведомление",
                "Срок действия сессии истёк"
            )
            app.window.addWidget(app.screens.LoginScreen.LoginScreen())
            app.window.setCurrentIndex(app.window.currentIndex() + 1)
        else:
            self.records_data = response.json()
            self.fill_table_from_dict_records(self.records_data)

            self.resize_columns(self.records_table)

    # Очистка таблиц
    def table_clear(self, table: QtWidgets.QTableWidget) -> None:
        while table.rowCount() > 0:
            table.removeRow(0)

    # Поиск
    def search_in_table(self, values_list: list[dict[str: object]], search_request: str, selected: list) \
            -> list[dict[str: object]]:
        result: list[dict[str: object]] = list()
        visited = list()
        for elem in selected:
            if elem is None:
                continue
            y = elem.row()
            if search_request in elem.text() and y not in visited:
                result.append(values_list[y])
                visited.append(y)
        return result

    # Поиск - кнопка
    def search_clients_clicked(self) -> None:
        selected = self.clients_table.selectedItems()
        if len(selected) == 0:
            for i in range(self.clients_table.rowCount()):
                for j in range(self.clients_table.columnCount()):
                    selected.append(self.clients_table.item(i, j))
        searched_rows = self.search_in_table(self.clients_data, self.search_line_edit_clients.text(), selected)
        self.table_clear(self.clients_table)
        self.fill_table_from_dict_clients(searched_rows)

        column_width = self.clients_table.width() // 5 - 3
        for i in range(5):
            self.clients_table.setColumnWidth(i, column_width)

    # Поиск - кнопка
    def search_organizations_clicked(self) -> None:
        selected = self.organizations_table.selectedItems()
        if len(selected) == 0:
            for i in range(self.organizations_table.rowCount()):
                for j in range(self.organizations_table.columnCount()):
                    selected.append(self.organizations_table.item(i, j))
        searched_rows = self.search_in_table(self.organizations_data, self.search_line_edit.text(), selected)
        self.table_clear(self.organizations_table)
        self.fill_table_from_dict_organizations(searched_rows)

    # Поиск - кнопка
    def search_records_clicked(self) -> None:
        selected = self.records_table.selectedItems()
        if len(selected) == 0:
            for i in range(self.records_table.rowCount()):
                for j in range(self.records_table.columnCount()):
                    selected.append(self.records_table.item(i, j))
        searched_rows = self.search_in_table(self.records_data, self.search_line_edit_records.text(), selected)
        self.table_clear(self.records_table)
        self.fill_table_from_dict_records(searched_rows)

    # Выбор страниц - главная - кнопка
    def page_1_button_clicked(self):
        self.page_title.setText("Главная")
        if self.page_1_button.isChecked():
            self.body_stack.setCurrentIndex(1)
            self.page_2_button.setChecked(False)
            self.page_3_button.setChecked(False)
        else:
            self.page_1_button.setChecked(True)

    # Выбор страниц - профиль - кнопка
    def page_2_button_clicked(self):
        self.page_title.setText("Аккаунт")
        if self.page_2_button.isChecked():
            self.body_stack.setCurrentIndex(0)
            self.page_1_button.setChecked(False)
            self.page_3_button.setChecked(False)
        else:
            self.page_2_button.setChecked(True)

    # Выбор страниц - логи - кнопка
    def page_3_button_clicked(self):
        self.page_title.setText("Логи")
        if self.page_3_button.isChecked():
            self.body_stack.setCurrentIndex(2)
            self.page_1_button.setChecked(False)
            self.page_2_button.setChecked(False)
        else:
            self.page_3_button.setChecked(True)

    # Выбор страниц - выход + logout
    def exit_button_clicked(self):
        question = QMessageBox.question(
            self,
            "Подтверждение",
            "Нажмите 'Ok', чтобы завершить сессию и выйти из программы",
            QMessageBox.StandardButton.Ok |
            QMessageBox.StandardButton.Cancel
        )

        if question == QMessageBox.StandardButton.Ok:
            app.storage.remove_key("token")
            exit(0)

    # Страница правого меню - экспорт - кнопка
    def right_menu_export_clicked(self, table_name: str, should_open=True) -> None:

        self.right_menu_stack.setCurrentIndex(9)

        if table_name == "organizations":
            self.right_menu_title_page_10.setText("Экспорт организаций:")
        elif table_name == "clients":
            self.right_menu_title_page_10.setText("Экспорт клиентов:")
        elif table_name == "records":
            self.right_menu_title_page_10.setText("Экспорт записей:")
        self.export_table_name = table_name

        if not self.right_menu_is_open() and should_open:
            self.slide_right_menu()

    # Страница правого меню - экспорт - кнопка
    def right_menu_add_clicked(self, table_name: str, should_open=True) -> None:

        if table_name == "organizations":
            self.right_menu_stack.setCurrentIndex(10)
        elif table_name == "clients":
            self.right_menu_stack.setCurrentIndex(11)
        elif table_name == "records":
            self.right_menu_stack.setCurrentIndex(12)

        if not self.right_menu_is_open() and should_open:
            self.slide_right_menu()

    # Страница правого меню - регистрация клиента - кнопка
    def right_menu_create_client_clicked(self):
        name = self.right_menu_input_page_12_1.text()
        email = self.right_menu_input_page_12_2.text()
        password = self.right_menu_input_page_12_3.text()

        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        response = requests.post(
            f"{BASE_URL}/client/signup",
            json={
                "name": name,
                "email": email,
                "password": password
            }
        )

        if response.status_code != 200:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Что-то введено некорректно"
            )
        else:
            QMessageBox.information(
                self,
                "Готово",
                "Аккаунт клиента создан"
            )

    # Страница правого меню - регистрация организации - кнопка
    def right_menu_create_organization_clicked(self):

        title = self.right_menu_input_page_11_1.text()
        email = self.right_menu_input_page_11_2.text()
        password = self.right_menu_input_page_11_3.text()

        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        response = requests.post(
            f"{BASE_URL}/organization/signup",
            json={
                "title": title,
                "email": email,
                "password": password
            }
        )

        if response.status_code != 200:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Что-то введено некорректно"
            )
        else:
            QMessageBox.information(
                self,
                "Готово",
                "Организация создана"
            )

    # Страница правого меню - регистрация записи - кнопка
    def right_menu_create_record_clicked(self):

        client_id = self.right_menu_input_page_13_1.text()
        organization_id = self.right_menu_input_page_13_2.text()

        if not client_id.isdigit() or not organization_id.isdigit():
            QMessageBox.warning(
                self,
                "Ошибка",
                "Что-то введено некорректно"
            )
            return

        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        response = requests.post(
            f"{BASE_URL}/admin/create/record",
            headers={"x-access-token": app.storage.get_value(key="token")},
            json={"client_id": client_id,
                  'organization_id': organization_id}
        )

        if response.status_code != 200:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Что-то введено некорректно"
            )
        else:
            QMessageBox.information(
                self,
                "Готово",
                "Запись создана"
            )

    # Страница правого меню - кнопка разрешения редактирования
    def update_input_data_page_2(self):
        self.right_menu_input_page_2.setEnabled(not self.right_menu_input_page_2.isEnabled())

    def update_input_data_page_3(self):
        self.check_box_page_3.setEnabled(not self.check_box_page_3.isEnabled())

    def update_input_data_page_7(self):
        self.right_menu_input_page_7_1.setEnabled(not self.right_menu_input_page_7_1.isEnabled())

    def update_data_main_button_page_2_clicked(self):

        if self.current_table_name == "clients":

            headers = ["id", "name", "email", "password", "is_private"]

            if not check_server():

                message_box = QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Не удалось подключиться к серверу",
                    QMessageBox.StandardButton.Abort
                )

                if message_box == QMessageBox.StandardButton.Abort:
                    exit(-1)

            _json = {"id": self.current_client_id}
            _key = headers[self.clients_table_current_selection[1]]
            _value = self.right_menu_input_page_2.text()
            _json[_key] = _value

            response = requests.put(
                f"{BASE_URL}/admin/clients/update",
                headers={"x-access-token": app.storage.get_value(key="token")},
                json=_json
            )

            if response.status_code != 200:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Что-то введено некорректно"
                )
            else:
                QMessageBox.information(
                    self,
                    "Готово",
                    "Данные обновлены"
                )

        elif self.current_table_name == "organizations":

            headers = ["id", "title", "email", "password", "limit", "sticker", "image"]

            if not check_server():

                message_box = QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Не удалось подключиться к серверу",
                    QMessageBox.StandardButton.Abort
                )

                if message_box == QMessageBox.StandardButton.Abort:
                    exit(-1)

            _json = {"id": self.current_organization_id}
            _key = headers[self.organizations_table_current_selection[1]]
            _value = self.right_menu_input_page_2.text()
            _json[_key] = _value

            if _key == "limit":
                if _value.isdigit():
                    _json[_key] = int(_value)
                else:
                    QMessageBox.warning(
                        self,
                        "Ошибка",
                        "Что-то введено некорректно"
                    )
                    return

            response = requests.put(
                f"{BASE_URL}/admin/organizations/update",
                headers={"x-access-token": app.storage.get_value(key="token")},
                json=_json
            )

            print(response.json())

            if response.status_code != 200:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Что-то введено некорректно"
                )
            else:
                QMessageBox.information(
                    self,
                    "Готово",
                    "Данные обновлены"
                )

    def update_data_main_button_page_3_clicked(self):

        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        _json = {"id": self.current_client_id, "is_private": self.check_box_page_3.isChecked()}

        response = requests.put(
            f"{BASE_URL}/admin/clients/update",
            headers={"x-access-token": app.storage.get_value(key="token")},
            json=_json
        )

        if response.status_code != 200:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Что-то введено некорректно"
            )
        else:
            QMessageBox.information(
                self,
                "Готово",
                "Данные обновлены"
            )

    def update_data_main_button_page_4_clicked(self):

        if self.current_table_name == "clients":
            question = QMessageBox.question(
                self,
                "Подтверждение",
                "Вы уверены, что хотите удалить этого клиента?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )
            if question == QMessageBox.StandardButton.No:
                return

            if not check_server():

                message_box = QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Не удалось подключиться к серверу",
                    QMessageBox.StandardButton.Abort
                )

                if message_box == QMessageBox.StandardButton.Abort:
                    exit(-1)

            response = requests.post(
                f"{BASE_URL}/admin/clients/remove",
                headers={"x-access-token": app.storage.get_value(key="token")},
                json={"id": self.current_client_id}
            )

            if response.status_code != 200:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Что-то введено некорректно"
                )
            else:
                QMessageBox.information(
                    self,
                    "Готово",
                    "Клиент удалён"
                )

        elif self.current_table_name == "organizations":
            question = QMessageBox.question(
                self,
                "Подтверждение",
                "Вы уверены, что хотите удалить эту организацию?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )
            if question == QMessageBox.StandardButton.No:
                return

            if not check_server():

                message_box = QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Не удалось подключиться к серверу",
                    QMessageBox.StandardButton.Abort
                )

                if message_box == QMessageBox.StandardButton.Abort:
                    exit(-1)

            response = requests.post(
                f"{BASE_URL}/admin/organizations/remove",
                headers={"x-access-token": app.storage.get_value(key="token")},
                json={"id": self.current_organization_id}
            )

            if response.status_code != 200:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Что-то введено некорректно"
                )
            else:
                QMessageBox.information(
                    self,
                    "Готово",
                    "Организация удалён"
                )

        elif self.current_table_name == "records":
            question = QMessageBox.question(
                self,
                "Подтверждение",
                "Вы уверены, что хотите удалить эту запись?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )
            if question == QMessageBox.StandardButton.No:
                return

            if not check_server():

                message_box = QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Не удалось подключиться к серверу",
                    QMessageBox.StandardButton.Abort
                )

                if message_box == QMessageBox.StandardButton.Abort:
                    exit(-1)

            response = requests.post(
                f"{BASE_URL}/admin/records/remove",
                headers={"x-access-token": app.storage.get_value(key="token")},
                json={"id": self.current_record_id}
            )

            if response.status_code != 200:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Что-то введено некорректно"
                )
            else:
                QMessageBox.information(
                    self,
                    "Готово",
                    "Запись удалена"
                )

    def update_data_main_button_page_7_clicked(self):
        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        try:
            int(self.right_menu_input_page_7_1.text())
        except ValueError:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Что-то введено некорректно"
            )
            return
        _json = {"id": self.current_record_id, "accumulated": int(self.right_menu_input_page_7_1.text())}

        response = requests.put(
            f"{BASE_URL}/admin/records/update",
            headers={"x-access-token": app.storage.get_value(key="token")},
            json=_json
        )

        if response.status_code != 200:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Что-то введено некорректно"
            )
        else:
            QMessageBox.information(
                self,
                "Готово",
                "Данные обновлены"
            )

    def input_data_changed_page_2(self):
        if self.current_table_name == "clients":
            before = self.clients_table.item(self.clients_table_current_selection[0],
                                             self.clients_table_current_selection[1]).text()
            if self.right_menu_input_page_2.text() != before:
                self.right_menu_main_button_page_2.setEnabled(True)
            else:
                self.right_menu_main_button_page_2.setEnabled(False)
        elif self.current_table_name == "organizations":
            before = self.organizations_table.item(self.organizations_table_current_selection[0],
                                                   self.organizations_table_current_selection[1]).text()
            if self.right_menu_input_page_2.text() != before:
                self.right_menu_main_button_page_2.setEnabled(True)
            else:
                self.right_menu_main_button_page_2.setEnabled(False)

    def input_data_changed_page_3(self):
        checked = self.check_box_page_3.isChecked()
        _b = self.clients_table.item(self.clients_table_current_selection[0],
                                     self.clients_table_current_selection[1]).text()
        before = _b == "Да"
        if checked != before:
            self.right_menu_main_button_page_3.setEnabled(True)
        else:
            self.right_menu_main_button_page_3.setEnabled(False)

        if self.check_box_page_3.isChecked():
            self.check_box_page_3.setText("Приватный")
        else:
            self.check_box_page_3.setText("Стандартный")

    def input_data_changed_page_7(self):
        before = self.records_table.item(self.records_table_current_selection[0],
                                         self.records_table_current_selection[1]).text()
        if self.right_menu_input_page_7_1.text() != before:
            self.right_menu_main_button_page_7.setEnabled(True)
        else:
            self.right_menu_main_button_page_7.setEnabled(False)

    # Экспорт csv - кнопка
    def export_as_csv_clicked(self) -> None:
        print(f"csv {self.export_table_name}")
        save_file_path = QFileDialog.getSaveFileName(self, 'Укажите, куда вы хотите сохранить файл', '',
                                                     'CSV Таблица (*.csv)')[0]
        with open(save_file_path, "w", encoding="utf-16") as csv_file:
            writer = csv.writer(csv_file)
            rows_to_write = list()
            if self.export_table_name == "clients":

                header = list()
                for key in self.clients_data[0].keys():
                    header.append(key)
                rows_to_write.append(header)
                print(self.clients_data)
                for y in range(len(self.clients_data)):
                    row = list()
                    for key in header:
                        item = str(self.clients_data[y][key])
                        row.append(item)
                    rows_to_write.append(row)
            elif self.export_table_name == "organizations":
                header = list()
                for key in self.organizations_data[0].keys():
                    header.append(key)
                rows_to_write.append(header)
                print(self.organizations_data)
                for y in range(len(self.organizations_data)):
                    row = list()
                    for key in header:
                        item = str(self.organizations_data[y][key])
                        if key == "image" and (item != "None"):
                            item = BASE_URL_IMAGE + item
                        row.append(item)
                    rows_to_write.append(row)
            else:
                header = list()
                for key in self.records_data[0].keys():
                    header.append(key)
                rows_to_write.append(header)
                print(self.records_data)
                for y in range(len(self.records_data)):
                    row = list()
                    for key in header:
                        item = str(self.records_data[y][key])
                        row.append(item)
                    rows_to_write.append(row)
            writer.writerows(rows_to_write)

    # Экспорт db - кнопка
    def export_as_db_clicked(self) -> None:
        save_file_path = QFileDialog.getSaveFileName(self, 'Укажите, куда вы хотите сохранить файл', '',
                                                     'База данных (*.db)')[0]
        connection = sqlite3.connect(save_file_path)
        data_base_cursor = connection.cursor()
        if self.export_table_name == "clients":
            data_base_cursor.execute("""CREATE TABLE clients 
                                        (
                                        id int NOT NULL, 
                                        email TEXT,
                                        is_private INTEGER,
                                        name TEXT,
                                        password TEXT,
                                        PRIMARY KEY (id) 
                                        )
    
            """)
            for i in range(len(self.clients_data)):
                data_base_cursor.execute(f"""
                REPLACE INTO clients (id, email, is_private, name, password) VALUES ('{self.clients_data[i]["id"]}', 
                '{self.clients_data[i]["email"]}', '{int(self.clients_data[i]["is_private"])}', 
                '{self.clients_data[i]["name"]}',
                '{self.clients_data[i]["password"]}')
            """)
            connection.commit()
            connection.close()
        elif self.export_table_name == "records":
            data_base_cursor.execute("""CREATE TABLE records
                                        (
                                        id int NOT NULL,
                                        accumulated INTEGER,

                                        client_number INTEGER,
                                        client_name TEXT,
                                        last_record_date TEXT,
                                        organization_number INTEGER,
                                        organization_title TEXT,
                                        PRIMARY KEY (id)
                                        )

            """)
            for i in range(len(self.records_data)):
                data_base_cursor.execute(f"""
                REPLACE INTO records (id, accumulated, client_number, client_name, last_record_date, 
                organization_number, organization_title) VALUES ('{self.records_data[i]["id"]}',
                '{self.records_data[i]["accumulated"]}', '{int(self.records_data[i]["client"])}', 
                '{self.records_data[i]["client_name"]}', '{self.records_data[i]["last_record_date"]}', 
                '{self.records_data[i]["organization"]}', '{self.records_data[i]["organization_title"]}')
            """)
            connection.commit()
            connection.close()
        else:
            data_base_cursor.execute("""CREATE TABLE organizations
                                                    (
                                                    id INTEGER NOT NULL,
                                                    email TEXT,
                                                    image TEXT,
                                                    limitation INTEGER,
                                                    password TEXT,
                                                    sticker TEXT,
                                                    title TEXT,
                                                    PRIMARY KEY (id)
                                                    )

                        """)
            for i in range(len(self.organizations_data)):
                data_base_cursor.execute(f"""
                            REPLACE INTO organizations (id, email, image, limitation, password, sticker,
                             title) VALUES ('{self.organizations_data[i]["id"]}',
                            '{self.organizations_data[i]["email"]}', 
                            '{"no" if self.organizations_data[i]["image"] == None
                else BASE_URL_IMAGE + self.organizations_data[i]["image"]}',
                                '{self.organizations_data[i]["limit"]}',
                            '{self.organizations_data[i]["password"]}', '{self.organizations_data[i]["sticker"]}',
                            '{self.organizations_data[i]["title"]}')
                        """)
            connection.commit()
            connection.close()

    # Страница правого меню - смена выбранных ячеек - event
    def right_menu_clients_selection_changed(self):

        selected = self.clients_table.selectedItems()

        if len(selected) == 1:

            self.current_client_id = self.clients_table.item(selected[0].row(), 0).text()
            self.clients_table_current_selection = (selected[0].row(), selected[0].column())

            if selected[0].column() == 0:
                self.right_menu_stack.setCurrentIndex(1)
                self.clients_table_can_edit = False

                self.right_menu_title_page_2.setText("Id:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(False)  # edit button

                self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 1:
                self.right_menu_stack.setCurrentIndex(1)
                self.clients_table_can_edit = True

                self.right_menu_title_page_2.setText("Имя:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(self.has_access)  # edit button
                if self.has_access:
                    self.right_menu_sub_text_page_2.setText(self.has_access_text)
                else:
                    self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 2:
                self.right_menu_stack.setCurrentIndex(1)
                self.clients_table_can_edit = True

                self.right_menu_title_page_2.setText("Email:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(self.has_access)  # edit button
                if self.has_access:
                    self.right_menu_sub_text_page_2.setText(self.has_access_text)
                else:
                    self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 3:
                self.right_menu_stack.setCurrentIndex(1)
                self.clients_table_can_edit = True

                self.right_menu_title_page_2.setText("Пароль:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(self.has_access)  # edit button
                if self.has_access:
                    self.right_menu_sub_text_page_2.setText(self.has_access_text)
                else:
                    self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 4:
                self.right_menu_stack.setCurrentIndex(2)
                self.clients_table_can_edit = True
                self.right_menu_title_page_3.setText("Приватность:")
                if selected[0].text() == "Да":
                    self.check_box_page_3.setChecked(True)
                    self.check_box_page_3.setText("Приватный")
                else:
                    self.check_box_page_3.setChecked(False)
                    self.check_box_page_3.setText("Стандартный")
                self.check_box_page_3.setEnabled(False)
                self.right_menu_main_button_page_3.setEnabled(False)
                self.right_menu_button_page_3.setEnabled(self.has_access)
                if self.has_access:
                    self.right_menu_sub_text_page_3.setText(self.has_access_text)
                else:
                    self.right_menu_sub_text_page_3.setText(self.has_no_access_text)

        elif len(selected) == self.clients_table.columnCount() and len(set([item.row() for item in selected])) == 1:
            self.current_client_id = self.clients_table.item(selected[0].row(), 0).text()

            self.right_menu_stack.setCurrentIndex(3)
            self.clients_table_can_edit = True

            self.right_menu_title_page_4.setText("Удалить:")
            if self.has_access:
                self.right_menu_sub_text_page_4.setText("Удаление не рекомендовано")
            else:
                self.right_menu_sub_text_page_4.setText("Вы не имеете право на удаления")
                self.right_menu_main_button_page_4.setEnabled(False)

        else:
            self.right_menu_stack.setCurrentIndex(0)

    def right_menu_organizations_selection_changed(self):

        selected = self.organizations_table.selectedItems()

        if len(selected) == 1:
            self.current_organization_id = self.organizations_table.item(selected[0].row(), 0).text()
            self.organizations_table_current_selection = (selected[0].row(), selected[0].column())

            if selected[0].column() == 0:
                self.right_menu_stack.setCurrentIndex(1)
                self.organizations_table_can_edit = False

                self.right_menu_title_page_2.setText("Id:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(False)  # edit button

                self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 1:
                self.right_menu_stack.setCurrentIndex(1)
                self.organizations_table_can_edit = True

                self.right_menu_title_page_2.setText("Название:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(self.has_access)  # edit button
                if self.has_access:
                    self.right_menu_sub_text_page_2.setText(self.has_access_text)
                else:
                    self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 2:
                self.right_menu_stack.setCurrentIndex(1)
                self.organizations_table_can_edit = True

                self.right_menu_title_page_2.setText("Email:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(self.has_access)  # edit button
                if self.has_access:
                    self.right_menu_sub_text_page_2.setText(self.has_access_text)
                else:
                    self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 3:
                self.right_menu_stack.setCurrentIndex(1)
                self.organizations_table_can_edit = True

                self.right_menu_title_page_2.setText("Пароль:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(self.has_access)  # edit button
                if self.has_access:
                    self.right_menu_sub_text_page_2.setText(self.has_access_text)
                else:
                    self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 4:
                self.right_menu_stack.setCurrentIndex(1)
                self.organizations_table_can_edit = True

                self.right_menu_title_page_2.setText("Лимит:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(self.has_access)  # edit button
                if self.has_access:
                    self.right_menu_sub_text_page_2.setText(self.has_access_text)
                else:
                    self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 5:
                self.right_menu_stack.setCurrentIndex(1)
                self.organizations_table_can_edit = True

                self.right_menu_title_page_2.setText("Стикер:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(self.has_access)  # edit button
                if self.has_access:
                    self.right_menu_sub_text_page_2.setText(self.has_access_text)
                else:
                    self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            elif selected[0].column() == 6:
                self.right_menu_stack.setCurrentIndex(8)
                self.organizations_table_can_edit = True

        elif len(selected) == self.organizations_table.columnCount() - 1 and len(
                set([item.row() for item in selected])) == 1:
            self.current_organization_id = self.organizations_table.item(selected[0].row(), 0).text()

            self.right_menu_stack.setCurrentIndex(3)
            self.clients_table_can_edit = True

            self.right_menu_title_page_4.setText("Удалить:")
            if self.has_access:
                self.right_menu_sub_text_page_4.setText("Удаление не рекомендовано")
            else:
                self.right_menu_sub_text_page_4.setText("Вы не имеете право на удаления")
                self.right_menu_main_button_page_4.setEnabled(False)
        else:
            self.right_menu_stack.setCurrentIndex(0)

    def right_menu_records_selection_changed(self):

        selected = self.records_table.selectedItems()

        if len(selected) == 1:
            self.current_record_id = self.records_table.item(selected[0].row(), 0).text()
            self.records_table_current_selection = (selected[0].row(), selected[0].column())

            if selected[0].column() == 0:
                self.right_menu_stack.setCurrentIndex(1)
                self.records_table_can_edit = False

                self.right_menu_title_page_2.setText("Id:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(False)  # edit button

                self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            if selected[0].column() == 1:
                self.right_menu_stack.setCurrentIndex(1)
                self.records_table_can_edit = False

                self.right_menu_title_page_2.setText("Организация:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(False)  # edit button

                self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            if selected[0].column() == 2:
                self.right_menu_stack.setCurrentIndex(1)
                self.records_table_can_edit = False

                self.right_menu_title_page_2.setText("Клиент:")
                self.right_menu_input_page_2.setText(selected[0].text())  # input text
                self.right_menu_input_page_2.setEnabled(False)  # input
                self.right_menu_main_button_page_2.setEnabled(False)  # main button
                self.right_menu_button_page_2.setEnabled(False)  # edit button

                self.right_menu_sub_text_page_2.setText(self.has_no_access_text)

            if selected[0].column() == 3:
                self.right_menu_stack.setCurrentIndex(6)
                self.records_table_can_edit = True

                self.right_menu_title_page_7.setText("Накоплено:")
                self.right_menu_input_page_7_1.setText(selected[0].text())  # input text
                self.right_menu_input_page_7_1.setEnabled(False)  # input
                self.right_menu_main_button_page_7.setEnabled(False)  # main button
                self.right_menu_button_page_7.setEnabled(self.has_access)  # edit button

                if self.has_access:
                    self.right_menu_sub_text_page_7.setText("Изменение не рекомендовано")
                else:
                    self.right_menu_sub_text_page_7.setText("Вы не имеете право на изменение")
                    self.right_menu_main_button_page_7.setEnabled(False)
            if selected[0].column() == 4:
                self.right_menu_stack.setCurrentIndex(0)

        elif len(selected) == self.records_table.columnCount() and len(set([item.row() for item in selected])) == 1:
            self.current_record_id = self.records_table.item(selected[0].row(), 0).text()

            self.right_menu_stack.setCurrentIndex(3)
            self.clients_table_can_edit = True

            self.right_menu_title_page_4.setText("Удалить:")
            if self.has_access:
                self.right_menu_sub_text_page_4.setText("Удаление не рекомендовано")
            else:
                self.right_menu_sub_text_page_4.setText("Вы не имеете право на удаления")
                self.right_menu_main_button_page_4.setEnabled(False)
        else:
            self.right_menu_stack.setCurrentIndex(0)

    # Смена вкладки - event
    def tab_changed(self) -> None:

        if self.tabWidget.currentIndex() == 0:
            self.current_table_name = "organizations"
        elif self.tabWidget.currentIndex() == 1:
            self.current_table_name = "clients"
        elif self.tabWidget.currentIndex() == 2:
            self.current_table_name = "records"

        if self.right_menu_stack.currentIndex() == 9:
            if self.tabWidget.currentIndex() == 0:
                self.right_menu_export_clicked("organizations", False)
            elif self.tabWidget.currentIndex() == 1:
                self.right_menu_export_clicked("clients", False)
            elif self.tabWidget.currentIndex() == 2:
                self.right_menu_export_clicked("records", False)
        if self.right_menu_stack.currentIndex() in [12, 11, 10]:
            if self.tabWidget.currentIndex() == 0:
                self.right_menu_add_clicked("organizations", False)
            elif self.tabWidget.currentIndex() == 1:
                self.right_menu_add_clicked("clients", False)
            elif self.tabWidget.currentIndex() == 2:
                self.right_menu_add_clicked("records", False)

        # self.right_menu_stack.setCurrentIndex(0)

    # Запрос на редактирование - кнопка
    def request_editing_clicked(self):
        question = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите запросить право на редактирование?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if question == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                self,
                "Отправлено",
                "Запрос был отправлен",
                QMessageBox.StandardButton.Ok
            )
            app.storage.set_value("edit_request_was_sent", str(True))
            self.editing_button.setEnabled(False)

    # Страница профиля
    def setup_admin_info(self) -> None:

        if not check_server():

            message_box = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if message_box == QMessageBox.StandardButton.Abort:
                exit(-1)

        response = requests.get(
            f"{BASE_URL}/admin/info",
            headers={"x-access-token": app.storage.get_value(key="token")}
        )

        response = response.json()
        self.account_label.setText("Профиль")
        self.email_label.setText("Почта:")
        self.email_field.setText(response["email"])
        self.password_label.setText("Пароль:")
        self.password_field.setText("пароль скрыт")
        self.editing_label.setText("Редактирование:")

        if response["can_edit"]:
            self.editing.setChecked(True)
            self.editing_button.setEnabled(False)

            self.has_access = True
        else:
            self.editing.setChecked(False)
            self.editing.setText("Запрещено")

            if app.storage.key_exists("edit_request_was_sent"):
                self.editing_button.setEnabled(False)

        self.editing_button.setText("Запросить доступ")
        self.logout_button.setText("Выйти")
