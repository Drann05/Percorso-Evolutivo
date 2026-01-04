from breezypythongui import EasyFrame, EasyCanvas
from .start_screen import StartScreen
from .leaderboard_view import LeaderboardView
from .game_view import GameView
from .menu import Menu

class MainView(EasyFrame):
    def __init__(self, controller, title="Percorso Evolutivo"):
        super().__init__(title=title, width=500, height=500)
        self._title = title
        self.controller = controller
        self.start_screen = None
        self.widgets = []

        self.show_start_screen()

    def show_start_screen(self):
        self.clear()
        self.start_screen = StartScreen(self, self.controller, self._title)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def grid_init(self, row, column):
        for r in range(row):
            self.rowconfigure(r, weight=1)
        for c in range(column):
            self.columnconfigure(c, weight=1)
