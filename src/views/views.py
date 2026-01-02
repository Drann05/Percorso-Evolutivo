from abc import ABC, abstractmethod
from breezypythongui import EasyCanvas, EasyFrame

class Views(EasyFrame, ABC):
    """Classe base astratta per tutte le schermate dell'applicazione"""
    def __init__(self, title, width, height):
        EasyFrame.__init__(self, title=title, width=width, height=height)
        self.build_ui()

    @abstractmethod
    def build_ui(self):
        """Metodo astratto obbligatorio per costruire l'interfaccia"""
        pass

    @abstractmethod
    def update(self):
        """Metodo astratto obbligatorio per aggiornare i widget"""
        pass

    @abstractmethod
    def handle_events(self, event_type):
        pass

    def create_label(self, container, text, row, column, sticky="NSEW"):
        return container.addLabel(text=text, row=row, column=column, sticky=sticky)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

