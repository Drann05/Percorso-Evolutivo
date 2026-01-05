from .views import Views

class StartScreen(Views):
    MAIN_FONT = ("Arial", 20, "bold")
    ACCENT_COLOR = "Pink"
    BACKGROUND_COLOR = "Purple"

    def __init__(self, parent_view, controller, title, width=500, height=500):
        super().__init__(title, width, height)
        self._widgets = []
        self._parent_view = parent_view
        self._controller = controller
        self._difficulty = None
        self._nickname = None

        self._parent_view.grid_init(12,12)
        self.build_ui()


    def style(self, widget):
        widget["font"]=self.MAIN_FONT
        widget["foreground"]=self.ACCENT_COLOR
        widget["background"]=self.BACKGROUND_COLOR

    def build_ui(self):
        title = self._parent_view.addLabel("PERCORSO EVOLUTIVO", row=2, column=4, columnspan=2)
        title["foreground"]="white"
        title["background"]="Pink"
        title["font"]=self.MAIN_FONT
        self._widgets.append(title)

        user=self._parent_view.addLabel(text="Inserisci un nickname ( massimo 20 caratteri)", row = 3, column=4, columnspan=2)
        user["foreground"]="white"
        user["background"]=self.BACKGROUND_COLOR
        user["font"]=self.MAIN_FONT
        self._widgets.append(user)

        self.nickname_field=self._parent_view.addTextField(text="", row = 4, column=4, columnspan=2)
        self.nickname_field["font"]=self.MAIN_FONT
        self._widgets.append(self.nickname_field)

        self.start_button=self._parent_view.addButton(text="Start game", row=5, column=4, columnspan=2, command=self.handle_start_btn)
        self.style(self.start_button)
        self._widgets.append(self.start_button)

        self.quit_button=self._parent_view.addButton(text="Quit game", row=6, column=4, columnspan=2, command=self._parent_view.quit)
        self.style(self.quit_button)
        self._widgets.append(self.quit_button)

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

    def save_name(self):
        if self.check_user():
            self._nickname = self.nickname_field.getText()
            self.correct_label["text"] = "Nome salvato con successo"
            self.correct_label.grid()

    def check_user(self):
        """Estrae il testo e verifica che esso sia valido"""
        name = self.nickname_field.getText().strip()

        if not name:
            raise ValueError("USERNAME_VUOTO")

        if len(name) > 20:
            raise ValueError("USERNAME_NON_VALIDO")

        return name

    def handle_start_btn(self):
        """Gestisce il funzionamento del pulsante Start e la logica degli errori"""
        self.error_label.grid_remove()
        self.correct_label.grid_remove()

        try:
            valid_name = self.check_user()
            self._nickname = valid_name

            self.set_difficulty()
        except ValueError as e:

            if str(e) == "USERNAME_VUOTO":
                self.error_label["text"] = "Errore: Inserisci un nome!"

            elif str(e) == "USERNAME_NON_VALIDO":
                self.error_label["text"] = "Errore: Nome troppo lungo (max 20)!"

            self.error_label.grid()


    @property
    def difficulty(self):
        return self._difficulty

    @property
    def nickname(self):
        return self._nickname
