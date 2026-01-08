from .views import Views


class LeaderboardView(Views):
    BG_COLOR = "#2C3E50"
    ACCENT_COLOR = "#1ABC9C"
    TEXT_COLOR = "#ECF0F1"

    def __init__(self, parent_view, leaderboard, title, width=500, height=600):
        super().__init__(title, width, height)
        self._parent_view = parent_view
        self._leaderboard = leaderboard

        self.MAIN_FONT = ("Segoe UI", 11)
        self.TITLE_FONT = ("Segoe UI", 20, "bold")
        self.HEADER_FONT = ("Segoe UI", 10, "bold")

        self.widgets = []
        self._parent_view.grid_init(25, 12)
        self._parent_view.setBackground(self.BG_COLOR)

        self.build_ui()

    def style(self, widget, is_header=False, is_top_three=False):
        if is_header:
            widget["font"] = self.TITLE_FONT
            widget["foreground"] = self.ACCENT_COLOR
        elif is_top_three:
            widget["font"] = ("Segoe UI", 11, "bold")
            widget["foreground"] = "#F1C40F"
        else:
            widget["font"] = self.MAIN_FONT
            widget["foreground"] = self.TEXT_COLOR
        widget["background"] = self.BG_COLOR

    def build_ui(self):
        title = self._parent_view.addLabel(
            "CLASSIFICA",
            row=1, column=0, columnspan=12
        )
        self.style(title, is_header=True)

        h_rank = self._parent_view.addLabel("LIVELLO", row=4, column=1)
        h_name = self._parent_view.addLabel("GIOCATORE", row=4, column=3)
        h_score = self._parent_view.addLabel("PUNTI", row=4, column=7)
        h_moves = self._parent_view.addLabel("MOSSE", row=4, column=10)

        for header in [h_rank, h_name, h_score, h_moves]:
            header["font"] = self.HEADER_FONT
            header["foreground"] = self.ACCENT_COLOR
            header["background"] = self.BG_COLOR

        top_players = self._leaderboard.get_top_10()

        start_row = 6
        for i, (name, stats) in enumerate(top_players, start=1):
            score, moves, level = stats

            is_top = i <= 3
            current_y = start_row + i

            lbl_rank = self._parent_view.addLabel(text=f"#{i}", row=current_y, column=1)
            lbl_name = self._parent_view.addLabel(text=name, row=current_y, column=3)
            lbl_score = self._parent_view.addLabel(text=str(score), row=current_y, column=7)
            lbl_moves = self._parent_view.addLabel(text=str(moves), row=current_y, column=10)

            for lbl in [lbl_rank, lbl_name, lbl_score, lbl_moves]:
                self.style(lbl, is_top_three=is_top)
                self.widgets.append(lbl)


        close_btn = self._parent_view.addButton(
            text="TORNA AL MENU", row=22, column=4, columnspan=4,
            command=self._parent_view.destroy
        )
        close_btn["background"] = self.ACCENT_COLOR
        close_btn["foreground"] = "white"
        close_btn["font"] = ("Segoe UI", 10, "bold")