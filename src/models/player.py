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
        self._moves += 1

        match direction:
            case "N":

                self._position[0] += 1
            case "S":
                self._position[0] -= 1
            case "E":
                self._position[1] += 1
            case "W":
                self._position[1] -= 1

    def get_position(self):
        return self._position

if __name__ == "__main__":
    player = Player("Player 1", (2,3))
    print(player.get_position())
    player.move_to("N")
    print(player.get_position())