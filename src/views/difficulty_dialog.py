from breezypythongui import EasyDialog

class DifficultyDialog(EasyDialog):
    def __init__(self, parent, controller):
        self._controller = controller
        super().__init__(parent, title="Selezione Difficoltà")

    def body(self, master):
        """Crea il corpo della finestra di dialogo."""
        self.addLabel(master, text="Seleziona il livello di sfida:", row=0, column=0, columnspan=3)

        self.addButton(master, text="Facile", row=1, column=0, command=lambda: self.set_difficulty("Facile"))
        self.addButton(master, text="Medio", row=1, column=1, command=lambda: self.set_difficulty("Medio"))
        self.addButton(master, text="Difficile", row=1, column=2, command=lambda: self.set_difficulty("Difficile"))

    def set_difficulty(self, difficulty):
        self._controller.on_difficulty_selected(difficulty)
        self.destroy()