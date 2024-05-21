from CTkListbox import CTkListbox
from customtkinter import CTkOptionMenu


class MappedListbox(CTkListbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_map = {}

    def insert_with_value(self, index, display_text, actual_value):
        """Fügt einen Eintrag mit einem zugehörigen Wert hinzu."""
        self.insert(index, display_text)
        self.value_map[display_text] = actual_value

    def get_value(self, index):
        """Gibt den tatsächlichen Wert für den ausgewählten Eintrag zurück."""
        display_text = self.get(index)
        return self.value_map.get(display_text, None)