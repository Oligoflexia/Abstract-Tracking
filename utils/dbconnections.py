import sqlite3

# Consider implementing context management
# (__enter__ and __exit__ methods) to use the DBConnection class with
# Python's with statement. This ensures that the connection is properly
# closed even if an error occurs.

class DBConnection:
    def __init__(self, db_name):
        self.db_path = "data/db/" + db_name
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None



