from .cell import Cell
from .player import Player
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
        "Facile": {"Muri": 15, "Risorse": 12, "Trappole": 3},
        "Medio": {"Muri": 20, "Risorse": 10, "Trappole": 5},
        "Difficile": {"Muri": 25, "Risorse": 8, "Trappole": 7}
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
        self.grid = [[Cell(col, row, self.MURO) for col in range(self._width)] for row in range(self._height)]
        self._grid_dimension = width * height
        self._safe_zone = []
        self._spawn_point = None

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

        self.generative_dfs()  # Algoritmo per generare la griglia con almeno una strada percorribile

        muri_count = int(self.DIFFICULTY[difficulty]["Muri"] * self._grid_dimension / 100) - self.cell_count(self.MURO)
        risorse_count = int(self.DIFFICULTY[difficulty]["Risorse"] * self._grid_dimension / 100)
        trappole_count = int(self.DIFFICULTY[difficulty]["Trappole"] * self._grid_dimension / 100)

        def place_cells_randomly(cell_type, count, min_distance_from_spawn=0):
            """
            Inserisce 'count' numero di celle di tipo 'cell_type' randomicamente.
            Può essere modificata una distanza minima dallo spawn (min_distance_from_spawn).
            ma se lo spawn_point non è definito, verrà ignorata.
            """
            distance = 0

            # Se le celle nella griglia già inizializzata sono maggiori del numero specificato in count, rimuove
            # quel tipo di cella fino a ottenere il numero stabilito

            if count < 0:
                removed = 0
                while removed < abs(count):
                    row = randint(0, self._height - 1)
                    col = randint(0, self._width - 1)
                    if self.grid[row][col].get_type() == cell_type:
                        self.grid[row][col] = Cell(row, col, self.CELLA_VUOTA)
                        removed += 1
            else:
                placed = 0
                while placed < count:
                    row = randint(0, self._height - 1)
                    col = randint(0, self._width - 1)
                    if self._spawn_point:
                        distance = abs(self._spawn_point[0] - row) + abs(self._spawn_point[1] - col)
                    if self.grid[row][
                        col].get_type() == self.CELLA_VUOTA and distance >= min_distance_from_spawn:  # controlla che la cella sia vuota e superi la distanza minima
                        if cell_type == self.PUNTO_DI_PARTENZA:
                            self._spawn_point = (row, col)
                        self.set_cell((row, col), cell_type)
                        placed += 1

        place_cells_randomly(self.MURO, muri_count)
        place_cells_randomly(self.RISORSA, risorse_count)
        place_cells_randomly(self.TRAPPOLA, trappole_count)
        place_cells_randomly(self.PUNTO_DI_PARTENZA, 1)
        place_cells_randomly(self.OBIETTIVO, 1, 15)

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

    @property
    def spawn_position(self):
        """
        Restituisce la posizione dello spawn point
        """

        return self._spawn_point

    def is_reachable(self, posizione_1: tuple, posizione_2: tuple):
        """
        Verifica se la cella obiettivo è raggiungibile dalla cella di spawn
        controllando le celle adiacenti in modo da vedere se esiste un percorso percorribile
        """
        to_visit = [(posizione_1)]
        visited = [(posizione_1)]

        while len(to_visit) > 0:
            current_x, current_y = to_visit.pop(0)

            if (current_x, current_y) == (posizione_2):
                return True

            neighbors = [
                (current_x - 1, current_y),  # N
                (current_x + 1, current_y),  # S
                (current_x, current_y - 1),  # O
                (current_x, current_y + 1)  # E
            ]

            for i, j in neighbors:
                if 0 <= i < self._height and 0 <= j < self._width:
                    if (self.grid[i][j].is_walkable()) and (i, j) not in visited:
                        to_visit.append((i, j))
                        visited.append((i, j))
        return False

    def cell_count(self, cell_type):
        counter = 0
        for row in range(self._height):
            for col in range(self._width):
                if self.grid[row][col].get_type() == cell_type:
                    counter += 1
        return counter


    def get_cell_view_data(self, position):
        cell = self.grid[position[0]][position[1]]
        return {
            "type": cell.get_type(),
            "walkable": cell.is_walkable()
        }

    def set_cell(self, position, cell_type):
        row, col = position
        self.grid[row][col].set_type(cell_type)

    def is_valid_movement(self, position):
        row, col = position
        return self.grid[row][col].is_walkable()

    def get_grid_dimension(self):
        return self._height, self._width

    def print_grid(self):
        for i in range(0, self._height):
            for j in range(0, self._width):
                print(self.grid[i][j].get_type(), end=" ")
            print("")


if __name__ == '__main__':
    grid = Grid(20, 20)

    grid.generate_grid("Difficile")
    # grid.generative_dfs()
    grid.print_grid()
    print(grid.cell_count('X'))
    print(grid.cell_count('R'))
    print(grid.cell_count('T'))