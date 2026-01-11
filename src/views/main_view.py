import tkinter as tk
from typing import Any, Type
from breezypythongui import EasyFrame
from .leaderboard_view import LeaderboardView
from .start_screen import StartScreen
from .base_view import BaseView
from .game_instructions import GameInstructions
from .difficulty_dialog import DifficultyDialog
from .game_view import GameView




class MainView(EasyFrame):
    """Main View agisce come 'container' principale.
    Gestisce lo switch tra le varie finestre e coordina i cicli di aggiornamento della UI"""

    # Costanti estetiche centralizzate
    COLORS = {
        "bg": "#121212",
        "accent": "#00ADB5",
        "text": "#EEEEEE",
        "error": "#FF3131",
        "panel_bg": "#1A1A1A"
    }

    def __init__(self, controller, title="Percorso Evolutivo"):
        super().__init__(title=title, width=500, height=500)
        self._title = title
        self.controller = controller

        # Lista delle Views su cui si può cambiare schermata
        self.SCREENS = [self.show_start_screen, self.show_game, self.show_leaderboard, self.show_instructions, self.show_difficulty_dialog]



        # Gestione Navigazione
        self.current_screen_func = None
        self.current_view = None
        self.came_from = None

        self.show_start_screen()

    def _clear_window(self):
        """Elimina i widget e resetta la griglia di breezypythongui"""
        for widget in self.winfo_children():
            widget.destroy()

        #rows, cols = self.grid_size()

        for r in range(20): self.rowconfigure(r, weight=0)
        for c in range(20): self.columnconfigure(c, weight=0)

        if hasattr(self, "menubar"):
            self.menubar.destroy()

    def _switch_to(self, view_class: Type[BaseView], *args: Any, **kwargs: Any):
        """Distrugge la view attuale, salva lo stato della precedente
        e istanzia la nuova view"""

        # Se stiamo visualizzando qualcosa, salviamo come tornarci
        if self.current_view:
            self.came_from = self.current_screen_func

        self._clear_window()

        # Istanzia la classe che viene passata come argomento
        self.current_view = view_class(self, self.controller, *args, **kwargs)

        # Salviamo la chiamata attuale alla funzione _switch_to per poterla utilizzare per il futuro con came_from
        self.current_screen_func = lambda: self._switch_to(view_class, *args, **kwargs)

    #-----------------|
    #   NAVIGAZIONE   |
    #-----------------|

    """Le funzioni di navigazione passano a _switch_to la classe relativa
    alla finestra da mostrare, e _switch_to dà le istruzioni per mostrarle nell'interfaccia"""

    def show_start_screen(self):
        self._switch_to(StartScreen, self._title)

    def show_game(self):
        self._switch_to(GameView, self._title)
        self.update_timer_loop()

    def show_leaderboard(self, scores: list):
        self._switch_to(LeaderboardView, self._title, scores)

    def show_instructions(self):
        self._switch_to(GameInstructions, self._title)

    def go_back(self):
        """Esegue il comando di ritorno salvato in _switch_to"""
        if self.came_from:
            self.came_from()
            self.came_from = None

    #-------------|
    #   OVERLAY   |
    #-------------|

    def show_difficulty_dialog(self):
        """Mostra l'overlay della scelta della difficoltà"""
        self.dialog = DifficultyDialog(self, self.controller)

    def show_game_over(self, won: bool, reason: str):
        """Mostra l'overlay di fine gioco"""
        if isinstance(self.current_view, GameView):
            self.current_view.display_game_over(won, reason)

    def setup_menu(self):
        """Crea la menu bar"""
        root = self.master
        self.menubar = tk.Menu(root)

        game_menu = tk.Menu(self.menubar, tearoff=0)
        game_menu.add_command(label="Nuova partita", command=self.controller.handle_restart_game_request)
        game_menu.add_separator()
        game_menu.add_command(label="Torna al menu", command=self.controller.init_start_screen)
        game_menu.add_command(label="Esci", command=root.quit)
        self.menubar.add_cascade(label="Gioco", menu=game_menu)

        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="Istruzioni",
                              command=lambda: self._switch_to(GameInstructions, self._title))
        self.menubar.add_cascade(label="Aiuto", menu=help_menu)

        root.config(menu=self.menubar)



    #--------------------------|
    #  CICLI DI AGGIORNAMENTO  |
    #--------------------------|

    def update_game(self, game_state: dict):
        if isinstance(self.current_view, GameView):
            self.current_view.set_game_state(game_state)
            self.current_view.update_game_view()

    def update_timer_loop(self):
        # Ferma il loop se l'utente cambia fermata
        if not isinstance(self.current_view, GameView) or not self.winfo_exists():
            return
        elapsed_time = self.controller.update_timer()
        try:
            self.current_view.update_timer(elapsed_time)

            self.after(1000, self.update_timer_loop)
        except Exception as e:
            print(f"Timer interrotto: {e}")
