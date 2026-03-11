from domain.document import Document
from domain.i_document_processor import IDocumentProcessor
import spacy
import es_core_news_sm
class DocumentProcessor(IDocumentProcessor):
        def __init__(self) -> None:
                self.nlp=es_core_news_sm.load()
        
        def process_document(self, doc: Document) -> list[str]:
                """
                Process a text and return normalized tokens
        
                Args:
                doc: Document. Document to process
                
                Returns:
                list. List of words 
                """
                text = self.nlp(doc.get_full_text())
                terms = []

                for token in text:
                        if token.is_punct or token.is_space:
                                continue
                
                        if token.is_stop:
                                continue
                
                        term = token.lemma_
                        term = term.lower()
                        terms.append(term)

                return terms
                
