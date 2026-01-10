

class DifficultyDialog:
    def __init__(self, parent_view, controller):
        self._parent_view = parent_view
        self._controller = controller
        self.build_ui()

    def build_ui(self):
        self.overlay = self._parent_view.addPanel(row=1, column=0, background="#212121")
        self.overlay.grid_configure(padx=100, pady=100)

        # Titolo dell'overlay
        self.title_lbl = self.overlay.addLabel(
            text="SELEZIONA DIFFICOLTÀ",
            row=0, column=0, columnspan=3
        )
        self.title_lbl.configure(
            font=("Impact", 25),
            foreground=self._parent_view.COLORS['accent'],
            background="#212121"
        )
        self.title_lbl.grid_configure(pady=(0, 30))

        # Configurazione bottoni
        difficulties = [
            ("FACILE", "#2ECC71"),
            ("MEDIO", "#F1C40F"),
            ("DIFFICILE", "#E74C3C")
        ]

        for i, (text, color) in enumerate(difficulties):
            btn = self.overlay.addButton(
                text=text,
                row=1, column=i,
                command=lambda t=text: self.set_difficulty(t)
            )
            btn.configure(
                font=("Segoe UI", 12, "bold"),
                width=12,
                height=2,
                relief="flat",
                background="#333333",
                foreground=color
            )
            btn.grid_configure(padx=10)

    def set_difficulty(self, difficulty):
        self.overlay.destroy()
        self._controller.handle_selected_difficulty(difficulty)