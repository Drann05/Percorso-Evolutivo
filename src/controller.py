from .models.game import Game
from .views.main_view import MainView


class Controller:
    """
    Controller è la classe che gestisce le interazioni dell'utente e coordina la comunicazione
    tra Model e View

    In dettaglio:
    Intercetta le richieste dell'utente (ad esempio il movimento)
    Fa da ponte tra Model e View, senza contenere dati persistenti né logica di presentazione
    """
    def __init__(self):

        self._start_screen = None
        self.game = None
        self._game_view = None

        self._main_view = MainView(self)
        self._main_view.mainloop()


    def init_menu(self):
        pass

    def init_game(self):
        """Inizializza il gioco passando all'istanza gli attributi
        nickname e difficulty, ottenuti dalla classe Start Screen"""
        nickname = self._main_view.start_screen.nickname
        difficulty = self._main_view.start_screen.difficulty
        self.game = Game(nickname, difficulty)
        self.game.start_game()


    def init_leaderboard(self):
        pass

    def init_start_screen(self):
        """Mostra la schermata iniziale"""
        self._main_view.show_start_screen()

    def handle_movement(self, direction):
        """Gestisce il movimento del giocatore e aggiorna
        l'interfaccia grafica di GameView"""
        self.game.move_player(direction)
        new_pos = self.game.player.position
        self._main_view.game_view.update_player_position_display()
        self._main_view.game_view.update_cell_display(new_pos)

if __name__ == '__main__':
    app = Controller()