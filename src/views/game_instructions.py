from .base_view import BaseView


class GameInstructions(BaseView):

    def __init__(self, parent_view, controller, title):
        # Il super().__init__ gestisce già parent_view, controller e background
        super().__init__(parent_view, controller, title)

    def build_ui(self):
        """Costruisce i componenti dell'interfaccia delle istruzioni"""
        self._setup_title()
        self._setup_text_area()
        self._setup_legend()
        self._setup_navigation()

    def _setup_title(self):
        title_lbl = self._parent_view.addLabel(
            "I S T R U Z I O N I",
            row=0, column=0, sticky="NSEW"
        )
        title_lbl.configure(
            font=("Impact", 32),
            foreground=self._parent_view.COLORS["accent"],
            background=self._parent_view.COLORS["bg"],
            pady=20
        )

    def _setup_text_area(self):
        istruzioni = (
            "> MOVIMENTO: Usa il D-Pad per muoverti all'interno della griglia.\n"
            "> OBIETTIVO (O): Raggiungi l'obiettivo entro il limite di mosse.\n"
            "> RISORSE (R): Raccogli le risorse per aumentare il punteggio.\n"
            "> TRAPPOLE (T): Tolgono punti se calpestate.\n"
            "> MURI (X): Ostacoli distruttibili con mossa speciale.\n"
            "> SPECIALI: Double-click su un muro o trappola per usare le abilità."
        )

        self.txt_area = self._parent_view.addTextArea(
            text=istruzioni, row=1, column=0, width=60, height=8
        )
        self.txt_area.configure(
            font=("Consolas", 11),
            background=self._parent_view.COLORS["panel_bg"],
            foreground=self._parent_view.COLORS["text"],
            padx=20, pady=20, borderwidth=0, relief="flat"
        )
        self.txt_area.grid_configure(padx=40, pady=10, sticky="NSEW")

    def _setup_legend(self):
        # Panel contenitore per la legenda
        legend_pnl = self._parent_view.addPanel(row=2, column=0, background=self._parent_view.COLORS["bg"])

        elementi = [
            ("GIOCATORE", "#E91E63", "oval"),
            ("MURO (X)", "#1A1A1A", "rect"),
            ("RISORSA (R)", "#F1C40F", "rect"),
            ("TRAPPOLA (T)", "#E74C3C", "rect"),
            ("OBIETTIVO (O)", "#2ECC71", "rect")
        ]

        for i, (nome, colore, shape) in enumerate(elementi):
            canvas = legend_pnl.addCanvas(row=i, column=0, width=30, height=30)
            canvas.configure(background=self._parent_view.COLORS["bg"], highlightthickness=0)

            if shape == "rect":
                canvas.create_rectangle(5, 5, 25, 25, fill=colore, outline="gray")
            else:
                canvas.create_oval(5, 5, 25, 25, fill=colore, outline="white", width=2)

            lbl = legend_pnl.addLabel(text=nome, row=i, column=1, sticky="W")
            lbl.configure(
                font=("Consolas", 10, "bold"),
                background=self._parent_view.COLORS["bg"],
                foreground=self._parent_view.COLORS["text"],
                padx=10
            )

    def _setup_navigation(self):
        back_btn = self._parent_view.addButton(
            text="TORNA INDIETRO", row=3, column=0,
            command=self._parent_view.go_back
        )
        back_btn.configure(
            background=self._parent_view.COLORS["accent"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat", width=20
        )
        back_btn.grid_configure(pady=20)
    def on_resize(self, event):
        total_rows = 25
        total_cols = 10
        for i in range(total_rows):
            self._parent_view.rowconfigure(i, weight=1)
        for j in range(total_cols):
            self._parent_view.columnconfigure(j, weight=1)


