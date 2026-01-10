from .views import Views
from breezypythongui import EasyFrame
import tkinter as tk


class GameView(Views):

    # Colori griglia
    CELL_COLORS = {
        'X': "#1A1A1A",
        'R': "#F1C40F",
        'T': "#E74C3C",
        'O': "#2ECC71",
        '.': "#2C3E50",
        'P': "#3498DB"
    }
    PLAYER_COLOR = "#E91E63"
    SPECIAL_USED_COLOR = "#555555"

    def __init__(self, parent_view, controller, title, width=1000, height=800):
        super().__init__(title, width, height)
        self._controller = controller
        self._parent_view = parent_view
        self._parent_view.setBackground(self._parent_view.COLORS['bg'])

        self.game_state = self._controller.get_game_state()

        self.rects = {}
        self.player_display_id = None
        self.cell_size = 30

        self.setup_menu()
        self.build_ui()
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Double-Button-1>", self.handle_double_click)

    def build_ui(self):
        self._setup_layout()
        self._setup_title()
        self._setup_canvas()
        self._setup_hud()

    def _setup_layout(self):

        self._parent_view.master.rowconfigure(0, weight=1)
        self._parent_view.master.columnconfigure(0, weight=1)

    def _setup_title(self):
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
        self.canvas = self._parent_view.addCanvas(row=1, column=0)
        self.canvas.configure(background="#1A1A1A", highlightthickness=0)
        self.canvas.grid_configure(sticky="NSEW", padx=20, pady=(10, 5))

    def _setup_hud(self):
        """Crea il panel per i comandi e le statistiche di gioco"""
        self.hud_panel = self._parent_view.addPanel(row=2, column=0, background=self._parent_view.COLORS['bg'])
        self.hud_panel.grid_configure(sticky="EW")

        # Configurazione colonne
        self.hud_panel.columnconfigure(0, weight=1, uniform="group1")
        self.hud_panel.columnconfigure(1, weight=0)
        self.hud_panel.columnconfigure(2, weight=1, uniform="group1")

        # Stats
        self.stats_pnl = self.hud_panel.addPanel(row=0, column=0, background=self._parent_view.COLORS['bg'])
        self.stats_pnl.grid_configure(sticky="W", padx=60)


        self.lbl_score = self.stats_pnl.addLabel("SCORE: 0", row=0, column=0, sticky="W")
        self.lbl_moves = self.stats_pnl.addLabel("MOVES: 0", row=1, column=0, sticky="W")
        self.lbl_timer = self.stats_pnl.addLabel("TIME: 0s", row=2, column=0, sticky="W")

        # Comandi
        self.ctrl_wrapper = self.hud_panel.addPanel(row=0, column=1, background=self._parent_view.COLORS['bg'])
        self.ctrl_wrapper.grid_configure(sticky="")

        btn_s = {
            "font": ("Segoe UI", 14, "bold"),
            "width": 4,
            "background": self._parent_view.COLORS['accent'],
            "foreground": "white",
            "relief": "flat"
        }

        self.ctrl_wrapper.addButton(
            text="▲", row=0, column=1,
            command=lambda: self._controller.handle_movement_request("N")
        ).configure(**btn_s)

        self.ctrl_wrapper.addButton(
            text="◀", row=1, column=0,
            command=lambda: self._controller.handle_movement_request("W")
        ).configure(**btn_s)

        self.ctrl_wrapper.addButton(
            text="▼", row=1, column=1,
            command=lambda: self._controller.handle_movement_request("S")
        ).configure(**btn_s)

        self.ctrl_wrapper.addButton(
            text="▶", row=1, column=2,
            command=lambda: self._controller.handle_movement_request("E")
        ).configure(**btn_s)

        # Abilità
        self.abil_pnl = self.hud_panel.addPanel(row=0, column=2, background=self._parent_view.COLORS['bg'])
        self.abil_pnl.grid_configure(sticky="E", padx=60)
        self.lbl_wall_abil = self.abil_pnl.addLabel("BREAK WALL: READY", row=0, column=0, sticky="E")
        self.lbl_trap_abil = self.abil_pnl.addLabel("CONVERT TRAP: READY", row=1, column=0, sticky="E")

        for lbl in [self.lbl_score, self.lbl_moves, self.lbl_timer, self.lbl_wall_abil, self.lbl_trap_abil]:
            lbl.configure(font=("Consolas", 11, "bold"), background=self._parent_view.COLORS['bg'], foreground=self._parent_view.COLORS['text'])

    def on_resize(self, event):
        """Centra la griglia dopo il resize della finestra"""
        grid_info = self.game_state["grid"]
        self.cell_size = min((event.width - 40) // grid_info["cols"],
                             (event.height - 40) // grid_info["rows"])

        self.refresh_grid_display()
        self.update_player_position_display()

    def refresh_grid_display(self):
        self.canvas.delete("all")
        self.rects = {}

        grid_info = self.game_state["grid"]
        grid_matrix = grid_info["grid"]

        # Centra la griglia nel canvas
        x_off = (self.canvas.winfo_width() - (grid_info["cols"] * self.cell_size)) // 2
        y_off = (self.canvas.winfo_height() - (grid_info["rows"] * self.cell_size)) // 2

        for r in range(grid_info["rows"]):
            for c in range(grid_info["cols"]):
                x1, y1 = x_off + (c * self.cell_size), y_off + (r * self.cell_size)
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                cell_type = grid_matrix[r][c]
                color = self.CELL_COLORS.get(cell_type, "#FFFFFF")

                self.rects[(r, c)] = self.canvas.drawRectangle(
                    x1, y1, x2, y2, fill=color, outline="#121212"
                )

    def screen_flicker(self):
        for rect in self.rects.values():
            self.canvas.itemconfig(rect, stipple="gray50")
        self.canvas.after(200, lambda: [
            self.canvas.itemconfig(r, stipple="") for r in self.rects.values()
        ])

    def draw_player(self):
        """Disegna il giocatore"""
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

            action_success = self._controller.handle_special_action_request(action, (row, col))

            if not action_success:
                self.screen_flicker()

    def setup_menu(self):
        """Crea la menu bar"""
        root = self._parent_view.master
        menubar = tk.Menu(root)

        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Restart Game", command=self._controller.handle_restart_game_request)
        game_menu.add_separator()
        game_menu.add_command(label="Exit to Menu", command=self._controller.init_start_screen)
        game_menu.add_command(label="Quit", command=root.quit)
        menubar.add_cascade(label="Game", menu=game_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to Play",
                              command=lambda: self._parent_view.change_screen(self._parent_view.show_instructions))
        menubar.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menubar)

    def show_game_over(self, won=True):
        """Mostra l'overlay di fine gioco"""


        self.overlay = self._parent_view.addPanel(row=1, column=0, background=self._parent_view.COLORS['bg'])

        self.overlay.grid_configure(padx=100, pady=100)

        # Colore e Testo in base al risultato
        title_text = "VITTORIA!" if won else "GAME OVER"
        title_color = self._parent_view.COLORS['accent'] if won else "#FF3131" # rosso


        # Titolo dell'overlay
        label_title = self.overlay.addLabel(text=title_text, row=0, column=0)
        label_title.configure(font=("Impact", 48), foreground=title_color, background=self._parent_view.COLORS['bg'])
        label_title.grid_configure(sticky="")

        # Statistiche finali
        stats = self.game_state["stats"]
        final_info = f"Punteggio Finale: {stats['score']} | Mosse: {stats['moves']}"
        label_info = self.overlay.addLabel(text=final_info, row=1, column=0)
        label_info.configure(font=("Consolas", 14), foreground="white", background=self._parent_view.COLORS['bg'])

        # Pulsanti di azione
        button_panel = self.overlay.addPanel(row=2, column=0, background=self._parent_view.COLORS['bg'])

        button_restart = button_panel.addButton(text="Riprova", row=0, column=0,
                                          command=self._controller.handle_restart_game_request)
        button_menu = button_panel.addButton(text="Menu Principale", row=0, column=1,
                                       command=lambda: self._parent_view.change_screen(self._parent_view.show_start_screen))

        # Stile pulsanti
        for button in [button_restart, button_menu]:
            button.configure(font=("Segoe UI", 12, "bold"), width=15, relief="flat",
                          background="#333333", foreground="white")
            button.grid_configure(padx=10, pady=20)

    def show_menu_bar(self):
        menu_bar = self._parent_view.addMenuBar(row=0, column=0, columnspan=5)
        file_menu = menu_bar.addMenu("Menu")
        file_menu.addMenuItem("Nuova Partita", command=self._parent_view.controller.handle_restart_game_request)
        file_menu.addMenuItem("Esci", command=self._parent_view.exit_game)
        file_menu.addMenuItem("Istruzioni", command=self._parent_view.show_instructions)
        file_menu.addMenuItem("Classifica", command=self._parent_view.show_leaderboard)

    def update_special_labels(self, specials):
        def style(lbl, ready):
            lbl.configure(
                foreground=self._parent_view.COLORS['accent'] if ready else self.SPECIAL_USED_COLOR,
                text=f"{lbl.cget('text').split(':')[0]}: {'READY' if ready else 'USED'}"
            )

        style(self.lbl_wall_abil, specials["remove_wall"])
        style(self.lbl_trap_abil, specials["convert_trap"])

    def update_stats(self):
        stats = self.game_state["stats"]
        self.lbl_score["text"] = f"Score: {stats['score']}"
        self.lbl_moves["text"] = f"Moves: {stats['moves']}"

    def update_timer(self, timer):
        if hasattr(self, 'lbl_timer') and self.lbl_timer.winfo_exists():
            display_time = timer if timer is not None else 0
            self.lbl_timer["text"] = f"TIME: {display_time}s"

            specials = self.game_state.get("special_moves", {"remove_wall": False, "convert_trap": False})
            self.update_special_labels(specials)

    def reset_game(self):
        pass

    def update_cell_display(self, position):
        """serve a modificare la cella su cui il giocatore si sposta nella view"""
        x, y = position
        cell_type = self.game_state["grid"][x][y]
        new_color = self.CELL_COLORS[cell_type]
        self.canvas.itemconfig(self.rects[(x,y)], fill=new_color)

    def update_player_position_display(self):
        self.canvas.delete(self.player_display_id)
        self.player_display_id = self.draw_player()

    def update_game_view(self, new_state=None):
        if new_state:
            self.game_state = new_state

        self.refresh_grid_display()

        self.update_player_position_display()

        self.update_stats()

    def set_game_state(self, game_state):
        self.game_state = game_state