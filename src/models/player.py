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
        self.score = 0
        self.moves = 0
        self._remove_wall_available = True
        self._convert_trap_available = True

    def move_to(self, direction):
        """
        Aggiorna la posizione del giocatore

        Il metodo si limita a cambiare la posizione del giocatore
        La validazione dello spostamento è gestita nella classe Game

        :param direction: String con la direzione (N, S, E, W)
        """

        row, col = self._position
        self.moves += 1

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

    def add_score(self, value):
        self.score += value

    def subtract_score(self, value):
        self.score -= value

    def use_remove_wall(self):
        self._remove_wall_available = False

    def use_convert_trap(self):
        self._convert_trap_available = False

    def get_move_count(self):
        return self.moves

    def get_score(self):
        return self.score
    
    def get_position(self):
        return self._position

