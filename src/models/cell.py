class Cell:
    """
        Rappresenta una singola cella della griglia di gioco

        Ogni cella è caratterizzata da:
        - una posizione (posx, posy)
        - un tipo, che stabilisce il colore e se è attraversabile o meno
    """
    CELL_TYPES= {
        'O': 'green',   # Obiettivo
        'P': 'blue',    # Punto di partenza
        'X': 'black',   # Muro (non attraversabile)
        'T': 'red',     # Trappola
        'R': 'yellow',  # Risorsa
        '.': 'white'    # Cella vuota
    }


    def __init__(self, row, col, cell_type):
        self._row = row
        self._col = col
        self._type = None
        self.set_type(cell_type)

    def get_score_modifier(self):
        if self._type == 'T': return -5
        elif self._type == 'R': return 10
        elif self._type == 'O': return 20
        return 0

    def is_walkable(self):
        """
            Indica se la cella è attraversabile o meno

            :return: False se la cella è un muro ('X'), True altrimenti
        """
        if self._type == "X":
            return False
        else:
            return True

    def set_type(self, cell_type: str):
        if cell_type not in self.CELL_TYPES.keys():
            raise ValueError("Il tipo deve essere uno tra: 'O', 'P', 'X', 'T', 'R', '.'")
        else:
            self._type = cell_type

    @property
    def type(self) -> str:
        return self._type

    @property
    def position(self) -> tuple[int, int]:
        return self._row, self._col