from .models.game import Game
from .views.main_view import MainView
from .views.start_screen import StartScreen
from .views.leaderboard_view import LeaderboardView
from .views.game_view import GameView
from .views.menu import Menu


class Controller:
    def __init__(self):

        self._start_screen = None
        self.game = None
        self._game_view = None

        self._main_view = MainView(self)
        self._main_view.mainloop()


    def init_menu(self):
        pass

    def init_game(self):
        nickname = self._main_view.start_screen.nickname
        difficulty = self._main_view.start_screen.difficulty
        self.game = Game(nickname, difficulty)
        self.game.start_game()

        self._main_view.show_game()

    def init_leaderboard(self):
        pass

    def init_start_screen(self):
        self._main_view.show_start_screen()

    def handle_movement(self, direction):
        self.game.move_player(direction)
        new_pos = self.game.player.position
        self._main_view.game_view.update_player_position_display()
        self._main_view.game_view.update_cell_display(new_pos)

if __name__ == '__main__':
    app = Controller()