import logging

from PySide2.QtCore import QObject, Signal


class LogHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super(LogHandler, self).__init__(*args, **kwargs)
        self.signals = LogHandlerSignals()

    def add_slots(self, *slots):
        for slot in slots:
            self.signals.log.connect(slot)

    def emit(self, record):
        self.signals.log.emit(self.format(record), record)


class LogHandlerSignals(QObject):
    log = Signal(str, logging.LogRecord)
