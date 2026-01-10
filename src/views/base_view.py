from abc import ABC, abstractmethod


class BaseView(ABC):
    """Classe base astratta per tutte le schermate dell'applicazione"""
    def __init__(self, parent_view, controller, title):
        self._parent_view = parent_view
        self._controller = controller
        self._title = title
        self.build_ui()

    @abstractmethod
    def build_ui(self):
        """Metodo astratto obbligatorio per costruire l'interfaccia"""
        pass

    def _setup_base_layout(self):
        self._parent_view.columnconfigure(0, weight=1)
        self._parent_view.rowconfigure(0, weight=1)



