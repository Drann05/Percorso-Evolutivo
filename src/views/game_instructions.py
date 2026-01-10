from .views import Views


class GameInstructions(Views):

    def __init__(self, parent_view, controller, title, width=600, height=700):
        super().__init__(title, width, height)
        self._parent_view = parent_view
        self._controller = controller

        self._parent_view.setBackground(self._parent_view.COLORS["bg"])

        self.build_ui()
        self._parent_view.bind("<Configure>", self.on_resize)

    def style(self, widget, is_header=False):
        if is_header:
            widget["font"] = ("Impact", 24)
            widget["foreground"] = self._parent_view.COLORS["accent"]
        else:
            widget["font"] = ("Segoe UI", 11)
            widget["foreground"] = self._parent_view.COLORS["text"]
        widget["background"] = self._parent_view.COLORS["bg"]

    def build_ui(self):
        title = self._parent_view.addLabel(
            "I S T R U Z I O N I",
            row=1, column=0, columnspan=10, sticky="NSEW",
        )
        self.style(title, is_header=True)


        istruzioni = (
            "> MOVIMENTO: Usa il D-Pad per muoverti all'interno della griglia.\n"
            "> OBIETTIVO (O): Raggiungi l'obiettivo entro 30 mosse.\n"
            "> RISORSE (R): Raccogli le risorse per aumentare il punteggio.\n"
            "> TRAPPOL<e (T): Fai attenzione alle trappole! Se ci passi sopra, ti toglieranno punti.\n"
            "> MURI (X): Non puoi attraversarli, ma puoi romperli con la mossa speciale.\n"
            "> MOSSE SPECIALI: Ne hai due a disposizione. Usa il Double-click su un muro o una trappola per utilizzarle."
        )

        self.txt_area = self._parent_view.addTextArea(
            text=istruzioni, row=4, column=2, columnspan=6, width=60, height=8
        )
        self.txt_area.configure(
            font=("Consolas", 11),
            background=self._parent_view.COLORS["bg"],
            foreground=self._controller.COLORS["text"],
            borderwidth=1,
            relief="flat"
        )
        self.txt_area.grid_configure(sticky="NSEW", padx=20, pady=10)

        legend_title = self._parent_view.addLabel(
            text="ELEMENTI PRINCIPALI", row=13, column=0, columnspan=10
        )
        self.style(legend_title)
        legend_title.configure(font=("Impact", 16), foreground=self._parent_view.COLORS["accent"])
        self.legend_panel = self._parent_view.addPanel(row=14, column=2, columnspan=6, rowspan=7,
                                                       background=self._controller.COLORS["bg"])

        elementi = [
            ("GIOCATORE", "#E91E63", "oval"),
            ("MURO (X)", "#1A1A1A", "rect"),
            ("RISORSA (R)", "#F1C40F", "rect"),
            ("TRAPPOLA (T)", "#E74C3C", "rect"),
            ("OBIETTIVO (O)", "#2ECC71", "rect"),
            ("CELLA VUOTA (.)", "#2C3E50", "rect")
        ]

        current_row = 15
        for nome, colore, shape in elementi:
            canvas = self._parent_view.addCanvas(
                row=current_row, column=3, width=25, height=25
            )
            canvas.configure(background=self._parent_view.COLORS["bg"], highlightthickness=0)

            if shape == "rect":
                canvas.create_rectangle(4, 4, 21, 21, fill=colore, outline="gray")
            else:
                canvas.create_oval(4, 4, 21, 21, fill=colore, outline="white", width=2)

            lbl = self._parent_view.addLabel(text=nome, row=current_row, column=4, sticky="W")
            lbl.configure(font=("Consolas", 10, "bold"), background=self._parent_view.COLORS["bg"], foreground=self._parent_view.COLORS["text"])
            current_row += 1

        close_btn = self._parent_view.addButton(
            text="TORNA AL GIOCO", row=23, column=3, columnspan=4,
            command=self._parent_view.show_game
        )
        close_btn.configure(
            background=self._parent_view.COLORS["accent"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=20
        )

    def on_resize(self, event):
        total_rows = 25
        total_cols = 10
        for i in range(total_rows):
            self._parent_view.rowconfigure(i, weight=1)
        for j in range(total_cols):
            self._parent_view.columnconfigure(j, weight=1)


