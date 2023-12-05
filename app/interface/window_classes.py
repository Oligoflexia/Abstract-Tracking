import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from typing import Union

# Global variables
# Metadata
VERSION: str = "pre-alpha"
VERSION_NUM: str = "v0.1"

# Window Options
BASE_WINDOW_WIDTH: int = 725
BASE_WINDOW_HEIGHT: int = 400

# Style Options
FONT: str = "Helvetica"


class BaseWindow:
    def __init__(
        self: "BaseWindow", parent: Union["MainWindow", "SecondaryWindow"]
    ) -> None:
        self.parent = parent
        self.configure_window()

    def configure_window(self: "BaseWindow") -> None:
        self.parent.title(f"Abstract Tracker {VERSION} {VERSION_NUM}")
        self.parent.minsize(width=BASE_WINDOW_WIDTH, height=BASE_WINDOW_HEIGHT)

        # Bring the window to the top
        self.parent.lift()

        # Remove 'always on top' after 1 second
        self.parent.after(
            1000, lambda: self.parent.attributes("-topmost", False)
        )


class MainWindow(tk.Tk, BaseWindow):
    def __init__(self: "MainWindow") -> None:
        tk.Tk.__init__(self)
        BaseWindow.__init__(self, self)

        self.create_banner()
        self.create_sidebar()
        self.create_main_area()
        self.configure_layout()

    def create_banner(self: "MainWindow") -> None:
        banner_frame = ttk.Frame(self)
        banner_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.banner = banner_frame

        banner_font = tkfont.Font(family=FONT, size=12, weight="bold")

        connected_db_text = "Currently connected database: " + "None"
        self.connected_db_text = tk.StringVar(value=connected_db_text)

        banner_label = tk.Label(
                                banner_frame,
                                textvariable=self.connected_db_text,
                                fg="white",
                                bg="#f75959",
                                font=banner_font,
                                 )

        banner_label.pack(fill="x")

    def create_sidebar(self: "MainWindow") -> None:
        sidebar_frame = ttk.Frame(self,
                                  width=200,
                                  relief="sunken",
                                  borderwidth=2
                                  )
        sidebar_frame.grid(row=1, column=0, sticky="ns")
        self.sidebar = sidebar_frame

    def create_main_area(self: "MainWindow") -> None:
        main_content_area_frame = ttk.Frame(self)
        main_content_area_frame.grid(row=1, column=1, sticky="nsew")
        self.main_content_area = main_content_area_frame

    def configure_layout(self: "MainWindow") -> None:
        # root
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # main_content_area
        self.main_content_area.columnconfigure(0, weight=1)
        self.main_content_area.rowconfigure(0, weight=1)
        self.main_content_area.columnconfigure(1, weight=1)
        self.main_content_area.rowconfigure(1, weight=1)
        self.main_content_area.columnconfigure(2, weight=1)
        self.main_content_area.rowconfigure(2, weight=1)

    def turn_banner_green(self: "MainWindow") -> None:
        for widget in self.banner.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg="#59f75a")


class SecondaryWindow(tk.Toplevel, BaseWindow):
    def __init__(
        self: "SecondaryWindow",
        parent: Union[MainWindow, "SecondaryWindow"]
    ) -> None:

        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        BaseWindow.__init__(self, self)
