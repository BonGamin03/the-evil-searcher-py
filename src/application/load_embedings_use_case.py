from  domain.i_embedding_generator import IEmbeddingGenerator
from domain.i_vector_repository import IVectorRepository

class LoadEmbeddingsUseCase:
    def __init__(self, document_repository , embedding_generator: IEmbeddingGenerator, vector_repository : IVectorRepository):
        self.document_repository = document_repository
        self.embedding_generator = embedding_generator
        self.vector_repository = vector_repository

    def execute(self):
        documents = self.document_repository.get_all_documents()
        for doc in documents:
            embedding = self.embedding_generator.document_to_embedding(doc)
            self.vector_repository.upsert(doc.id, embedding)
    

        