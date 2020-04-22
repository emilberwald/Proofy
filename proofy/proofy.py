import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QThread

from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow(app)
    window.show()

    sys.exit(app.exec_())
