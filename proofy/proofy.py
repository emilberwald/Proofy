import sys

from PySide2 import QtWebEngine
from PySide2.QtWidgets import QApplication

from main_window import MainWindow

if __name__ == "__main__":
    QtWebEngine.QtWebEngine.initialize()

    app = QApplication(sys.argv)

    window = MainWindow(app)
    window.show()

    sys.exit(app.exec_())
