import math
from domain.document import Document
from domain.inverted_index import InvertedIndex
from domain.i_document_processor import IDocumentProcessor

class ProbabilisticModel:
    def __init__(self, inverted_index: InvertedIndex, document_processor: IDocumentProcessor):
        self.vocab = set(inverted_index._index.keys())
        self.ni = {term: inverted_index._index[term].size for term in self.vocab}
        self.document_processor = document_processor

        # Persistimos los pesos entre iteraciones del pseudo feedback.
        # Empiezan vacíos y se inicializan en calculate_similarity.
        # Decisión: diccionario por término para O(1) de acceso.
        self._weights: dict[str, float] = {}

    # ─────────────────────────────────────────────
    # Cálculo del peso w(t) dado p y u
    # ─────────────────────────────────────────────
    def _compute_weight(self, p: float, u: float) -> float:
        """
        Fórmula log-odds del BIM:
            w(t) = log(p / 1-p) + log((1-u) / u)

        Decisión: método privado separado para poder reutilizarlo
        tanto en la inicialización como en el recompute del feedback,
        sin duplicar lógica.

        El clamp a [0.01, 0.99] evita log(0) e infinitos.
        Usamos log natural (math.log) en lugar de log10 porque
        el BIM está derivado con log natural — log10 solo escala
        los scores uniformemente pero es conceptualmente incorrecto.
        """
        p = max(0.01, min(0.99, p))
        u = max(0.01, min(0.99, u))
        return math.log(p / (1 - p)) + math.log((1 - u) / u)

    # ─────────────────────────────────────────────
    # Pesos iniciales (arranque en frío)
    # ─────────────────────────────────────────────
    def _initialize_weights(self, query_terms: set[str], N: int) -> None:
        """
        Sin información de relevancia previa:
            p = 0.5         →  no sabemos nada, asumimos 50/50
            u = ni[t] / N   →  frecuencia real del término en el corpus

        Decisión: inicializamos SOLO los términos de la query,
        no todo el vocabulario. El BIM solo necesita pesos de
        los términos presentes en la query para calcular RSV,
        y así ahorramos memoria y tiempo en vocabularios grandes.
        """
        for term in query_terms:
            if term in self.vocab:
                p = 0.5
                u = self.ni[term] / N
                self._weights[term] = self._compute_weight(p, u)

    # ─────────────────────────────────────────────
    # Score RSV de un documento dado la query
    # ─────────────────────────────────────────────
    def _score_document(self, doc_terms: set[str], query_terms: set[str]) -> float:
        """
        RSV(d, q) = Σ w(t)  para t en (query ∩ documento ∩ vocab)

        Decisión: solo sumamos términos que están en los tres conjuntos.
        - Si el término no está en la query: no aporta al RSV (BIM estándar).
        - Si no está en el documento: w_{i,j} = 0 en el modelo binario.
        - Si no está en el vocab: no tenemos ni[t], no podemos estimar u.
        """
        return sum(
            self._weights[term]
            for term in query_terms
            if term in doc_terms and term in self._weights
        )

    # ─────────────────────────────────────────────
    # Recompute de pesos con los top-k como relevantes
    # ─────────────────────────────────────────────
    def _recompute_weights(
        self,
        query_terms: set[str],
        top_k_docs: list[tuple[Document, float]],
        N: int,
        k: int = 5
    ) -> None:
        """
        Pseudo Relevance Feedback: asumimos que los top-k son relevantes.

            vri   = cuántos de los top-k contienen el término
            N_rel = k  (tamaño del conjunto relevante asumido)

            p = (vri + 0.5) / (N_rel + 1)   →  estimación suavizada de p(t|R)
            u = (ni[t] - vri + 0.5) / (N - N_rel + 1)  →  estimación de p(t|NR)

        Decisión del suavizado (+ 0.5 / + 1):
            Laplace smoothing — evita p=0 o p=1 cuando vri=0 o vri=N_rel.
            Sin esto, un término ausente en los top-k obtendría log(0) = -∞.

        Decisión de k=5:
            Valor clásico en literatura de PRF (Robertson & Sparck Jones).
            Suficiente señal sin incluir demasiado ruido de docs irrelevantes.

        Solo recomputamos términos de la query — mismo argumento que en
        _initialize_weights.
        """
        N_rel = min(k, len(top_k_docs))
        relevant_docs = [doc for doc, _ in top_k_docs[:N_rel]]

        for term in query_terms:
            if term not in self.vocab:
                continue

            # Contar cuántos docs relevantes contienen el término
            # Decisión: usamos process_document para ser consistentes
            # con el mismo pipeline de preprocesamiento usado en el índice.
            vri = sum(
                1 for doc in relevant_docs
                if term in set(self.document_processor.process_document(doc))
            )

            p = (vri + 0.5) / (N_rel + 1)
            u = (self.ni[term] - vri + 0.5) / (N - N_rel + 1)
            self._weights[term] = self._compute_weight(p, u)

    # ─────────────────────────────────────────────
    # Ranking completo
    # ─────────────────────────────────────────────
    def _rank_documents(
        self, query_terms: set[str], documents: list[Document]
    ) -> list[tuple[Document, float]]:
        """
        Genera el ranking completo del corpus para la query actual.

        Decisión: método separado de calculate_similarity para poder
        llamarlo tanto en la iteración inicial como en cada vuelta
        del pseudo feedback sin duplicar código.
        """
        results = []
        for doc in documents:
            doc_terms = set(self.document_processor.process_document(doc))
            score = self._score_document(doc_terms, query_terms)
            results.append((doc, score))

        # Descendente: mayor score = más relevante
        return sorted(results, key=lambda x: x[1], reverse=True)

    # ─────────────────────────────────────────────
    # Punto de entrada público
    # ─────────────────────────────────────────────
    def calculate_similarity(
        self, query: str, documents: list[Document]
    ) -> list[tuple[Document, float]]:
        """
        Pipeline completo con Pseudo Relevance Feedback:

            1. Inicializar pesos (arranque en frío)
            2. Ranking inicial
            3. Loop PRF hasta convergencia o max_iter
            4. Resetear pesos para la próxima query

        Decisión de max_iter=10:
            Cota de seguridad ante oscilaciones. En la práctica
            el ranking converge en 2-3 iteraciones.

        Decisión de resetear _weights al final:
            Los pesos del PRF son específicos a esta query.
            Si no reseteamos, la siguiente query arrancaría con
            pesos "contaminados" por la anterior.
        """
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