from .views import Views

class StartScreen(Views):

    MAIN_FONT = ("Arial", 20, "bold")
    ACCENT_COLOR = ("Pink")
    BACKGROUND_COLOR = ("Purple")

    def __init__(self, parent, title, width, height):
        super().__init__(title, width, height)
        self.parent = parent
        self.widgets = []
        self.grid_init(12,12)

        self.build_ui()

    def style(self, widget):
        widget["font"]=self.MAIN_FONT
        widget["foreground"]=self.ACCENT_COLOR
        widget["background"]=self.BACKGROUND_COLOR

    def build_ui(self):
        title = self.parent.addLabel("PERCORSO EVOLUTIVO", row=2, column=4, columnspan=2)
        title["foreground"]="white"
        title["background"]="Pink"
        title["font"]=self.MAIN_FONT
        self.widgets.append(title)

        user=self.parent.addLabel(text="Inserisci un nickname ( massimo 12 caratteri)", row = 3, column=4, columnspan=2)
        user["foreground"]="white"
        user["background"]=self.BACKGROUND_COLOR
        user["font"]=self.MAIN_FONT
        self.widgets.append(user)

        self.nickname_field=self.parent.addTextField(text="", row = 4, column=4, columnspan=2)
        self.nickname_field["font"]=self.MAIN_FONT
        self.widgets.append(self.nickname_field)

        self.start_button=self.parent.addButton(text="Start game", row=5, column=4, columnspan=2)
        self.style(self.start_button)
        self.widgets.append(self.start_button)



    def update_ui(self):
        pass

    def handle_events(self):
        pass

    def get_player_name(self):
        pass

    def get_difficulty(self):
        pass
