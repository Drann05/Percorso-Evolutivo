from abc import ABC, abstractmethod


class Views(ABC):
    """Classe base astratta per tutte le schermate dell'applicazione"""
    def __init__(self, title, width, height):
        pass

    @abstractmethod
    def build_ui(self):
        """Metodo astratto obbligatorio per costruire l'interfaccia"""
        pass




