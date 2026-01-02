from .models.game import Game
from .views.start_screen import StartScreen
from .views.leaderboard_view import LeaderboardView
from .views.game_view import GameView
from .views.menu import Menu
from breezypythongui import EasyFrame

class MainApp():
    def __init__(self):
        pass
        #self.leaderboard = LeaderboardView(self)
        #self.start_screen = StartScreen(self)
        #self.game_view = GameView(self)
        #self.menu = Menu(self)

    def run(self):
        """Funzione che avvia il programma"""
        self.show_start_screen()
        self._widget = []

    def show_menu(self):
        pass

    def show_game(self):
        pass

    def show_leaderboard(self):
        pass

    def show_start_screen(self):
        pass

if __name__ == '__main__':
    app = MainApp()