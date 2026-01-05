from breezypythongui import EasyFrame, EasyCanvas
from .start_screen import StartScreen
from .difficulty_dialog import DifficultyDialog
from .game_view import GameView

class MainView(EasyFrame):
    def __init__(self, controller, title="Percorso Evolutivo"):
        super().__init__(title=title, width=500, height=500)
        self._title = title
        self.controller = controller
        self.start_screen = None
        self.game_view = None

        self.show_start_screen()

    def show_start_screen(self):
        self.clear()
        self.start_screen = StartScreen(self, self.controller, self._title)

    def show_difficulty_dialog(self):
        dialog = DifficultyDialog(self, self.controller)

    def show_game(self):
        self.clear()
        self.game_view = GameView(self, self.controller, self._title)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def grid_init(self, row, column):
        for r in range(row):
            self.rowconfigure(r, weight=1)
        for c in range(column):
            self.columnconfigure(c, weight=1)

    def update_game(self, game_state):
        if not self.game_view:
            return
        else:
            self.game_view.set_game_state(game_state)
            self.game_view.update_game_view()

    def show_error(self):
        pass
