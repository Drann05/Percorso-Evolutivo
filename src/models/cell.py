class Cell:
    """
    Rappresenta una singola cella della griglia (Grid)

    Verifica se la cella è attraversabile o meno tramite
    la funzione is_walkalble().

    Definisce il colore e il tipo di cella:
    - O: Obiettivo
    - P: Punto iniziale
    - X: Muro
    - T: Trappola
    - R: Risorsa
    - .: Cella vuota
    """

    CELL_TYPES = {
        'O': 'green',   # Obiettivo
        'P': 'blue',    # Punto iniziale
        'X': 'black',   # Muro
        'T': 'red',     # Trappola
        'R': 'yellow',  # Risorsa
        '.': 'white'    # Cella vuota
    }


    def __init__(self, posx, posy, type):
        self._posx = posx
        self._posy = posy
        self.set_type(type)

    def is_walkable(self):
        if self._type == "X":
            return False
        else:
            return True

    def set_type(self, type):
        if type not in self.CELL_TYPES.keys():
            raise ValueError("Il tipo deve essere uno tra: 'O', 'P', 'X', 'T', 'R'")
        else:
            self._type = type

    def get_type(self):
        return self._type
