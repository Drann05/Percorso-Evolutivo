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
        self._grid = [[Cell(col,row,self.MURO) for col in range(self._width)] for row in range(self._height)]
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

        def place_cells(cell_type, count):

            if count < 0:
                removed = 0
                while removed < abs(count):
                    row = randint(0, self._height - 1)
                    col = randint(0, self._width - 1)
                    if self._grid[row][col].get_type() == cell_type:
                        self._grid[row][col] = Cell(row, col, self.CELLA_VUOTA)
                        removed += 1
            else:
                placed = 0
                while placed < count:
                    row = randint(0, self._height - 1)
                    col = randint(0, self._width - 1)
                    if self._grid[row][col].get_type() == self.CELLA_VUOTA:
                        self._grid[row][col] = Cell(row, col, cell_type)
                        placed += 1

        place_cells(self.MURO, muri_count)
        place_cells(self.RISORSA, risorse_count)
        place_cells(self.TRAPPOLA, trappole_count)
        place_cells(self.OBIETTIVO, 1)
        place_cells(self.PUNTO_DI_PARTENZA, 1)

    def generative_dfs(self):
        """
        Genera un labirinto utilizzando un algoritmo Depth-First Search (DFS)
        in versione generativa

        L'algoritmo parte da una cella iniziale (inizializzata a 0,0) e visita
        (in modo iterativo tramite stack) le celle non ancora visitate.
        """

        visited = set()
        stack = [(0,0)]

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
                mid_x = (x+nx)//2
                mid_y = (y+ny)//2

                self._grid[mid_x][mid_y] = Cell(mid_x, mid_y, self.CELLA_VUOTA) # Scava la cella intermedia
                self.set_cell((x, y), self.CELLA_VUOTA)  # Scava la cella corrente
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()


    def get_spawn_position(self):
        """
            Genera delle cordinate casuali finché non trova una cella vuota
            Restituisce la posizione dello spawn point 
        """
        while True:
            x = randint(0, self._height - 1)
            y = randint(0, self._width - 1)
            if self._grid[x][y].get_type() == self.CELLA_VUOTA:
                self.set_cell((x, y), self.PUNTO_DI_PARTENZA)
                self._spawn_point = (x, y)
                return (x, y)
            
    def set_objective_position(self, x, y, min_distance=15):
        """
            Genera delle cordinate casuali finché non trova una cella vuota
            che sia almeno a 15 celle di distanza dalla posizione dello spawn point
            usa la logica della distanza di Manhattan 
        """
        while True:
            target_x = randint(0, self._height - 1)
            target_y = randint(0, self._width - 1)
            distance = abs(target_y-y) + abs(target_x-x)
            if self._grid[target_x][target_y].get_type() == self.CELLA_VUOTA and distance >= min_distance:
                self.set_cell((target_x, target_y), self.OBIETTIVO)
                return (target_x, target_y)
            
    def is_reachable(self, x, y, target_x, target_y):
        """
            Verifica se la cella obiettivo è raggiungibile dalla cella di spawn
            controllando le celle adiacenti in modo da vedere se esiste un percorso percorribile 
        
        """
        to_visit = [(x, y)]
        visited = [(x, y)]

        while len(to_visit) > 0:
            current_x, current_y = to_visit.pop(0)

            if (current_x, current_y) == (target_x, target_y):
                return True

            neighbors = [
                (current_x - 1, current_y),  # N
                (current_x + 1, current_y),  # S
                (current_x, current_y - 1),  # O
                (current_x, current_y + 1)   # E
            ]

            for i, j in neighbors:
                if (0 <= i < self._height and 0 <= j < self._width):
                    if (self._grid[i][j].is_walkable()) and (i, j) not in visited:
                        to_visit.append((i, j))
                        visited.append((i, j))
        return False

    def check_status(self, x, y, target_x, target_y):
        """
            Verifica se l'obiettivo è raggiungibile durante il gioco
        """
        if self.is_reachable(x, y, target_x, target_y):
            #print("Obiettivo Raggiungibile")
            return True
        
        if self._remove_wall_aviable:
            #print("Mossa Speciale Necessaria")
            return True
        return False

    def cell_count(self, cell_type):
        counter = 0
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col].get_type() == cell_type:
                    counter += 1
        return counter

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

    def remove_wall(self, wall_x, wall_y):
        if self._remove_wall_aviable():
            self._grid[wall_x][wall_y] = Cell(wall_x, wall_y, self.CELLA_VUOTA)
            self._remove_wall_aviable = False
        if self._grid[wall_x][wall_y].get_type() != self.MURO:
            return True
        
    def _remove_wall_aviable(self):
        return True        
        
if __name__ == '__main__':
    grid = Grid(20, 20)

    grid.generate_grid("Difficile")
    #grid.generative_dfs()
    grid.print_grid()
    print(grid.cell_count('X'))
    print(grid.cell_count('R'))
    print(grid.cell_count('T'))