import tkinter as tk
from tkinter import ttk, filedialog
from os import path
from pandas import DataFrame

from .. import SecondaryWindow
from utils import get_df_csv


class CSVEntry(SecondaryWindow):
    from .. import MainApplication

    def __init__(self: "CSVEntry", parent: MainApplication) -> None:
        self.df = self.init_df()
        super().__init__(parent)
        self.parent = parent
        self.frames = {}
        self.conn = self.parent.get_conn()
        self.cursor = self.parent.get_cursor()
        self.title("CSV Record Import Tool")
        self.create_window_elements()
        self.configure_layout()
        self.init_conferences()

    def init_df(self: "CSVEntry") -> DataFrame:
        global CSV_DATA
        filename = ""
        filetypes = [("Spreadsheet Files", ".xlsx .xls .csv")]
        filename = filedialog.askopenfilename(
            initialdir=path.abspath(path.join("data", "raw")),
            filetypes=filetypes
         )
        return get_df_csv(filename)

    def create_window_elements(self: "CSVEntry") -> None:
        # root
        step_banner_frame = ttk.Frame(self)
        self.step_banner = step_banner_frame
        step_banner_frame.grid(row=0, column=0, sticky="ew")

        main_content_frame = ttk.Frame(self)
        self.main_content = main_content_frame
        main_content_frame.grid(row=1, column=0, sticky="nsew")

        # step_banner
        conference_label = ttk.Label(self.step_banner, text="1. Conferences")
        self.conference = conference_label
        conference_label.grid(row=0, column=0, padx=5, sticky="e")

        people_label = ttk.Label(self.step_banner, text="2. People")
        self.people = people_label
        people_label.grid(row=0, column=1, padx=5)

        abstract_label = ttk.Label(self.step_banner, text="3. Abstracts")
        self.abstract = abstract_label
        abstract_label.grid(row=0, column=2, padx=5)

        submissions_label = ttk.Label(self.step_banner, text="4. Submissions")
        self.submissions = submissions_label
        submissions_label.grid(row=0, column=3, padx=5)

        presentations_label = ttk.Label(
            self.step_banner, text="5. Presentations"
         )
        self.presentations = presentations_label
        presentations_label.grid(row=0, column=4, padx=5)

        attendences_label = ttk.Label(self.step_banner, text="6. Attendences")
        self.attendences = attendences_label
        attendences_label.grid(row=0, column=5, padx=5, sticky="w")

    def configure_layout(self) -> None:
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.step_banner.columnconfigure(0, weight=1)
        self.step_banner.columnconfigure(1, weight=1)
        self.step_banner.columnconfigure(2, weight=1)
        self.step_banner.columnconfigure(3, weight=1)
        self.step_banner.columnconfigure(4, weight=1)
        self.step_banner.columnconfigure(5, weight=1)

        self.main_content.rowconfigure(0, weight=1)
        self.main_content.columnconfigure(0, weight=1)

    def init_conferences(self: "CSVEntry") -> None:
        from .conferences_frame import Conferences

        conf_frame = Conferences(self.main_content, self)
        self.frames["Conferences"] = conf_frame
        conf_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Conferences")

    def show_frame(self, content) -> None:
        frame = self.frames[content]
        frame.tkraise()
