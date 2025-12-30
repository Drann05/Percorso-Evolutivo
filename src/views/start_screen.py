from .views import Views
from breezypythongui import EasyDialog
class StartScreen(Views):

    MAIN_FONT = ("Arial", 20, "bold")
    ACCENT_COLOR = "Pink"
    BACKGROUND_COLOR = "Purple"

    def __init__(self, parent, title, width, height):
        super().__init__(title, width, height)
        self.correct_label = None
        self.error_label = None
        self.quit_button = None
        self.start_button = None
        self.nickname_field = None
        self.difficulty=None
        self.parent = parent
        self.widgets = []
        self.grid_init(12,12)

        self.build_ui()
        self.nickname = None

    def style(self, widget):
        widget["font"]=self.MAIN_FONT
        widget["foreground"]=self.ACCENT_COLOR
        widget["background"]=self.BACKGROUND_COLOR

    def build_ui(self):
        title = self.addLabel("PERCORSO EVOLUTIVO", row=2, column=4, columnspan=2)
        title["foreground"]="white"
        title["background"]="Pink"
        title["font"]=self.MAIN_FONT
        self.widgets.append(title)

        user=self.addLabel(text="Inserisci un nickname ( massimo 20 caratteri)", row = 3, column=4, columnspan=2)
        user["foreground"]="white"
        user["background"]=self.BACKGROUND_COLOR
        user["font"]=self.MAIN_FONT
        self.widgets.append(user)

        self.nickname_field=self.addTextField(text="", row = 4, column=4, columnspan=2)
        self.nickname_field["font"]=self.MAIN_FONT
        self.widgets.append(self.nickname_field)

        self.start_button=self.addButton(text="Start game", row=5, column=4, columnspan=2, command=self.handle_start_btn)
        self.style(self.start_button)
        self.widgets.append(self.start_button)

        self.quit_button=self.addButton(text="Quit game", row=6, column=4, columnspan=2, command=self.destroy)
        self.style(self.quit_button)
        self.widgets.append(self.quit_button)

        self.error_label = self.addLabel(
            text="Messaggio di errore",
            row=4,
            column=4,
            columnspan=6,
        )
        self.error_label["foreground"] = "red"
        self.error_label["background"] = self.BACKGROUND_COLOR
        self.error_label["font"] = ("Arial", 14, "italic")

        self.error_label.grid_remove()

        self.correct_label = self.addLabel(
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
            self.nickname = self.nickname_field.getText()
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
            self.nickname = valid_name

            self.get_difficulty()
        except ValueError as e:
            if str(e) == "USERNAME_VUOTO":
                self.error_label["text"] = "Errore: Inserisci un nome!"
            elif str(e) == "USERNAME_NON_VALIDO":
                self.error_label["text"] = "Errore: Nome troppo lungo (max 20)!"

    def get_difficulty(self):
        """Passaggio alla fase successiva: selezione difficoltà."""
        dialog = DifficultyDialog(self)

        if dialog.choice:
            self.difficulty = dialog.choice
            print(f"Hai scelto la difficoltà: {self.difficulty}")
            self.messageBox(title="Pronto!", message=f"Partita avviata in modalità {self.difficulty}")
        else:
            self.error_label["text"] = "Devi scegliere una difficoltà per iniziare!"
            self.error_label.grid()

class DifficultyDialog(EasyDialog):
    def __init__(self, parent):
        self.choice = None
        super().__init__(parent, title="Selezione Difficoltà")

    def body(self, master):
        """Crea il corpo della finestra di dialogo."""
        self.addLabel(master, text="Seleziona il livello di sfida:", row=0, column=0, columnspan=3)

        self.addButton(master, text="Facile", row=1, column=0, command=self.set_easy)
        self.addButton(master, text="Medio", row=1, column=1, command=self.set_medium)
        self.addButton(master, text="Difficile", row=1, column=2, command=self.set_hard)

    def set_easy(self):
        self.choice = "Facile"
        self.apply()

    def set_medium(self):
        self.choice = "Medio"
        self.apply()

    def set_hard(self):
        self.choice = "Difficile"
        self.apply()

    def apply(self):
        """Metodo chiamato alla chiusura per confermare l'azione."""
        self.destroy()
