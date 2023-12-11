import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from typing import List, Tuple

from app.logger import error_box
from utils import add_conference_records


class Conferences(ttk.Frame):
    from .csv_entry import CSVEntry

    def __init__(
        self: "Conferences", parent: ttk.Frame, controller: CSVEntry
     ) -> None:

        super().__init__(parent)
        self.controller = controller
        self.create_window_elements()
        self.configure_layout()
        self.get_conferences()

    def create_window_elements(self: "Conferences") -> None:

        # Text at the top of the window
        ttk.Label(self, text="INFO:", font=("Arial", 10, "bold")).grid(
            row=0, sticky="w", padx=(10, 0), pady=(10, 0)
         )

        string = "Click existing Conference record to link new CSV records."
        ttk.Label(self, text=string).grid(row=1, sticky="w", padx=(10, 0))

        string = "Add new Conference record:"
        ttk.Label(self, text=string, font=("Arial", 10, "bold")).grid(
            row=2, sticky="w", padx=(10, 0), pady=(25, 0)
         )

        # Input area
        toggle_button = ttk.Button(
            self, text="Show", command=self.toggle_fields
         )
        self.toggle = toggle_button

        toggle_button.grid(
            row=3, column=0, sticky="w", padx=(10, 0), pady=(5, 0)
         )

        input_frame = ttk.Frame(self)
        self.input = input_frame

        input_frame.grid(row=4, sticky="ew", padx=(50, 0), pady=(10, 0))
        input_frame.grid_remove()

        # Name
        ttk.Label(input_frame, text="Conference Name:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        name_entry = ttk.Entry(input_frame)
        self.name_entry = name_entry

        name_entry.grid(row=0, column=1, sticky="w", padx=5)

        # Location
        ttk.Label(input_frame, text="Location (City):").grid(
            row=1, column=0, sticky="w", pady=5
        )
        location_entry = ttk.Entry(input_frame)
        self.location = location_entry

        location_entry.grid(row=1, column=1, sticky="w", padx=5)

        # Organizer name
        ttk.Label(input_frame, text="Organizer Name:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        organization_entry = ttk.Entry(input_frame)
        self.organization = organization_entry

        organization_entry.grid(row=2, column=1, sticky="w", padx=5)

        # start
        ttk.Label(input_frame, text="Start date:").grid(
            row=3, column=0, sticky="w", pady=2
        )
        start_date_entry = DateEntry(input_frame, width=12)
        self.start_date = start_date_entry

        start_date_entry.grid(row=4, column=0, sticky="w", padx=3)

        # end
        ttk.Label(input_frame, text="End date:").grid(
            row=3, column=1, sticky="w", pady=2
        )
        end_date_entry = DateEntry(input_frame, width=12)
        self.end_date = end_date_entry

        end_date_entry.grid(row=4, column=1, sticky="w", padx=3)

        # buttons
        submit_button = ttk.Button(
            input_frame, text="Create Record", command=self.submit_new_conference
         )
        submit_button.grid(
            row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=(35, 0)
        )

        # Table area
        string = "Current Conference records:"
        ttk.Label(self, text=string, font=("Arial", 10, "bold")).grid(
                row=5, sticky="w", padx=(10, 0), pady=(30, 10)
         )

        # set up Conference records table
        tree = ttk.Treeview(self, columns=(1, 2, 3, 4, 5, 6), show="headings")
        self.tree = tree

        tree.grid(row=6, sticky="nesw", padx=(10, 0), pady=(0, 10), columnspan=2)

        tree.heading(1, text="ID")
        tree.column(1, width=30, stretch=tk.NO)
        tree.heading(2, text="Conference Name")
        tree.column(2, width=175, stretch=tk.YES)
        tree.heading(3, text="City")
        tree.column(3, width=100, stretch=tk.YES)
        tree.heading(4, text="Start Date")
        tree.column(4, width=125, stretch=tk.NO)
        tree.heading(5, text="End Date")
        tree.column(5, width=125, stretch=tk.NO)
        tree.heading(6, text="Organizer")
        tree.column(6, width=175, stretch=tk.YES)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        scrollbar.grid(row=6, column=2, sticky="nse", pady=(0, 10), padx=(0, 10))
        self.tree.configure(yscrollcommand=scrollbar.set)

        submit_button = ttk.Button(self, text="Submit", command=self.submit)
        submit_button.grid(row=7, column=1, sticky="se", padx=(0, 10), pady=(0, 10), columnspan=2)

    def configure_layout(self: "Conferences") -> None:
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=0)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=0)

        self.columnconfigure(0, weight=1)

    def toggle_fields(self: "Conferences") -> None:
        if self.input.winfo_viewable():
            self.input.grid_remove()
            self.toggle.configure(text="Show")
        else:
            self.input.grid()
            self.toggle.configure(text="Hide")

    def prompt_box(self: "Conferences", name: str) -> bool:
        string = f"Are you sure you want to link new CSV records with:\n{name}"
        response = messagebox.askyesno("Confirm Selection", string)
        return response

    def submit_new_conference(self: "Conferences") -> None:
        name = self.name_entry.get()
        if name == "":
            error_box("Conference must have a name!")
            return

        location = self.location.get()
        organization = self.organization.get()
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()

        if start_date > end_date:
            error_box("Start date can't be after end date!")
            return

        dict_list = [
            {
                "conference_name": name,
                "location": location,
                "start_date": start_date.strftime(r"%Y-%m-%d"),
                "end_date": end_date.strftime(r"%Y-%m-%d"),
                "organization": organization,
            }
        ]

        try:
            add_conference_records(self.controller.conn, dict_list)
        except Exception:
            return

        self.get_conferences()

    def get_conferences(self: "Conferences") -> None:
        import sqlite3
        try:
            self.controller.cursor.execute("SELECT * from Conferences")
            rows = self.controller.cursor.fetchall()
            self.update_table(rows)
        except sqlite3.Error as error:
            messagebox.showerror("Query Error", f"An error occurred: {error}")

    def update_table(
        self: "Conferences", rows: List[Tuple[int, str, str, str, str, str]]
         ) -> None:

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def submit(self):
        row_item = self.tree.item(self.tree.selection()[0])["values"]

        if self.prompt_box(row_item[1]):
            self.controller.show_frame("People")
            return row_item[0]
