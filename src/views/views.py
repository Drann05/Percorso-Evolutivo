from abc import ABC, abstractmethod

class Views(ABC):

    @abstractmethod
    def build_ui(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def handle_events(self):
        pass

