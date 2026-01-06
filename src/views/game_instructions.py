from .views import Views

class GameInstructions(Views):
    def __init__(self, parent_view, title, width=500, height=500):
        super().__init__(title, width, height)
        self._parent_view = parent_view

        self.MAIN_FONT = ("Arial", 12, "bold")
        self.ACCENT_COLOR = "Purple"
        self.BACKGROUND_COLOR = "LightSkyBlue1"

        self.widgets = []
        self._parent_view.grid_init(30, 25)

        self.build_ui()

    def style(self, widget):
        widget["font"]=self.MAIN_FONT
        widget["foreground"]=self.ACCENT_COLOR
        widget["background"]=self.BACKGROUND_COLOR

    def build_ui(self):
        title = self._parent_view.addLabel("Percorso Evolutivo: manuale di gioco", row=2, column=4, columnspan=2)
        title["foreground"] = "white"
        title["background"] = "Purple"
        title["font"] = self.MAIN_FONT

        istruzioni = (
            "1. Usa i tasti direzionali per muovere il giocatore (cerchio rosa).\n"
            "2. Raggiungi l'obiettivo (O) per vincere la partita.\n"
            "3. Raccogli risorse (R) per aumentare il tuo punteggio.\n"
            "4. Evita le trappole (T) che ostacolano il tuo percorso.\n"
            "5. I muri (X) non sono attraversabili senza abilità speciali."
        )
        self._parent_view.addTextArea(text=istruzioni, row=1, column=0, columnspan=2, width=40, height=6)

        self._parent_view.addLabel(text="Legenda Elementi", row=2, column=0, columnspan=2, font=("Arial", 12, "bold"))

        elementi = [
            ("Giocatore", "Pink"),
            ("Muro (X)", "black"),
            ("Risorsa (R)", "yellow"),
            ("Trappola (T)", "red"),
            ("Obiettivo (O)", "green"),
            ("Percorso (.)", "white")
        ]

        current_row = 3
        for nome, colore in elementi:
            canvas = self._parent_view.addCanvas(row=current_row, column=0, width=20, height=20)
            canvas.create_rectangle(2, 2, 18, 18, fill=colore, outline="gray")
            self._parent_view.addLabel(text=nome, row=current_row, column=1, sticky="W")
            current_row += 1

