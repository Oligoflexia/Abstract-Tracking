import tkinter as tk
from tkinter import ttk
from .. import SecondaryWindow


class CSVEntry(SecondaryWindow):
    from .. import MainApplication

    def __init__(self: "CSVEntry", parent: MainApplication) -> None:
        super().__init__(parent)
        self.title("CSV Record Import Tool")
        self.create_window_elements()

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

