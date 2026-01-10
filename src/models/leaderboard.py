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
        """Carica i dati dal file e restituisce un dizionario."""
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

    @staticmethod
    def is_better(self, n_score, n_moves, n_level, o_score, o_moves, o_level):
        """
        Logica: punteggio alto meglio.
        A parità di punti, meno mosse meglio.
        A parità di mosse, livello più alto meglio.
        """
        return (n_score, n_moves, n_level) > (o_score, o_moves, o_level)

    def save(self, name, score, moves, level):
        """Aggiorna la classifica se il punteggio è migliore e salva su file."""
        name = name.strip()
        if os.path.exists(self._filepath):
            with open(self._filepath, "w") as f:
                f.write(f"{name}:{score}:{moves}:{level}:{name}\n")

        old_data = self._scores.get(name)

        if not old_data or self.is_better(score, moves, level, *old_data):
            self._scores[name] = (score, moves, level)

            sorted_items = sorted(
                self._scores.items(),
                key=lambda x: (-x[1][0], x[1][1], -x[1][2]),
                reverse=True
            )

            with open(self._filepath, "w") as f:
                for s_name, (s_score, s_moves, s_level) in sorted_items:
                    f.write(f"{s_score}:{s_moves}:{s_level}:{s_name}\n")

    def get_top_10(self, n=10):
        """Ritorna i primi N giocatori ordinati."""
        return [(nome, *valori) for i, (nome, valori) in enumerate(self._scores.items()) if i < n]

    @staticmethod
    def difficulty_to_int(difficulty):
        if difficulty.lower() == 'facile':
            return 1
        elif difficulty.lower() == 'medio':
            return 2
        elif difficulty.lower() == 'difficile':
            return 3

        raise ValueError(f"La difficoltà {difficulty} non esiste")