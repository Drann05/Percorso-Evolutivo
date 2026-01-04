#Classe per la gestione del timer.
#Utilizzo time per aggiornare il tempo trascorso ogni secondo.

import time

class Timer:
    def __init__ (self):
        self._starting_time = 0
        self._elapsed = 0
        self._running = False

    #incrementa il tempo trascorso ogni secondo e imposta lo stato a Vero
    def start_timer(self): 
        self._running = True
        while self._running:
            time.sleep(1)
            self._elapsed += 1

    #ferma il timer quando richiamata       
    def stop_timer(self):
        self._running = False

    #azzera il tempo trascorso e imposta lo stato a Falso   
    def reset_timer(self):
        self._elapsed = self._starting_time
        self._running = False

    #metodo get per ottenere il tempo trascorso
    def get_elapsed(self):
        return self._elapsed
    