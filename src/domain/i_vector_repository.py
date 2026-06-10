from abc import ABC, abstractmethod
from typing import Any


class IVectorRepository(ABC):
    @abstractmethod
    def upsert(self, doc_id: int, chunk_id : int, embedding: list[float], metadata: dict[str, Any] | None = None) -> None:
        """Insert or update the embedding associated with doc_id."""
        pass

    @abstractmethod
    def delete(self, chunk_id: int) -> None:
        pass

    @abstractmethod
    def query(self,query_embedding: list[float],k: int = 10,
        where: dict[str, Any] | None = None,
    ) -> list[tuple[int,int]]:
        """Query the vector store for the most similar embeddings to the query_embedding"""
        pass

    @abstractmethod   
    def get_doc_centroids_batch(self, doc_ids: list[int]) -> dict[int, list[float]]:
        """Get the centroid embeddings for a batch of document IDs."""
        pass