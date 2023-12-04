import sqlite3
import os

# Consider implementing context management
# (__enter__ and __exit__ methods) to use the DBConnection class with
# Python's with statement. This ensures that the connection is properly
# closed even if an error occurs.
# use logging module


class DBConnection:
    def __init__(self: "DBConnection", db_path: str) -> None:
        if not os.path.exists(db_path):
            raise FileNotFoundError("Database does not exist")
        self.db_path = db_path
        self.connection = None

    def get_connection(self: "DBConnection") -> sqlite3.Connection:
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def close_connection(self: "DBConnection") -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None
