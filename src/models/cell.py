class Cell:

    CELL_TYPES = {
        'O': 'green',
        'P': 'blue',
        'X': 'black',
        'T': 'red',
        'R': 'white'
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
