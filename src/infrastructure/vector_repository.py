import chromadb
from domain.i_vector_repository import IVectorRepository
class ChromaVectorRepository(IVectorRepository):
    def __init__(self, persist_path: str = "./chroma_data", collection_name: str = "documents"):
        self._client = chromadb.PersistentClient(path=persist_path)
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(self, doc_id: int, chunk_id: int , embedding: list[float], metadata={}) -> None:
        
        metadata["doc_id"] = doc_id
        metadata["chunk_id"] = chunk_id 
        
        self._collection.upsert(
            ids=[f"{doc_id}_{chunk_id}"],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    def query(self, query_embedding: list[float], k=50, where=None) -> list[tuple[int, int]]:
        res = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where,
            include=["metadatas"],
        )
        results = []

        for meta in res["metadatas"][0]:
            results.append((int(meta["doc_id"]), int(meta["chunk_id"])))

        return results
    
    #No me consta de que esto esté bien implementado ni que sea necesario 
    def delete(self, doc_id):
        return super().delete(doc_id)
