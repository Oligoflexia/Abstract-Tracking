import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from utils import dbconnections

# Mapping of foreign key columns (column name to referenced table)
foreign_key_mappings = {
    'submitter_ID': ('People', 'person_ID'),
    'first_author': ('People', 'person_ID'),
    'c_id': ('Conference', 'conference_ID'),
    'p_id': ('People', 'person_ID'),
    'a_id': ('Abstract', 'abstract_ID')
}

def export_to_csv():
    try:
        # Open a file dialog to choose where to save the CSV
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
        if not file_path:  # Check if the user canceled the save operation
            return

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(tree["columns"])  # Write column headers

            for row_id in tree.get_children():
                row = tree.item(row_id)['values']
                writer.writerow(row)

        messagebox.showinfo("Export Status", f"Data exported to '{file_path}' successfully.")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred: {e}")

def run_query():
    query = query_box.get("1.0", 'end-1c')  # Get the query from text box
    try:
        cursor.execute(query)
        column_names = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        update_treeview_columns(column_names)
        update_table(rows)
        messagebox.showinfo("Query Status", "Query executed successfully.")
    except sqlite3.Error as error:
        messagebox.showerror("Query Error", f"An error occurred: {error}")

def update_treeview_columns(column_names):
    tree["columns"] = column_names
    tree.delete(*tree.get_children())
    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

def update_table(rows):
    for row in rows:
        tree.insert("", 'end', values=row)

def on_treeview_click(event):
    region = tree.identify("region", event.x, event.y)
    if region == "cell":
        row_id = tree.identify_row(event.y)
        column_id = tree.identify_column(event.x)
        column_name = tree.heading(column_id, 'text')
        if column_name in foreign_key_mappings:
            foreign_key_value = tree.set(row_id, column_id)
            referenced_table, primary_key_column = foreign_key_mappings[column_name]
            display_referenced_data(foreign_key_value, referenced_table, primary_key_column)

def display_referenced_data(foreign_key_value, referenced_table, primary_key_column):
    query = f"SELECT * FROM {referenced_table} WHERE {primary_key_column} = ?"
    cursor.execute(query, (foreign_key_value,))
    data = cursor.fetchone()
    if data:
        # Fetch the column names for the referenced table
        column_names = [description[0] for description in cursor.description]
        formatted_data = '\n'.join([f"{col}: {val}" for col, val in zip(column_names, data)])

        # Create a Toplevel window
        top = tk.Toplevel(root)
        top.title(f"{referenced_table} Details")
        top.wm_attributes("-topmost", True)

        # Create a Text widget
        text = tk.Text(top, wrap='none')  # 'none' to avoid line wrapping
        text.insert('1.0', formatted_data)
        text.config(state='disabled')  # Make the text read-only
        text.pack(expand=True, fill='both')

        # Optionally, add a scrollbar
        scrollbar = tk.Scrollbar(top, command=text.yview)
        scrollbar.pack(side='right', fill='y')
        text['yscrollcommand'] = scrollbar.set
    else:
        messagebox.showerror("Data Not Found", f"No data found for ID {foreign_key_value} in {referenced_table}")

# Set up the main window and Treeview
root = tk.Tk()
root.title("Query Viewer")

# Configure the grid layout
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Text box for SQL query with a scrollbar
query_frame = tk.Frame(root)
query_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
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
tree.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10)
tree.bind("<Button-1>", on_treeview_click)

# Adding a button for CSV export
export_button = ttk.Button(root, text="Export to CSV", command=export_to_csv)
export_button.grid(row=2, column=1, pady=5, padx=10)


if __name__ == "__main__":
    
    dbconnection = dbconnections.DBConnection('abstracts.db')
    
    try:
        conn = dbconnection.get_connection()
        cursor = conn.cursor()

        root.lift()  # Bring the window to the top
        root.after(1000, lambda: root.attributes("-topmost", False))  # Remove 'always on top' after 1 second
        root.mainloop()

    
    finally:
        dbconnection.close_connection()

