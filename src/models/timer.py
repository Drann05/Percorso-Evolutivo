"""
Classe per la gestione del timer.
Utilizza time per aggiornare il tempo trascorso ogni secondo.
"""
import time

class Timer:
    def __init__(self):
        self._starting_time = None
        self._elapsed = 0
        self._running: bool = False

    def start_timer(self):
        """Fa partire il timer e imposta lo stato a vero"""
        if not self._running:
            self._starting_time = time.time()
            self._running = True

    def get_elapsed(self) -> int:
        """Ritorna il tempo trascorso come intero"""
        if self._running and self._starting_time is not None:
            self._elapsed = int(time.time() - self._starting_time)
        return self._elapsed

    def stop_timer(self):
        """Ferma il timer e imposta lo stato a falso"""
        self.get_elapsed()
        self._running = False

    def reset_timer(self):
        """Riporta i valori a quelli iniziali"""
        self._starting_time = None
        self._elapsed = 0
        self._running = False
