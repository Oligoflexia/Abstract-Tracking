from tkinter import ttk, filedialog
from typing import Union
from sqlite3 import Connection
import os

from utils import DBConnection
from .window_classes import MainWindow
from .SQL_explorer import SQLExplorer


# Global variables
# DBConnection object
DBCONNECTION: Union[DBConnection, None] = None


class MainApplication(MainWindow):
    def __init__(self: "MainApplication") -> None:
        super().__init__()
        self.DBConnection = None

        self.populate_sidebar()
        self.populate_main_content_area()

    def populate_sidebar(self: "MainApplication") -> None:
        sql_explorer_button = ttk.Button(
            self.sidebar,
            text="SQL Explorer",
            command=lambda: print("SQLExplorer"),
        )
        sql_explorer_button.pack(padx=10, pady=10)

        db_explorer_button = ttk.Button(
            self.sidebar,
            text="DB Explorer",
            command=lambda: print("DB Explorer"),
        )
        db_explorer_button.pack(padx=10, pady=10, fill="x")

    def populate_main_content_area(self: "MainApplication") -> None:
        connect_db_button = ttk.Button(
            self.main_content_area,
            text="Connect",
            command=self.connect_db,
        )
        connect_db_button.grid(row=0, column=0)

        csv_button = ttk.Button(
            self.main_content_area,
            text="CSV Import",
            command=lambda: print("CSV Import"),
        )
        csv_button.grid(row=1, column=0)

        data_folder_button = ttk.Button(
            self.main_content_area,
            text="Data Files",
            command=lambda: print("Data Files")
        )
        data_folder_button.grid(row=1, column=1)

        docs_button = ttk.Button(
            self.main_content_area,
            text="Documentation",
            command=lambda: print("Documentation")
        )
        docs_button.grid(row=2, column=0)

        settings_button = ttk.Button(
            self.main_content_area,
            text="Settings",
            command=lambda: print("Settings")
        )
        settings_button.grid(row=2, column=1)

    def connect_db(self: "MainApplication") -> None:
        global DBCONNECTION
        data_folder_dir_path = os.path.join("data", "db")
        abs_data_folder_dir_path = os.path.abspath(data_folder_dir_path)

        file_types = [("Database Files", "*.db")]

        filename = filedialog.askopenfilename(
            initialdir=abs_data_folder_dir_path,
            filetypes=file_types
        )
        if filename:
            self.DBConnection = DBConnection(filename)
            DBCONNECTION = self.DBConnection

            db_name = os.path.basename(filename)
            connected_db_text = "Currently connected database: " + db_name
            self.connected_db_text.set(connected_db_text)
            self.turn_banner_green()

    def open_SQLExplorer(self: "MainApplication") -> None:
        SQLexplorer = SQLExplorer(self)

    def get_connection(self: "MainApplication") -> Connection:
        if self.DBConnection:
            return self.DBConnection.get_connection()
