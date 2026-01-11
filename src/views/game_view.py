from .base_view import BaseView
from .restart_dialog import RestartDialog


class GameView(BaseView):
    """
        Classe responsabile della visualizzazione dell'interfaccia di gioco.
        Gestisce la griglia, il giocatore, le statistiche e l'input dell'utente.
        """

     # Colori griglia
    CELL_COLORS = {
        'X': "#1A1A1A",  # Muro
        'R': "#F1C40F",  # Risorsa
        'T': "#E74C3C",  # Trappola
        'O': "#2ECC71",  # Obiettivo
        '.': "#2C3E50",  # Percorso vuoto
        'P': "#3498DB"   # Spawn point
    }
    PLAYER_COLOR = "#E91E63"    # Giocatore
    SPECIAL_USED_COLOR = "#555555"   # Colore per le abilità già utilizzate

    def __init__(self, parent_view, controller, title, width=1000, height=800):

        # Inizializzazione variabili per la gestione grafica
        self.rects = {}
        self.player_display_id = None
        self.cell_size = 30
        self._controller = controller
        self.game_state = self._controller.get_game_state()  # Recupera lo stato iniziale dal controller

        super().__init__(parent_view, controller, title)


        self._parent_view = parent_view
        self._parent_view.setBackground(self._parent_view.COLORS['bg'])


        self._parent_view.setup_menu()


        # Bind degli eventi: resize della finestra e doppio click per abilità speciali
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Double-Button-1>", self.handle_double_click)

    def build_ui(self):
        """Costruisce i componenti principali dell'interfaccia"""
        self._setup_title()
        self._setup_canvas()
        self._setup_hud()

    def _setup_title(self):
        """Crea l'intestazione con il titolo del gioco"""
        self.header_panel = self._parent_view.addPanel(row=0, column=0, background=self._parent_view.COLORS['bg'])
        self.header_panel.grid_configure(sticky="EW")

        self.title_lbl = self.header_panel.addLabel(
            "P E R C O R S O  E V O L U T I V O",
            row=0, column=0, sticky="NSEW"
        )

        self.title_lbl.configure(
            font=("Impact", 32),
            foreground=self._parent_view.COLORS['accent'],
            background=self._parent_view.COLORS['bg'],
            padx=20, pady=20
        )

    def _setup_canvas(self):
        """Inizializza l'area di disegno per la griglia di gioco"""
        self.canvas = self._parent_view.addCanvas(row=1, column=0)
        self.canvas.configure(background="#1A1A1A", highlightthickness=0)
        self.canvas.grid_configure(sticky="NSEW", padx=20, pady=(10, 5))

    def _setup_hud(self):
        """Crea il panel HUD (Heads-Up Display) per statistiche, comandi e abilità"""
        self.hud_panel = self._parent_view.addPanel(row=2, column=0, background=self._parent_view.COLORS['bg'])
        self.hud_panel.grid_configure(sticky="EW")

        # Configurazione colonne
        self.hud_panel.columnconfigure(0, weight=1, uniform="group1")
        self.hud_panel.columnconfigure(1, weight=0)
        self.hud_panel.columnconfigure(2, weight=1, uniform="group1")

        # Stats
        self.stats_pnl = self.hud_panel.addPanel(row=0, column=0, background=self._parent_view.COLORS['bg'])
        self.stats_pnl.grid_configure(sticky="W", padx=60)


        self.lbl_score = self.stats_pnl.addLabel(f"PUNTI: {self.game_state["stats"]["score"]}", row=0, column=0, sticky="W")
        self.lbl_moves = self.stats_pnl.addLabel(f"MOSSE: {self.game_state["stats"]["moves"]}", row=1, column=0, sticky="W")
        self.lbl_timer = self.stats_pnl.addLabel("TEMPO: 0s", row=2, column=0, sticky="W")

        # Comandi
        self.ctrl_wrapper = self.hud_panel.addPanel(row=0, column=1, background=self._parent_view.COLORS['bg'])
        self.ctrl_wrapper.grid_configure(sticky="")

        d_pad_layout = {
            "▲": (0, 1, "N"),
            "◀": (1, 0, "W"),
            "▼": (1, 1, "S"),
            "▶": (1, 2, "E")
        }

        btn_s = {
            "font": ("Segoe UI", 14, "bold"),
            "width": 4,
            "background": self._parent_view.COLORS['accent'],
            "foreground": "white",
            "relief": "flat"
        }

        for icon, (r, c, direction) in d_pad_layout.items():
            btn = self.ctrl_wrapper.addButton(
                text=icon, row=r, column=c,
                command=lambda d=direction: self._controller.handle_movement_request(d)
            )
            btn.configure(**btn_s)

        # Abilità
        self.abil_pnl = self.hud_panel.addPanel(row=0, column=2, background=self._parent_view.COLORS['bg'])
        self.abil_pnl.grid_configure(sticky="E", padx=60)
        self.lbl_wall_abil = self.abil_pnl.addLabel("DISTRUGGI IL MURO: PRONTA", row=0, column=0, sticky="E")
        self.lbl_trap_abil = self.abil_pnl.addLabel("CONVERTI TRAPPOLA: PRONTA", row=1, column=0, sticky="E")

        for lbl in [self.lbl_score, self.lbl_moves, self.lbl_timer, self.lbl_wall_abil, self.lbl_trap_abil]:
            lbl.configure(font=("Consolas", 11, "bold"), background=self._parent_view.COLORS['bg'], foreground=self._parent_view.COLORS['text'])

    def on_resize(self, event):
        """Ricalcola la dimensione delle celle quando la finestra viene ridimensionata"""
        grid_info = self.game_state["grid"]
        self.cell_size = min((event.width - 40) // grid_info["cols"],
                             (event.height - 40) // grid_info["rows"])

        self.refresh_grid_display()
        self.update_player_position_display()

    def refresh_grid_display(self):
        """Ridisegna l'intera griglia di gioco sul Canvas"""
        self.canvas.delete("all")
        self.rects = {}

        grid_info = self.game_state["grid"]
        grid_matrix = grid_info["grid"]

        # Calcola l'offset per centrare la griglia nel canvas
        x_off = (self.canvas.winfo_width() - (grid_info["cols"] * self.cell_size)) // 2
        y_off = (self.canvas.winfo_height() - (grid_info["rows"] * self.cell_size)) // 2

        for r in range(grid_info["rows"]):
            for c in range(grid_info["cols"]):
                x1, y1 = x_off + (c * self.cell_size), y_off + (r * self.cell_size)
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                cell_type = grid_matrix[r][c]
                color = self.CELL_COLORS.get(cell_type, "#FFFFFF")

                # Disegna la cella e salva l'ID per aggiornamenti futuri
                self.rects[(r, c)] = self.canvas.drawRectangle(
                    x1, y1, x2, y2, fill=color, outline="#121212"
                )

    def screen_flicker(self):
        """Effetto visivo immediato per segnalare l'uso di un'abilità in una cella non consentita"""
        for rect in self.rects.values():
            self.canvas.itemconfig(rect, stipple="gray50")
        self.canvas.after(200, self._reset_flicker)

    def _reset_flicker(self):
        """Metodo di supporto per screen_flicker"""
        for rect in self.rects.values():
            self.canvas.itemconfig(rect, stipple="")

    def draw_player(self):
        """Crea l'oggetto grafico che rappresenta il giocatore"""
        row, col = self.game_state["player_position"]
        grid_info = self.game_state["grid"]

        x_off = (self.canvas.winfo_width() - (grid_info["cols"] * self.cell_size)) // 2
        y_off = (self.canvas.winfo_height() - (grid_info["rows"] * self.cell_size)) // 2

        padding = self.cell_size // 6
        x1 = x_off + (col * self.cell_size) + padding
        y1 = y_off + (row * self.cell_size) + padding
        x2 = x1 + self.cell_size - (padding * 2)
        y2 = y1 + self.cell_size - (padding * 2)

        return self.canvas.create_oval(x1, y1, x2, y2, fill=self.PLAYER_COLOR, outline="white", width=2)

    def handle_double_click(self, event):
        """Gestisce il doppio click per le mosse speciali"""
        grid_info = self.game_state["grid"]

        x_off = (self.canvas.winfo_width() - (grid_info["cols"] * self.cell_size)) // 2
        y_off = (self.canvas.winfo_height() - (grid_info["rows"] * self.cell_size)) // 2

        relative_x = event.x - x_off
        relative_y = event.y - y_off

        col = relative_x // self.cell_size
        row = relative_y // self.cell_size

        if 0 <= row < grid_info["rows"] and 0 <= col < grid_info["cols"]:
            cell_type = grid_info["grid"][row][col]

            action = None
            if cell_type == 'X':
                action = "remove_wall"
            elif cell_type == 'T':
                action = "convert_trap"
            print(action)
            action_success = self._controller.handle_special_action_request(action, (row, col))

            if not action_success:
                self.screen_flicker()



    def display_game_over(self, won: bool = True, reason: str = ""):
        """Mostra una schermata (overlay) di fine partita con i risultati"""
        self.overlay = self._parent_view.addPanel(row=1, column=0, background=self._parent_view.COLORS['bg'])
        self.overlay.grid_configure(padx=100, pady=100)

        title_text = "VITTORIA!" if won else "GAME OVER"
        title_color = self._parent_view.COLORS['accent'] if won else "#FF3131"

        label_title = self.overlay.addLabel(text=title_text, row=0, column=0)
        label_title.configure(font=("Impact", 48), foreground=title_color, background=self._parent_view.COLORS['bg'])
        label_title.grid_configure(pady=(0, 10))

        if reason:
            label_reason = self.overlay.addLabel(text=reason.upper(), row=1, column=0)
            label_reason.configure(
                font=("Consolas", 12, "bold"),
                foreground="#FFD700",
                background=self._parent_view.COLORS['bg']
            )
            label_reason.grid_configure(pady=(0, 20))

        # Statistiche finali
        stats = self.game_state["stats"]
        final_info = f"Punteggio Finale: {stats['score']} | Mosse: {stats['moves']}"
        label_info = self.overlay.addLabel(text=final_info, row=2, column=0)
        label_info.configure(font=("Consolas", 14), foreground="white", background=self._parent_view.COLORS['bg'])

        # Panel pulsanti
        button_panel = self.overlay.addPanel(row=3, column=0, background=self._parent_view.COLORS['bg'])
        button_restart = button_panel.addButton(text="Riprova", row=0, column=0,
                                                command=lambda: self._controller.handle_game_over_buttons("restart"))

        button_menu = button_panel.addButton(text="Menu Principale", row=0, column=1,
                                             command=lambda: self._controller.handle_game_over_buttons("menu"))

        # Stile pulsanti
        for button in [button_restart, button_menu]:
            button.configure(font=("Segoe UI", 12, "bold"), width=15, relief="flat",
                          background="#333333", foreground="white")
            button.grid_configure(padx=10, pady=20)

    def update_special_labels(self, specials: dict[str, int]):
        """Aggiorna visivamente lo stato delle abilità speciali"""
        def style(lbl, ready):
            lbl.configure(
                foreground=self._parent_view.COLORS['accent'] if ready else self.SPECIAL_USED_COLOR,
                text=f"{lbl.cget('text').split(':')[0]}: {'PRONTA' if ready else 'USATA'}"
            )

        style(self.lbl_wall_abil, specials["remove_wall_count"])
        style(self.lbl_trap_abil, specials["convert_trap_count"])

    def update_stats(self):
        """Aggiorna Score e Moves nell'HUD"""
        stats = self.game_state["stats"]
        self.lbl_score["text"] = f"Punti: {stats['score']}"
        self.lbl_moves["text"] = f"Mosse: {stats['moves']}"

    def update_timer(self, timer: int):
        """Aggiorna il timer nell'interfaccia"""
        if hasattr(self, 'lbl_timer') and self.lbl_timer.winfo_exists():
            display_time = timer if timer is not None else 0
            self.lbl_timer["text"] = f"TEMPO: {display_time}s"

            specials = self.game_state.get("special_moves", {"remove_wall_count": 0, "convert_trap_count": 0})
            self.update_special_labels(specials)

    def update_cell_display(self, position: tuple[int, int]):
        """serve a modificare la cella su cui il giocatore si sposta nella view"""
        x, y = position
        cell_type = self.game_state["grid"][x][y]
        new_color = self.CELL_COLORS[cell_type]
        self.canvas.itemconfig(self.rects[(x,y)], fill=new_color)

    def update_player_position_display(self):
        """Sposta il giocatore cancellando il vecchio e disegnando il nuovo"""
        self.canvas.delete(self.player_display_id)
        self.player_display_id = self.draw_player()

    def update_game_view(self, new_state: dict =None):
        """Metodo principale per il refresh completo della view"""
        if new_state:
            self.game_state = new_state

        self.refresh_grid_display()

        self.update_player_position_display()

        self.update_stats()

    def set_game_state(self, game_state: dict):
        """Aggiorna il riferimento allo stato del gioco"""
        self.game_state = game_state
