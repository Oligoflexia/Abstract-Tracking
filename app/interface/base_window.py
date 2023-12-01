class BaseWindow:
    def __init__(self, parent_window) -> None:
        self.parent_window = parent_window

    foreign_key_mappings = {
        "submitter_ID": ("People", "person_ID"),
        "first_author": ("People", "person_ID"),
        "c_id": ("Conference", "conference_ID"),
        "p_id": ("People", "person_ID"),
        "a_id": ("Abstract", "abstract_ID"),
    }
