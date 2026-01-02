from .player import Player
from .grid import Grid
from .timer import Timer
from .leaderboard import Leaderboard

class Game:
    """
    Gestisce la logica principale di Percorso Evolutivo

    Utilizza le classi Player, Grid, Timer e Leaderboard per implementare la logica
    di Percorso Evolutivo tra cui:
    - Avvio gioco
    - Interazione input utente -> gioco
    - Applicazione effetto cella
    - Controlli validità spostamento
    - Gestione fine gioco
    """

    def __init__(self, player_name, difficulty):
        self._player_name = player_name
        self._difficulty = difficulty
        self.grid = Grid(20, 20)
        self.player = None
        self.timer = Timer()
        self._started = False

    def start_game(self):
        self.grid.generate_grid(self._difficulty)

        spawn_point = self.grid.spawn_position
        self.player = Player(self._player_name, spawn_point)

        self.timer.start_timer()

    def move_player(self, direction):
        if not self.is_reachable(direction):
            return

        if self.player.get_moves_count() >= 30:
            self.end_game()
            return

        self.player.move_to(direction)

        new_position = self.player.get_position()
        cell_data = self.grid.get_cell_view_data(new_position)

        self.apply_cell_effect(cell_data["type"])

    def apply_cell_effect(self, cell_type):
        """
        Applica l'effetto della cella su cui si trova il giocatore

        TODO: implementare gli effetti di ciascuna cella
        """

    def end_game(self):
        self.timer.stop_timer()

    def is_reachable(self, direction):
        row, col = self.player.get_position()

        match direction:
            case "N":
                row -= 1
            case "S":
                row += 1
            case "E":
                col += 1
            case "W":
                col -= 1

        position = (row, col)

        return self.grid.is_valid_movement(position)

