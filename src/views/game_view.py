from .views import Views

class GameView(Views):
    def __init__(self, parent):
        self._parent = parent
        self.labels_grid = {}
        super().__init__(title="Percorso Evolutivo", width=700, height=850)

    def build_ui(self):
        """Costruisce la griglia e i controlli"""
        self.header=self.addPanel(row=0, column=0, columnspan=4)
        self.lbl_points= self.create_label(self.header, "Points:", 0, 0)

        self.grid_panel=self.addPanel(row=1, column=0, columnspan=4)
        self.create_grid_view()

        self.addButton(text="↑", row=2, column=1,
                        command = lambda: self.handle_events("move", direction = "up"))

    def create_grid_view(self):
       pass

    def handle_events(self, event_type, **kwargs):
        if event_type == "move":
            direction = kwargs.get("direction")
            self.game.move_player(direction)

        elif event_type == "special":
            r, c = kwargs.get("row"), kwargs.get("col")
            self.game.special_move(r, c)

        self.update_view()

    def update(self):
        self.lbl_points["text"] = f"Points: {len(self.game.points)}"