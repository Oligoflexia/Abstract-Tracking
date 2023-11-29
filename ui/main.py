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
banner_frame.grid(row=0, column=0,columnspan=2, sticky="ew")

db_text = "Currently connected database: "
db_name = "abstracts.db"

banner_label = tk.Label(banner_frame, text=db_text + db_name, fg="white", bg="#f75959", font=banner_font)
banner_label.pack(fill="x")

# sidebar
sidebar = ttk.Frame(root, width=200, relief="sunken", borderwidth=2)
sidebar.grid(row=1, column=0, sticky="ns")

# Buttons in the sidebar
button1 = ttk.Button(sidebar, text="App 1", command=lambda: print("Open App 1"))
button1.pack(padx=10, pady=10, fill="x")

button2 = ttk.Button(sidebar, text="App 2", command=lambda: print("Open App 2"))
button2.pack(padx=10, pady=10, fill="x")

# Main content area below the banner, next to the sidebar
main_content = ttk.Label(root, text="Main Content Area", anchor="center")
main_content.grid(row=1, column=1, sticky="nsew")





if __name__ == "__main__":
    
    dbconnection = dbconnections.DBConnection('abstracts.db')
    
    try:
        conn = dbconnection.get_connection()
        #cursor = conn.cursor()

        root.lift()  # Bring the window to the top
        root.after(1000, lambda: root.attributes("-topmost", False))  # Remove 'always on top' after 1 second
        root.mainloop()

    finally:
        dbconnection.close_connection()

tkfont.Font()
