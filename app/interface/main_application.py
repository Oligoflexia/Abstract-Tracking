from tkinter import ttk, filedialog
from sqlite3 import Cursor, Connection
import os

from utils import DBConnection
from .window_classes import MainWindow


class MainApplication(MainWindow):
    def __init__(self: "MainApplication") -> None:
        super().__init__()

        self.populate_sidebar()
        self.populate_main_content_area()

    def populate_sidebar(self: "MainApplication") -> None:
        sql_explorer_button = ttk.Button(
            self.sidebar,
            text="SQL Explorer",
            command=self.open_sqlexplorer,
        )
        sql_explorer_button.pack(padx=10, pady=10)

        db_explorer_button = ttk.Button(
            self.sidebar,
            text="DB Explorer",
            command=self.open_dbexplorer,
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
            command=self.open_csventry,
        )
        csv_button.grid(row=1, column=0)

        data_folder_button = ttk.Button(
            self.main_content_area,
            text="Data Files",
            command=self.show_data_folder,
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
        data_folder_dir_path = os.path.join("data", "db")
        abs_data_folder_dir_path = os.path.abspath(data_folder_dir_path)
        self.data_path = abs_data_folder_dir_path

        file_types = [("Database Files", "*.db")]

        filename = filedialog.askopenfilename(
            initialdir=abs_data_folder_dir_path,
            filetypes=file_types
        )
        if filename:
            self.DBConnection = DBConnection(filename)

            db_name = os.path.basename(filename)
            connected_db_text = "Currently connected database: " + db_name
            self.connected_db_text.set(connected_db_text)
            self.turn_banner_green()

    def open_sqlexplorer(self: "MainApplication") -> None:
        from .sql_explorer import SQLExplorer
        self.sqlexplorer = SQLExplorer(self)

    def open_dbexplorer(self: "MainApplication") -> None:
        from .db_explorer import DBExplorer
        self.dbexplorer = DBExplorer(self)

    def open_csventry(self: "MainApplication") -> None:
        from .csv_entry import CSVEntry
        self.csventry = CSVEntry(self)

    def get_cursor(self: "MainApplication") -> Cursor:
        return self.DBConnection.get_connection().cursor()

    def get_conn(self: "MainApplication") -> Connection:
        return self.DBConnection.get_connection()


    # TODO: Default folder for upload
    # TODO: Think about a separate button for viewing and download
    def show_data_folder(self: "MainApplication") -> None:
        file_types = [
            ("New Microsoft Excel", "*.xlsx"),
            ("Old Microsoft Excel", "*.xls"),
            ("Comma Separated Values (CSV)", "*.csv"),
            ]
        file_names = filedialog.askopenfilenames(
            title="Upload data files", filetypes=file_types
        )

        if file_names:
            for file in file_names:
                print(file)
