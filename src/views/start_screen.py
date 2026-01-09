from .views import Views


class StartScreen(Views):
    # --- Matched Color Palette ---
    BG_COLOR = "#121212"  # Same dark background as GameView
    ACCENT_COLOR = "#00ADB5"  # Neon Teal (Mint)
    TEXT_COLOR = "#EEEEEE"  # Off-white text
    ERROR_COLOR = "#FF3131"  # Red matching your timer color
    PANEL_BG = "#1A1A1A"  # Slightly lighter dark for panels

    def __init__(self, parent_view, controller, title, width=800, height=600):
        super().__init__(title, width, height)

        self._parent_view = parent_view
        self._controller = controller

        self._setup_layout()
        self.build_ui()

    def style_button(self, button, is_primary=True):
        """Applies the GameView button aesthetic."""
        button["font"] = ("Segoe UI", 12, "bold")
        button["foreground"] = "white"
        button["background"] = self.ACCENT_COLOR if is_primary else "#444444"
        button["width"] = 20
        button["relief"] = "flat"

    def build_ui(self):
        # --- 1. TITLE (Matched to GameView Header) ---
        title = self._parent_view.addLabel(
            text="P E R C O R S O  E V O L U T I V O",
            row=3, column=5, columnspan=10, sticky="NSEW"
        )
        title.configure(
            font=("Impact", 32),
            foreground=self.ACCENT_COLOR,
            background=self.BG_COLOR
        )
        self._widgets.append(title)


        # --- 2. INPUT PANEL (Grouped logic) ---
        # Using a panel to create a centered "login" area
        input_panel = self._parent_view.addPanel(row=7, column=6, columnspan=8, rowspan=6, background=self.PANEL_BG)
        input_panel.grid_configure(padx=20, pady=20)

        user_inst = input_panel.addLabel(
            text="INSERISCI UN NICKNAME:",
            row=0, column=0, sticky="W"
        )
        user_inst.configure(font=("Consolas", 11, "bold"), background=self.PANEL_BG, foreground=self.TEXT_COLOR)

        self.nickname_field = input_panel.addTextField(text="", row=1, column=0, sticky="EW")
        self.nickname_field.configure(font=("Consolas", 14), width=25)

        # Error text inside the panel
        self.error_label = input_panel.addLabel(text="", row=2, column=0)
        self.error_label.configure(foreground=self.ERROR_COLOR, background=self.PANEL_BG,
                                   font=("Segoe UI", 10, "italic"))
        self.error_label.grid_remove()

        # --- 3. BUTTONS ---
        self.start_button = self._parent_view.addButton(
            text="NUOVA PARTITA",
            row=14, column=7, columnspan=6,
            command=self.handle_start_btn
        )
        self.style_button(self.start_button)
        self._widgets.append(self.start_button)

        self.instructions_button = self._parent_view.addButton(
            text="ISTRUZIONI",
            row=16, column=7, columnspan=6,
            command=lambda: self._parent_view.change_screen(self._parent_view.show_instructions)
        )
        self.style_button(self.instructions_button, is_primary=False)
        self._widgets.append(self.instructions_button)

        self.quit_button = self._parent_view.addButton(
            text="ESCI",
            row=18, column=8, columnspan=4,
            command=self._parent_view.quit
        )
        self.quit_button.configure(background="#333333", foreground="#888888", font=("Segoe UI", 9), relief="flat")
        self._widgets.append(self.quit_button)

    def _setup_layout(self):
        self._parent_view.setBackground(self.BG_COLOR)
        self._parent_view.columnconfigure(0, weight=1)
        self._parent_view.rowconfigure(0, weight=1) # Spazio superiore
        self._parent_view.rowconfigure(2, weight=1) # Spazio inferiore

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

