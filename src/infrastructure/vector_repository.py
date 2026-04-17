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
        )

    def query(self, query_embedding: list[float], k=10, where=None) -> list[int]:
        res = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )
        return res["ids"][0] # Esto es porque res["ids"] es una lista de listas, y queremos la primera lista que corresponde a nuestra consulta
    
    def delete(self, doc_id):
        return super().delete(doc_id)
