from abc import ABC, abstractmethod
from document import Document

class IDocumentProcessor(ABC):
    @abstractmethod
    def process_document(self,doc:Document)->list[str]:
        pass
