from breezypythongui import EasyFrame, EasyCanvas

from .leaderboard_view import LeaderboardView
from .start_screen import StartScreen
from .game_instructions import GameInstructions
from .difficulty_dialog import DifficultyDialog
from .game_view import GameView



class MainView(EasyFrame):
    """Main View agisce come 'container' principale.
    Gestisce lo switch tra le varie finestre e coordina i cicli di aggiornamento della UI"""

    # Costanti estetiche centralizzate
    COLORS = {
        "bg": "#121212",
        "accent": "#00ADB5",
        "text": "#EEEEEE",
        "error": "#FF3131",
        "panel_bg": "#1A1A1A"
    }

    def __init__(self, controller, title="Percorso Evolutivo"):
        super().__init__(title=title, width=500, height=500)
        self._title = title
        self.controller = controller

        self.SCREENS = [self.show_start_screen, self.show_game, self.show_leaderboard, self.show_instructions]

        self.start_screen = None
        self.game_view = None
        self.game_instructions = None
        self.leaderboard_view = None

        self.current_screen = None
        self.came_from = None

        self.change_screen(self.show_start_screen)

    def _clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

        rows, cols = self.grid_size()

        for r in range(rows + 1): self.rowconfigure(r, weight=0)
        for c in range(cols + 1): self.columnconfigure(c, weight=0)

    def change_screen(self, screen, *args):
        """Centralizza il cambio della finestra, salvando la finestra
        che viene prima"""
        if screen not in self.SCREENS:
            raise ValueError("funzione non valida")

        self.came_from = self.current_screen
        self._clear_window()
        screen(*args)
        self.current_screen = screen

    def show_start_screen(self):
        self._clear_window()
        self.start_screen = StartScreen(self, self.controller, self._title)
        self.current_screen = self.start_screen

    def show_difficulty_dialog(self):
        dialog = DifficultyDialog(self, self.controller)


    def show_game(self):

        self.game_view = GameView(self, self.controller, self._title)
        self.after(20, self.update_timer)

    def show_instructions(self):
        self._clear_window()
        self.game_instructions = GameInstructions(self, self.controller, self._title)

    def show_leaderboard(self, scores):
        self.leaderboard_view = LeaderboardView(self, self.controller, self._title, scores)

    def exit_game(self):
        self.quit()
        self.after(20, quit)



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
        if not self.game_view or not self.winfo_exists():
            return

        timer = self.controller.update_timer()

        try:
            self.game_view.update_timer(timer)
            self.after(1000, self.update_timer)
        except Exception:
            pass


    def go_back(self):
        self.change_screen(self.came_from)