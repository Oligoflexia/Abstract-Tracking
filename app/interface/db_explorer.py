from .window_classes import SecondaryWindow


class DBExplorer(SecondaryWindow):
    from .main_application import MainApplication
    def __init__(self: "DBExplorer", parent: MainApplication) -> None:
        super().__init__(parent)
        self.title("DB Explorer")

    def create_window_elements(self: "DBExplorer") -> None:
        pass

    def configure_grids(self: "DBExplorer") -> None:
        pass
