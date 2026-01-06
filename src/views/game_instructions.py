from .views import Views

class GameInstructions(Views):
    def __init__(self, title, width, height):
        super().__init__(title, width, height)
