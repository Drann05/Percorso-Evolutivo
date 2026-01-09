"""
Classe per la gestione del timer.
Utilizzo time per aggiornare il tempo trascorso ogni secondo.
"""
import time

class Timer:
    def __init__ (self):
        self._starting_time = 0
        self._elapsed = 0
        self._running = False

    def start_timer(self): 
        """
        incrementa il tempo trascorso ogni secondo e imposta lo stato a Vero
        """
        if not self._running:
            self._starting_time = time.time()
            self._running = True
            self.update_elapsed()

    def update_elapsed(self):
        if self._running:
            self._elapsed = int(time.time() - self._starting_time)
            return self._elapsed
  
    def stop_timer(self):
        """
        ferma il timer quando richiamata e aggiorna self._elapsed
        """
        self.get_elapsed()
        self._running = False
   
    def reset_timer(self):
        self._elapsed = 0
        self._running = False

    def get_elapsed(self):
        self.update_elapsed()
        return int(self._elapsed)
