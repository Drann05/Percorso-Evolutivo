from .models.leaderboard import Leaderboard
from .views.leaderboard_view import LeaderboardView
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

        self.leaderboard = Leaderboard()
        self.game = None

        self._main_view = MainView(self)


    def run(self):
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
            # -------------------#

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
    def get_game_state(self):
        return {
            "grid": self.game.grid.serialize(),
            "player_position": self.game.player.position,
            "stats": {
                "score": self.game.player.score,
                "moves": self.game.player.moves,
                "timer": self.game.timer.get_elapsed()
            },
            "special_moves": {
                "remove_wall": self.game.player.is_remove_wall_available(),
                "convert_trap": self.game.player.is_convert_trap_available()
            },
            "is_moves_out_of_limit": self.game.is_moves_out_of_limit,
            "is_negative_score": self.game.is_negative_score,
            "is_objective_reached": self.game.is_objective_reached
        }

    def handle_restart_game_request(self):
        self.game.start_game()
        self._main_view.change_screen(self._main_view.show_game)

    def handle_movement_request(self, direction):
        """Gestisce il movimento del giocatore e aggiorna
        l'interfaccia grafica di GameView"""

        if not self.game:
            return

        moved = self.game.move_player(direction)

        if not moved:
            return

        self._main_view.update_game(self.get_game_state())
        if moved["game_over"]:
            self.handle_game_over()

    def handle_special_action_request(self, action, target_position):

        if not self.game:
            return False
    
        is_success = self.game.use_special_action(action, target_position)
        if not is_success:
            self._main_view.show_error()
            return False
    
        self._main_view.update_game(self.get_game_state())
        return True

    def update_timer(self):
        if self.game and self.game.timer:
            return self.game.timer.get_elapsed()
        return False

    def handle_leaderboard_request(self):
        scores = self.leaderboard.get_top_10()
        self._main_view.change_screen(self._main_view.show_leaderboard, scores)

    def handle_game_over(self):
        won = True
        if self.game.is_moves_out_of_limit or self.game.is_negative_score:
            won = False
        if self.game.is_objective_reached:
            won = True

        nickname = self.game.player.nickname
        score = self.game.player.score
        moves = self.game.player.moves
        difficulty = self.game.difficulty

        if won:
            try:
                self.leaderboard.save(
                    name = nickname,
                    score = score,
                    moves = moves,
                    level = difficulty
                )
                print(f"Dati salvati per {nickname}: {score} punti.")
            except Exception as e:
                print(f"Errore durante il salvataggio della classifica: {e}")
        self._main_view.game_view.show_game_over(won)

if __name__ == '__main__':
    app = Controller()
