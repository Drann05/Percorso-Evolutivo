from abc import ABC, abstractmethod
from breezypythongui import EasyCanvas, EasyFrame, EasyCanvas, EasyDialog


class Views(EasyFrame, EasyCanvas, EasyDialog, ABC):
    """Classe base astratta per tutte le schermate dell'applicazione"""
    def __init__(self, title, width, height):
        EasyFrame.__init__(self, title=title, width=width, height=height)

    @abstractmethod
    def build_ui(self):
        """Metodo astratto obbligatorio per costruire l'interfaccia"""
        pass


    def create_label(self, container, text, row, column, sticky="NSEW"):
        return container.addLabel(text=text, row=row, column=column, sticky=sticky)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def grid_init(self, row, column):
        for r in range(row):
            self.rowconfigure(r, weight=1)
        for c in range(column):
            self.columnconfigure(c, weight=1)
