import math
from domain.document import Document
from domain.inverted_index import InvertedIndex
from domain.i_document_processor import IDocumentProcessor

class ProbabilisticModel:
    def __init__(self, inverted_index: InvertedIndex , document_processor: IDocumentProcessor):
        self.vocab = inverted_index._index.keys()
        self.ni = {term: inverted_index._index[term].size for term in self.vocab}
        self.document_processor = document_processor
        
    def calculate_similarity(self, query :  str, documents : list[Document]) -> list[tuple[Document, float]]:
        
        N = len(documents)
        query_terms = set(self.document_processor.process_query(query))
        rankings = []

        for doc in documents:
            doc_terms = set(self.document_processor.process_document(doc))
            score = 0.0

            # Solo consideramos términos presentes en la consulta y el documento
            # según el Modelo de Independencia Binaria (w_{i,q} * w_{i,j})
            for term in query_terms:
                if term in doc_terms and term in self.vocab :
                    # Estimaciones iniciales según la fuente
                    p_ti_R = 0.5
                    p_ti_not_R = self.ni[term] / N
                    
                    # Evitar logaritmo de cero o división por cero
                    p_ti_not_R = max(0.01, min(0.99, p_ti_not_R))
                    
                    # Fórmula de log-odds
                    part1 = math.log10(p_ti_R / (1 - p_ti_R))
                    part2 = math.log10((1 - p_ti_not_R) / p_ti_not_R)
                    
                    score += (part1 + part2)
                
            rankings.append((doc, score))
        sorted_rankings = sorted(rankings, key=lambda x: x[1])

        return  sorted_rankings
    
    
