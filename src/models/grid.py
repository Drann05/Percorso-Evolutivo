from cell import Cell
from player import Player
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


    def __init__(self, width, height):
        """
        Inizializza la griglia con le dimensioni specificate

        :param width: numero di colonne che compongono la griglia
        :param height: numero di righe che compongono la griglia
        """

        self._width = width
        self._height = height
        self._grid = []
        self._safe_zone = []
        self._spawn_point = None # Tupla (x,y)

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

        self._grid = [[Cell(col,row,'X') for col in range(self._width)] for row in range(self._height)]
        grid_dimension = self.get_grid_dimension()
        #muri_count = int(self.DIFFICULTY[difficulty]["Muri"] * grid_dimension / 100)
        #risorse_count = int(self.DIFFICULTY[difficulty]["Risorse"] * grid_dimension / 100)
        #trappole_count = int(self.DIFFICULTY[difficulty]["Trappole"] * grid_dimension / 100)

        def place_cells(cell_type, count):
            placed = 0
            while placed < count:
                row = randint(0, self._height - 1)
                col = randint(0, self._width - 1)
                if self._grid[col][row].get_type() == ".":
                    self._grid[col][row] = Cell(col, row, cell_type)
                    placed += 1

        #place_cells("X", muri_count)
        #place_cells("R", risorse_count)
        #place_cells("T", trappole_count)

    def dfs(self):
        visited = set()

        stack = [(0,0)]
        is_goal_reached = False

        while (not is_goal_reached) and stack:
            x, y = stack.pop()


            self.set_cell((x, y), '.')  # scava la cella corrente

            neighbors = []
            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:  # vicini a distanza 2
                nx, ny = x + dx, y + dy
                if 0 <= nx < self._height and 0 <= ny < self._width:
                    if (nx, ny) not in visited:
                        neighbors.append((nx, ny))


            random.shuffle(neighbors)  # per percorsi casuali

            for nx, ny in neighbors:
                mid_x = (x+nx)//2
                mid_y = (y+ny)//2

                self._grid[mid_x][mid_y] = Cell(mid_x, mid_y, '.')
                visited.add((nx, ny))
                stack.append((nx, ny))

    def get_spawn_position(self):
        """
            Restituisce la posizione dello spawn point

            TODO: implementare logica di spawn
        """
        return (3,2)

    def get_cell(self, position):
        row, col = position
        return self._grid[row][col].get_type()

    def set_cell(self, position, cell_type):
        row, col = position
        self._grid[row][col].set_type(cell_type)

    def is_valid_movement(self, position):
        row, col = position
        return self._grid[row][col].is_walkable()

    def get_grid_dimension(self):
        return self._width * self._height

    def print_grid(self):
        for i in range(0, self._height):
            for j in range(0, self._width):
                print(self._grid[i][j].get_type(), end = " ")
            print("")

if __name__ == '__main__':
    grid = Grid(20, 20)
    grid.generate_grid("Difficile")

    grid.dfs()
    grid.print_grid()




