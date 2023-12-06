import logging
from logging import LogRecord
from tkinter import messagebox

class LoggingHandler(logging.Handler):
    def emit(self: "LoggingHandler", record: LogRecord) -> None:
        log_entry = self.format(record)
        error_box(log_entry)

def error_box(message: str) -> None:
    messagebox.showerror("Error!", message)

