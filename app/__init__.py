from loguru import logger
from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget
from config import LOG_NAME, LOG_ROTATION
from app.database.Storage import Storage
from app.screens.LoadingScreen import LoadingScreen
from app.screens.LoginScreen import LoginScreen

# Создание базы данных
storage = Storage()

# Инициализация приложения
app = QApplication([])
window = QStackedWidget()
window.setWindowTitle("Admin панель")
window.setMinimumSize(600, 400)
window.setGeometry(100, 100, 1200, 800)
window.addWidget(LoadingScreen())
window.show()

# Добавление файла сохранения log-ов
logger.add(
    sink=LOG_NAME,
    level="DEBUG",
    rotation=LOG_ROTATION,
    compression="zip",
)
