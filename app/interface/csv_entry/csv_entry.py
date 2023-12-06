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
        self.init_conferences()

    def init_df(self: "CSVEntry") -> DataFrame:
        global CSV_DATA
        filename = ""
        filetypes = [
            ("New Excel", "*.xlsx"),
            ("Old Excel", "*.xls"),
            ("Comma Separated Values (CSV)", "*.csv")
         ]
        filename = filedialog.askopenfilename(
            initialdir=path.abspath(path.join("data", "raw")),
            filetypes=filetypes
         )
        return get_df_csv(filename)

    def create_window_elements(self: "CSVEntry") -> None:
        # root
        step_banner_frame = ttk.Frame(self)
        self.step_banner = step_banner_frame
        step_banner_frame.pack()

        main_content_frame = ttk.Frame(self)
        self.main_content = main_content_frame
        main_content_frame.pack()

        # step_banner
        conference_label = ttk.Label(self.step_banner, text="1. Conferences")
        self.conference = conference_label
        conference_label.grid(row=0, column=0)

        people_label = ttk.Label(self.step_banner, text="2. People")
        self.people = people_label
        people_label.grid(row=0, column=1)

        abstract_label = ttk.Label(self.step_banner, text="3. Abstracts")
        self.abstract = abstract_label
        abstract_label.grid(row=0, column=2)

        submissions_label = ttk.Label(self.step_banner, text="4. Submissions")
        self.submissions = submissions_label
        submissions_label.grid(row=0, column=3)

        presentations_label = ttk.Label(
            self.step_banner, text="5. Presentations"
         )
        self.presentations = presentations_label
        presentations_label.grid(row=0, column=4)

        attendences_label = ttk.Label(self.step_banner, text="6. Attendences")
        self.attendences = attendences_label
        attendences_label.grid(row=0, column=5)

    def init_conferences(self: "CSVEntry") -> None:
        from .conferences_frame import Conferences

        conf_frame = Conferences(self.main_content, self)
        self.frames[Conferences] = conf_frame
        conf_frame.grid(row=0, column=0)
        self.show_frame(conf_frame)

    def show_frame(self, content) -> None:
        frame = self.frames[content]
        frame.tkraise()
