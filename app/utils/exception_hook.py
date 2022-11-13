import sys
import traceback
from PyQt6 import QtWidgets


def exception_hook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QtWidgets.QApplication.quit()


sys.excepthook = exception_hook
