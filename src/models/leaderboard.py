import os

""" 
    Questa classe si occupa della gestione della classifica in un file.
    All'interno del file devono essere salvati: nome, punteggio, mosse, livello.
    Vengono salvati nel dizionario scores in questo formato: {'Nome': (punteggio, mosse, livello)}.

"""

class Leaderboard:
    def __init__(self, filepath, entry):
        self._filepath = "classifica.txt"
        self._entry = entry
    
    def load(self):
        scores = {}
        if os.path.exists(self._filepath):
            with open(self._filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and ":" in line:
                        try:
                            score, moves, level, name = line.split(":")
                            scores[name.strip()] = (int(score.strip()), int(moves.strip()), int(level.strip()))
                        except ValueError:
                            continue
        return scores
    

    def save(self, entry):
        name = entry.get()
        scores = self.load()
        if name not in scores or (score > scores[name][0]) or (score == scores[name][0] and moves < scores[name][1]) or (score == scores[name][0] and moves == scores[name][1] and level > scores[name][2]):
            scores[name] = (score, moves, level)
            with open(self._filepath, "w") as f:
                for name, (score, moves, level) in scores.items():
                    f.write(f"{score}:{moves}:{level}:{name}\n")
    
    #priorità: punteggio > mosse > livello > nome
    def get_top_10(self, n=10):
        pass