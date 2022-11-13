import requests
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QPropertyAnimation
from PyQt6 import QtCore, QtGui, QtWidgets
from config import BASE_URL
import app
from app import logger
from app.utils.check_server import check_server


class MainScreen(QMainWindow):

    def __init__(self):
        super().__init__()

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
        self.central_widget.setObjectName("centralwidget")

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
        self.verticalLayout_2_2 = QtWidgets.QVBoxLayout(self.left_menu_container)
        self.verticalLayout_2_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2_2.setObjectName("verticalLayout_2")

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

        self.verticalLayout_2_2.addWidget(self.left_menu)

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
        self.verticalLayout__2 = QtWidgets.QVBoxLayout(self.main_body)
        self.verticalLayout__2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout__2.setSpacing(0)
        self.verticalLayout__2.setObjectName("verticalLayout")

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

        self.verticalLayout__2.addWidget(self.header)

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
        self.page_1_2 = QtWidgets.QWidget()
        self.page_1_2.setObjectName("page_1")

        # HorizontalLayout 4
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.page_1_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        spacer_item4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                             QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacer_item4)

        # Forme layout
        self.forme_layout = QtWidgets.QFrame(self.page_1_2)
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
        self.password_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
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
        self.editing_layout.setObjectName("editing_layoit")

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

        self.body_stack.addWidget(self.page_1_2)

        # Page 2
        self.page_2_2 = QtWidgets.QWidget()
        self.page_2_2.setObjectName("page_2")

        # HorizontalLayout 6
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.page_2_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        # Tab widget
        self.tabWidget = QtWidgets.QTabWidget(self.page_2_2)
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
        self.sort_button = QtWidgets.QPushButton(self.organizations_layout)
        self.sort_button.setMinimumHeight(self.search_line_edit.height() - 7)
        self.sort_button.setMinimumWidth(80)
        self.sort_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sort_button.setStyleSheet("""
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
        self.sort_button.setObjectName("sort_button")

        self.horizontalLayout_5.addWidget(self.sort_button)

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
        self.sort_button_clients = QtWidgets.QPushButton(self.clients_layout)
        self.sort_button_clients.setMinimumHeight(self.search_line_edit_clients.height() - 7)
        self.sort_button_clients.setMinimumWidth(80)
        self.sort_button_clients.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sort_button_clients.setStyleSheet("""
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
        self.sort_button_clients.setObjectName("sort_button_clients")

        self.top_panel_clients.addWidget(self.sort_button_clients)

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
        self.sort_button_records = QtWidgets.QPushButton(self.records_layout)
        self.sort_button_records.setMinimumHeight(self.search_line_edit_records.height() - 7)
        self.sort_button_records.setMinimumWidth(80)
        self.sort_button_records.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sort_button_records.setStyleSheet("""
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
        self.sort_button_records.setObjectName("sort_button_records")

        self.top_panel_records.addWidget(self.sort_button_records)

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
        self.tableWidget = QtWidgets.QTableWidget(self.records_layout)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.verticalLayout_7.addWidget(self.tableWidget)

        self.tabWidget.addTab(self.records_layout, "")

        self.horizontalLayout_6.addWidget(self.tabWidget)

        self.body_stack.addWidget(self.page_2_2)

        # Page 1
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")

        self.body_stack.addWidget(self.page_3)

        self.horizontalLayout_3.addWidget(self.body_stack)

        self.verticalLayout__2.addWidget(self.body)

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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.right_menu_not_working_label.sizePolicy().hasHeightForWidth())
        self.right_menu_not_working_label.setSizePolicy(sizePolicy)
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
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_2.addItem(spacerItem)
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
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_2.addItem(spacerItem1)
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
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_3.addItem(spacerItem2)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check_box_page_3.sizePolicy().hasHeightForWidth())
        self.check_box_page_3.setSizePolicy(sizePolicy)
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
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_3.addItem(spacerItem3)
        self.right_menu_main_button_page_3 = QtWidgets.QPushButton(self.page_3_right_menu)
        self.right_menu_main_button_page_3.setObjectName("right_menu_main_button_page_3")
        self.right_menu_vertical_layout_page_3.addWidget(self.right_menu_main_button_page_3)
        self.right_menu_stack.addWidget(self.page_3_right_menu)
        self.page_4_right_menu = QtWidgets.QWidget()
        self.page_4_right_menu.setObjectName("page_4_right_menu")
        self.right_menu_vertical_layout_page_4 = QtWidgets.QVBoxLayout(self.page_4_right_menu)
        self.right_menu_vertical_layout_page_4.setSpacing(9)
        self.right_menu_vertical_layout_page_4.setObjectName("right_menu_vertical_layout_page_4")
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_4.addItem(spacerItem4)
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
        self.change_data_button_page_4 = QtWidgets.QPushButton(self.page_4_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.change_data_button_page_4.setFont(font)
        self.change_data_button_page_4.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.change_data_button_page_4.setObjectName("change_data_button_page_4")
        self.complex_layout_page_4.addWidget(self.change_data_button_page_4)
        self.right_menu_vertical_layout_page_4.addLayout(self.complex_layout_page_4)
        self.right_menu_sub_text_page_4 = QtWidgets.QLabel(self.page_4_right_menu)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_sub_text_page_4.setFont(font)
        self.right_menu_sub_text_page_4.setObjectName("right_menu_sub_text_page_4")
        self.right_menu_vertical_layout_page_4.addWidget(self.right_menu_sub_text_page_4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 462, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_4.addItem(spacerItem5)
        self.right_menu_stack.addWidget(self.page_4_right_menu)
        self.page_5_right_menu = QtWidgets.QWidget()
        self.page_5_right_menu.setObjectName("page_5_right_menu")
        self.right_menu_vertical_layout_page_5 = QtWidgets.QVBoxLayout(self.page_5_right_menu)
        self.right_menu_vertical_layout_page_5.setObjectName("right_menu_vertical_layout_page_5")
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_5.addItem(spacerItem6)
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
        spacerItem7 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_5.addItem(spacerItem7)
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
        spacerItem8 = QtWidgets.QSpacerItem(20, 432, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_5.addItem(spacerItem8)
        self.right_menu_stack.addWidget(self.page_5_right_menu)
        self.page_6_right_menu = QtWidgets.QWidget()
        self.page_6_right_menu.setObjectName("page_6_right_menu")
        self.right_menu_vertical_layout_page_6 = QtWidgets.QVBoxLayout(self.page_6_right_menu)
        self.right_menu_vertical_layout_page_6.setObjectName("right_menu_vertical_layout_page_6")
        spacerItem9 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_6.addItem(spacerItem9)
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
        spacerItem10 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_6.addItem(spacerItem10)
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
        spacerItem11 = QtWidgets.QSpacerItem(20, 429, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_6.addItem(spacerItem11)
        self.right_menu_stack.addWidget(self.page_6_right_menu)
        self.page_7_right_menu = QtWidgets.QWidget()
        self.page_7_right_menu.setObjectName("page_7_right_menu")
        self.right_menu_vertical_layout_page_7 = QtWidgets.QVBoxLayout(self.page_7_right_menu)
        self.right_menu_vertical_layout_page_7.setSpacing(10)
        self.right_menu_vertical_layout_page_7.setObjectName("right_menu_vertical_layout_page_7")
        spacerItem12 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_7.addItem(spacerItem12)
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
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_text_mid_page_7.setFont(font)
        self.right_menu_text_mid_page_7.setObjectName("right_menu_text_mid_page_7")
        self.complex_layout_page_7.addWidget(self.right_menu_text_mid_page_7)
        self.right_menu_input_page_7_2 = QtWidgets.QLineEdit(self.page_7_right_menu)
        self.right_menu_input_page_7_2.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_input_page_7_2.setFont(font)
        self.right_menu_input_page_7_2.setObjectName("right_menu_input_page_7_2")
        self.complex_layout_page_7.addWidget(self.right_menu_input_page_7_2)
        self.right_menu_button_page_7 = QtWidgets.QPushButton(self.page_7_right_menu)  ####
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.right_menu_button_page_7.setFont(font)
        self.right_menu_button_page_7.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.right_menu_button_page_7.setObjectName("right_menu_button_page_7")
        self.complex_layout_page_7.addWidget(self.right_menu_button_page_7)
        self.right_menu_vertical_layout_page_7.addLayout(self.complex_layout_page_7)
        self.right_menu_progress_bar_page_7 = QtWidgets.QProgressBar(self.page_7_right_menu)
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
        spacerItem13 = QtWidgets.QSpacerItem(20, 396, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_7.addItem(spacerItem13)
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
        self.right_menu_vertical_layout_page_8.setObjectName("right_menu_vertical_layout_page_8")
        spacerItem14 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_8.addItem(spacerItem14)
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
        spacerItem15 = QtWidgets.QSpacerItem(20, 218, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_8.addItem(spacerItem15)
        self.right_menu_main_button_page_8 = QtWidgets.QPushButton(self.page_8_right_menu)
        self.right_menu_main_button_page_8.setObjectName("right_menu_main_button_page_8")
        self.right_menu_vertical_layout_page_8.addWidget(self.right_menu_main_button_page_8)
        self.right_menu_stack.addWidget(self.page_8_right_menu)
        self.page_9_right_menu = QtWidgets.QWidget()
        self.page_9_right_menu.setObjectName("page_9_right_menu")
        self.right_menu_vertical_layout_page_9 = QtWidgets.QVBoxLayout(self.page_9_right_menu)
        self.right_menu_vertical_layout_page_9.setObjectName("right_menu_vertical_layout_page_9")
        spacerItem16 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_9.addItem(spacerItem16)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
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
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_9.addItem(spacerItem17)
        self.right_menu_stack.addWidget(self.page_9_right_menu)
        self.page_10_right_menu = QtWidgets.QWidget()
        self.page_10_right_menu.setObjectName("page_10_right_menu")
        self.right_menu_vertical_layout_page_10 = QtWidgets.QVBoxLayout(self.page_10_right_menu)
        self.right_menu_vertical_layout_page_10.setObjectName("right_menu_vertical_layout_page_10")
        spacerItem18 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_10.addItem(spacerItem18)
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
        spacerItem19 = QtWidgets.QSpacerItem(20, 494, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_10.addItem(spacerItem19)
        self.right_menu_stack.addWidget(self.page_10_right_menu)
        self.page_11_right_menu = QtWidgets.QWidget()
        self.page_11_right_menu.setObjectName("page_11_right_menu")
        self.right_menu_vertical_layout_page_11 = QtWidgets.QVBoxLayout(self.page_11_right_menu)
        self.right_menu_vertical_layout_page_11.setObjectName("right_menu_vertical_layout_page_11")
        spacerItem20 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_11.addItem(spacerItem20)
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
        spacerItem21 = QtWidgets.QSpacerItem(20, 418, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_11.addItem(spacerItem21)
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
        self.right_menu_vertical_layout_page_12.setObjectName("right_menu_vertical_layout_page_12")
        spacerItem22 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_12.addItem(spacerItem22)
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
        spacerItem23 = QtWidgets.QSpacerItem(20, 418, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_12.addItem(spacerItem23)
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
        self.right_menu_vertical_layout_page_13.setObjectName("right_menu_vertical_layout_page_13")
        spacerItem24 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Fixed)
        self.right_menu_vertical_layout_page_13.addItem(spacerItem24)
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
        spacerItem25 = QtWidgets.QSpacerItem(20, 444, QtWidgets.QSizePolicy.Policy.Minimum,
                                             QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_menu_vertical_layout_page_13.addItem(spacerItem25)
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

        QtCore.QMetaObject.connectSlotsByName(self)

        self.setup_ui()
        self.setup_stacks_and_tabs()
        self.setup_text()
        self.update_ui()

    def setup_text(self):
        self.left_menu_title.setText("Страницы:")
        self.page_1_button.setText("Главная")
        self.page_2_button.setText("Аккаунт")
        self.page_3_button.setText("Логи")
        self.exit_button.setText("Выйти")
        self.page_title.setText("Название")
        self.search_line_edit.setPlaceholderText("Поиск")
        self.search_button.setText("Поиск")
        self.sort_button.setText("Сортировка")
        self.save_button.setText("Экспорт")
        self.refresh_button.setText("Обновить")
        self.search_line_edit_clients.setPlaceholderText("Поиск")
        self.search_button_clients.setText("Поиск")
        self.sort_button_clients.setText("Сортировка")
        self.save_button_clients.setText("Экспорт")
        self.refresh_button_clients.setText("Обновить")
        self.search_line_edit_records.setPlaceholderText("Поиск")
        self.search_button_records.setText("Поиск")
        self.sort_button_records.setText("Сортировка")
        self.save_button_records.setText("Экспорт")
        self.refresh_button_records.setText("Обновить")
        self.account_label.setText("Профиль")
        self.email_label.setText("Почта:")
        self.email_field.setText("RuslanBosin28Gmail.com")
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

    def setup_stacks_and_tabs(self):
        self.body_stack.setCurrentIndex(1)
        self.right_menu_stack.setCurrentIndex(3)
        self.tabWidget.setCurrentIndex(0)

    def setup_ui(self):

        self.page_1_button.setCheckable(True)
        self.page_1_button.setChecked(True)
        self.page_1_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.page_1_button.setIcon(QtGui.QIcon("app/static/icons/database.svg"))
        self.page_1_button.clicked.connect(self.page_1_button_clicked)

        self.page_2_button.setCheckable(True)
        self.page_2_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.page_2_button.setIcon(QtGui.QIcon("app/static/icons/user.svg"))
        self.page_2_button.clicked.connect(self.page_2_button_clicked)

        self.page_3_button.setCheckable(True)
        self.page_3_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.page_3_button.setIcon(QtGui.QIcon("app/static/icons/logs.svg"))
        self.page_3_button.clicked.connect(self.page_3_button_clicked)

        self.exit_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.exit_button.setIcon(QtGui.QIcon("app/static/icons/logout.svg"))
        self.exit_button.setIconSize(QtCore.QSize(12, 12))
        self.exit_button.clicked.connect(self.exit_button_clicked)

        def search_button_when_text_changed():
            if self.search_line_edit.text() == "":
                self.search_button.setEnabled(False)
            else:
                self.search_button.setEnabled(True)

        self.search_button.setEnabled(False)
        self.search_line_edit.textChanged.connect(search_button_when_text_changed)

        def search_button_clients_when_text_changed():
            if self.search_line_edit_clients.text() == "":
                self.search_button_clients.setEnabled(False)
            else:
                self.search_button_clients.setEnabled(True)

        self.search_button_clients.setEnabled(False)
        self.search_line_edit_clients.textChanged.connect(search_button_clients_when_text_changed)

        def search_button_records_when_text_changed():
            if self.search_line_edit_records.text() == "":
                self.search_button_records.setEnabled(False)
            else:
                self.search_button_records.setEnabled(True)

        self.search_button_records.setEnabled(False)
        self.search_line_edit_records.textChanged.connect(search_button_records_when_text_changed)

        self.open_left_menu_button.clicked.connect(self.slide_left_menu)
        self.open_right_menu_button.clicked.connect(self.slide_right_menu)

    def update_ui(self):

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

        self.refresh_button_clients.clicked.connect(self.refresh_clients)

    def slide_left_menu(self):
        width = self.left_menu_container.width()

        if width == 0:
            new_width = 250
            self.open_left_menu_button.setIcon(QtGui.QIcon("app/static/icons/left_arrow.svg"))
        else:
            new_width = 0
            self.open_left_menu_button.setIcon(QtGui.QIcon("app/static/icons/menu.svg"))

        self.animation = QPropertyAnimation(self.left_menu_container, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()

    def slide_right_menu(self):
        width = self.right_menu_container.width()

        if width == 0:
            new_width = 600
            self.open_right_menu_button.setIcon(QtGui.QIcon("app/static/icons/right_arrow.svg"))
        else:
            new_width = 0
            self.open_right_menu_button.setIcon(QtGui.QIcon("app/static/icons/menu.svg"))

        self.animation = QPropertyAnimation(self.right_menu_container, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation.start()

    def page_1_button_clicked(self):
        self.page_title.setText("Главная")
        if self.page_1_button.isChecked():
            self.body_stack.setCurrentIndex(1)
            self.page_2_button.setChecked(False)
            self.page_3_button.setChecked(False)
        else:
            self.page_1_button.setChecked(True)

    def page_2_button_clicked(self):
        self.page_title.setText("Аккаунт")
        if self.page_2_button.isChecked():
            self.body_stack.setCurrentIndex(0)
            self.page_1_button.setChecked(False)
            self.page_3_button.setChecked(False)
        else:
            self.page_2_button.setChecked(True)

    def page_3_button_clicked(self):
        self.page_title.setText("Логи")
        if self.page_3_button.isChecked():
            self.body_stack.setCurrentIndex(2)
            self.page_1_button.setChecked(False)
            self.page_2_button.setChecked(False)
        else:
            self.page_3_button.setChecked(True)

    def exit_button_clicked(self):
        print("exit")

    def refresh_clients(self):
        self.clients_table.setSortingEnabled(True)
        self.clients_table.setColumnCount(5)
        self.clients_table.setHorizontalHeaderLabels([
            "id",
            "имя",
            "email",
            "пароль",
            "приватный"
        ])

        if not check_server():

            messageBox = QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось подключиться к серверу",
                QMessageBox.StandardButton.Abort
            )

            if messageBox == QMessageBox.StandardButton.Abort:
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
            data = response.json()
            self.clients_table.setRowCount(len(data))
            k = 0

            for client in data:
                id = QTableWidgetItem(str(client["id"]))
                name = QTableWidgetItem(client["name"])
                email = QTableWidgetItem(client["email"])
                password = QTableWidgetItem(client["password"])
                is_private = QTableWidgetItem("Да" if client["is_private"] else "Нет")

                self.clients_table.setItem(k, 0, id)

                '''
                brn = QtWidgets.QPushButton("Hey")
                brn.setStyleSheet("""
                    .QPushButton {
                        background-color: red;
                    }
                    .QPushButton:pressed {
                        background-color: blue;
                    }
                """)
                self.clients_table.setCellWidget(k, 0, brn)
                '''

                self.clients_table.setItem(k, 1, name)
                self.clients_table.setItem(k, 2, email)
                self.clients_table.setItem(k, 3, password)
                self.clients_table.setItem(k, 4, is_private)

                k += 1

        column_width = self.clients_table.width() // 5 - 3
        for i in range(5):
            self.clients_table.setColumnWidth(i, column_width)
