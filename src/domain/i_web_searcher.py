from abc import ABC, abstractmethod
from typing import Any

class IWebSearcher(ABC):
    """Interface for web searching operations."""

    @abstractmethod
    def search(self, query: str) -> list[Any]:
        pass