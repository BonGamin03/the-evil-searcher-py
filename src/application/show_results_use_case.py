from domain.i_document_repository import IDocumentRepository
from domain.i_vector_repository import IVectorRepository
from domain.i_embedding_generator import IEmbeddingGenerator
from domain.document import Document
from domain.inverted_index import InvertedIndex
from domain.i_document_processor import IDocumentProcessor
from domain.probabilistic_model import ProbabilisticModel
from domain.i_rag import IRAG

class ShowResultsUseCase:
    def __init__(
        self,
        document_repository: IDocumentRepository,
        inverted_index : InvertedIndex,
        document_procesor : IDocumentProcessor,
        vector_repository: IVectorRepository,
        embedding_generator: IEmbeddingGenerator,
        rag_model : IRAG
    ):
        self._document_repository = document_repository
        self.inverted_index = inverted_index
        self. document_procesor = document_procesor
        self._vector_repository = vector_repository
        self._embedding_generator = embedding_generator
        self._rag_model = rag_model

    def execute(self, query: str) -> tuple[list[Document], str]:
        query_embedding = self._embedding_generator.text_to_embedding(query)

        vector_results =  self._vector_repository.query(query_embedding=query_embedding, k=50)
        if not vector_results:
            return [], "No se encontraron resultados para la búsqueda."

        documents = []
        fetched_docs = {}  # Caché para no consultar la base de datos por el mismo documento
        context_chunks = []

        for result in vector_results:

            doc_id = result[0]
            chunk_id = result[1]
            
            if len(fetched_docs) >= 10:
                break

            if doc_id not in fetched_docs:
                doc = self._document_repository.get_document(doc_id)
       
                fetched_docs[doc_id] = doc
                documents.append(doc) 
            
            document = fetched_docs.get(doc_id)
            context_chunks.append(document.content[chunk_id])

        model = ProbabilisticModel(self.inverted_index,self.document_procesor)

        documents = [x for x in model.calculate_similarity(query, documents)]

        # Preparar contexto y consultar al RAG
        context_str = "\n...\n".join(context_chunks)

        rag_response = self._rag_model.generate_response(query=query, context=context_str)

        return documents, rag_response