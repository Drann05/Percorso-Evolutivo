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

    def start_game(self):
        self.grid.generate_grid(self._difficulty)

        spawn_point = self.grid.spawn_position
        self.player = Player(self._player_name, spawn_point)
        print(self.is_reachable((0,0),(1,7),10))

        self.timer.start_timer()

    def move_player(self, direction):
        if not self.is_neighbor_reachable(direction):
            return {'moved': False, 'new_position': None, 'cell_data': None, 'game_over': False}

        if self.player.moves >= 30:
            self.end_game()
            return {'moved': False, 'new_position': self.player.position, 'cell_data': None, 'game_over': True}

        self.player.move_to(direction)

        new_position = self.player.position
        cell_data = self.grid.get_cell_data(new_position)
        self.apply_cell_effect(cell_data)

        return {'moved': True, 'new_position': self.player.position, 'cell_data': cell_data, 'game_over': False}

    def apply_cell_effect(self, cell_data):
        cell_type = cell_data["type"]
        cell_position = cell_data["position"]

        cell_type = cell_type.upper()

        if cell_type in self.SCORES:
            self.player.change_score(self.SCORES[cell_type])

        if cell_type == "R":
            self.grid.set_cell(cell_position, '.')


    def end_game(self):
        self.timer.stop_timer()

    def is_reachable(self, start: tuple, target: tuple, player_score, breakable_walls = 0, convertable_traps = 0):
        """
        Algoritmo per trovare un percorso minimo in passi dalla cella 'start' alla cella 'target'.
        Tiene conto di:
        - Muri che possono essere distrutti (fino a breakable_walls)
        - Trappole che possono essere convertite (fino a convertable_traps)
        - Punteggio del giocatore (non deve andare in negativo)

        Ogni nodo esplorato contiene:
        (x, y) - coordinate nella griglia
        broken_walls - numero di muri distrutti per arrivare qui
        converted_traps - numero di trappole convertite per arrivare qui
        user_score - punteggio attuale del giocatore

        COMPLESSITA' LOGICA: O(H*W*(B+1)*(T+1))
        H: Height
        W: Width
        B: Breakable Walls
        T: Converted Traps
        """

        DEBUG = True

        # Coda BFS: nodi da esplorare
        to_visit = [(start, 0, 0, player_score)]

        # Set degli stati già visitate: serve a non riesplorare stati già controllati
        visited = {(start, 0, 0, player_score)}

        # Dizionario parent per ricostruire il percorso
        # Chiave: stato logico (posizione, broken_walls, converted_trap)
        # Valore: stato precedente
        parent = {(start, 0, 0, player_score): None}

        count_moves = 0

        if DEBUG:
            print(f"\n=== BFS START ===")
            print(f"Start: {start}, Target: {target}")
            print(f"Score iniziale: {player_score}")
            print(f"Muri rompibili: {breakable_walls}, Trappole convertibili: {convertable_traps}\n")

        # Ciclo principale: continua finché non rimangono altri nodi da visitare, oppure finché non superiamo il limite di mosse
        while len(to_visit) > 0 and count_moves <= 30:

            current_level = len(to_visit)

            if DEBUG:
                print(f"\n--- LIVELLO BFS {count_moves} ---")
                print(f"Nodi nel livello: {current_level}")
                print(f"Coda: {to_visit}")

            # Espando tutti i nodi del livello corrente prima di passare al livello successivo
            # Ogni livello equivale agli stati nelle celle adiacenti del livello precedente
            for _ in range(current_level):
                # Prendo il primo nodo dalla coda (FIFO)
                (current_x, current_y), broken_walls, converted_traps, score = to_visit.pop(0)

                if DEBUG:
                    print(f"\nEspando nodo:")
                    print(f"  Posizione: ({current_x}, {current_y})")
                    print(f"  Muri rotti: {broken_walls}")
                    print(f"  Trappole convertite: {converted_traps}")
                    print(f"  Score: {score}")

                # Controllo se abbiamo raggiunto il target
                if (current_x, current_y) == target:
                    if DEBUG:
                        print("\n TARGET RAGGIUNTO!")
                    # Ricostruzione del percorso partendo dal target (current_x, current_y)
                    path = []
                    state = ((current_x, current_y), broken_walls, converted_traps, score)
                    while state is not None:
                        print(state)
                        pos,_,_,_ = state
                        path.append(pos)
                        state = parent[state]
                    path.reverse()  # Percorso dall'inizio del target

                    if DEBUG:
                        print(f"Percorso trovato: {path}")

                    return True, path   # Ritorna: percorso trovato, strada minima

                # Salvo le posizioni dei vicini (celle adiacenti a (current_x, current_y))
                neighbors = [
                    (current_x - 1, current_y),  # N
                    (current_x + 1, current_y),  # S
                    (current_x, current_y - 1),  # O
                    (current_x, current_y + 1)   # E
                ]

                # Esploro ogni vicino
                for nx, ny in neighbors:
                    # Controllo i confini della griglia
                    if not (0 <= nx < self.grid.height and 0 <= ny < self.grid.width):
                        if DEBUG:
                            print(f"  Vicino ({nx},{ny}) fuori griglia -> scarto")
                        continue

                    cell = self.grid.get_cell((nx,ny))

                    # Copio i valori correnti per modificarli nel vicino
                    new_broken_walls = broken_walls
                    new_converted_traps = converted_traps
                    new_score = score

                    if DEBUG:
                        print(f"\n  Analizzo vicino ({nx},{ny})")

                    if cell.is_walkable():
                        if cell.type == self.grid.TRAPPOLA:  # Se la cella è una trappola
                            if score >= 5:              # E lo score dell'utente è maggiore a quello che sottrae la trappola
                                new_score -= 5          # Attraversala
                                if DEBUG:
                                    print(F"    Trappola -> perdo 5 punti: {new_score}")
                            elif converted_traps < convertable_traps:   # Altrimenti, se puoi, convertila
                                new_converted_traps += 1
                                if DEBUG:
                                    print("    Trappola -> convertita")
                            else:
                                # Se non si può attraversare e non si può convertire, cerca un'altra strada
                                continue
                        if cell.type == self.grid.RISORSA:
                            new_score += 10
                            if DEBUG:
                                print(f"    Risorsa -> prendo 10 punti: {new_score}")

                    # Se la cella non è camminabile (muro) e posso distruggere dei muri
                    elif broken_walls < breakable_walls:
                        new_broken_walls += 1
                        if DEBUG:
                            print("    Muro -> distrutto")

                    else:
                        if DEBUG:
                            print("    Muro non distruggibile -> scarto")
                        # Se non posso attraversare e non posso rompere, cerca un'altra strada
                        continue

                    # Chiave dello stato logico per visited e parent (senza score)
                    state_key = ((nx, ny), new_broken_walls, new_converted_traps, new_score)
                    prev_key = ((current_x, current_y), broken_walls, converted_traps, score)

                    # Se lo stato è già stato visitato, non lo riesploro
                    if state_key in visited:
                        if DEBUG:
                            print(f"    Stato {state_key} già visitato -> scarto")
                        continue

                    visited.add(state_key)  # Salvo il nodo visitato per non rivisitarlo
                    new_state = ((nx,ny), new_broken_walls, new_converted_traps, new_score) # Salvo il nuovo nodo da visitare da aggiungere alla coda
                    parent[state_key] = prev_key    # Aggiorno il parent per poter ricostruire il percorso
                    to_visit.append(new_state)      # Aggiungo il nuovo nodo alla coda BFS

                    if DEBUG:
                        print(f"    Aggiunto in coda: {new_state}")

            count_moves += 1

        if DEBUG:
            print("\n Target NON raggiungibile")

        # Se esco dal while senza aver raggiunto il target, non è raggiungibile
        return False, []

    def is_neighbor_reachable(self, direction):
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

