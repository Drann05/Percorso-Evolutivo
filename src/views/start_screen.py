from .views import Views

class StartScreen(Views):
    MAIN_FONT = ("Arial", 20, "bold")
    ACCENT_COLOR = "Pink"
    BACKGROUND_COLOR = "Purple"

    def __init__(self, parent_view, controller, title, width=500, height=500):
        super().__init__(title, width, height)

        self._parent_view = parent_view
        self._controller = controller

        self._widgets = []  # Lista di tutti i widgets di start_screen

        # --- Variabili di Gioco ---
        self._difficulty = None
        self._nickname = None

        # --- Widgets ---
        self.nickname_field = None
        self.start_button = None
        self.quit_button = None
        self.error_label = None
        self.correct_label = None


        self._parent_view.grid_init(12,12)
        self.build_ui()


    def style(self, widget):
        widget["font"]=self.MAIN_FONT
        widget["foreground"]=self.ACCENT_COLOR
        widget["background"]=self.BACKGROUND_COLOR

    def build_ui(self):
        # --- Titolo ---
        title = self._parent_view.addLabel("PERCORSO EVOLUTIVO", row=2, column=4, columnspan=2)
        title["foreground"]="white"
        title["background"]="Pink"
        title["font"]=self.MAIN_FONT
        self._widgets.append(title)

        # --- Scelta Nickname ---
        user=self._parent_view.addLabel(text="Inserisci un nickname ( massimo 20 caratteri)", row = 3, column=4, columnspan=2)
        user["foreground"]="white"
        user["background"]=self.BACKGROUND_COLOR
        user["font"]=self.MAIN_FONT
        self._widgets.append(user)

        self.nickname_field=self._parent_view.addTextField(text="", row = 4, column=4, columnspan=2)
        self.nickname_field["font"]=self.MAIN_FONT
        self._widgets.append(self.nickname_field)

        # --- Pulsante Start ---
        self.start_button=self._parent_view.addButton(text="Start game", row=5, column=4, columnspan=2, command=self.handle_start_btn)
        self.style(self.start_button)
        self._widgets.append(self.start_button)

        # --- Pulsante Quit ---
        self.quit_button=self._parent_view.addButton(text="Quit game", row=6, column=4, columnspan=2, command=self._parent_view.quit)
        self.style(self.quit_button)
        self._widgets.append(self.quit_button)

        # --- Testo di Errore ---
        self.error_label = self._parent_view.addLabel(
            text="Messaggio di errore",
            row=4,
            column=4,
            columnspan=6,
        )
        self.error_label["foreground"] = "red"
        self.error_label["background"] = self.BACKGROUND_COLOR
        self.error_label["font"] = ("Arial", 14, "italic")

        self.error_label.grid_remove()

        # --- Testo di Successo ---
        self.correct_label = self._parent_view.addLabel(
            text="Messaggio",
            row=5,
            column=4,
            columnspan=6,
        )
        self.correct_label["foreground"] = "green"
        self.correct_label["background"] = self.BACKGROUND_COLOR
        self.correct_label["font"] = ("Arial", 14, "italic")

        self.correct_label.grid_remove()

    def validate_nickname(self):
        """Estrae il testo e verifica che esso sia valido"""
        name = self.nickname_field.getText().strip()

        if not name:
            return False, "Inserisci un nome!"

        if len(name) > 20:
            return False, "Nome troppo lungo (max 20)"

        return True, name

    def show_error(self, result):
        self.error_label.grid_remove()
        self.error_label["text"] = result
        self.error_label.grid()

    def clear_messages(self):
        self.error_label.grid_remove()
        self.correct_label.grid_remove()

    def handle_start_btn(self):
        """Gestisce il funzionamento del pulsante Start e la logica degli errori"""
        valid, result = self.validate_nickname()
        if not valid:
            self.show_error(result)
            return

        self._controller.start_game_request(result)

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def nickname(self):
        return self._nickname
