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

    # Costanti di configurazione punteggi
    SCORES = {
        Grid.OBIETTIVO: 20,
        Grid.RISORSA: 10,
        Grid.TRAPPOLA: -5,
        Grid.MURO: 0,
        Grid.CELLA_VUOTA: 0,
        Grid.PUNTO_DI_PARTENZA: 0,
        "movement": -1
    }

    MOVES_BEFORE_EVOLUTION = 5

    def __init__(self, player_name, difficulty):
        self._player_name = player_name
        self._difficulty = difficulty
        self._started = False

        # Componenti del modello
        self.grid = None
        self.player = None
        self.timer = Timer()
        self._pathfinder = None

        # Flag di stato
        self._is_objective_reached = False
        self._is_moves_out_of_limit = False
        self._is_negative_score = False
        self._is_objective_unreachable = False

    # ----------------|
    #   PROPERTIES   |
    # ----------------|

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def is_negative_score(self):
        return self._is_negative_score

    @property
    def is_moves_out_of_limit(self):
        return self._is_moves_out_of_limit

    @property
    def is_objective_unreachable(self):
        return self._is_objective_unreachable

    @property
    def is_objective_reached(self):
        return self._is_objective_reached


    #-----------------------------------|
    #   METODI DI GESTIONE CICLO VITA   |
    #-----------------------------------|

    def setup_game(self):
        """Inizializza una nuova sessione garantendo una mappa risolvibile"""

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

            valid_map,_ = self.can_reach()

        if not valid_map:
            raise RuntimeError("Impossibile generare una mappa valida")

    def start_game(self):
        """Avvia la partita e il cronometro"""
        self.setup_game()
        self._started = True
        self.timer.start_timer()

    def end_game(self):
        """Termina la partita e ferma il cronometro"""
        self._started = False
        self.timer.stop_timer()

    def restart_game(self):
        """Scorciatoia per riavviare il gioco con gli stessi parametri"""
        self.start_game()

    def move_player(self, direction):
        """Muove il giocatore, se possibile, e applica gli effetti della cella.
        Ritorna un dizionario utile per l'interfaccia grafica"""
        if not self._started:
            raise RuntimeError("Il gioco è finito")

        if not self._is_neighbor_reachable(direction):
            return self._move_result(False)

        # Esecuzione movimento
        self.player.move_to(direction)
        self.player.change_score(self.SCORES["movement"])
        cell_data = self.grid.get_cell_data(self.player.position)
        self._apply_cell_effect(cell_data)

        # Evoluzione della griglia ogni 'MOVES_BEFORE_EVOLUTION' moves
        if self.player.moves % self.MOVES_BEFORE_EVOLUTION == 0:
            self.grid.step(self.player.position)
            self._is_objective_unreachable = not self.can_reach()[0]
            if self._is_objective_unreachable:
                return self._move_result(True, cell_data, True)


        # Controllo terminazione (viene fatto prima di step per evitare l'evoluzione della griglia a fine partita)
        game_over = self.check_game_over()
        if game_over:
            self.end_game()

        return self._move_result(True, cell_data, game_over)

    def use_special_action(self, action, target_position):
        """Gestisce l'uso di abilità speciali alle celle adiacenti (N, S, O, E)"""

        if not self._started or not self._is_adjacent(target_position):
            return False

        cell = self.grid.get_cell(target_position)

        if action == "remove_wall" and self.player.remove_wall_count > 0:
            if cell.type == self.grid.MURO:
                self.grid.set_cell(target_position, self.grid.CELLA_VUOTA)
                self.player.use_remove_wall()
                return True

        elif action == "convert_trap" and self.player.convert_trap_count > 0:
            if cell.type == self.grid.TRAPPOLA:
                self.grid.set_cell(target_position, self.grid.RISORSA)
                self.player.use_convert_trap()
                return True

        return False

    #-------------------------------|
    #   METODI DI CONTROLLO STATO   |
    #-------------------------------|

    def check_game_over(self):
        """Controlla tutte le condizioni di fine partita"""
        self._is_moves_out_of_limit = self.player.moves >= 30
        self._is_negative_score = self.player.score < 0
        self._is_objective_reached = self.grid.get_cell(self.player.position).type == self.grid.OBIETTIVO


        return self._is_moves_out_of_limit or self._is_negative_score or self._is_objective_reached

    def can_reach(self):
        """Interroga il pathfinder per la raggiungibilità di un target"""
        return self._pathfinder.is_reachable(
            start = self.player.position,
            target = self.grid.target_position,
            player_score = self.player.score,
            max_breakable_walls= self.player.remove_wall_count,
            max_convertible_traps= self.player.convert_trap_count
        )

    def _apply_cell_effect(self, cell_data):
        """Applica i bonus/malus della cella calpestata"""
        cell_type = cell_data["type"].upper()
        points = self.SCORES.get(cell_type, 0)

        if points != 0:
            self.player.change_score(points)

        if cell_type == self.grid.RISORSA:
            self.grid.set_cell(cell_data["position"], self.grid.CELLA_VUOTA)

    def _is_neighbor_reachable(self, direction):
        """Verifica se la cella adiacente è raggiungibile"""
        row, col = self.player.position

        match direction:
            case "N":row -= 1
            case "S":row += 1
            case "E":col += 1
            case "W":col -= 1

        return self.grid.is_valid_movement((row,col))

    def _is_adjacent(self, target_position):
        """Verifica se una coordinata è a distanza 1 da 'target_position'"""
        p_row, p_col = self.player.position
        t_row, t_col = target_position

        return abs(p_row - t_row) + abs(p_col - t_col) == 1

    def _move_result(self, moved, cell_data=None, game_over=False):
        """Formato standard della risposta di movimento"""
        return {
            "moved": moved,
            "new_position": self.player.position if moved else None,
            "cell_data": cell_data,
            "game_over": game_over
        }


