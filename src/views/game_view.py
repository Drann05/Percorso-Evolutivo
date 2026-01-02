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

        self.game_box = self.addPanel(row=2, column=1, columnspan=23, rowspan=15)
        self.game_box["background"] = "black"

        self.generate_grid_view()

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

    def generate_grid_view(self):
        rows, cols = self.game.grid.get_grid_dimension()
        for row in range(rows):
            for col in range(cols):
                cell_data = self.game.grid.get_cell_view_data((row, col))
                color = self.CELL_COLORS.get(cell_data["type"])          #label per ogni cella della griglia

                cell_widget = self.game_box.addLabel(text=" ", row=row, column=col,
                                             sticky="NSEW")
                cell_widget["background"] = color
                cell_widget["width"] = 2  # rende le celle quadrate

                self.grid_widgets[(row, col)] = cell_widget


    def update_grid_display(self):
        """sincronizza la GUI con lo stato attuale della griglia."""
        rows, cols = self.game.grid.get_grid_dimension()
        for row in range(rows):
            for col in range(cols):
                cell_data = self.game.grid.get_cell_view_data((row, col))

                color = self.CELL_COLORS.get(cell_data["type"])

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