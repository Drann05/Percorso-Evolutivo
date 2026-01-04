class Event:
    def __init__(self, event_type):
        self.type = event_type

class DifficultySelected(Event):
    def __init__(self, difficulty: str):
        super().__init__("DIFFICULTY_SELECTED")
        self.difficulty = difficulty

class StartGame(Event):
    def __init__(self):
        super().__init__("START_GAME")