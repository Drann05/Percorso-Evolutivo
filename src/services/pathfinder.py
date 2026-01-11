class Pathfinder:
    """
    Implementa un BFS avanzato che tiene conto di:
    - punteggio del giocatore
    - muri distruggibili
    - trappole convertibili
    """

    DEBUG = False

    def __init__(self, grid):
        self.grid = grid

    def is_reachable(self, start: tuple[int,int], target: tuple[int,int], player_score: int, max_breakable_walls: int = 0, max_convertible_traps: int = 0):
        """
        Algoritmo per trovare un percorso minimo in passi dalla cella 'start' alla cella 'target'.
        Tiene conto di:
        - Muri che possono essere distrutti (fino a breakable_walls)
        - Trappole che possono essere convertite (fino a convertible_traps)
        - Punteggio del giocatore (non deve andare in negativo)

        Ogni nodo esplorato contiene:
        (x, y) - coordinate nella griglia
        broken_walls - numero di muri distrutti per arrivare qui
        converted_traps - numero di trappole convertite per arrivare qui
        user_score - punteggio attuale del giocatore

        COMPLESSITA' LOGICA: O(H*W*(B+1)*(T+1))
        H: Height
        W: Width
        B: Breakable Walls
        T: Convertible Traps
        """

        # Coda BFS: nodi da esplorare
        to_visit = [(start, 0, 0, player_score)]

        # Set degli stati già visitate: serve a non riesplorare stati già controllati
        visited = {(start, 0, 0, player_score)}

        # Dizionario parent per ricostruire il percorso
        # Chiave: stato logico (posizione, broken_walls, converted_trap)
        # Valore: stato precedente
        parent = {(start, 0, 0, player_score): None}

        count_moves = 0
        MAX_MOVES = 30

        if self.DEBUG:
            print(f"\n=== BFS START ===")
            print(f"Start: {start}, Target: {target}")
            print(f"Score iniziale: {player_score}")
            print(f"Muri rompibili: {max_breakable_walls}, Trappole convertibili: {max_convertible_traps}\n")

        # Ciclo principale: continua finché non rimangono altri nodi da visitare, oppure finché non superiamo il limite di mosse
        while len(to_visit) > 0 and count_moves <= MAX_MOVES:

            current_level = len(to_visit)

            if self.DEBUG:
                print(f"\n--- LIVELLO BFS {count_moves} ---")
                print(f"Nodi nel livello: {current_level}")
                print(f"Coda: {to_visit}")

            # Espando tutti i nodi del livello corrente prima di passare al livello successivo
            # Ogni livello equivale agli stati nelle celle adiacenti del livello precedente
            for _ in range(current_level):
                # Prendo il primo nodo dalla coda (FIFO)
                state: None | tuple[tuple[int, int], int, int, int] = to_visit.pop(0)
                (current_x, current_y), broken_walls, converted_traps, score = state

                if self.DEBUG:
                    print(f"\nEspando nodo:")
                    print(f"  Posizione: ({current_x}, {current_y})")
                    print(f"  Muri rotti: {broken_walls}")
                    print(f"  Trappole convertite: {converted_traps}")
                    print(f"  Score: {score}")

                # Controllo se abbiamo raggiunto il target
                if (current_x, current_y) == target:
                    return True, self._reconstruct_path(state, parent)

                neighbors = self._extend_neighbors(current_x, current_y, broken_walls, converted_traps, score, max_breakable_walls, max_convertible_traps)

                # Chiave dello stato logico per visited e parent (senza score)
                prev_key: None | tuple[tuple[int, int], int, int, int] = ((current_x, current_y), broken_walls, converted_traps, score)

                for new_state in neighbors:
                    # Se lo stato è già stato visitato, non lo riesploro
                    if new_state in visited:
                        if self.DEBUG:
                            print(f"    Stato {new_state} già visitato -> scarto")
                        continue

                    visited.add(new_state)  # Salvo il nodo visitato per non rivisitarlo
                    parent[new_state] = prev_key  # Aggiorno il parent per poter ricostruire il percorso
                    to_visit.append(new_state)  # Aggiungo il nuovo nodo alla coda BFS

                    if self.DEBUG:
                        print(f"    Aggiunto in coda: {new_state}")

            count_moves += 1

        if self.DEBUG:
            print("\n Target NON raggiungibile")

        # Se esco dal while senza aver raggiunto il target, non è raggiungibile
        return False, []


    def _extend_neighbors(self, current_x: int, current_y: int, broken_walls: int,
                          converted_traps: int, score: int, breakable_walls: int,
                          convertible_traps: int):
        neighbors = []

        # Salvo le posizioni dei vicini (celle adiacenti a (current_x, current_y))
        directions = [
            (current_x - 1, current_y),  # N
            (current_x + 1, current_y),  # S
            (current_x, current_y - 1),  # O
            (current_x, current_y + 1)  # E
        ]

        # Esploro ogni vicino
        for nx, ny in directions:
            # Controllo i confini della griglia
            if not (0 <= nx < self.grid.height and 0 <= ny < self.grid.width):
                if self.DEBUG:
                    print(f"  Vicino ({nx},{ny}) fuori griglia -> scarto")
                continue

            cell = self.grid.get_cell((nx, ny))

            # Copio i valori correnti per modificarli nel vicino
            new_broken_walls = broken_walls
            new_converted_traps = converted_traps
            new_score = score

            if self.DEBUG:
                print(f"\n  Analizzo vicino ({nx},{ny})")

            if score >= 1:
                new_score -= 1
                if cell.is_walkable():


                    if cell.type == self.grid.TRAPPOLA:  # Se la cella è una trappola
                        if score >= 5:  # E lo score dell'utente è maggiore a quello che sottrae la trappola
                            new_score -= 5  # Attraversala
                            if self.DEBUG:
                                print(f"    Trappola -> perdo 5 punti: {new_score}")
                        elif converted_traps < convertible_traps:  # Altrimenti, se puoi, convertila
                            new_converted_traps += 1
                            new_score += 10
                            if self.DEBUG:
                                print("    Trappola -> convertita")
                        else:
                            # Se non si può attraversare e non si può convertire, cerca un'altra strada
                            continue
                    if cell.type == self.grid.RISORSA:
                        new_score += 10
                        if self.DEBUG:
                            print(f"    Risorsa -> prendo 10 punti: {new_score}")

                # Se la cella non è camminabile (muro) e posso distruggere dei muri
                elif broken_walls < breakable_walls:
                    new_broken_walls += 1
                    if self.DEBUG:
                        print("    Muro -> distrutto")

                else:
                    if self.DEBUG:
                        print("    Muro non distruggibile -> scarto")
                    # Se non posso attraversare e non posso rompere, cerca un'altra strada
                    continue

                neighbors.append(((nx,ny), new_broken_walls, new_converted_traps, new_score))
            else:
                continue
        return neighbors

    def _reconstruct_path(self, state: tuple[tuple[int, int], int, int, int], parent):
        if self.DEBUG:
            print("\n TARGET RAGGIUNTO!")
        # Ricostruzione del percorso partendo dal target (current_x, current_y)
        path = []

        while state:
            pos, _, _, _ = state
            path.append(pos)
            state = parent[state]
            print(state)
        path.reverse()  # Percorso dall'inizio del target

        if self.DEBUG:
            print(f"Percorso trovato: {path}")

        return path  # ritorna strada minima