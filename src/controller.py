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
        self.start()


    def start(self):
        self._main_view.mainloop()

    def init_menu(self):
        raise NotImplementedError("Menu non ancora implementato")

    def init_leaderboard(self):
        raise NotImplementedError("Menu non ancora implementato")

    def init_start_screen(self):
        """Imposta lo stato iniziale dell'app e mostra
        la shermata di avvio attraverso MainView"""
        self._main_view.show_start_screen()

            #--------------------#
            #    START SCREEN    #
            # --------------------#

    def start_game_request(self, nickname):
        self.pending_nickname = nickname
        self._main_view.show_difficulty_dialog()

    def handle_difficulty_selected(self, difficulty):
        """Inizializza il gioco passando all'istanza gli attributi
        nickname e difficulty, ottenuti dalla classe Start Screen"""

        self.game = Game(self.pending_nickname, difficulty)
        self.game.start_game()
        self._main_view.show_game()

                #------------#
                #    GAME    #
                #------------#
    def game_state(self):
        return {
            "grid": self.game.grid,
            "player_position": self.game.player.position,
            "stats": {
                "score": self.game.player.score,
                "moves": self.game.player.moves,
                "timer": self.game.player.timer
            },
            "special_moves": {
                "remove_wall": self.game.player.is_remove_wall_available(),
                "convert_trap": self.game.player.is_convert_trap_available()
            }
        }

    def handle_restart_game_request(self):
        self.game.restart_game()
        self._main_view.show_game()

    def handle_movement_request(self, direction):
        """Gestisce il movimento del giocatore e aggiorna
        l'interfaccia grafica di GameView"""

        if not self.game:
            return

        moved = self.game.move_player(direction)

        if not moved:
            return

        self._main_view.update_game(self.game_state)

    def handle_special_action_request(self, special_move, direction):

        if not self.game:
            return

        special_move = special_move.upper()
        if special_move == "REMOVE_WALL":
            special_move_used = self.game.use_remove_wall(direction)
        else:
            special_move_used = self.game.use_convert_trap(direction)

        if not special_move_used:
            return

        self._main_view.update_game(self.game_state)


if __name__ == '__main__':
    app = Controller()