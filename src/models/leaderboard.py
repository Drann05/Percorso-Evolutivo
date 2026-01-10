import os

class Leaderboard:
    """
    Gestisce una classifica salvata su file.
    Formato file: punteggio:mosse:livello:nome
    """

    def __init__(self, filepath="classifica.txt"):
        self._filepath = filepath
        self._scores = self.load()

    def load(self):
        """Carica i dati dal file, verifica che siano nel formato corretto,
         trasforma le statistiche in interi e restituisce un dizionario."""

        scores = {}
        if os.path.exists(self._filepath):
            with open(self._filepath, "r") as f:
                for line in f:
                    parts = line.strip().split(":")
                    if len(parts) == 4:
                        try:
                            score, moves, difficulty, name = parts
                            scores[name] = (int(score), int(moves), difficulty)
                        except ValueError:
                            continue
        return scores

    def save(self, name, score, moves, level):
        """
        Aggiorna la classifica solo se il punteggio è migliore del precedente,
        richiama la funzione di sorting per ordinare volta per volta
        e sovrascrive il file solo se necessario.
        """

        name = name.strip()
        old_data = self._scores.get(name)
        if not old_data or self.is_better(score, moves, level, *old_data):
            self._scores[name] = (score, moves, level)

            sorted_items = self.sorting()

            with open(self._filepath, "w") as f:
                for s_name, (s_score, s_moves, s_level) in sorted_items:
                    f.write(f"{s_score}:{s_moves}:{s_level}:{s_name}\n")
            self._scores = dict(sorted_items) #aggiorna il dizionario per mantenere l'ordine corretto

    def sorting(self):
        """
        Usa l'algoritmo Insertion Sort.
        Restituisce una lista di tuple (nome, (punti, mosse, livello))
        ordinata in base alla logica is_better.
        """

        current_data = list(self._scores.items())
        sorted_data = []

        for item in current_data:
            inserted = False
            p_name, (p_score, p_moves, p_level) = item

            """Dopo aver estratto i dati del giocatore corrente cerca la posizione corretta nella lista già ordinata"""
            for i in range(len(sorted_data)):
                s_name, (s_score, s_moves, s_level) = sorted_data[i]

                """Confronta il giocatore corrente con l'i-esimo e decide se inserirlo"""
                if self.is_better(p_score, p_moves, p_level, s_score, s_moves, s_level):
                    sorted_data.insert(i, item)
                    inserted = True
                    break
            if not inserted:
                sorted_data.append(item) #se non è stato inserito viene messo in coda
        return sorted_data

    def get_top_10(self, n=10):
        """
        Ritorna i primi N giocatori ordinati.
        Crea una lista di tuple appiattite con lo Splat Operator
        dopo aver effettuato l'unpacking e associa un indice a ogni elemento.
        Questo viene incrementato fino ad n.
        """

        return [(nome, *valori) for i, (nome, valori) in enumerate(self._scores.items()) if i < n]

    @staticmethod
    def is_better(n_score, n_moves, n_level, o_score, o_moves, o_level):
        """
        Logica: punteggio alto meglio.
        A parità di punti, meno mosse meglio.
        A parità di mosse, livello più alto meglio.
        """

        n_l = Leaderboard.difficulty_to_int(n_level)
        o_l = Leaderboard.difficulty_to_int(o_level)
        return (n_score, -n_moves, n_l) > (o_score, -o_moves, o_l)

    @staticmethod
    def difficulty_to_int(difficulty):
        """Associa a ogni livello un numero intero per effettuare i confronti"""
        if difficulty.lower() == 'facile':
            return 1
        elif difficulty.lower() == 'medio':
            return 2
        elif difficulty.lower() == 'difficile':
            return 3

        raise ValueError(f"La difficoltà {difficulty} non esiste")