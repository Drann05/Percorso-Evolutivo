from .models.game import Game
from .views.main_view import MainView
from .views.start_screen import StartScreen
from .views.leaderboard_view import LeaderboardView
from .views.game_view import GameView
from .views.menu import Menu


class MainApp():
    def __init__(self):

        self.start_screen = None
        self.game = None
        self.game_view = None

        self.main_view = MainView(self)
        self.main_view.mainloop()


    def init_menu(self):
        pass

    def init_game(self):
        pass

    def init_leaderboard(self):
        pass

    def init_start_screen(self):
        self.main_view.show_start_screen()

    
if __name__ == '__main__':
    app = MainApp()