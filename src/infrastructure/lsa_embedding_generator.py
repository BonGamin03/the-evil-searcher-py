import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from domain.document import Document
from domain.i_embedding_generator import IEmbeddingGenerator

class LSAEmbeddingGenerator(IEmbeddingGenerator):
    def __init__(self, documents: list[Document], n_components: int = 100): #hay que ver cual es la cantidad de componentes ideales 
        self.model_path = "./lsaModel"
        self.vectorizer_file = os.path.join(self.model_path, "vectorizer.joblib")
        self.svd_file = os.path.join(self.model_path, "svd.joblib")

        if os.path.exists(self.vectorizer_file) and os.path.exists(self.svd_file):
            self.load_model()
        elif documents is not None :
            self.train_save(documents, n_components)
        else:
            raise ValueError("No se encontraron modelos guardados ni se a proporcionaron documentos para entrenar.")

    def train_save(self, documents: list[Document], n_components: int):
        corpus = [doc.get_full_text() for doc in documents]

        self.vectorizer = TfidfVectorizer()
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        
        n_components = min(n_components, tfidf_matrix.shape[1] - 1)
        self.svd = TruncatedSVD(n_components=n_components)
        self.svd.fit(tfidf_matrix)

        #Guardar modelo
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(self.vectorizer, self.vectorizer_file)
        joblib.dump(self.svd, self.svd_file)

    def load_model(self):
        self.vectorizer = joblib.load(self.vectorizer_file)
        self.svd = joblib.load(self.svd_file)

    def text_to_embedding(self, text: str) -> list[float]:
        tfidf_vector = self.vectorizer.transform([text])
        lsa_vector = self.svd.transform(tfidf_vector)
        return lsa_vector[0].tolist()

    def document_to_embedding(self, document: Document) -> list[float]:
        return self.text_to_embedding(document.get_full_text())
    