from .models.game import Game
from .views.start_screen import StartScreen
from .views.leaderboard_view import LeaderboardView
from .views.game_view import GameView
from .views.menu import Menu


class MainApp():
    def __init__(self):
        self.start_screen = None
        self.game = None
        self.game_view = None
        self.init_game()

    def init_menu(self):
        pass

    def init_game(self):
        self.game = Game("Gioele", "facile")
        self.game.start_game()
        self.game_view = GameView(self, "Percorso Evolutivo")
        self.game_view.mainloop()

    def init_leaderboard(self):
        pass

    def init_start_screen(self):
        pass

    def handle_movement(self, direction):
        self.game.move_player(direction)
        new_pos = self.game.player.position
        self.game_view.update_player_position_display()
        self.game_view.update_cell_display(new_pos)


if __name__ == '__main__':
    app = MainApp()