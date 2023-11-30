import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from utils import dbconnections

# root settings
root = tk.Tk()
root.title("Abstract Tracker pre-alpha v0.1")
root.minsize(width=725, height=400)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

# top banner
banner_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
banner_frame = tk.Frame(root)
banner_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

db_text = "Currently connected database: "
db_name = "abstracts.db"

banner_label = tk.Label(
    banner_frame,
    text=db_text + db_name,
    fg="white",
    bg="#f75959",
    font=banner_font,
)
banner_label.pack(fill="x")

# sidebar
sidebar = ttk.Frame(root, width=200, relief="sunken", borderwidth=2)
sidebar.grid(row=1, column=0, sticky="ns")

# Buttons in the sidebar
sql_explorer_button = ttk.Button(
    sidebar,
    text="SQL Explorer",
    command=lambda: print("SQL Explorer"),
)
sql_explorer_button.pack(padx=10, pady=10)

db_explorer_button = ttk.Button(
    sidebar,
    text="DB Explorer",
    command=lambda: print("DB Explorer"),
)
db_explorer_button.pack(padx=10, pady=10, fill="x")

# Main content area below the banner, next to the sidebar
main_content = ttk.Frame(root)
main_content.grid(row=1, column=1, sticky="nsew")

main_content.columnconfigure(0, weight=1)
main_content.rowconfigure(0, weight=1)
main_content.columnconfigure(1, weight=1)
main_content.rowconfigure(1, weight=1)
main_content.columnconfigure(2, weight=1)
main_content.rowconfigure(2, weight=1)

connect_button = ttk.Button(
    main_content,
    text="Connect",
    command=lambda: print("Connect DB"),
)
connect_button.grid(row=0, column=0)

csv_button = ttk.Button(
    main_content,
    text="CSV Import",
    command=lambda: print("CSV Import"),
)
csv_button.grid(row=1, column=0)

data_folder_button = ttk.Button(
    main_content, text="Data Files", command=lambda: print("Data Files")
)
data_folder_button.grid(row=1, column=1)

docs_button = ttk.Button(
    main_content, text="Documentation", command=lambda: print("Documentation")
)
docs_button.grid(row=2, column=0)

settings_button = ttk.Button(
    main_content, text="Settings", command=lambda: print("Settings")
)
settings_button.grid(row=2, column=1)


if __name__ == "__main__":
    dbconnection = dbconnections.DBConnection("abstracts.db")

    try:
        conn = dbconnection.get_connection()
        # cursor = conn.cursor()

        root.lift()  # Bring the window to the top
        # Remove 'always on top' after 1 second
        root.after(1000, lambda: root.attributes("-topmost", False))
        root.mainloop()

    finally:
        dbconnection.close_connection()
