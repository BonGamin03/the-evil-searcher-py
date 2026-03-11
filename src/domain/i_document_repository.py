from abc import ABC, abstractmethod
from domain.document  import Document

class IDocumentRepository(ABC):
    @abstractmethod
    def save_document(self,title:str,league:str,url:str,content:str):
        pass

    @abstractmethod
    def get_all_documents(self)->list[Document]:
        pass

    @abstractmethod
    def get_document(self,id:str)->Document:
        pass