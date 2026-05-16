from  domain.i_embedding_generator import IEmbeddingGenerator
from domain.i_vector_repository import IVectorRepository
from domain.document import Document 

class LoadEmbeddingsUseCase:
    def __init__(self, document_repository , embedding_generator: IEmbeddingGenerator, vector_repository : IVectorRepository):
        self.document_repository = document_repository
        self.embedding_generator = embedding_generator
        self.vector_repository = vector_repository

    def execute(self, documents : list[Document]):
        for doc in documents:
            
            i=0
            for chunk in doc.content:
                embedding = self.embedding_generator.text_to_embedding(chunk)
                self.vector_repository.upsert(doc.id, i, embedding)
                i+=1
                
        print("Carga de embeddings completada.")
    

        