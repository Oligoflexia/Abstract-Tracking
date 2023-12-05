import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Any
import sqlite3

from utils import write_CSV, execute_sql
from .window_classes import SecondaryWindow


foreign_key_mappings = {}

# TODO: Don't let you launch the app unless DB connected
# TODO: figure out automatic way to get foreign_key_mappings
# TODO: type annotations
class SQLExplorer(SecondaryWindow):
    from .main_application import MainApplication
    def __init__(self: "SQLExplorer", parent: MainApplication) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title("SQL Query Viewer")
        self.create_window_elements()
        self.configure_grids()

    def create_window_elements(self: "SQLExplorer") -> None:
        # Text box for SQL query with a scrollbar
        # main Frame to hold everything
        main_frame = ttk.Frame(self)
        self.main = main_frame

        main_frame.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )

        query_box = tk.Text(main_frame, height=4, width=50)
        self.query_box = query_box

        query_box.grid(row=0, column=0, sticky="ew")

        scrollbar = ttk.Scrollbar(main_frame, command=query_box.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        query_box["yscrollcommand"] = scrollbar.set

        # Button to execute the SQL query
        run_button = ttk.Button(self, text="Run Query", command=self.run_query)
        run_button.grid(row=2, column=0, pady=5, padx=10)

        # Treeview for the table
        tree = ttk.Treeview(self, columns=(1, 2, 3), show="headings")
        self.tree = tree

        tree.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10)
        tree.bind("<Button-1>", self.on_treeview_click)

        # Adding a button for CSV export
        export_button = ttk.Button(
            self, text="Export to CSV", command=self.export_to_csv
        )
        export_button.grid(row=2, column=1, pady=5, padx=10)

    def configure_grids(self: "SQLExplorer") -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

    def export_to_csv(self: "SQLExplorer") -> None:
        filetypes = [("CSV files", "*.csv")]
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv", filetypes=filetypes
            )
            if not file_path:
                return
            else:
                write_CSV(file_path, self.tree)
                success_message = f"Exported to '{file_path}' successfully!"
                messagebox.showinfo("Export Status", success_message)
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {e}")

    def run_query(self: "SQLExplorer") -> None:
        from .main_application import MainApplication
        query = self.query_box.get("1.0", "end-1c")
        assert(isinstance(self.parent, MainApplication))
        cursor = self.parent.get_cursor()

        try:
            column_names, rows = execute_sql(query, cursor)
            self.update_treeview_columns(column_names)
            self.update_table(rows)
        except sqlite3.Error as e:
            messagebox.showerror("Query Eror", f"An error occurred: {e}")

    def update_treeview_columns(
        self: "SQLExplorer", column_names: list[str]
    ) -> None:
        self.tree["columns"] = column_names
        self.tree.delete(*self.tree.get_children())
        for col in column_names:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

    def update_table(self: "SQLExplorer", rows: list[Any]) -> None:
        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_treeview_click(self: "SQLExplorer", event) -> None:
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.tree.identify_row(event.y)
            column_id = self.tree.identify_column(event.x)
            column_name = self.tree.heading(column_id, "text")
            if column_name in foreign_key_mappings:
                foreign_key_value = self.tree.set(row_id, column_id)
                referenced_table, primary_key_column = foreign_key_mappings[
                    column_name
                ]
                self.display_referenced_data(
                    foreign_key_value, referenced_table, primary_key_column
                )

    def display_referenced_data(
        self, foreign_key_value, referenced_table, primary_key_column
    ) -> None:
        from .main_application import MainApplication

        query = (
            f"SELECT * FROM {referenced_table} WHERE {primary_key_column} = ?"
        )
        assert(isinstance(self.parent, MainApplication))
        cursor = self.parent.get_cursor()

        # TODO: refactor this  into db_operations
        cursor.execute(query, (foreign_key_value,))
        data = cursor.fetchone()

        if data:
            # Fetch the column names for the referenced table
            column_names = [
                description[0] for description in cursor.description
            ]
            formatted_data = "\n".join(
                [f"{col}: {val}" for col, val in zip(column_names, data)]
            )

            # Create a Toplevel window
            top = tk.Toplevel(self)
            top.title(f"{referenced_table} Details")
            top.wm_attributes("-topmost", True)

            # Create a Text widget
            text = tk.Text(top, wrap="none")  # 'none' to avoid line wrapping
            text.insert("1.0", formatted_data)
            text.config(state="disabled")  # Make the text read-only
            text.pack(expand=True, fill="both")

            # Optionally, add a scrollbar
            scrollbar = tk.Scrollbar(top, command=text.yview)
            scrollbar.pack(side="right", fill="y")
            text["yscrollcommand"] = scrollbar.set
        else:
            messagebox.showerror(
                "Data Not Found",
                f"No data found for ID {foreign_key_value} in {referenced_table}",
            )
