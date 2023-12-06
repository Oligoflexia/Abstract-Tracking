import tkinter as tk
from tkinter import ttk


class People(ttk.Frame):
    from .csv_entry import CSVEntry

    def __init__(
        self: "People", parent: ttk.Frame, controller: CSVEntry
     ) -> None:
        super().__init__()
        self.create_window_elements()
        self.configure_layout()

    def create_window_elements(self: "People") -> None:
        main_content_frame = ttk.Frame(self)
        self.main_content = main_content_frame

        main_content_frame.pack()

    def configure_layout(self: "People") -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class PeopleErrors(ttk.Frame):
    def __init__(
        self: "PeopleErrors", parent: ttk.Frame, controller: People
     ) -> None:
        super().__init__()
        self.create_window_elements()
        self.configure_layout()

    def create_window_elements(self: "PeopleErrors") -> None:
        main_content_frame = ttk.Frame(self)
        self.main_content = main_content_frame

        main_content_frame.pack()

        # top text label
        string = "The following names need formatting before insertion:"
        ttk.Label(self.main_content, text=string).pack()

        # error frame
        error_content_frame = ttk.Frame(self.main_content)
        error_content_frame.pack()

        # table
        column_names = ("Selected", "Full Name")
        name_table = ttk.Treeview(
            error_content_frame, columns=column_names, selectmode="extended"
         )
        self.name_table = name_table
        name_table.grid(row=0, column=0)

        # info + number selection + button
        sub_error_content_frame = ttk.Frame(error_content_frame)
        sub_error_content_frame.grid(row=0, column=1)

        string = "How many words are the selected names?"
        ttk.Label(sub_error_content_frame, text=string).pack()
        ttk.Combobox(sub_error_content_frame, values=["1", "3"]).pack()
        ttk.Button(
            sub_error_content_frame,
            text="Submit",
            command=lambda: print("Working!")
         )

    def configure_layout(self: "PeopleErrors") -> None:
        pass
