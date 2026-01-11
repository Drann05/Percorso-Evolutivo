class Player:
    """
        Rappresenta il giocatore di Percorso Evolutivo

        La classe Player gestisce esclusivamente lo stato del giocatore,
        tra cui la posizione corrente, il punteggio, il numero di mosse
        effettuate e la disponibilità delle sue abilità

        Non contiene la logica di gioco né modifica direttamente la griglia
    """
    def __init__(self, nickname, position):
        self._nickname = nickname
        self._position = position
        self._score = 0
        self._moves = 0
        self._has_remove_wall = True
        self._has_convert_trap = True


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
        self._has_remove_wall = False

    def use_convert_trap(self):
        self._has_convert_trap = False

    def is_remove_wall_available(self):
        return self._has_remove_wall

    def is_convert_trap_available(self):
        return self._has_convert_trap

    #-----------------------------|
    #   RESET DELLE STATISTICHE   |
    #-----------------------------|


    def reset_all_stats(self):
        self.reset_score()
        self.reset_moves()
        self.reset_remove_wall()
        self.reset_convert_trap()

    def reset_score(self):
        self._score = 0

    def reset_moves(self):
        self._moves = 0

    def reset_remove_wall(self):
        self._has_remove_wall = True

    def reset_convert_trap(self):
        self._has_convert_trap = True



