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

    SCORES = {
        "O": 20,    # Obiettivo
        "R": 10,    # Risorsa
        "T": -5     # Trappola
    }
    def __init__(self, player_name, difficulty):
        self._player_name = player_name
        self._difficulty = difficulty

        self.grid = Grid(20, 20)
        self.player = None
        self.timer = Timer()
        self._started = False
        self._game_over = False

    def start_game(self):
        self._started = True

        self.grid.generate_grid(self._difficulty)

        spawn_point = self.grid.spawn_position
        self.player = Player(self._player_name, spawn_point)

        self.timer.start_timer()

    def move_player(self, direction):
        if not self.is_reachable(direction):
            return

        if self.player.moves >= 30:
            self.end_game()
            return

        if self._game_over:
            return

        self.player.move_to(direction)

        new_position = self.player.position
        cell_data = self.grid.get_cell_data(new_position)

        self.apply_cell_effect(cell_data)

    def apply_cell_effect(self, cell_data):
        cell_type = cell_data["type"]
        cell_position = cell_data["position"]

        cell_type = cell_type.upper()

        if cell_type in self.SCORES:
            self.player.change_score(self.SCORES[cell_type])

        if cell_type == self.grid.RISORSA:
            self.grid.set_cell(cell_position, '.')
        elif cell_type == self.grid.OBIETTIVO:
            self.end_game()

    def end_game(self):
        self._game_over = True
        self.timer.stop_timer()

    def is_reachable(self, direction):
        return self.grid.is_valid_movement(self.next_position(direction))

    def next_position(self, direction):
        row, col = self.player.position

        match direction:
            case "N":
                row -= 1
            case "S":
                row += 1
            case "E":
                col += 1
            case "W":
                col -= 1