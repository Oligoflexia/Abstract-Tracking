import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from typing import List, Tuple

from app.logger import error_box
from utils import add_conference_records
from .csv_entry import CSVEntry


class Conferences(ttk.Frame):
    controller: CSVEntry
    toggle: ttk.Button
    input: ttk.Frame
    name_entry: ttk.Entry
    location: ttk.Entry
    organization: ttk.Entry
    start_date: DateEntry
    end_date: DateEntry
    tree: ttk.Treeview

    def __init__(self: "Conferences", parent: ttk.Frame, controller: CSVEntry) -> None: ...

    def create_window_elements(self: "Conferences") -> None: ...

    def configure_layout(self: "Conferences") -> None: ...

    def toggle_fields(self: "Conferences") -> None: ...

    def on_treeview_click(self: "Conferences", event: tk.Event) -> str: ...

    def prompt_box(self: "Conferences", name: str) -> bool: ...

    def submit(self: "Conferences") -> None: ...

    def get_conferences(self: "Conferences") -> None: ...

    def update_table(self: "Conferences", rows: List[Tuple[int, str, str, str, str, str]]) -> None: ...
