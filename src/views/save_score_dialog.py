from breezypythongui import EasyDialog


class SaveScoreDialog(EasyDialog):
    """Finestra di dialogo per confermare il salvataggio."""

    def __init__(self, parent, title="Salva Partita"):
        self._result = False
        super().__init__(parent, title)

    def body(self, master):
        self.addLabel(master, text="Vuoi salvare il tuo punteggio in classifica?",
                      row=0, column=0, columnspan=2)

    def apply(self):
        self._result = True

    def get_result(self):
        return self._result
