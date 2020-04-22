import logging

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Slot, QObject, Signal, Qt
from PySide2.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QDockWidget

from graph_widget import GraphWidget

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LogHandlerSignals(QObject):
    log = Signal(str, logging.LogRecord)


class LogHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super(LogHandler, self).__init__(*args, **kwargs)
        self.signals = LogHandlerSignals()

    def add_slots(self, *slots):
        for slot in slots:
            self.signals.log.connect(slot)

    def emit(self, record):
        self.signals.log.emit(self.format(record), record)


class LogConsole(QtWidgets.QTextEdit):
    COLORS = {
        logging.DEBUG: "black",
        logging.INFO: "blue",
        logging.WARNING: "orange",
        logging.ERROR: "red",
        logging.CRITICAL: "purple",
    }

    def __init__(self, *args, **kwargs):
        super(LogConsole, self).__init__(*args, **kwargs)
        font = QtGui.QFont("Consolas")
        font.setStyleHint(font.Monospace)
        self.setFont(font)
        self.setReadOnly(True)
        self.handler = LogHandler()
        self.handler.add_slots(self.emit)
        self.handler.setFormatter(
            logging.Formatter(
                '<table align="left" cellspacing="7">'
                '<tr>'
                '<th align="left">levelname</th>'
                '<th align="left">message</th>'
                '<th align="left">funcName</th>'
                '<th align="left">name</th>'
                '<th align="left">threadName</th>'
                '<th align="left">processName</th>'
                '<th align="left">pathname</th>'
                '<th align="left">lineno</th>'
                '<th align="left">asctime</th>'
                '<th align="left">relativeCreated</th>'
                '</tr>'
                '<tr>'
                '<td align="left">%(levelname)s</td>'
                '<td align="left">%(message)s</td>'
                '<td align="left">%(funcName)s</td>'
                '<td align="left">%(name)s</td>'
                '<td align="left">%(threadName)s</td>'
                '<td align="left">%(processName)s</td>'
                '<td align="left">%(pathname)s</td>'
                '<td align="left">%(lineno)s</td>'
                '<td align="left">%(asctime)s</td>'
                '<td align="left">%(relativeCreated)07dms</td>'
                '</tr>'
                '</table>'
            )
        )
        self.handler.setLevel(logging.DEBUG)

    def add_slots(self, *slots):
        self.handler.add_slots(*slots)

    def add_loggers(self, *loggers):
        for log in loggers:
            log.addHandler(self.handler)

    @Slot(str, logging.LogRecord)
    def emit(self, status, record):
        color = self.COLORS.get(record.levelno, "black")
        s = f'<font color="{color}">{status}</font>'
        self.insertHtml(s)
        self.ensureCursorVisible()


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # LOGGING
        self.log_console = LogConsole()
        self.log_console.add_slots(self.show_log_as_status)
        self.log_console.add_loggers(logger)

        self.console_dock = QDockWidget("Console")
        self.console_dock.setWidget(self.log_console)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_dock)

        # Widget
        self.widget = GraphWidget(self.log_console)
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

    @Slot()
    def exit(self):
        logger.debug(locals())
        QApplication.quit()

    @Slot()
    def open(self):
        logger.debug(locals())
        path = QFileDialog.getOpenFileName(self, caption="Open Graph", filter=self.widget.get_file_types())
        if path:
            try:
                self.widget.open_file(*path)
            except Exception as e:
                logger.error(e)

    @Slot()
    def save_as(self):
        logger.debug(locals())
        path = QFileDialog.getSaveFileName(self, caption="Save Graph", filter=self.widget.get_file_types())
        if path:
            try:
                self.widget.save_file(*path)
            except Exception as e:
                logger.error(e)

    @Slot(str, logging.LogRecord)
    def show_log_as_status(self, status, record):
        levels = {0: "NOTSET", 10: "DEBUG", 20: "INFO", 30: "WARNING", 40: "ERROR", 50: "CRITICAL"}

        self.status.showMessage(f"Welcome to Proofy! Loglevel: {levels[record.levelno]}")
        self.update()
