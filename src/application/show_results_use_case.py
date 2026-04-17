from domain.i_document_repository import IDocumentRepository
from domain.i_vector_repository import IVectorRepository
from domain.i_embedding_generator import IEmbeddingGenerator
from domain.document import Document

class ShowResultsUseCase:
    def __init__(
        self,
        document_repository: IDocumentRepository,
        vector_repository: IVectorRepository,
        embedding_generator: IEmbeddingGenerator
    ):
        self._document_repository = document_repository
        self._vector_repository = vector_repository
        self._embedding_generator = embedding_generator

    def execute(self, query: str) -> list[Document]:
        query_embedding = self._embedding_generator.text_to_embedding(query)

        vector_results =  self._vector_repository.query(query_embedding=query_embedding, k=10)
        if not vector_results:
            return [] #Aqui despues hacemos la busqueda con el modulo de hacer busquedas en linea 

        documents = []
        for result in vector_results:
            doc_id = result
            document = self._document_repository.get_document(doc_id)
            if document:
                documents.append(document)
        return documents