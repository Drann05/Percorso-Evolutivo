from .views import Views

class GameView(Views):
    CELL_COLORS = {
        'X': "black",
        'R': "yellow",
        'T': "red",
        'O': "green",
        '.': "white",
        'P': "blue"
    }
    PLAYER_COLOR = "Pink"
    CELL_PIXEL_SIZE = 30

    def __init__(self, parent_view, controller, title, width=500, height=500):
        super().__init__(title, width, height)
        self._controller = controller
        self._parent_view = parent_view

        # --- Inizializzazione Interfaccia ---
        self.MAIN_FONT = ("Arial", 12, "bold")
        self.ACCENT_COLOR = "White"
        self.BACKGROUND_COLOR = "Light Blue"

        self.widgets = []
        self._parent_view.grid_init(30, 25)

        self.player_display_id = None

        self.game_state = self._controller.get_game_state()

        # --- Statistiche di Gioco ---
        self.label_score = None
        self.label_moves = None
        self.label_timer = None

        # --- Pulsanti Giocatore ---
        self.btn_up = None
        self.btn_left = None
        self.btn_down = None
        self.btn_right = None

        self.special_move_btn = None

        # --- Canvas ---
        self.rects = {}
        self.canvas = None


        # Costruzione UI
        self.build_ui()

    def style(self, widget):
        widget["font"] = self.MAIN_FONT
        widget["foreground"] = self.ACCENT_COLOR
        widget["background"] = self.BACKGROUND_COLOR

    def build_ui(self):

        menu_bar = self._parent_view.addMenuBar(row=0, column=0, columnspan=5)
        file_menu = menu_bar.addMenu("File")
        file_menu.addMenuItem("Nuova Partita", command=self._controller.handle_restart_game_request)
        file_menu.addMenuItem("Esci", command=self._parent_view.quit)


        titolo = self._parent_view.addLabel(text="Percorso Evolutivo", row=1, column=0, columnspan=25)
        self.style(titolo)


        self.draw_grid()
        self.player_display_id=self.draw_player()

        stats = self.game_state["stats"]
        row_stats = 18
        self.label_score = self._parent_view.addLabel(text=f"Score: {stats['score']}", row=row_stats, column=2)
        self.label_moves = self._parent_view.addLabel(text=f"Moves: {stats['moves']}", row=row_stats, column=11)
        self.label_timer = self._parent_view.addLabel(text=f"Timer: {stats['timer']}s", row=row_stats, column=20)

        for lbl in [self.label_score, self.label_moves, self.label_timer]:
            self.style(lbl)

        control_panel = self._parent_view.addPanel(row=20, column=0, columnspan=25)

        self.btn_up = control_panel.addButton(text="▲", row=0, column=1,
                                              command=lambda: self._controller.handle_movement_request("N"))
        self.btn_left = control_panel.addButton(text="◀", row=1, column=0,
                                                command=lambda: self._controller.handle_movement_request("W"))
        self.btn_down = control_panel.addButton(text="▼", row=1, column=1,
                                                command=lambda: self._controller.handle_movement_request("S"))
        self.btn_right = control_panel.addButton(text="▶", row=1, column=2,
                                                 command=lambda: self._controller.handle_movement_request("E"))


    def draw_grid(self):
        grid_info = self.game_state["grid"]
        grid_matrix = grid_info["grid"]

        rows, cols = grid_info["rows"], grid_info["cols"]
        canvas_width = cols * self.CELL_PIXEL_SIZE
        canvas_height = rows * self.CELL_PIXEL_SIZE
        self.canvas = self._parent_view.addCanvas(row=2, column=1,
                                     columnspan=25, rowspan=15,
                                     width=canvas_width,
                                     height=canvas_height
                                     )
        self.canvas.grid_configure(sticky="")
        self.canvas["background"] = "white"

        for row in range(rows):
            for col in range(cols):
                x1 = col * self.CELL_PIXEL_SIZE
                y1 = row * self.CELL_PIXEL_SIZE
                x2 = x1 + self.CELL_PIXEL_SIZE
                y2 = y1 + self.CELL_PIXEL_SIZE

                cell_type = grid_matrix[row][col]
                color = self.CELL_COLORS[cell_type]

                self.rects[(row, col)]=self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def draw_player(self):
        p_row, p_col = self.game_state["player_position"]

        cx1 = p_col * self.CELL_PIXEL_SIZE + 5  # margine di 5px
        cy1 = p_row * self.CELL_PIXEL_SIZE + 5
        cx2 = cx1 + self.CELL_PIXEL_SIZE - 10
        cy2 = cy1 + self.CELL_PIXEL_SIZE - 10

        return self.canvas.drawOval(cx1, cy1, cx2, cy2, fill=self.PLAYER_COLOR, outline="white")

    def update_stats(self):
        stats = self.game_state["stats"]
        self.label_score["text"] = f"Score: {stats['score']}"
        self.label_moves["text"] = f"Moves: {stats['moves']}"
        self.label_timer["text"] = f"Timer: {stats['timer']}s"

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

    def update_game_view(self):
        self.update_player_position_display()
        self.refresh_grid_display()
        self.update_stats()

    def refresh_grid_display(self):
        grid_info = self.game_state["grid"]
        grid_matrix = grid_info["grid"]

        for row in range(grid_info["rows"]):
            for col in range(grid_info["cols"]):
                cell_type = grid_matrix[row][col]
                color = self.CELL_COLORS[cell_type]

                self.canvas.itemconfig(self.rects[(row, col)], fill=color)

