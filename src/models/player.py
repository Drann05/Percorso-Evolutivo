class Player:
    """
        Rappresenta il giocatore di Percorso Evolutivo

        La classe Player gestisce esclusivamente lo stato del giocatore,
        tra cui la posizione corrente, il punteggio, il numero di mosse
        effettuate e la disponibilità delle sue abilità

        Non contiene la logica di gioco né modifica direttamente la griglia
    """
    def __init__(self, name, position):
        self._name = name
        self._position = position
        self._score = 0
        self._moves = 0
        self.remove_wall_available = True
        self.convert_trap_available = True

    def move_to(self, direction):
        """
        Aggiorna la posizione del giocatore

        Il metodo si limita a cambiare la posizione del giocatore
        La validazione dello spostamento è gestita nella classe Game

        :param direction: String con la direzione (N, S, E, W)
        """

        row, col = self._position
        self._moves += 1

        match direction:
            case "N":
                row -= 1
            case "S":
                row += 1
            case "E":
                col += 1
            case "W":
                col -= 1

        self._position = (row, col)

    def change_score(self, value):
        """Aggiunge o sottrae punti al punteggio del giocatore"""
        self._score += value

    def use_remove_wall(self):
        self.remove_wall_available = False

    def use_convert_trap(self):
        self.convert_trap_available = False

    def is_remove_wall_available(self):
        return self.remove_wall_available

    def is_convert_trap_available(self):
        return self.convert_trap_available

    @property
    def moves(self):
        return self._moves

    @property
    def score(self):
        return self._score

    @property
    def position(self):
        return self._position

