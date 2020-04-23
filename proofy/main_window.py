import logging

from PySide2 import QtWidgets
from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import (
    QMainWindow,
    QApplication,
    QAction,
    QFileDialog,
    QDockWidget,
)

from widgets.graph import Graph
from widgets.log_console import LogConsole
from widgets.tools import Tools

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Widgets
        # Logging
        self.log_console = LogConsole()
        self.log_console.add_slots(self.show_log_as_status)
        self.log_console.add_loggers(logger)
        # Graph
        self.graph_widget = Graph(self.log_console)
        # Tools
        self.tools = Tools(slot_draw_graph=self.graph_widget.draw_graph)

        # Layout
        self.setCentralWidget(self.graph_widget)

        console_dock = QDockWidget("Console")
        console_dock.setWidget(self.log_console)
        self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)

        tools_dock = QDockWidget("Tools")
        tools_dock.setWidget(self.tools)
        self.addDockWidget(Qt.RightDockWidgetArea, tools_dock)

        self.setWindowTitle("Proofy")

        # Menu
        # Exit QAction
        exit_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DialogCloseButton), "Exit", self)
        exit_action.triggered.connect(self.exit)
        # Open File
        open_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton), "Open...", self)
        open_action.triggered.connect(self.open)
        # Save File
        save_action = QAction(app.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton), "Save As...", self)
        save_action.triggered.connect(self.save_as)
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
        path = QFileDialog.getOpenFileName(
            self, caption="Open Graph", filter=self.graph_widget.get_open_file_extensions()
        )
        if path:
            try:
                self.graph_widget.open_file(*path)
            except Exception as e:
                logger.error(e)

    @Slot()
    def save_as(self):
        logger.debug(locals())
        path = QFileDialog.getSaveFileName(
            self, caption="Save Graph", filter=self.graph_widget.get_save_file_extensions()
        )
        if path:
            try:
                self.graph_widget.save_file(*path)
            except Exception as e:
                logger.error(e)

    @Slot(str, logging.LogRecord)
    def show_log_as_status(self, status, record):
        levels = {0: "NOTSET", 10: "DEBUG", 20: "INFO", 30: "WARNING", 40: "ERROR", 50: "CRITICAL"}

        self.status.showMessage(f"Welcome to Proofy! Loglevel: {levels[record.levelno]}")
        self.update()
