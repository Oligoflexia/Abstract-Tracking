import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


def submit():
    
    name = name_entry.get()
    location = location_entry.get()
    organization = organization_entry.get()
    
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    
    print(name, location, organization, start_date, end_date)

def toggle_fields():
    if input_frame.winfo_viewable():
        input_frame.grid_remove()
        toggle_button.configure(text="Show")
    else:
        input_frame.grid()
        toggle_button.configure(text="Hide")

# Main window and frame setup
root = tk.Tk()
root.title("Conference Selection")
root.minsize(width=600, height=500)

ttk.Label(root, text="Add new Conference record:").grid(row=0, sticky='w', padx=(10, 0), pady=(10, 0))

toggle_button = ttk.Button(root, text="Show", command=toggle_fields)
toggle_button.grid(row=1, column=0, sticky='w', padx=(5, 0), pady=(5, 0))

input_frame = ttk.Frame(root)
input_frame.grid(row=2, sticky='ew', padx=(50, 0), pady=(10, 0))
input_frame.grid_remove()
input_frame.columnconfigure(1, weight=1)

ttk.Label(root, text="Current Conference records:").grid(row=3, sticky='w', padx=(10, 0), pady=(10, 0))

# Setup and place entry fields into frame
# Name
ttk.Label(input_frame, text="Conference Name:").grid(row=0, column=0, sticky='w', pady=5)
name_entry = ttk.Entry(input_frame)
name_entry.grid(row=0, column=1, sticky='ew', padx=5)

# Location
ttk.Label(input_frame, text="Location (City):").grid(row=1, column=0, sticky='w', pady=5)
location_entry = ttk.Entry(input_frame)
location_entry.grid(row=1, column=1, sticky='ew', padx=5)

# Organizer name
ttk.Label(input_frame, text="Organizer Name:").grid(row=2, column=0, sticky='w', pady=5)
organization_entry = ttk.Entry(input_frame)
organization_entry.grid(row=2, column=1, sticky='ew', padx=5)

# start
ttk.Label(input_frame, text="Start date:").grid(row=3, column=0, sticky='w', pady=2)
start_date_entry = DateEntry(input_frame, width=12)
start_date_entry.grid(row=4, column=0, sticky='w', padx=3)

# end
ttk.Label(input_frame, text="End date:").grid(row=3, column=1, sticky='w', pady=2)
end_date_entry = DateEntry(input_frame, width=12)
end_date_entry.grid(row=4, column=1, sticky ='w', padx=3)

submit_button = ttk.Button(input_frame, text="Create Record", command=submit)
submit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(20,0))





root.mainloop()

