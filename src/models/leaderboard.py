import os

""" 
    Questa classe si occupa della gestione della classifica in un file.
    All'interno del file devono essere salvati: nome, punteggio, mosse, livello.
    Vengono salvati nel dizionario scores in questo formato: {'Nome': (punteggio, mosse, livello)}.

"""

class Leaderboard:
    def __init__(self, filepath="classifica.txt", entry=None):
        self._filepath = filepath
        self._entry = entry
        self._scores = self.load()

    
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
    

    def save(self, score, moves, level):
        name = self._entry.get().strip()
        
        old_data = self._scores.get(name, (0, 30, 0)) #valori di default se il nome non esiste
        if self.is_better(score, moves, level, old_data[0], old_data[1], old_data[2]):
            self._scores[name] = (score, moves, level)

            sorted_data = self.sorting()

            with open(self._filepath, "w") as f:
                for name, (score, moves, level) in sorted_data:
                    f.write(f"{score}:{moves}:{level}:{name}\n")
        else:
            return

    """
    Funzione di ordinamento. 
    Trasforma il dizionario in una lista di tuple per ordinare la classifica, successivamente confrontiamo il giocatore attuale con l'ultimo inserito:
    se è migliore, prende il posto del giocatore nella lista e tutti i successivi "scivolano" di un posto, altrimenti viene confrontato con gli altri giocatori, se non è migliore di nessuno viene inserito in coda.
    """
    def sorting(self):
        current_data = list(self._scores.items())
        sorted_data = []

        for item in current_data:
            inserted = False
            for i in range(len(sorted_data)):
                p_score, p_moves, p_level = item[1]  
                _, (s_score, s_moves, s_level) = sorted_data[i]

                if self.is_better(p_score, p_moves, p_level, s_score, s_moves, s_level):
                    sorted_data.insert(i, item)
                    inserted = True
                    break
        
            if not inserted:
                sorted_data.append(item)
        
        return sorted_data

    @staticmethod
    def is_better(new_score, new_moves, new_level, old_score, old_moves, old_level):
        """riceve i dati della nuova e dell'ultima partita, stabilisce se è migliore in base alla priorità: punteggio > mosse > livello"""
        return (new_score, new_moves, new_level) > (old_score, old_moves, old_level)

    
    def get_top_10(self, n=10):
        ordered_data = self.sorting()
        return ordered_data[:n]