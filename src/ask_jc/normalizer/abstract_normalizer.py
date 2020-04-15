from abc import ABC, abstractmethod


class AbstractNormalizer(ABC):
    @abstractmethod
    def normalize(self, text: str) -> str:
        pass
