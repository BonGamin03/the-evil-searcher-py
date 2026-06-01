from abc import ABC, abstractmethod

class IQueryExpander(ABC):
    @abstractmethod
    def expand_query(self, query: str, topn: int = 2) -> list[str]:
        """Expande la consulta original devolviendo una lista de términos enriquecidos."""
        pass
    def train_model(self):
        pass
    