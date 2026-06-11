import chromadb
import numpy as np
from typing import Optional
from domain.i_profile_repository import IProfileRepository


class ChromaUserProfileRepository(IProfileRepository):
  
    def __init__(self, persist_path: str = "./chroma_data", collection_name: str = "user_profiles"):
        self._client = chromadb.PersistentClient(path=persist_path)
        
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    

    def upsert_profile(self, email: str, embedding: list[float], alpha=0.15) -> None:
        existing = self.get_profile(email)
 
        if existing is None:
            new_embedding = self._normalize(np.array(embedding))
        else:
            prev = np.array(existing["embedding"])
            curr = np.array(embedding)
            merged = alpha * curr + (1 - alpha) * prev
            new_embedding = self._normalize(merged)
  
 
        self._collection.upsert(
            ids=[email],
            embeddings=[new_embedding.tolist()],
             
        )

   
    def get_profile(self, email: str) -> Optional[dict]:
         
        try:
            result = self._collection.get(
                ids=[email],
                include=["embeddings", "metadatas"],
            )
            if result["ids"]:
                return {
                    "embedding": result["embeddings"][0],
                     
                }
        except Exception:
            pass
        return None

    @staticmethod
    def _normalize(v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else v
 