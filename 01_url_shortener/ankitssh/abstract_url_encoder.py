from abc import ABC, abstractmethod
class Encoder(ABC):
    @abstractmethod
    def encode_url(self, long_url):
        pass