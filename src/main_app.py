from .models.game import Game
from .views.start_screen import StartScreen
from .views.leaderboard_view import LeaderboardView
from .views.game_view import GameView
from .views.menu import Menu


class MainApp():
    def __init__(self):
        self._nickname = None
        self._difficulty = None
        self.run()


    def run(self):
        """Funzione che avvia il programma"""
        self.show_start_screen()

    def show_menu(self):
        pass

    def show_game(self):
        pass

    def show_leaderboard(self):
        pass

    def show_start_screen(self):
        self.start_screen = StartScreen(self, "Percorso Evolutivo")
        self.start_screen.mainloop()
        self._nickname = self.start_screen.nickname
        self._difficulty = self.start_screen.difficulty

if __name__ == '__main__':
    app = MainApp()