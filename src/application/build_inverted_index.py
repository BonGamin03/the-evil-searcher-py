from domain.i_document_repository import IDocumentRepository
from domain.i_document_processor import IDocumentProcessor
from domain.inverted_index import InvertedIndex
import joblib
import os
import sys

class BuildInvertedIndexUseCase:
    def __init__(self, doc_repo: IDocumentRepository, doc_processor: IDocumentProcessor, index_path: str = "inverted_index.joblib"):
        self.doc_repo = doc_repo
        self.doc_processor = doc_processor
        self.index_path = index_path
    
    def execute(self) -> InvertedIndex:
        # Si el índice ya existe en disco, lo cargamos
        if os.path.exists(self.index_path):
            print(f"Cargando índice desde {self.index_path}...")
            inverted_index = InvertedIndex()
            inverted_index._index = joblib.load(self.index_path)
            
            return inverted_index

        print("Construyendo índice desde cero...")
        inverted_index = InvertedIndex()
        docs = self.doc_repo.get_all_documents()
        for doc in docs:
            terms = self.doc_processor.process_document(doc)
            inverted_index.add_document(doc.id, terms)
        
        sys.setrecursionlimit(10000) 
        joblib.dump(inverted_index._index, self.index_path)
        
        return inverted_index

# class BuildInvertedIndexUseCase:
#     def __init__(self,doc_repo:IDocumentRepository,doc_processor:IDocumentProcessor):
#         self.doc_repo = doc_repo
#         self.doc_processor = doc_processor

    
#     def execute(self)->InvertedIndex:
#         inverted_index = InvertedIndex()
#         docs=self.doc_repo.get_all_documents()
#         for doc in docs:
#             terms = self.doc_processor.process_document(doc)
#             inverted_index.add_document(doc.id,terms)
#         return inverted_index