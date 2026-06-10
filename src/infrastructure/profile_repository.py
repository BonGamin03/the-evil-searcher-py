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

    

    def upsert_profile(self, email: str, embedding: list[float],ALPHA=0.1) -> None:
         
        existing = self.get_profile(email)

        if existing is None:
            new_embedding = embedding
            new_count = 1
        else:
            prev = np.array(existing["embedding"])
            curr = np.array(embedding)
            # EMA: perfil_nuevo = α * query_actual + (1-α) * perfil_anterior
            new_embedding_np = ALPHA * curr + (1 -ALPHA) * prev
            # Re-normalizar para mantener en la esfera unitaria
            # (importante para que la distancia coseno funcione bien)
            norm = np.linalg.norm(new_embedding_np)
            new_embedding = (new_embedding_np / norm).tolist() if norm > 0 else new_embedding_np.tolist()
            new_count = existing["metadata"].get("query_count", 1) + 1

        final_metadata = { "query_count": new_count}

        self._collection.upsert(
            ids=[email],
            embeddings=[new_embedding],
            metadatas=[final_metadata],
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
                    "metadata": result["metadatas"][0],
                }
        except Exception:
            pass
        return None

     
 