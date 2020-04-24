import logging

from PySide2.QtCore import QObject, Signal


class LogSignals(QObject):
    log = Signal(str, logging.LogRecord)
