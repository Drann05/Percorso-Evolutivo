from .player import Player
from .grid import Grid
from .timer import Timer
from ..services.pathfinder import Pathfinder
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
        Grid.OBIETTIVO: 20,    # Obiettivo
        Grid.RISORSA: 10,    # Risorsa
        Grid.TRAPPOLA: -5,    # Trappola
        Grid.MURO: 0,     # Muro
        Grid.CELLA_VUOTA: 0,     # Cella vuota
        Grid.PUNTO_DI_PARTENZA: 0      # Punto di partenza
    }

    def __init__(self, player_name, difficulty):
        self._player_name = player_name
        self._difficulty = difficulty
        self.grid = None
        self.player = None
        self.timer = Timer()
        self.is_objective_reached = False
        self.is_moves_out_of_limit = False
        self.is_negative_score = False
        self._started = False

        self._pathfinder = None

    def setup_game(self):
        valid_map = False
        attempts = 0
        max_attempts = 10

        while not valid_map and attempts < max_attempts:
            attempts += 1

            self.grid = Grid(20, 20)
            self.grid.generate_grid(self._difficulty)

            spawn_point = self.grid.spawn_position
            self._pathfinder = Pathfinder(self.grid)

            if not self.player:
                self.player = Player(self._player_name, spawn_point)
            else:
                self.player.position = spawn_point
                self.player.reset_all_stats()

            valid_map,_ = self.can_reach(self.grid.target_position,0,0)

        if not valid_map:
            raise RuntimeError("Impossibile generare una mappa valida")

    def start_game(self):
        """Inizializza griglia, giocatore e timer"""
        self.setup_game()
        self._started = True

        self.timer.start_timer()

    def end_game(self):
        """Termina la partita e ferma il timer"""
        self._started = False
        self.timer.stop_timer()

    def restart_game(self):
        self.start_game()

    def move_player(self, direction):
        """Muove il giocatore, se possibile, e applica gli effetti della cella.
        Ritorna un dizionario utile per l'interfaccia grafica"""
        if not self._started:
            raise RuntimeError("Il gioco è finito")

        if not self.is_neighbor_reachable(direction):
            return self._move_result(False)

        self.player.move_to(direction)
        cell_data = self.grid.get_cell_data(self.player.position)

        self.apply_cell_effect(cell_data)

        game_over = self.check_game_over()
        if game_over:
            self.end_game()

        if self.player.moves % 5 == 0:
            self.grid.step(self.player.position)

        return self._move_result(True, cell_data, game_over)

    def can_reach(self, target, breakable_walls, convertable_traps):
        return self._pathfinder.is_reachable(
            start = self.player.position,
            target = target,
            player_score = self.player.score,
            breakable_walls = breakable_walls,
            convertable_traps = convertable_traps
        )

    def check_game_over(self):
        """Controlla tutte le condizioni di fine partita"""
        self.is_moves_out_of_limit = self.player.moves >= 30
        self.is_negative_score = self.player.score < 0
        self.is_objective_reached = self.grid.get_cell(self.player.position).type == self.grid.OBIETTIVO


        return self.is_moves_out_of_limit or self.is_negative_score or self.is_objective_reached

    def _move_result(self, moved, cell_data=None, game_over=False):
        """Formato standard della risposta di movimento"""
        return {
            "moved": moved,
            "new_position": self.player.position if moved else None,
            "cell_data": cell_data,
            "game_over": game_over
        }


    def is_neighbor_reachable(self, direction):
        """Verifica se la cella adiacente è raggiungibile"""
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

        position = (row, col)

        return self.grid.is_valid_movement(position)

    def apply_cell_effect(self, cell_data):
        cell_type = cell_data["type"].upper()

        points = self.SCORES.get(cell_type, 0)

        if points != 0:
            self.player.change_score(points)

        if cell_type == self.grid.RISORSA:
            self.grid.set_cell(cell_data["position"], self.grid.CELLA_VUOTA)

    def get_game_config(self):
        return {
            "nickname": self.player.nickname,
            "difficulty": self.difficulty,
        }

    def use_special_action(self, action, target_position):
        if not self._started:
            return False

        p_row, p_col = self.player.position
        t_row, t_col = target_position

        distance = abs(p_row - t_row) + abs(p_col - t_col)
        if distance != 1:
            return False

        cell = self.grid.get_cell(target_position)

        if action == "remove_wall":
            if self.player.is_remove_wall_available() and cell.type == self.grid.MURO:
                self.grid.set_cell(target_position, self.grid.CELLA_VUOTA)
                self.player.use_remove_wall()
                return True

        elif action == "convert_trap":
            if self.player.is_convert_trap_available() and cell.type == self.grid.TRAPPOLA:
                self.grid.set_cell(target_position, self.grid.RISORSA)
                self.player.use_convert_trap()
                return True

        return False

    @property
    def difficulty(self):
        return self._difficulty