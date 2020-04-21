import logging

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Slot, QObject, Signal, Qt
from PySide2.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QDockWidget

from graph_widget import GraphWidget

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LogSignaller(QObject):
    log = Signal(str, logging.LogRecord)


class LogHandler(logging.Handler):
    def __init__(self, slot_function, *args, **kwargs):
        super(LogHandler, self).__init__(*args, **kwargs)
        self.log_signaller = LogSignaller()
        self.log_signaller.log.connect(slot_function)

    def emit(self, record):
        self.log_signaller.log.emit(self.format(record), record)


class MainWindow(QMainWindow):
    COLORS = {
        logging.DEBUG: "black",
        logging.INFO: "blue",
        logging.WARNING: "orange",
        logging.ERROR: "red",
        logging.CRITICAL: "purple",
    }

    def __init__(self, app):
        super().__init__()
        self.app = app

        # LOGGING
        self.log_console = self.get_console()
        self.log_handler = LogHandler(self.log_message)
        self.log_handler.setFormatter(
            logging.Formatter(
                "[%(levelname)s][%(name)s][%(asctime)s][%(relativeCreated)07dms][%(processName)s:%(threadName)s][%(pathname)s:%(lineno)s][%(funcName)s]\n%(message)s"
            )
        )
        self.log_handler.setLevel(logging.DEBUG)
        self.console_dock = QDockWidget("Console")
        self.console_dock.setWidget(self.log_console)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_dock)
        logger.addHandler(self.log_handler)

        # Widget
        self.widget = GraphWidget(self.log_handler)
        self.setCentralWidget(self.widget)

        # Exit QAction
        exit_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DialogCloseButton), "Exit", self)
        exit_action.triggered.connect(self.exit)
        # Open File
        open_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton), "Open...", self)
        open_action.triggered.connect(self.open)
        # Save File
        save_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton), "Save As...", self)
        save_action.triggered.connect(self.save_as)

        self.setWindowTitle("Proofy")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.file_menu.addAction(open_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(exit_action)

        self.status = self.statusBar()
        self.status.showMessage("Welcome to Proofy!")

    def get_console(self):
        log_console = QtWidgets.QPlainTextEdit(self)
        font = QtGui.QFont("Consolas")
        font.setStyleHint(font.Monospace)
        log_console.setFont(font)
        log_console.setReadOnly(True)
        return log_console

    @Slot(str, logging.LogRecord)
    def log_message(self, status, record):
        color = self.COLORS.get(record.levelno, "black")
        s = f'<pre><font color="{color}">{status}</font></pre>'
        self.log_console.appendHtml(s)
        self.status.showMessage(f"{status}")
        self.update()

    @Slot()
    def open(self):
        path = QFileDialog.getOpenFileName(self, caption="Open Graph", filter=self.widget.get_file_types())
        if path:
            try:
                self.widget.open_file(*path)
            except Exception as e:
                logger.error(e)

    @Slot()
    def save_as(self):
        path = QFileDialog.getSaveFileName(self, caption="Save Graph", filter=self.widget.get_file_types())
        if path:
            try:
                self.widget.save_file(*path)
            except Exception as e:
                logger.error(e)

    @Slot()
    def exit(self):
        QApplication.quit()
