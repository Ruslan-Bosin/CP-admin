from loguru import logger
from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget
from config import LOG_NAME, LOG_ROTATION
from app.screens.LoadingScreen import LoadingScreen
from app.screens.LoginScreen import LoginScreen
from app.database.Storage import Storage

# Создание базы данных
storage = Storage()
storage.set_value("token", "-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4iLCJpZCI6MSwiZXhwIjoxNjY4MTU0ODI1fQ.HZogV0uF1M7rWUaT5E1NuGShmVPLfciG-EK6GKhmDZI")

# Инициализация приложения
app = QApplication([])
window = QStackedWidget()
window.setWindowTitle("Admin панель")
window.setMinimumSize(300, 150)
window.addWidget(LoadingScreen())
window.show()

# Добавление файла сохранения log-ов
logger.add(
    sink=LOG_NAME,
    level="DEBUG",
    rotation=LOG_ROTATION,
    compression="zip",
)
