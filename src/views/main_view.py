from breezypythongui import EasyFrame, EasyCanvas

from .leaderboard_view import LeaderboardView
from .start_screen import StartScreen
from .game_instructions import GameInstructions
from .difficulty_dialog import DifficultyDialog
from .game_view import GameView



class MainView(EasyFrame):
    COLORS = {
        "bg": "#121212",
        "accent": "#00ADB5",
        "text": "#EEEEEE",
        "error": "#FF3131",
        "panel_bg": "#1A1A1A"
    }

    COLORS = {
        "bg": "#121212",  # Same dark background as GameView
        "accent": "#00ADB5",  # Neon Teal (Mint)
        "text": "#EEEEEE",  # Off-white text
        "error": "#FF3131",  # Red matching your timer color
        "panel_bg": "#1A1A1A"  # Slightly lighter dark for panels
    }

    def __init__(self, controller, title="Percorso Evolutivo"):
        super().__init__(title=title, width=500, height=500)
        self._title = title
        self.controller = controller

        self.SCREENS = [self.show_start_screen, self.show_game, self.show_leaderboard, self.show_instructions,
                        self.show_menu_bar]

        self.start_screen = None
        self.game_view = None
        self.game_instructions = None
        self.leaderboard_view = None

        self.current_screen = None
        self.came_from = None

        self.change_screen(self.show_start_screen)

    def change_screen(self, screen, *args):
        """Centralizza il cambio della finestra, salvando la finestra
        che viene prima"""
        if screen not in self.SCREENS:
            raise ValueError("funzione non valida")

        self.came_from = self.current_screen
        self.clear()
        screen(*args)
        self.current_screen = screen

    def show_start_screen(self):
        self.clear()
        self.start_screen = StartScreen(self, self.controller, self._title)
        self.current_screen = self.start_screen

    def show_difficulty_dialog(self):
        dialog = DifficultyDialog(self, self.controller)

    def show_game(self):
        self.clear()

        self.game_view = GameView(self, self.controller, self._title)
        self.after(2000, self.update_timer)

    def show_instructions(self):
        self.clear()
        self.game_instructions = GameInstructions(self, self._title, self.controller)

    def show_leaderboard(self, scores):
        self.leaderboard_view = LeaderboardView(self, self.controller, self._title, scores)

    def exit_game(self):
        self.quit()
        self.after(20, quit)

    def show_menu_bar(self):
        menu_bar = self.addMenuBar(row=0, column=0, columnspan=5)
        file_menu = menu_bar.addMenu("Menu")
        file_menu.addMenuItem("Nuova Partita", command=self.controller.handle_restart_game_request)
        file_menu.addMenuItem("Esci", command=self.exit_game)
        file_menu.addMenuItem("Istruzioni", command=self.show_instructions)
        file_menu.addMenuItem("Classifica", command=self.show_leaderboard)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

        for i in range(21):
            self.columnconfigure(i, weight=0)
            self.rowconfigure(i, weight=0)

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

    def update_timer(self):
        if not self.game_view:
            return
        timer = self.controller.update_timer()
        self.game_view.update_timer(timer)
        self.after(1000, self.update_timer)

    def show_error(self):
        pass

    def go_back(self):
        pass