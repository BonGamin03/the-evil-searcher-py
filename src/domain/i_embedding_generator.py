from abc import ABC, abstractmethod
from domain.document import *

class IEmbeddingGenerator(ABC) :

    @abstractmethod
    def document_to_embedding(document:Document) -> list[float]:
        pass
    
    @abstractmethod
    def text_to_embedding(text:str) -> list[float]:
        pass

    
    
