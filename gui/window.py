import tkinter as tk
from tkinter import ttk
import sqlite3

def run_query():
    query = query_box.get("1.0", 'end-1c')  # Get the query from text box
    try:
        cursor.execute(query)
        # Retrieve column names from cursor
        column_names = [description[0] for description in cursor.description]
        update_treeview_columns(column_names)
        rows = cursor.fetchall()
        update_table(rows)
    except sqlite3.Error as error:
        print("Error: ", error)

def update_treeview_columns(column_names):
    tree["columns"] = column_names  # Set the columns of the Treeview
    tree.delete(*tree.get_children())  # Clear existing rows and columns

    # Configure column headings and column settings
    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

def update_table(rows):
    for row in rows:
        tree.insert("", 'end', values=row)


# Set up the main window
root = tk.Tk()
root.title("SQL Query Executor")

# Configure the grid layout
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Text box for SQL query with a scrollbar
query_frame = tk.Frame(root)
query_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
query_frame.grid_columnconfigure(0, weight=1)

query_box = tk.Text(query_frame, height=4, width=50)
query_box.grid(row=0, column=0, sticky='ew')

scrollbar = tk.Scrollbar(query_frame, command=query_box.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
query_box['yscrollcommand'] = scrollbar.set

# Button to execute the query
run_button = tk.Button(root, text="Run Query", command=run_query)
run_button.grid(row=2, column=0, pady=5, padx=10)

# Treeview for the table
tree = ttk.Treeview(root, columns=(1, 2, 3), show="headings")
tree.grid(row=1, column=0, sticky='nsew', padx=10)

# Connect to SQLite3 database
conn = sqlite3.connect('abstracts.db')
cursor = conn.cursor()

root.mainloop()