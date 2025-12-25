from .cell import Cell
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
        self._cells = []
        self._safe_zone = []

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

        self._cells = [[Cell(col,row,'.') for col in range(self._width)] for row in range(self._height)]
        grid_dimension = self.get_grid_dimension()
        muri_count = int(self.DIFFICULTY[difficulty]["Muri"] * grid_dimension / 100)
        risorse_count = int(self.DIFFICULTY[difficulty]["Risorse"] * grid_dimension / 100)
        trappole_count = int(self.DIFFICULTY[difficulty]["Trappole"] * grid_dimension / 100)

        def place_cells(cell_type, count):
            placed = 0
            while placed < count:
                row = randint(0, self._height - 1)
                col = randint(0, self._width - 1)
                if self._cells[col][row].get_type() == ".":
                    self._cells[col][row] = Cell(col, row, cell_type)
                    placed += 1

        place_cells("X", muri_count)
        place_cells("R", risorse_count)
        place_cells("T", trappole_count)


    def get_cell(self, position):
        row, col = position
        return self._cells[col][row].get_type()

    def is_valid_movement(self, position):
        row, col = position
        return self._cells[col][row].is_walkable()

    def get_grid_dimension(self):
        return self._width * self._height

    def print_grid(self):
        for i in range(0, self._height):
            for j in range(0, self._width):
                print(self._cells[i][j].get_type(), end = " ")
            print("")

if __name__ == '__main__':
    grid = Grid(20, 20)
    grid.generate_grid("Difficile")
    grid.print_grid()




