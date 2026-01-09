from .views import Views
import tkinter as tk


class GameView(Views):
    # Colori
    BG_COLOR = "#121212"
    ACCENT_COLOR = "#00ADB5"
    TEXT_COLOR = "#EEEEEE"
    USED_COLOR = "#555555"

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

    def __init__(self, parent_view, controller, title, width=1000, height=800):
        super().__init__(title, width, height)
        self._controller = controller
        self._parent_view = parent_view
        self._parent_view.setBackground(self.BG_COLOR)

        self._parent_view.grid_init(30, 30)
        self.game_state = self._controller.get_game_state()

        self.rects = {}
        self.player_display_id = None
        self.cell_size = 30

        self.setup_menu()
        self.build_ui()
        self.canvas.bind("<Configure>", self.on_resize)

    def build_ui(self):
        # Titolo
        self.header_panel = self._parent_view.addPanel(row=0, column=0, columnspan=30, background=self.BG_COLOR)

        self.title_lbl = self.header_panel.addLabel(
            "P E R C O R S O  E V O L U T I V O",
            row=0, column=0, sticky="NSEW"
        )

        self.title_lbl.configure(
            font=("Impact", 32),
            foreground=self.ACCENT_COLOR,
            background=self.BG_COLOR,
            padx=20, pady=20
        )

        # Canvas
        self.canvas = self._parent_view.addCanvas(row=3, column=5, columnspan=20, rowspan=15)
        self.canvas.configure(background="#1A1A1A", highlightthickness=0)
        self.canvas.grid_configure(sticky="NSEW")
        self.canvas.bind("<Double-Button-1>", self.handle_double_click)

        # HUD
        self.setup_hud()

    def setup_hud(self):
        """Crea il panel per i comandi e le statistiche di gioco"""
        self.hud_panel = self._parent_view.addPanel(row=22, column=2, columnspan=26, background=self.BG_COLOR)

        # Stats
        self.stats_pnl = self.hud_panel.addPanel(row=0, column=0, background=self.BG_COLOR)
        self.lbl_score = self.stats_pnl.addLabel("SCORE: 0", row=0, column=0, sticky="W")
        self.lbl_moves = self.stats_pnl.addLabel("MOVES: 0", row=1, column=0, sticky="W")
        self.lbl_timer = self.stats_pnl.addLabel("TIME: 0s", row=2, column=0, sticky="W")

        # Comandi
        self.ctrl_pnl = self.hud_panel.addPanel(row=0, column=1, background=self.BG_COLOR)
        btn_s = {"font": ("Segoe UI", 12, "bold"), "width": 3, "background": self.ACCENT_COLOR, "foreground": "white"}
        self.ctrl_pnl.addButton(text="▲", row=0, column=1,
                                command=lambda: self._controller.handle_movement_request("N")).configure(**btn_s)
        self.ctrl_pnl.addButton(text="◀", row=1, column=0,
                                command=lambda: self._controller.handle_movement_request("W")).configure(**btn_s)
        self.ctrl_pnl.addButton(text="▼", row=1, column=1,
                                command=lambda: self._controller.handle_movement_request("S")).configure(**btn_s)
        self.ctrl_pnl.addButton(text="▶", row=1, column=2,
                                command=lambda: self._controller.handle_movement_request("E")).configure(**btn_s)

        # Abilitià
        self.abil_pnl = self.hud_panel.addPanel(row=0, column=2, background=self.BG_COLOR)
        self.lbl_wall_abil = self.abil_pnl.addLabel("BREAK WALL: READY", row=0, column=0, sticky="E")
        self.lbl_trap_abil = self.abil_pnl.addLabel("CONVERT TRAP: READY", row=1, column=0, sticky="E")

        for lbl in [self.lbl_score, self.lbl_moves, self.lbl_timer, self.lbl_wall_abil, self.lbl_trap_abil]:
            lbl.configure(font=("Consolas", 11, "bold"), background=self.BG_COLOR, foreground=self.TEXT_COLOR)

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

                self.rects[(r, c)] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="#121212"
                )
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

            if action:
                self.flash_cell(row, col, self.ACCENT_COLOR)
                self._controller.handle_special_action_request(action, (row, col))
            else:
                self.flash_cell(row, col, "#d11a02")

    def flash_cell(self, row, col, color, duration=150):
        rect = self.rects.get((row, col))
        if not rect:
            return

        original = self.canvas.itemcget(rect, "fill")
        self.canvas.itemconfig(rect, fill=color)
        self.canvas.after(duration, lambda: self.canvas.itemconfig(rect, fill=original))

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

    def update_special_labels(self, specials):
        def style(lbl, ready):
            lbl.configure(
                foreground=self.ACCENT_COLOR if ready else self.USED_COLOR,
                text=f"{lbl.cget('text').split(':')[0]}: {'READY' if ready else 'USED'}"
            )

        style(self.lbl_wall_abil, specials["remove_wall"])
        style(self.lbl_trap_abil, specials["convert_trap"])

    def update_stats(self):
        stats = self.game_state["stats"]
        self.lbl_score["text"] = f"Score: {stats['score']}"
        self.lbl_moves["text"] = f"Moves: {stats['moves']}"

    def update_timer(self, timer):
        self.lbl_timer["text"] = f"Timer: {timer}s"

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