
from .views import Views

class GameInstructions(Views):
    BG_COLOR = "#2C3E50"
    ACCENT_COLOR = "#1ABC9C"
    TEXT_COLOR = "#ECF0F1"

    def __init__(self, parent_view, controller, title, width=500, height=600):
        super().__init__(title, width, height)
        self._parent_view = parent_view

        self.MAIN_FONT = ("Segoe UI", 11)
        self.TITLE_FONT = ("Segoe UI", 18, "bold")

        self.widgets = []
        self._parent_view.grid_init(20, 10)
        self._parent_view.setBackground(self.BG_COLOR)

        self.build_ui()

    def style(self, widget, is_header=False):
        if is_header:
            widget["font"] = self.TITLE_FONT
            widget["foreground"] = self.ACCENT_COLOR
        else:
            widget["font"] = self.MAIN_FONT
            widget["foreground"] = self.TEXT_COLOR
        widget["background"] = self.BG_COLOR

    def build_ui(self):
        title = self._parent_view.addLabel(
            "MANUALE DI GIOCO",
            row=1, column=5, columnspan=10, sticky="NSEW",
        )
        self.style(title, is_header=True)

        istruzioni = (
            "1. MUOVI: Usa i pulsanti direzionali per spostarti.\n"
            "2. OBIETTIVO (O): Raggiungilo per completare il livello.\n"
            "3. RISORSE (R): Raccogli i quadrati gialli per i punti.\n"
            "4. TRAPPOLE (T): Evita i blocchi rossi!\n"
            "5. MURI (X): Ostacoli non attraversabili."
        )

        txt_area = self._parent_view.addTextArea(
            text=istruzioni, row=3, column=5, columnspan=5, width=50, height=7
        )
        txt_area["font"] = ("Consolas", 10)
        txt_area["background"] = "#34495E"
        txt_area["foreground"] = self.TEXT_COLOR
        txt_area["borderwidth"] = 0

        legenda_title = self._parent_view.addLabel(
            text="LEGENDA ELEMENTI", row=11, column=5, columnspan=10
        )
        self.style(legenda_title)
        legenda_title["font"] = ("Segoe UI", 12, "bold")

        elementi = [
            ("Giocatore", "Pink"),
            ("Muro (X)", "#1a1a1a"),
            ("Risorsa (R)", "#F1C40F"),
            ("Trappola (T)", "#E74C3C"),
            ("Obiettivo (O)", "#2ECC71"),
            ("Percorso (.)", "white")
        ]

        current_row = 12
        for nome, colore in elementi:
            canvas = self._parent_view.addCanvas(
                row=current_row, column=5, width=20, height=20
            )
            canvas["background"] = self.BG_COLOR
            canvas["highlightthickness"] = 0
            canvas.create_rectangle(2, 2, 18, 18, fill=colore, outline="gray")

            lbl = self._parent_view.addLabel(text=nome, row=current_row, column=4, sticky="W")
            self.style(lbl)

            current_row += 1

        close_btn = self._parent_view.addButton(
            text="TORNA AL GIOCO", row=19, column=5, columnspan=4,
            command=self._parent_view.show_game
        )
        close_btn["background"] = self.ACCENT_COLOR
        close_btn["foreground"] = "white"
        close_btn["font"] = ("Segoe UI", 10, "bold")
