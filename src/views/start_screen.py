
from .views import Views

class StartScreen(Views):
    BG_COLOR = "#2C3E50"
    ACCENT_COLOR = "#1ABC9C"
    TEXT_COLOR = "#ECF0F1"
    ERROR_COLOR = "#E74C3C"

    def __init__(self, parent_view, controller, title, width=500, height=500):
        super().__init__(title, width, height)

        self._parent_view = parent_view
        self._controller = controller

        self._widgets = []  # Lista di tutti i widgets di start_screen

        # --- Widgets ---
        self.nickname_field = None
        self.start_button = None
        self.quit_button = None
        self.error_label = None
        self.correct_label = None

        self._parent_view.setBackground(self.BG_COLOR)
        self._parent_view.grid_init(15,15)
        self.build_ui()


    def style(self, widget, font_size=12, bold=False):
        weight = "bold" if bold else "normal"
        widget["font"] = ("Segoe UI", font_size, weight)
        widget["background"] = self.BG_COLOR
        widget["foreground"] = self.TEXT_COLOR

    def build_ui(self):
        # --- Titolo ---
        title = self._parent_view.addLabel(
            text="PERCORSO EVOLUTIVO",
            row=2, column=4, columnspan=7, sticky="NSEW"
        )
        title["font"] = ("Segoe UI", 26, "bold")
        title["foreground"] = self.ACCENT_COLOR
        title["background"] = self.BG_COLOR
        self._widgets.append(title)

        # --- Scelta Nickname ---
        user_inst = self._parent_view.addLabel(
            text="Inserisci un nickname (massimo 20 caratteri):",
            row=5, column=4, columnspan=7, sticky="NSEW"
        )
        self.style(user_inst, font_size=15)
        self._widgets.append(user_inst)

        self.nickname_field = self._parent_view.addTextField(
            text="", row=6, column=5, columnspan=5, sticky="NSEW"
        )
        self.nickname_field["font"] = ("Segoe UI", 14)
        self.nickname_field["width"] = 20
        self._widgets.append(self.nickname_field)

        # --- Pulsante Start ---
        self.start_button = self._parent_view.addButton(
            text="START GAME",
            row=9, column=5, columnspan=5,
            command=self.handle_start_btn
        )
        self.start_button["background"] = self.ACCENT_COLOR
        self.start_button["foreground"] = "white"
        self.start_button["font"] = ("Segoe UI", 12, "bold")
        self._widgets.append(self.start_button)

        # --- Pulsante Quit ---
        self.quit_button = self._parent_view.addButton(
            text="QUIT",
            row=11, column=6, columnspan=3,
            command=self._parent_view.quit
        )
        self.quit_button["background"] = "#95A5A6"
        self.quit_button["foreground"] = "white"
        self.quit_button["font"] = ("Segoe UI", 12, "bold")
        self._widgets.append(self.quit_button)

        # --- Testo di Errore ---
        self.error_label = self._parent_view.addLabel(
            text="", row=7, column=4, columnspan=7
        )
        self.error_label["foreground"] = self.ERROR_COLOR
        self.error_label["background"] = self.BG_COLOR
        self.error_label["font"] = ("Segoe UI", 14, "italic")
        self.error_label.grid_remove()

        # --- Testo di Successo ---
        self.correct_label = self._parent_view.addLabel(
            text="", row=7, column=4, columnspan=7
        )
        self.correct_label["foreground"] = self.ERROR_COLOR
        self.correct_label["background"] = self.BG_COLOR
        self.correct_label["font"] = ("Segoe UI", 20, "italic")
        # Start hidden
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

