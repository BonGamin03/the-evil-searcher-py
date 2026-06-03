from domain.i_embedding_generator import IEmbeddingGenerator
from sentence_transformers import SentenceTransformer
from domain.document import Document 

class HGEmbeddingGen(IEmbeddingGenerator):
    def __init__(self):
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def document_to_embedding(self,document :  Document) -> list[float]: 
        full_text = document.get_full_text()
        return self.text_to_embedding(full_text)

    def text_to_embedding(self, text : str) -> list[float]:
        return self.embedding_model.encode(text).tolist()
  

    