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
        self._grid = Grid(20, 20)
        self._player = None
        self._timer = Timer()
        self._started = False

    def start_game(self):
        self._grid.generate_grid(self._difficulty)

        spawn_point = self._grid.get_spawn_position()
        self._player = Player(self._player_name, spawn_point)

        self._timer.start_timer()

    def move_player(self, direction):
        if not self.is_reachable(direction):
            return

        if self._player.get_moves_count() >= 30:
            self.end_game()
            return

        self._player.move_to(direction)

        new_position = self._player.get_position()
        cell_type = self._grid.get_cell(new_position)

        self.apply_cell_effect(cell_type)

    def apply_cell_effect(self, cell_type):
        """
        Applica l'effetto della cella su cui si trova il giocatore

        TODO: implementare gli effetti di ciascuna cella
        """

    def end_game(self):
        self._timer.stop_timer()

    def is_reachable(self, direction):
        row, col = self._player.get_position()

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

        return self._grid.is_valid_movement(position)

