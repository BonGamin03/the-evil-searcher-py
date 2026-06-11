import numpy as np
from typing import Optional

from domain.i_profile_repository import IProfileRepository
from domain.i_document_repository import IDocumentRepository
from domain.i_vector_repository import IVectorRepository
from domain.i_user_repository import IUserRepository
from domain.i_embedding_generator import IEmbeddingGenerator


class UpdateUserProfileUseCase:
    
    def __init__(self,profile_repo: IProfileRepository,doc_repo: IDocumentRepository, vector_repo:IVectorRepository,
                 user_repo: IUserRepository, embedding_gen: IEmbeddingGenerator):
        self.profile_repo = profile_repo
        self.doc_repo = doc_repo
        self.vector_repo = vector_repo
        self.user_repo = user_repo
        self.embedding_gen = embedding_gen

    def execute(self,email: str,query:str) -> None:
        print(f"Updating profile for {email} with query: {query}")
        query_emb = self.embedding_gen.text_to_embedding(query)
        user=self.user_repo.get_by_email(email)
        read_doc_ids = user.read_docs if user and user.read_docs else []
        signal_vector = self._build_signal_vector(query_emb, read_doc_ids)
        if signal_vector is None:
            return
  
        self.profile_repo.upsert_profile(
            email=email,
            embedding=signal_vector.tolist(),
        )
        print("Finish")
    def _build_signal_vector(self, query_emb: list[float], read_doc_ids: list[int], W_QUERY=0.4, W_DOCS=0.6) -> Optional[np.ndarray]:
        components = []
        weights = []
         
        q_emb = np.array(query_emb)
        components.append(q_emb)
        weights.append(W_QUERY)

        if read_doc_ids:
            centroids_dict = self.vector_repo.get_doc_centroids_batch(read_doc_ids)
            if centroids_dict:
                 
                doc_vectors = np.array(list(centroids_dict.values()))   
                doc_centroid = doc_vectors.mean(axis=0)                 
                components.append(doc_centroid)
                weights.append(W_DOCS)

        weights_arr = np.array(weights)
        components_arr = np.array(components)   
        combined = np.sum(weights_arr[:, np.newaxis] * components_arr, axis=0)
        total_weight = np.sum(weights_arr)
        if total_weight > 0:
            combined = combined / total_weight

        norm = np.linalg.norm(combined)
        return combined / norm if norm > 0 else combined

 