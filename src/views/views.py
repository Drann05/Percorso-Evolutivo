from abc import ABC, abstractmethod
from breezypythongui import EasyFrame, EasyCanvas

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
    def handle_events(self, event_type, **kwargs):
        pass

    def grid_init(self, row, column):
        for r in range(row):
            self.rowconfigure(r, weight=1)
        for c in range(column):
            self.columnconfigure(c, weight=1)



