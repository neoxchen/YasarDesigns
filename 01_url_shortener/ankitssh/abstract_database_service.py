from abc import ABC, abstractmethod
class DatabaseService(ABC):
    @abstractmethod
    def save_to_db(self, key, value):
        pass
    @abstractmethod
    def load_from_db(self, key):
        pass