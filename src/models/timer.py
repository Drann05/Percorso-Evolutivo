#Classe per la gestione del timer.
#Utilizza time per aggiornare il tempo trascorso ogni secondo.

import time

class Timer:
    def __init__ (self):
        self.__starting_time = 0
        self.__elapsed = None
        self.__running = False

    #incrementa il tempo trascorso ogni secondo e imposta lo stato a Vero
    def start_timer(self): 
        self.__running = True             
        while self.__running:
            time.sleep(1)
            self.__elapsed += 1

    #ferma il timer quando richiamata       
    def stop_timer(self):
        self.__running = False

    #azzera il tempo trascorso e imposta lo stato a Falso   
    def reset_timer(self):
        self.__elapsed = self.__starting_time
        self.__running = False

    #metodo get per ottenere il tempo trascorso
    def get_elapsed(self):
        return self.__elapsed
    