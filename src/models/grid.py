from cell import Cell
import random
from random import randint


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

        self._walls_positions = set()
        self._resources_positions = set()
        self._traps_positions = set()
        self._empty_cells_positions = set()

    def generate_grid(self, difficulty):
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

        muri_count = int(self.DIFFICULTY[difficulty]["Muri"] * self._grid_dimension / 100) - self.cell_count(self.MURO)
        risorse_count = int(self.DIFFICULTY[difficulty]["Risorse"] * self._grid_dimension / 100)
        trappole_count = int(self.DIFFICULTY[difficulty]["Trappole"] * self._grid_dimension / 100)

        def place_cells_randomly(cell_type, count, min_distance_from_spawn=0):
            """
            Inserisce 'count' numero di celle di tipo 'cell_type' randomicamente.
            Può essere modificata una distanza minima dallo spawn (min_distance_from_spawn).
            ma se lo spawn_position non è definito, verrà ignorata.
            """
            distance = 0

            # Se le celle nella griglia già inizializzata sono maggiori del numero specificato in count, rimuove
            # quel tipo di cella fino a ottenere il numero stabilito

            if count < 0:
                removed = 0
                while removed < abs(count):
                    row = randint(0, self._height - 1)
                    col = randint(0, self._width - 1)
                    if self.grid[row][col].type == cell_type:
                        self.grid[row][col] = Cell(row, col, self.CELLA_VUOTA)
                        removed += 1
            else:
                placed = 0
                while placed < count:
                    row = randint(0, self._height - 1)
                    col = randint(0, self._width - 1)
                    if self._spawn_position:
                        distance = abs(self._spawn_position[0] - row) + abs(self._spawn_position[1] - col)
                    if self.grid[row][col].type == self.CELLA_VUOTA and distance >= min_distance_from_spawn:  # controlla che la cella sia vuota e superi la distanza minima
                        self.register_cell_positions(cell_type, row, col)
                        self.set_cell((row, col), cell_type)
                        placed += 1

        place_cells_randomly(self.MURO, muri_count)
        place_cells_randomly(self.RISORSA, risorse_count)
        place_cells_randomly(self.TRAPPOLA, trappole_count)
        place_cells_randomly(self.PUNTO_DI_PARTENZA, 1)
        place_cells_randomly(self.OBIETTIVO, 1, 15)



        """
        self._spawn_position = (0,0)
        self._target_position = (1,7)
        self.set_cell((0,0), self.PUNTO_DI_PARTENZA)
        self.set_cell((1,7), self.OBIETTIVO)

        self.set_cell((0,1), self.CELLA_VUOTA)
        self.set_cell((0, 2), self.TRAPPOLA)
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
        self.set_cell((1, 3), self.MURO)
        """

        print(self.is_reachable(self._spawn_position, self._target_position, 4))

    def _adjust_cells(self, cell_type, target_count):
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

                self.grid[mid_x][mid_y] = Cell(mid_x, mid_y, self.CELLA_VUOTA)  # Scava la cella intermedia
                self.set_cell((x, y), self.CELLA_VUOTA)  # Scava la cella corrente
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()


    def step(self):

        def pick_cells(cell_type_positions, number_of_cells):
            chosen_positions = []
            if len(cell_type_positions) >= number_of_cells:
                chosen_positions = random.sample(list(cell_type_positions), 2)
            elif len(cell_type_positions) < number_of_cells:
                chosen_positions = random.sample(list(cell_type_positions), len(number_of_cells))
            return chosen_positions

        chosen_resource_positions = pick_cells(self._resources_positions, 2)
        chosen_empty_cells_positions = pick_cells(self._empty_cells_positions, 2)
        chosen_traps_positions = pick_cells(self._traps_positions, 1)

        print(chosen_resource_positions)
        print(chosen_empty_cells_positions)
        print(chosen_traps_positions)

        self.set_multiple_cells(chosen_resource_positions, self.CELLA_VUOTA)
        self.set_multiple_cells(chosen_empty_cells_positions, self.TRAPPOLA)
        self.set_multiple_cells(chosen_traps_positions, self.CELLA_VUOTA)


    #---------------------#
    #   CELL MANAGEMENT   #
    #---------------------#

    def set_cell(self, position, cell_type):
        row, col = position
        old_type = self.grid[row][col].type

        self.grid[row][col].set_type(cell_type)

        self._unregister_position(old_type, position)
        self._register_position(cell_type, position)

    def _register_position(self, cell_type, pos):
        if cell_type == self.MURO:
            self._walls_positions.add(pos)
        elif cell_type == self.RISORSA:
            self._resources_positions.add(pos)
        elif cell_type == self.TRAPPOLA:
            self._traps_positions.add(pos)
        elif cell_type == self.CELLA_VUOTA:
            self._empty_cells_positions.add(pos)
        elif cell_type == self.PUNTO_DI_PARTENZA:
            self._spawn_position = pos
        elif cell_type == self.OBIETTIVO:
            self._target_position = pos


        """for r in range(self._height):
            for c in range(self._width):
                if self.grid[row][col].type == self.CELLA_VUOTA:
                    self._empty_cells_positions.add((r, c))"""

    def _unregister_position(self, cell_type, pos):
        if cell_type == self.MURO:
            self._walls_positions.discard(pos)
        elif cell_type == self.RISORSA:
            self._resources_positions.discard(pos)
        elif cell_type == self.TRAPPOLA:
            self._traps_positions.discard(pos)
        elif cell_type == self.CELLA_VUOTA:
            self._empty_cells_positions.discard(pos)

    #-----------------------#
    #   RANDOM PLACEMENT    #
    #-----------------------#


    def _add_random_cells(self, cell_type, count):
        candidates = list(self._empty_cells_positions)
        random.shuffle(candidates)

        for pos in candidates[:count]:
            self.set_cell(pos, cell_type)

    def _remove_random_cells(self, cell_type, count):
        positions = list(self._get_positions_by_type(cell_type))
        random.shuffle(positions)

        for pos in positions[:count]:
            self.set_cell(pos, self.CELLA_VUOTA)

    #------------------#
    #     UTILITIES    #
    #------------------#

    def _count_cells(self, cell_type):
        return len(self._get_positions_by_type(cell_type))

    def _get_positions_by_type(self, cell_type):
        return {
            self.MURO: self._walls_positions,
            self.RISORSA: self._resources_positions,
            self.TRAPPOLA: self._traps_positions,
            self.CELLA_VUOTA: self._empty_cells_positions
        }.get(cell_type, set())

    def _distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_cell_data(self, position):
        cell = self.grid[position[0]][position[1]]
        return {
            "type": cell.type,
            "position": position,
            "walkable": cell.is_walkable()
        }



    def is_valid_movement(self, position):
        row, col = position
        return self.grid[row][col].is_walkable() and 0 <= row < self._height and 0 <= col < self._width

    def get_grid_dimension(self):
        return self._height, self._width

    #----------------------#
    #    SERIALIZATION     #
    #----------------------#

    def serialize(self):
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

    def print_grid(self):
        for i in range(0, self._height):
            for j in range(0, self._width):
                print(self.grid[i][j].type, end=" ")
            print("")


if __name__ == '__main__':
    grid = Grid(20, 20)

    grid.generate_grid("Difficile")
    # grid.generative_dfs()
    grid.print_grid()
    print("")
    print("")
    grid.step()
    grid.print_grid()
    print(grid.cell_count('X'))
    print(grid.cell_count('R'))
    print(grid.cell_count('T'))