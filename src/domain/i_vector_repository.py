from abc import ABC, abstractmethod
from typing import Any


class IVectorRepository(ABC):
    @abstractmethod
    def upsert(self, doc_id: int, embedding: list[float], metadata: dict[str, Any] | None = None) -> None:
        """Insert or update the embedding associated with doc_id."""
        pass

    @abstractmethod
    def delete(self, doc_id: int) -> None:
        pass

    @abstractmethod
    def query(self,query_embedding: list[float],k: int = 10,
        where: dict[str, Any] | None = None,
    ) -> list[tuple[int, float]]:
        """Query the vector store for the most similar embeddings to the query_embedding"""
        pass