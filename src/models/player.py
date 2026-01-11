class Player:
    """
        Rappresenta il giocatore di Percorso Evolutivo

        La classe Player gestisce esclusivamente lo stato del giocatore,
        tra cui la posizione corrente, il punteggio, il numero di mosse
        effettuate e la disponibilità delle sue abilità

        Non contiene la logica di gioco né modifica direttamente la griglia
    """
    INITIAL_VALUES = {
        "score": 0,
        "moves": 0,
        "remove_wall_count": 1,
        "convert_trap_count": 1
    }

    def __init__(self, nickname, position):
        self._nickname = nickname
        self._position = position
        self._score = self.INITIAL_VALUES["score"]
        self._moves = self.INITIAL_VALUES["moves"]
        self._remove_wall_count = self.INITIAL_VALUES["remove_wall_count"]
        self._convert_trap_count = self.INITIAL_VALUES["convert_trap_count"]


    #----------------|
    #   PROPERTIES   |
    #----------------|

    @property
    def nickname(self):
        return self._nickname

    @property
    def score(self):
        return self._score

    @property
    def moves(self):
        return self._moves

    @property
    def position(self):
        return self._position

    @property
    def remove_wall_count(self):
        return self._remove_wall_count

    @property
    def convert_trap_count(self):
        return self._convert_trap_count

    #------------|
    #   SETTER   |
    #------------|

    @position.setter
    def position(self, value):
        self._position = value

    #---------------------|
    #   LOGICA DI GIOCO   |
    #---------------------|

    def move_to(self, direction):
        """
        Aggiorna la posizione del giocatore

        Il metodo si limita a cambiare la posizione del giocatore
        La validazione dello spostamento è gestita nella classe Game

        :param direction: String con la direzione (N, S, E, W)
        """
        row, col = self._position

        match direction:
            case "N": row -= 1
            case "S": row += 1
            case "E": col += 1
            case "W": col -= 1

        self._position = (row, col)
        self._moves += 1

    def change_score(self, value):
        """Aggiunge o sottrae punti al punteggio del giocatore"""
        self._score += value

    #--------------------------------|
    #   METODI PER AZIONI SPECIALI   |
    #--------------------------------|

    def use_remove_wall(self):
        self._remove_wall_count -= 1

    def use_convert_trap(self):
        self._convert_trap_count -= 1

    #-----------------------------|
    #   RESET DELLE STATISTICHE   |
    #-----------------------------|


    def reset_all_stats(self):
        self.reset_score()
        self.reset_moves()
        self.reset_remove_wall()
        self.reset_convert_trap()

    def reset_score(self):
        self._score = self.INITIAL_VALUES["score"]

    def reset_moves(self):
        self._moves = self.INITIAL_VALUES["moves"]

    def reset_remove_wall(self):
        self._remove_wall_count = self.INITIAL_VALUES["remove_wall_count"]

    def reset_convert_trap(self):
        self._convert_trap_count = self.INITIAL_VALUES["convert_trap_count"]



