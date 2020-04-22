import logging

from widgets.log_signals import LogSignals


class LogHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super(LogHandler, self).__init__(*args, **kwargs)
        self.signals = LogSignals()

    def add_slots(self, *slots):
        for slot in slots:
            self.signals.log.connect(slot)

    def emit(self, record):
        self.signals.log.emit(self.format(record), record)
