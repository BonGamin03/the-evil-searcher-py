from domain.i_document_repository import IDocumentRepository
from domain.i_document_processor import IDocumentProcessor
from domain.inverted_index import InvertedIndex
from application.save_inverted_index import SaveInvertedIndexUseCase
import joblib
import os
import sys

class BuildInvertedIndexUseCase:
    def __init__(self, doc_repo: IDocumentRepository, doc_processor: IDocumentProcessor, index_path: str = "inverted_index.joblib"):
        self.doc_repo = doc_repo
        self.doc_processor = doc_processor
        self.index_path = index_path
    
    def execute(self) -> InvertedIndex:
         

        print("Construyendo índice desde cero...")
        inverted_index = InvertedIndex()
        docs = self.doc_repo.get_all_documents()
        for doc in docs:
            terms = self.doc_processor.process_document(doc)
            inverted_index.add_document(doc.id, terms)

         

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