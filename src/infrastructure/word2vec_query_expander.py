import os
import sys
from gensim.models import Word2Vec
from domain.i_query_expander import IQueryExpander
from domain.i_document_repository import IDocumentRepository
from domain.i_document_processor import IDocumentProcessor

class Word2VecQueryExpander(IQueryExpander):
    def __init__(
        self, 
        doc_repo: IDocumentRepository, 
        doc_processor: IDocumentProcessor, 
        model_path: str = "./w2v_model/w2v_futbol.model"
    ):
        self.doc_repo = doc_repo
        self.doc_processor = doc_processor
        self.model_path = model_path
        self.model = None
        self._load_or_train()

    def _load_or_train(self):
        """Carga el modelo de disco o lo entrena desde cero si no existe."""
        if os.path.exists(self.model_path):
            print(f"Cargando modelo Word2Vec desde {self.model_path}...")
            self.model = Word2Vec.load(self.model_path)
        else:
            self.train_model()

    def train_model(self):
        print("Entrenando modelo Word2Vec con el corpus de documentos...")
        docs = self.doc_repo.get_all_documents()
        
        # Procesamos cada documento usando tu DocumentProcessor para mantener 
        # las mismas reglas de limpieza (lematización, stopwords) que el índice
        corpus = [self.doc_processor.process_document(doc) for doc in docs]
        # Si no hay documentos, no entrenar
        corpus = [c for c in corpus if c]  # filtrar listas vacías
        if not corpus:
             
            self.model = None
            return
        
        # Entrenamos el modelo. 
        # vector_size=100 es ideal para corpus pequeños/medianos. window=5 es el contexto.
        self.model = Word2Vec(
            sentences=corpus, 
            vector_size= 40, 
            window=3, 
            min_count=2, # Ignora palabras que aparezcan menos de 2 veces
            workers=4,
            epochs=30
        )
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        sys.setrecursionlimit(10000000)
        self.model.save(self.model_path)
        print("Modelo Word2Vec entrenado y guardado con éxito.")

        print(self.model.wv.most_similar('lesión'))
        print(self.model.wv.most_similar('gol'))

    def expand_query(self, query: str, topn: int = 2) -> str:
        """Retorna la query original más sus sinónimos semánticos."""
        # Procesamos la query original para que coincida con el vocabulario
        query_terms = self.doc_processor.process_query(query)
        expanded_terms = set(query_terms)
        if self.model is None:
            return query
        for term in query_terms:
            if term in self.model.wv:
                # Buscamos los términos más cercanos en el espacio vectorial
                similares = self.model.wv.most_similar(term, topn=topn)
                for sim_term, score in similares:
                    if score > 0.65:  # Umbral de confianza para no meter basura
                        expanded_terms.add(sim_term)
        
        return " ".join(expanded_terms)