from .views import Views

class GameView(Views):
    def __init__(self, parent, title, width, height, nickname, difficulty):
        super().__init__(title, width, height)
        self.parent = parent
        self.nickname = nickname
        self.difficulty = difficulty
        self.player = Player()

        self.grid_logic = Grid(20, 20)
        self.grid_logic.generate_grid(self.difficulty)

        self.COLORS = {
            'X': "black",
            'R': "green",
            'T': "red",
            'O': "yellow",
            '.': "white",
            'P': "blue"
        }

        self.score = 0
        self.moves = 20
        self.timer = 60

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

        self.game_box = self.addPanel(row=2, column=1, columnspan=23, rowspan=15)
        self.game_box["background"] = "black"

        row_stats = 18
        self.label_score = self.addLabel(text=f"Score: {self.score}", row=row_stats, column=2)
        self.label_moves = self.addLabel(text=f"Moves: {self.moves}", row=row_stats, column=11)
        self.label_timer = self.addLabel(text=f"Timer: {self.timer}s", row=row_stats, column=20)

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

    def generate_grid_view(self):
        for row in range(20):
            for col in range(20):
                cell_type = self.grid_logic.get_cell((row, col))
                color = self.COLORS.get(cell_type, "white")           #label per ogni cella della griglia

                lbl = self.game_box.addLabel(text=" ", row=row, column=col,
                                             sticky="NSEW")
                lbl["background"] = color
                lbl["width"] = 2  # rende le celle quadrate

                self.grid_widgets[(row, col)] = lbl

    def update_grid_display(self):
        """sincronizza la GUI con lo stato attuale della griglia."""
        for row in range(self.grid_logic._height):
            for col in range(self.grid_logic._width):
                cell_type = self.grid_logic.get_cell((row, col))

                color = Cell.CELL_TYPES.get(cell_type, "white")

                self.grid_widgets[(row, col)]["background"] = color

    def handle_move(self, direction):
        # recupera la posizione precedente, prima del movimento
        old_pos = (self.player.get_row(), self.player.get_col())

        self.player.move_to(direction)

        # recupera la nuova posizione
        new_pos = (self.player.get_row(), self.player.get_col())

        self.grid_logic.set_cell(old_pos, '.')
        self.grid_logic.set_cell(new_pos, 'P')

        self.update_grid_display()
        self.update_stats()

    def special_move(self):
        """Esegue la mossa speciale."""
        print("Mossa Speciale Attivata!")

    def update_stats(self):
        """Aggiorna i testi delle label a video."""
        pass

    def reset_game(self):
        pass