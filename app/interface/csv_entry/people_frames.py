import tkinter as tk
from tkinter import ttk
import pandas as pd


class People(ttk.Frame):
    from .csv_entry import CSVEntry

    def __init__(
        self: "People", parent: ttk.Frame, controller: CSVEntry
     ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.create_window_elements()
        self.configure_layout()
        self.init_people_errors()

    def create_window_elements(self: "People") -> None:
        main_content_frame = ttk.Frame(self)
        self.main_content = main_content_frame

        main_content_frame.grid(row=0, sticky="nsew")

    def configure_layout(self: "People") -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.main_content.rowconfigure(0, weight=1)
        self.main_content.columnconfigure(0, weight=1)

    def init_people_errors(self) -> None:
        PeopleErrors(self.main_content, self).grid(row=0, sticky="nsew")

    def raise_edit_table(self):
        df = pd.DataFrame([["Souvik Maiti"], ["something else"], ["I just don't want it to crash man"]])
        from .editable_table_frame import EditableTable
        x_offset = self.controller.main_content.winfo_x()
        y_offset = self.controller.main_content.winfo_y()
        print(x_offset, y_offset)
        frame = EditableTable(self.main_content, self, df, "Abstracts", x_offset, y_offset)
        frame.grid(row=0, sticky="nsew")
        frame.tkraise()

    def submit(self, frame_name: str):
        self.controller.show_frame(frame_name)

class PeopleErrors(ttk.Frame):
    def __init__(
        self: "PeopleErrors", parent: ttk.Frame, controller: People
     ) -> None:
        super().__init__(parent)
        self.controller = controller
        self.create_window_elements()
        self.configure_layout()

    def create_window_elements(self: "PeopleErrors") -> None:
        main_content_frame = ttk.Frame(self)
        self.main_content = main_content_frame
        self.main_content.grid(row=0, column=0, sticky="nsew")

        # top text label
        string = "The following names need formatting before insertion:"
        ttk.Label(self.main_content, text=string).grid(row=0, column=0)

        # error frame
        error_content_frame = ttk.Frame(self.main_content)
        self.error_content = error_content_frame
        self.error_content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=10
        )

        # table
        column_names = ("Index", "Full Name")
        name_table = ttk.Treeview(
            master=error_content_frame,
            columns=column_names,
            selectmode="none",
            show="headings",
         )
        self.name_table = name_table
        self.name_table.heading("Index", text='#')
        self.name_table.heading("Full Name", text="Full name")
        self.name_table.column("Index", width=20, stretch=tk.NO)
        self.name_table.column("Full Name", stretch=tk.YES)
        self.name_table.grid(row=0, column=0, sticky="nsew")

        # TODO: Implement actual logic to deliver improper names here
        names = self.controller.controller.df
        for index, row in enumerate(names, start=1):
            name_table.insert("", "end", values=(index, row[0]))

        scrollbar = ttk.Scrollbar(error_content_frame, orient="vertical", command=name_table.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.name_table.configure(yscrollcommand=scrollbar.set)

        # info + number selection + button
        sub_error_content_frame = ttk.Frame(self.main_content)
        sub_error_content_frame.grid(row=2, column=0, sticky="nsew")
        self.sub_error_content = sub_error_content_frame

        string = "How many words are in the selected names?"
        ttk.Label(sub_error_content_frame, text=string).grid(row=0, column=0, padx=(35, 0))
        name_number_combobox = ttk.Combobox(
            sub_error_content_frame,
            values=["1", "3"]
         )
        self.name_number = name_number_combobox
        self.name_number.grid(row=0, column=1, padx=(15, 0))
        self.name_number.config(width=7)
        ttk.Button(
            sub_error_content_frame,
            text="Submit",
            command=self.submit_selections
         ).grid(row=1, column=2, sticky="se", padx=(0, 15), pady=(0, 15))

        name_table.bind('<Button-1>', self.on_tree_click)

    def configure_layout(self: "PeopleErrors") -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.main_content.rowconfigure(1, weight=1)
        self.main_content.columnconfigure(0, weight=1)
        self.error_content.rowconfigure(0, weight=1)
        self.error_content.columnconfigure(0, weight=1)
        self.sub_error_content.columnconfigure(2, weight=1)

    def on_tree_click(self: "PeopleErrors", event: tk.Event) -> None:
        item = self.name_table.identify('item', event.x, event.y)
        if item:
            # Toggle selection
            if item in self.name_table.selection():
                self.name_table.selection_remove(item)
            else:
                self.name_table.selection_add(item)

    def submit_selections(self: "PeopleErrors") -> None:
        for row in self.name_table.selection():
            print(row)
            print(type(row))
        print(int(self.name_number.get()))
        print(type(self.name_table.selection()))
        print(self.name_table.selection())
        self.update_table(self.name_table.selection())

        if self.is_empty():
            self.controller.raise_edit_table()

    def update_table(
        self: "PeopleErrors",
        selections: tuple[str, ...]
     ) -> None:

        self.name_table.delete(*selections)

    def is_empty(self: "PeopleErrors") -> bool:
        if len(self.name_table.get_children()) == 0:
            return True
        else:
            return False
