import chromadb
from domain.i_vector_repository import IVectorRepository
class ChromaVectorRepository(IVectorRepository):
    def __init__(self, persist_path: str = "./chroma_data", collection_name: str = "documents"):
        self._client = chromadb.PersistentClient(path=persist_path)
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(self, doc_id: int, embedding: list[float], metadata=None) -> None:
        self._collection.upsert(
            ids=[str(doc_id)],
            embeddings=[embedding],
            metadatas=[metadata or {}],
        )

    def query(self, query_embedding: list[float], k=10, where=None) -> list[tuple[int, float]]:
        res = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where,
            include=["distances"],
        )
        # falta score y proceso que dependen del embedding y la norma
        ...