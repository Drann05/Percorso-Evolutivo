from .views import Views
import breezypythongui

class StartScreen(Views):

    MAIN_FONT = ("Arial", 20, "bold")
    ACCENT_COLOR = "Pink"
    BACKGROUND_COLOR = "Purple"

    def __init__(self, parent, title, width, height):
        super().__init__(title, width, height)
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

        user=self.parent.addLabel(text="Inserisci un nickname ( massimo 20 caratteri)", row = 3, column=4, columnspan=2)
        user["foreground"]="white"
        user["background"]=self.BACKGROUND_COLOR
        user["font"]=self.MAIN_FONT
        self.widgets.append(user)

        self.nickname_field=self.parent.addTextField(text="", row = 4, column=4, columnspan=2)
        self.nickname_field["font"]=self.MAIN_FONT
        self.widgets.append(self.nickname_field)

        self.start_button=self.addButton(text="Start game", row=5, column=4, columnspan=2, command=self.get_difficulty)
        self.style(self.start_button)
        self.widgets.append(self.start_button)

        self.quit_button=self.addButton(text="Quit game", row=6, column=4, columnspan=2)

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
        self.error_label["foreground"] = "green"
        self.error_label["background"] = self.BACKGROUND_COLOR
        self.error_label["font"] = ("Arial", 14, "italic")

        self.error_label.grid_remove()

    def save_name(self):
        if self.check_user():
            self.nickname = self.nickname_field.getText()
            self.correct_label["text"] = "Nome salvato con successo"
            self.correct_label.grid()

    def check_user(self):

        if not self.nickname:
            raise ValueError("USERNAME_VUOTO")

        if len(self.nickname) > 20:
            raise ValueError("USERNAME_NON_VALIDO")

    def handle_start_btn(self):
        try:
            self.check_user()
        except ValueError as e:
            if str(e) == "USERNAME_VUOTO":
                pass
            elif str(e) == "USERNAME_NON_VALIDO":
                pass




    def update_ui(self):
        pass

    def handle_events(self, eve):
        pass

    def get_difficulty(self):
        pass
