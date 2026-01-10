from .views import Views


class LeaderboardView(Views):
    BG_COLOR = "#2C3E50"
    ACCENT_COLOR = "#1ABC9C"
    TEXT_COLOR = "#ECF0F1"

    def __init__(self, parent_view, controller, title, scores, width=500, height=600):
        super().__init__(title, width, height)
        self._parent_view = parent_view
        self._controller = controller
        self._scores = scores
        self._setup_layout()
        self.build_ui()

    def style(self, widget, is_header=False, is_top_three=False):
        if is_header:
            widget["font"] = self.TITLE_FONT
            widget["foreground"] = self.ACCENT_COLOR
        elif is_top_three:
            widget["font"] = ("Segoe UI", 11, "bold")
            widget["foreground"] = "#F1C40F"
        else:
            widget["font"] = self.MAIN_FONT
            widget["foreground"] = self.TEXT_COLOR
        widget["background"] = self.BG_COLOR

    def _setup_layout(self):
        self._parent_view.setBackground(self._parent_view.COLORS["bg"])
        self._parent_view.columnconfigure(0, weight=1)
        self._parent_view.rowconfigure(0, weight=1)  # Spazio superiore
        self._parent_view.rowconfigure(2, weight=1)  # Spazio inferiore

    def build_ui(self):

        # --- MAIN CONTAINER ---
        self.main_container = self._parent_view.addPanel(row=0, column=0, background=self._parent_view.COLORS["bg"])
        self.main_container.grid_configure(sticky="")

        # Titolo
        self.title = self.main_container.addLabel(text="Classifica", row=0, column=0)
        self.title.configure(font=("Impact", 32), background=self._parent_view.COLORS["bg"],
                             foreground=self._parent_view.COLORS["accent"])
        self.title.grid_configure(sticky="")

        # --- LEADERBOARD AREA ---
        self._setup_leaderboard()

        close_btn = self.main_container.addButton(
            text="TORNA INDIETRO", row=2, column=0,
            command=self._parent_view.go_back
        )
        close_btn.grid_configure(sticky="", pady=(30, 0))
        close_btn.configure(
            background=self._parent_view.COLORS["accent"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=20
        )

    def _setup_leaderboard(self):

        self.leaderboard_area = self.main_container.addPanel(row=1, column=0, background=self._parent_view.COLORS["panel_bg"])

        self.leaderboard_area.grid_configure(sticky="NSEW", padx=20, pady=20, ipadx=10, ipady=10)

        leaderboard_keys = ['pos', 'Giocatore', 'Punti', 'Mosse', 'Livello']

        # --- HEADER DELLA TABELLA ---
        for i, title in enumerate(leaderboard_keys):
            header = self.leaderboard_area.addLabel(text=title.upper(), row=0, column=i)
            header.configure(
                font=("Consolas", 12, "bold"),
                foreground=self._parent_view.COLORS["accent"],
                background=self._parent_view.COLORS["panel_bg"]
            )
            header.grid_configure(pady=(0, 15), padx=15)

        # --- DATI DEI GIOCATORI ---
        for j, (player, moves, score, difficulty) in enumerate(self._scores, start=1):
            # Colore speciale per i primi 3
            if j == 1:
                color = "#FFD700"  # Oro
            elif j == 2:
                color = "#C0C0C0"  # Argento
            elif j == 3:
                color = "#CD7F32"  # Bronzo
            else:
                color = self._parent_view.COLORS["text"]

            # Font: bold per il podio
            row_font = ("Segoe UI", 11, "bold") if j <= 3 else ("Segoe UI", 11)

            row_data = [f"#{j}", player, moves, score, difficulty]

            for col, text in enumerate(row_data):
                label = self.leaderboard_area.addLabel(text=text, row=j, column=col)
                label.configure(
                    font=row_font,
                    foreground=color,
                    background=self._parent_view.COLORS["panel_bg"]
                )
                # Allinea i nomi (colonna 1) a sinistra ("W"), gli altri al centro
                sticky_value = "W" if col == 1 else ""
                label.grid_configure(sticky=sticky_value, padx=15, pady=5)