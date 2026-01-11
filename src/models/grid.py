from .cell import Cell
import random



class Grid:
    """
    Rappresenta la griglia di gioco

    La griglia è una matrice bidimensionale di oggetti Cell e gestisce
    metodi per:
    - generare la griglia iniziale
    - evolvere la griglia (quando viene chiamato il metodo step nella classe Game)
    - verificare la validità dei movimenti
    """

    DIFFICULTY = {
        "facile": {"Muri": 15, "Risorse": 12, "Trappole": 3},
        "medio": {"Muri": 20, "Risorse": 10, "Trappole": 5},
        "difficile": {"Muri": 25, "Risorse": 8, "Trappole": 7}
    }

    MURO = 'X'
    RISORSA = 'R'
    TRAPPOLA = 'T'
    OBIETTIVO = 'O'
    PUNTO_DI_PARTENZA = 'P'
    CELLA_VUOTA = '.'

    def __init__(self, width, height):
        """
        Inizializza la griglia con le dimensioni specificate

        :param width: numero di colonne che compongono la griglia
        :param height: numero di righe che compongono la griglia
        """

        self._width = width
        self._height = height
        self.grid = [[Cell(row, col, self.MURO) for row in range(self._height)] for col in range(self._width)]
        self._grid_dimension = width * height
        self._safe_zone = []
        self._spawn_position = None
        self._target_position = None

        self._positions = {
            self.MURO: {(r, c) for r in range(self._height) for c in range(self._width)},
            self.RISORSA: set(),
            self.TRAPPOLA: set(),
            self.CELLA_VUOTA: set()
        }
    def generate_grid(self, difficulty: str):
        """
        Genera la griglia di gioco in base alla difficoltà scelta:

        Ogni posizione della griglia viene inizializzata con una Cell
        di tipo '.' (cella vuota)

        :param difficulty: definisce la difficoltà della griglia:
        - Facile: 15% Muri, 12% Risorse, 3% Trappole
        - Medio: 20% Muri, 10% Risorse, 5% Trappole
        - Difficile: 25% Muri, 8% Risorse, 7% Trappole
        """

        difficulty = difficulty.lower()
        self.generative_dfs()  # Algoritmo per generare la griglia con almeno una strada percorribile

        walls_target = int(self.DIFFICULTY[difficulty]["Muri"] * self._grid_dimension / 100)
        resources_target = int(self.DIFFICULTY[difficulty]["Risorse"] * self._grid_dimension / 100)
        traps_target = int(self.DIFFICULTY[difficulty]["Trappole"] * self._grid_dimension / 100)

        self._adjust_cells(self.MURO, walls_target)
        self._adjust_cells(self.RISORSA, resources_target)
        self._adjust_cells(self.TRAPPOLA, traps_target)
        self._place_special_cells()



        """self._spawn_position = (0,0)
        self._target_position = (1,7)
        self.set_cell((0,0), self.PUNTO_DI_PARTENZA)
        self.set_cell((1,7), self.OBIETTIVO)

        self.set_cell((0,1), self.CELLA_VUOTA)
        self.set_cell((0, 2), self.MURO)
        self.set_cell((1, 0), self.TRAPPOLA)
        #self.set_cell((0, 3), self.TRAPPOLA)
        #self.set_cell((0, 4), self.TRAPPOLA)
        self.set_cell((1, 1), self.RISORSA)
        self.set_cell((0, 1), self.CELLA_VUOTA)

        self.set_cell((0,3), self.CELLA_VUOTA)
        self.set_cell((1, 2), self.MURO)
        self.set_cell((2, 0), self.MURO)
        self.set_cell((2, 1), self.MURO)
        self.set_cell((2, 2), self.MURO)
        self.set_cell((1, 3), self.MURO)"""


    def _adjust_cells(self, cell_type: str, target_count: int):
        current = self._count_cells(cell_type)
        difference = target_count - current

        if difference > 0:
            self._add_random_cells(cell_type, difference)
        elif difference < 0:
            self._remove_random_cells(cell_type, abs(difference))

    #--------------#
    #   DFS Maze   #
    #--------------#

    def generative_dfs(self):
        """
        Genera un labirinto utilizzando un algoritmo Depth-First Search (DFS)
        in versione generativa

        L'algoritmo parte da una cella iniziale (inizializzata a 0,0) e visita
        (in modo iterativo tramite stack) le celle non ancora visitate.
        """

        visited = set()
        stack = [(0, 0)]

        while stack:
            x, y = stack[-1]

            neighbors = []
            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:  # vicini a distanza 2
                nx, ny = x + dx, y + dy
                if 0 <= nx < self._height and 0 <= ny < self._width:
                    if (nx, ny) not in visited:
                        neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                mid_x = (x + nx) // 2
                mid_y = (y + ny) // 2

                self.set_cell((mid_x,mid_y), self.CELLA_VUOTA)  # Scava la cella intermedia
                self.set_cell((x, y), self.CELLA_VUOTA)  # Scava la cella corrente
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

    def step(self, player_position: tuple[int,int]):
        """Evolve lo stato della griglia ogni 5 mosse seguendo queste regole:
        - Due risorse non raccolte vengono trasformate in celle vuote
        - Una cella vuota casuale viene trasformata in risorsa
        - Due celle vuote casuali vengono trasformate in trappole
        - Una trappola casuale viene trasformata in cella vuota
        - L'evoluzione non può modificare la posizione iniziale (P), l'obiettivo (O) i muri (X) e la Safe Zone"""

        def pick_cells(positions: set, number_of_cells: int):
            """Seleziona 'number_of_cells' posizioni casuali da una lista 'positions'"""
            player_neighbors = self.get_neighbors(player_position)
            safe_zone = set(player_neighbors)
            safe_zone.add(player_position)

            cells_picked = player_neighbors.copy()

            if not positions:
                return []
            while any(position in cells_picked for position in safe_zone):  # Finché la posizione scelta appartiene alla safe zone
                cells_picked = random.sample(list(positions), min(len(positions), number_of_cells))

            return cells_picked

        to_remove_resources = pick_cells(self._positions[self.RISORSA], 2)
        to_add_traps = pick_cells(self._positions[self.CELLA_VUOTA], 2)
        to_remove_traps = pick_cells(self._positions[self.TRAPPOLA], 1)

        for pos in to_remove_resources:
            self.set_cell(pos, self.CELLA_VUOTA)
        for pos in to_add_traps:
            self.set_cell(pos, self.TRAPPOLA)
        for pos in to_remove_traps:
            self.set_cell(pos, self.CELLA_VUOTA)



    #---------------------#
    #   CELL MANAGEMENT   #
    #---------------------#

    def set_cell(self, position: tuple[int,int], cell_type: str):
        """Modifica il tipo di una cella data la sua posizione e il nuovo tipo"""
        row, col = position
        old_type = self.grid[row][col].type

        self.grid[row][col].set_type(cell_type)

        self._unregister_position(old_type, position)
        self._register_position(cell_type, position)

    def _register_position(self, cell_type: str, pos: tuple[int,int]):
        """Registra le posizioni delle celle nei rispettivi insiemi (set)"""

        if cell_type in self._positions:
            self._positions[cell_type].add(pos)
        elif cell_type == self.PUNTO_DI_PARTENZA:
            self._spawn_position = pos
        elif cell_type == self.OBIETTIVO:
            self._target_position = pos


        """for r in range(self._height):
            for c in range(self._width):
                if self.grid[row][col].type == self.CELLA_VUOTA:
                    self._empty_cells_positions.add((r, c))"""

    def _unregister_position(self, cell_type: str, pos: tuple[int,int]):
        """Rimuove dalla registrazione degli insiemi di 'cell_type'
        la cella in posizione 'pos'"""
        if cell_type in self._positions:
            self._positions[cell_type].discard(pos)

    def _place_special_cells(self):
        """Sceglie randomicamente dall'insieme delle celle vuote, una posizione
        per la spawn_position e una per la target_position"""
        self._spawn_position = random.choice(list(self._positions[self.CELLA_VUOTA]))
        self.set_cell(self._spawn_position, self.PUNTO_DI_PARTENZA)

        valid_target_positions = [
            pos for pos in self._positions[self.CELLA_VUOTA]
            if self._manhattan_distance(pos, self._spawn_position) >= 10
        ]

        self._target_position = random.choice(valid_target_positions)
        self.set_cell(self._target_position, self.OBIETTIVO)

    #-----------------------#
    #   RANDOM PLACEMENT    #
    #-----------------------#


    def _add_random_cells(self, cell_type: str, count: int):
        """Aggiunge alla griglia 'count' volte 'cell_type', occupando celle vuote randomiche"""
        candidates = list(self._positions[self.CELLA_VUOTA])
        random.shuffle(candidates)  # Mescola la lista di candidati (celle vuote)

        for pos in candidates[:count]:
            self.set_cell(pos, cell_type)

    def _remove_random_cells(self, cell_type: str, count: int):
        """Rimuove dalla griglia 'count' volte 'cell_type'"""
        positions = list(self._get_positions_by_type(cell_type))
        random.shuffle(positions)

        for pos in positions[:count]:
            self.set_cell(pos, self.CELLA_VUOTA)

    #------------------#
    #     UTILITIES    #
    #------------------#

    def _count_cells(self, cell_type: str):
        """Conta il numero totale di 'cell_type' contenute nella griglia"""
        return len(self._get_positions_by_type(cell_type))

    def _get_positions_by_type(self, cell_type: str):
        """Restituisce il set di posizioni per il tipo di cella specificato.
            Usa il metodo dict.get() per evitare KeyError se il tipo non esiste."""
        return self._positions.get(cell_type, set())

    def get_cell(self, position: tuple[int,int]):
        """Restituisce il riferimento alla cella in posizione 'position'"""
        return self.grid[position[0]][position[1]]


    def get_cell_data(self, position: tuple[int,int]):
        """Restituisce informazioni sulla cella in posizione 'position'"""
        cell = self.get_cell(position)
        return {
            "type": cell.type,
            "position": position,
            "walkable": cell.is_walkable()
        }

    def is_valid_movement(self, position: tuple[int,int]):
        """Verifica se un movimento in direzione cardinale è valido"""
        row, col = position
        if not (0 <= row < self._height and 0 <= col < self._width):
            return False
        return self.grid[row][col].is_walkable() and 0 <= row < self._height and 0 <= col < self._width

    def get_grid_dimension(self):
        return self._height, self._width

    #----------------------#
    #    SERIALIZATION     #
    #----------------------#

    def serialize(self):
        """Ritorna un dizionario con informazioni utili sulla griglia,
        IMPORTANTE: non deve passare alcun riferimento alla griglia o alle celle, solo dati primitivi"""
        grid_data = [
            [cell.type for cell in row]
            for row in self.grid
        ]
        return {
            "rows": self._height,
            "cols": self._width,
            "grid": grid_data,
            "spawn_position": self.spawn_position,
            "target_position": self.target_position
        }

    @property
    def spawn_position(self):
        """Restituisce la posizione dello spawn point"""
        return self._spawn_position

    @property
    def target_position(self):
        """Restituisce la posizione del target point"""
        return self._target_position

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @staticmethod
    def get_neighbors(position: tuple[int,int]):
        return [
            (position[0] - 1, position[1]),  # N
            (position[0] + 1, position[1]),  # S
            (position[0], position[1] - 1),  # O
            (position[0], position[1] + 1)  # E
        ]

    @staticmethod
    def _manhattan_distance(a: tuple[int,int], b: tuple[int,int]):
        """Calcola la distanza tra due celle"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def print_grid(self):
        for i in range(0, self._height):
            for j in range(0, self._width):
                print(self.grid[i][j].type, end=" ")
            print("")

