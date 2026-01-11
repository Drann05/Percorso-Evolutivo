class DifficultyDialog:
    def __init__(self, parent_view, controller):
        self._parent_view = parent_view
        self._controller = controller
        self.build_ui()

        self._parent_view.bind("<Configure>", self.on_resize)

    def build_ui(self):
        self.overlay = self._parent_view.addPanel(row=1, column=0, background="#212121")

        self.buttons = []

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
            self.buttons.append(btn)


    def on_resize(self, event):
        padx = max(20, event.width // 5)
        pady = max(20, event.height // 5)

        self.overlay.grid_configure(padx=padx, pady=pady)

        new_header_size = max(18, event.width // 35)
        new_btn_size = max(10, event.width // 60)

        self.title_lbl.configure(font=("Impact", new_header_size))

        for btn in self.buttons:
            btn.configure(font=("Segoe UI", new_btn_size, "bold"))

    def set_difficulty(self, difficulty):
        self._parent_view.unbind("<Configure>")
        self.overlay.destroy()
        self._controller.handle_selected_difficulty(difficulty)