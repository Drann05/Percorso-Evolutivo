from .models.leaderboard import Leaderboard
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

        self._leaderboard = Leaderboard()
        self._game = None

        self._session_data: dict[str, str | None] = {"nickname": None}

        self._main_view = MainView(self)


    def run(self):
        self._main_view.mainloop()

    #---------------------------------|
    #   GESTIONE NAVIGAZIONE E MENU   |
    #---------------------------------|

    def init_start_screen(self):
        """Imposta lo stato iniziale dell'app e mostra
        la shermata di avvio attraverso MainView"""
        self._main_view.show_start_screen()

    def handle_leaderboard_request(self):
        scores = self._leaderboard.get_top_10()
        self._main_view.show_leaderboard(scores)

    def handle_instruction_request(self):
        self._main_view.show_instructions()

    #---------------------|
    #   LOGICA DI GIOCO   |
    #---------------------|

    def start_game_request(self, nickname: str):
        self._session_data["nickname"] = nickname
        self._main_view.show_difficulty_dialog()

    def handle_selected_difficulty(self, difficulty: str):
        nickname = self._session_data["nickname"]
        self._game = Game(nickname, difficulty)
        self._game.start_game()
        self._main_view.show_game()

    def handle_movement_request(self, direction: str):
        """Gestisce il movimento del giocatore e aggiorna
        l'interfaccia grafica di GameView"""

        if not self._game:
            return

        move_result = self._game.move_player(direction)

        if move_result["moved"]:
            self._refresh_view()

        if move_result["game_over"]:
            self._handle_game_over()

    def handle_special_action_request(self, action: str, target_position: tuple[int, int]):

        if not self._game:
            return False

        is_success = self._game.use_special_action(action, target_position)
        if is_success:
            self._refresh_view()
            return True

        return False

    def handle_restart_game_request(self):
        if self._game:
            self._game.restart_game()
            self._main_view.show_game()

    #---------------|
    #   UTILITIES   |
    #---------------|

    def _refresh_view(self):
        state = self.get_game_state()
        self._main_view.update_game(state)

    def get_game_state(self):
        return {
            "grid": self._game.grid.serialize(),
            "player_position": self._game.player.position,
            "stats": {
                "score": self._game.player.score,
                "moves": self._game.player.moves,
                "timer": self._game.timer.get_elapsed()
            },
            "special_moves": {
                "remove_wall_count": self._game.player.remove_wall_count,
                "convert_trap_count": self._game.player.convert_trap_count
            },
            "is_moves_out_of_limit": self._game.is_moves_out_of_limit,
            "is_negative_score": self._game.is_negative_score,
            "is_objective_reached": self._game.is_objective_reached,
            "is_objective_unreachable": self._game.is_objective_unreachable
        }

    def update_timer(self):
        if self._game and self._game.timer:
            return self._game.timer.get_elapsed()
        return "00:00"

    def _handle_game_over(self):
        """Gestisce la fine della partita leggendo gli attributi di Game"""
        won = self._game.is_objective_reached
        is_moves_out_of_limit = self._game.is_moves_out_of_limit
        is_negative_score = self._game.is_negative_score
        is_objective_unreachable = self._game.is_objective_unreachable
        reason = ""

        if won:
            reason = "Hai raggiunto l'obiettivo!"
        elif is_moves_out_of_limit:
            reason = "Hai esaurito le mosse disponibili (Max 30)!"
        elif is_negative_score:
            reason = "Il tuo punteggio è sceso sotto lo zero!"
        elif is_objective_unreachable:
            reason = "L'obiettivo non è più raggiungibile!"

        self._main_view.show_game_over(won, reason)

    def handle_game_over_buttons(self, action_type):
        """Gestisce i pulsanti di game over.
        Permette di far scegliere se salvare o meno lo score"""
        if self._game.is_objective_reached:
            self._main_view.show_restart_dialog()
            if self._main_view.restart_dialog.get_result():
                self.handle_save_request()

        if action_type == "restart":
            self.handle_restart_game_request()
        else:
            self._main_view.show_start_screen()

    def handle_save_request(self):
        try:
            self._leaderboard.save(
                name=self._game.player.nickname,
                score=self._game.player.score,
                moves=self._game.player.moves,
                level=self._game.difficulty
            )
        except Exception as e:
            print(f"Errore nel salvataggio: {e}")

if __name__ == '__main__':
    app = Controller()
