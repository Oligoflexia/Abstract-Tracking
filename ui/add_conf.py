from logging import LogRecord
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import logging

from utils import db_operations, dbconnections

class LoggingHandler(logging.Handler):
    def emit(self, record: LogRecord) -> None:
        log_entry = self.format(record)
        error_box(log_entry)

def error_box(message:str):
    messagebox.showerror("Error!", message)

def prompt_box(name:str):
    string = f"Are you sure you want to link new CSV records with: \n {name}"
    response = messagebox.askyesno("Confirm Selection", string)
    return response

def submit():
    
    name = name_entry.get()
    if name == "": 
        error_box("Conference must have a name!")
        return
    
    location = location_entry.get()
    organization = organization_entry.get()
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    if start_date > end_date:
        error_box("Start date can't be after end date!")
        return
    
    dict_list = [{"conference_name": name,
                      "location": location,
                      "start_date": start_date.strftime(r"%Y-%m-%d"),
                      "end_date": end_date.strftime(r"%Y-%m-%d"),
                      "organization": organization
                    }
                ]
    
    try: db_operations.add_conference_records(conn, dict_list)
    except Exception as e: return
    get_conferences()

def toggle_fields():
    if input_frame.winfo_viewable():
        input_frame.grid_remove()
        toggle_button.configure(text="Show")
    else:
        input_frame.grid()
        toggle_button.configure(text="Hide")

def get_conferences():
    try:
        cursor.execute("SELECT * from Conferences")
        rows = cursor.fetchall()
        update_table(rows)
    except sqlite3.Error as error:
        messagebox.showerror("Query Error", f"An error occurred: {error}")

def update_table(rows):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", 'end', values=row)

def on_treeview_click(event) -> int:
    region = tree.identify("region", event.x, event.y)
    if region == "cell":
        row_id = tree.identify_row(event.y)
        row_item = tree.item(row_id)
        ConferenceID = row_item['values'][0]
        
        if prompt_box(row_item['values'][1]):
            root.quit()
            return ConferenceID

# Main window and frame setup
root = tk.Tk()
root.title("Conference Selection")
root.minsize(width=725, height=550)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=0)
root.rowconfigure(3, weight=0)
root.rowconfigure(4, weight=0)
root.rowconfigure(5, weight=0)
root.rowconfigure(6, weight=1)

ttk.Label(root, text="INFO:", font=("Arial", 10, "bold")).grid(row=0, sticky='w', padx=(10, 0), pady=(10, 0))

string = "Click existing Conference record to link new CSV records."
ttk.Label(root, text=string).grid(row=1, sticky='w', padx=(10, 0))
ttk.Label(root, text="Add new Conference record:", font=("Arial", 10, "bold")).grid(row=2, sticky='w', padx=(10, 0), pady=(25, 0))

toggle_button = ttk.Button(root, text="Show", command=toggle_fields)
toggle_button.grid(row=3, column=0, sticky='w', padx=(10, 0), pady=(5, 0))

input_frame = ttk.Frame(root)
input_frame.grid(row=4, sticky='ew', padx=(50, 0), pady=(10, 0))
input_frame.grid_remove()

ttk.Label(root, text="Current Conference records:", font=("Arial", 10, "bold")).grid(row=5, sticky='w', padx=(10, 0), pady=(30, 10))

#set up Conference records table
tree = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6), show="headings")
tree.grid(row=6, sticky='nesw', padx=10, pady=(0, 10))
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
tree.bind("<Button-1>", on_treeview_click)

# Setup and place entry fields into frame
# Name
ttk.Label(input_frame, text="Conference Name:").grid(row=0, column=0, sticky='w', pady=5)
name_entry = ttk.Entry(input_frame)
name_entry.grid(row=0, column=1, sticky='w', padx=5)

# Location
ttk.Label(input_frame, text="Location (City):").grid(row=1, column=0, sticky='w', pady=5)
location_entry = ttk.Entry(input_frame)
location_entry.grid(row=1, column=1, sticky='w', padx=5)

# Organizer name
ttk.Label(input_frame, text="Organizer Name:").grid(row=2, column=0, sticky='w', pady=5)
organization_entry = ttk.Entry(input_frame)
organization_entry.grid(row=2, column=1, sticky='w', padx=5)

# start
ttk.Label(input_frame, text="Start date:").grid(row=3, column=0, sticky='w', pady=2)
start_date_entry = DateEntry(input_frame, width=12)
start_date_entry.grid(row=4, column=0, sticky='w', padx=3)

# end
ttk.Label(input_frame, text="End date:").grid(row=3, column=1, sticky='w', pady=2)
end_date_entry = DateEntry(input_frame, width=12)
end_date_entry.grid(row=4, column=1, sticky ='w', padx=3)

# buttons
submit_button = ttk.Button(input_frame, text="Create Record", command=submit)
submit_button.grid(row=5, column=0, columnspan=2, sticky='ew', padx=10, pady=(35,0))

if __name__ == "__main__":
    
    dbconnection = dbconnections.DBConnection('abstracts.db')
    
    try:
        logger = logging.getLogger()
        logger.addHandler(LoggingHandler())
        
        conn = dbconnection.get_connection()
        cursor = conn.cursor()

        get_conferences()
        
        root.lift()  # Bring the window to the top
        root.after(1000, lambda: root.attributes("-topmost", False))  # Remove 'always on top' after 1 second
        root.mainloop()

    finally:
        dbconnection.close_connection()
