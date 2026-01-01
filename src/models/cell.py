class Cell:
    """
        Rappresenta una singola cella della griglia di gioco

        Ogni cella è caratterizzata da:
        - una posizione (posx, posy)
        - un tipo, che stabilisce il colore e se è attraversabile o meno
    """
    CELL_TYPES = {
        'O': 'green',   # Obiettivo
        'P': 'blue',    # Punto di partenza
        'X': 'black',   # Muro (non attraversabile)
        'T': 'red',     # Trappola
        'R': 'yellow',  # Risorsa
        '.': 'white'    # Cella vuota
    }


    def __init__(self, posx, posy, cell_type):
        self._posx = posx
        self._posy = posy
        self._cell_type = None
        self.set_type(cell_type)

    def is_walkable(self):
        """
            Indica se la cella è attraversabile o meno

            :return: False se la cella è un muro ('X'), True altrimenti
        """
        if self._cell_type == "X":
            return False
        else:
            return True

    def set_type(self, cell_type):
        if cell_type not in self.CELL_TYPES.keys():
            raise ValueError("Il tipo deve essere uno tra: 'O', 'P', 'X', 'T', 'R', '.'")
        else:
            self._cell_type = cell_type

    def get_type(self):
        return self._cell_type