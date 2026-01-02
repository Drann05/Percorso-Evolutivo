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

    def __init__(self, game, title, width=500, height=500):
        super().__init__(title, width, height)
        self.game = game

        self.MAIN_FONT = ("Arial", 12, "bold")
        self.ACCENT_COLOR = "White"
        self.BACKGROUND_COLOR = "Light Blue"

        self.widgets = []
        self.grid_widgets = {}
        self.grid_init(30, 25)
        self.build_ui()

    def style(self, widget):
        widget["font"] = self.MAIN_FONT
        widget["foreground"] = self.ACCENT_COLOR
        widget["background"] = self.BACKGROUND_COLOR

    def build_ui(self):

        menu_bar = self.addMenuBar(row=0, column=0, columnspan=5)
        file_menu = menu_bar.addMenu("File")
        file_menu.addMenuItem("Nuova Partita", command=self.reset_game)
        file_menu.addMenuItem("Esci", command=self.destroy)


        titolo = self.addLabel(text="Percorso Evolutivo", row=1, column=0, columnspan=25)
        self.style(titolo)


        self.draw_grid()


        row_stats = 18
        self.label_score = self.addLabel(text=f"Score: {self.game.player.score}", row=row_stats, column=2)
        self.label_moves = self.addLabel(text=f"Moves: {self.game.player.moves}", row=row_stats, column=11)
        self.label_timer = self.addLabel(text=f"Timer: {self.game.timer}s", row=row_stats, column=20)

        for lbl in [self.label_score, self.label_moves, self.label_timer]:
            self.style(lbl)

        control_panel = self.addPanel(row=20, column=0, columnspan=25)

        self.btn_up = control_panel.addButton(text="▲", row=0, column=1,
                                              command=lambda: self.handle_move("N"))
        self.btn_left = control_panel.addButton(text="◀", row=1, column=0,
                                                command=lambda: self.handle_move("W"))
        self.btn_down = control_panel.addButton(text="▼", row=1, column=1,
                                                command=lambda: self.handle_move("S"))
        self.btn_right = control_panel.addButton(text="▶", row=1, column=2,
                                                 command=lambda: self.handle_move("E"))

        self.special_btn = control_panel.addButton(text="MOSSA SPECIALE", row=1, column=4, command=self.special_move)
        self.special_btn["background"] = "Gold"
        self.special_btn["foreground"] = "Black"

    def draw_grid(self):
        self.grid_size = 20
        self.cell_pixel_size = 30
        canvas_width = self.grid_size * self.cell_pixel_size
        canvas_height = self.grid_size * self.cell_pixel_size

        self.canvas = self.addCanvas(row=2, column=1,
                                     columnspan=23, rowspan=15,
                                     width=canvas_width,
                                     height=canvas_height)
        self.canvas["background"] = "white"

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_pixel_size
                y1 = row * self.cell_pixel_size
                x2 = x1 + self.cell_pixel_size
                y2 = y1 + self.cell_pixel_size

                cell_data = self.game.grid.get_cell_view_data((row, col))
                color = self.CELL_COLORS[cell_data["type"]]

                self.grid_widgets[(row, col)]=self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

            """ 
            p_row, p_col = self._position
    
            cx1 = p_col * self.cell_pixel_size + 5  # margine di 5px
            cy1 = p_row * self.cell_pixel_size + 5
            cx2 = cx1 + self.cell_pixel_size - 10
            cy2 = cy1 + self.cell_pixel_size - 10
    
            self.canvas.drawOval(cx1, cy1, cx2, cy2, fill=self.PLAYER_COLOR, outline="white")
            """


    def handle_move(self, direction):
        """sposta il giocatore"""
        old_pos = self.player._position
        new_row, new_col = old_pos

        if direction == "N":
            new_row -= 1
        elif direction == "S":
            new_row += 1
        elif direction == "E":
            new_col += 1
        elif direction == "W":
            new_col -= 1

        if self.grid_logic.is_valid_movement((new_row, new_col)):
            self.player.move_to(direction)

            self.draw_grid()
            self.update_stats()

    def special_move(self):
        """Esegue la mossa speciale."""
        print("Mossa Speciale Attivata!")

    def update_stats(self):
        """Aggiorna i testi delle label a video."""
        pass

    def reset_game(self):
        pass