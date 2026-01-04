from .models.game import Game
from .views.start_screen import StartScreen
from .views.leaderboard_view import LeaderboardView
from .views.game_view import GameView
from .views.menu import Menu


class MainApp():
    def __init__(self):
        self.show_game()

    def run(self):
        """Funzione che avvia il programma"""
        self.show_start_screen()
        self._widget = []

    def show_menu(self):
        pass

    def show_game(self):
        self.game = Game("Gioele", "facile")
        self.game.start_game()
        self.game_view = GameView(self.game,"Percorso Evolutivo")
        self.game_view.mainloop()

    def show_leaderboard(self):
        pass

    def show_start_screen(self):
        pass
    
if __name__ == '__main__':
    app = MainApp()