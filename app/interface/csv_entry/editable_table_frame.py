import tkinter as tk
from tkinter import ttk
import pandas as pd


class EditableTable(ttk.Frame):
    def __init__(self, parent, controller, df: pd.DataFrame, next_frame: str, parent_x: int = 0, parent_y: int = 0) -> None:
        super().__init__(parent)
        self.df = df
        self.controller = controller
        self.next = next_frame
        self.parent_x = parent_x
        self.parent_y = parent_y

        self.create_window_elements()
        self.configure_layout()
        self.entryPopup = None

    def create_window_elements(self) -> None:
        main_content_frame = ttk.Frame(self)
        self.main_content = main_content_frame
        self.main_content.grid(row=0, column=0, sticky="nsew")

        # TODO: A way to get the actual table name
        table_name = "TEMP"
        string = f"Review records for insertion into <{table_name}>:"
        ttk.Label(self.main_content, text=string).grid(row=0, column=0)

        string = "Double click a cell to edit the value"
        ttk.Label(self.main_content, text=string).grid(row=1, column=0)

        # table frame
        table_content_frame = ttk.Frame(self.main_content)
        self.table_content = table_content_frame
        self.table_content.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=30,
            pady=10
        )

        # table
        column_names = self.df.columns.tolist()
        table = ttk.Treeview(
            master=self.table_content,
            columns=column_names,
            show="headings"
         )
        self.table = table

        for col in column_names:
            self.table.heading(col, text=col)
            self.table.column(col, anchor=tk.W)

        for _, row in self.df.iterrows():
            self.table.insert("", "end", values=row.tolist())

        self.table.grid(row=0, column=0, sticky="nsew")
        self.table.bind("<Double-1>", self.on_double_click)

        ttk.Button(
            master=self.main_content,
            text="Submit",
            command=lambda: self.controller.submit(self.next)
         ).grid(row=3, column=0, sticky="se", padx=(0, 15), pady=(0, 15))

    def configure_layout(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.main_content.rowconfigure(2, weight=1)
        self.main_content.columnconfigure(0, weight=1)
        self.table_content.rowconfigure(0, weight=1)
        self.table_content.columnconfigure(0, weight=1)

    def on_double_click(self, event):
        if self.entryPopup:
            self.entryPopup.destroy()

        item = self.table.identify_row(event.y)
        column = self.table.identify_column(event.x)
        col_index = int(column.replace('#', '')) - 1

        x, y, width, height = self.table.bbox(item, column)

        assert (isinstance(x, int))
        assert (isinstance(y, int))
        assert (isinstance(width, int))
        assert (isinstance(height, int))

        tree_y = self.parent_y
        tree_y += self.table_content.winfo_y()
        tree_y += self.table.winfo_y()
        tree_y += y

        tree_x = self.parent_x
        tree_x += self.table_content.winfo_x()
        tree_x += self.table.winfo_x()
        tree_x += x

        self.entryPopup = tk.Entry(self.winfo_toplevel())
        self.entryPopup.place(x=tree_x, y=tree_y, width=width, height=height)
        old_val = self.table.item(item, "values")[col_index]
        self.entryPopup.insert(0, old_val)
        self.entryPopup.focus()

        def on_entry_confirm(event=None):
            if self.entryPopup:
                new_value = self.entryPopup.get()
                self.table.set(item, column=column, value=new_value)

                row_index = self.table.index(item)
                self.df.iat[row_index, col_index] = new_value
                self.entryPopup.destroy()

        self.entryPopup.bind("<Return>", on_entry_confirm)
        self.entryPopup.bind("<FocusOut>", on_entry_confirm)

    def submit(self) -> pd.DataFrame:
        return self.df
