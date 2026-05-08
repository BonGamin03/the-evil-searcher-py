from abc import ABC, abstractmethod

class IJudge(ABC):
    """Interface for evaluating the sufficiency of context to answer a user's query."""

    @abstractmethod
    def evaluate_context(self, query: str, context: str) -> str:
        pass