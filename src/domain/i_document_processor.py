from abc import ABC, abstractmethod
from domain.document import Document

class IDocumentProcessor(ABC):
    @abstractmethod
    def process_document(self,doc:Document)->list[str]:
        pass
