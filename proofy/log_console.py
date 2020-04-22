import logging

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import Slot

from log_handler import LogHandler


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
                "<tr>"
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
                "</tr>"
                "<tr>"
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
                "</tr>"
                "</table>"
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
