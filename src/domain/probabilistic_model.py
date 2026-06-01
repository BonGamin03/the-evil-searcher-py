import math
from domain.document import Document
from domain.inverted_index import InvertedIndex
from domain.i_document_processor import IDocumentProcessor

class ProbabilisticModel:
    def __init__(self, inverted_index: InvertedIndex, document_processor: IDocumentProcessor):
        self.vocab = set(inverted_index._index.keys())
        self.ni = {term: inverted_index._index[term].size for term in self.vocab}
        self.document_processor = document_processor

        
        self._weights: dict[str, float] = {}

    
    def _compute_weight(self, p: float, u: float) -> float:
         
        p = max(0.01, min(0.99, p))
        u = max(0.01, min(0.99, u))
        return math.log(p / (1 - p)) + math.log((1 - u) / u)

  
    def _initialize_weights(self, query_terms: set[str], N: int) -> None:
        
        for term in query_terms:
            if term in self.vocab:
                p = 0.5
                u = self.ni[term] / N
                self._weights[term] = self._compute_weight(p, u)

   
    def _score_document(self, doc_terms: set[str], query_terms: set[str]) -> float:
        
        return sum(
            self._weights[term]
            for term in query_terms
            if term in doc_terms and term in self._weights
        )

   
    def _recompute_weights(self,query_terms: set[str],top_k_docs: list[tuple[Document, float]],N: int,k: int = 5) -> None:
        
        N_rel = min(k, len(top_k_docs))
        relevant_docs = [doc for doc, _ in top_k_docs[:N_rel]]

        for term in query_terms:
            if term not in self.vocab:
                continue

             
            vri = sum(
                1 for doc in relevant_docs
                if term in set(self.document_processor.process_document(doc))
            )

            p = (vri + 0.5) / (N_rel + 1)
            u = (self.ni[term] - vri + 0.5) / (N - N_rel + 1)
            self._weights[term] = self._compute_weight(p, u)

     
    def _rank_documents(self, query_terms: set[str], documents: list[Document]) -> list[tuple[Document, float]]:
         
        results = []
        for doc in documents:
            doc_terms = set(self.document_processor.process_document(doc))
            score = self._score_document(doc_terms, query_terms)
            results.append((doc, score))

        
        return sorted(results, key=lambda x: x[1], reverse=True)

    
    def calculate_similarity(self, query: str, documents: list[Document]) -> list[tuple[Document, float]]:
        
        N = len(documents)
        query_terms = set(self.document_processor.process_query(query))

        # 1. Pesos iniciales
        self._initialize_weights(query_terms, N)

        # 2. Ranking inicial
        current_ranking = self._rank_documents(query_terms, documents)

        # 3. Pseudo Relevance Feedback iterativo
        max_iter = 10
        for _ in range(max_iter):
            self._recompute_weights(query_terms, current_ranking, N, k=5)
            new_ranking = self._rank_documents(query_terms, documents)

            # Criterio de convergencia: el orden de los documentos no cambió
            # Decisión: comparamos solo los doc IDs, no los scores,
            # porque los scores pueden cambiar levemente sin alterar el orden.
            if [d.id for d, _ in new_ranking] == [d.id for d, _ in current_ranking]:
                break

            current_ranking = new_ranking

        # 4. Resetear pesos para la próxima query
        self._weights = {}

        return current_ranking