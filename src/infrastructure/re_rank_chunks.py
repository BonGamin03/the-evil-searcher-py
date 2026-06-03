from sentence_transformers import CrossEncoder
from domain.i_re_rank_llm_context import IReRankLLMContext
class ReRankCTexts(IReRankLLMContext):
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def re_rank_results(self ,query : str, retrieved_text : list[str]) -> list[tuple[float,str]]:    

        pairs = [[query, chunk] for chunk in retrieved_text]
        
        # Obtenemos las puntuaciones de relevancia
        scores = self.model.predict(pairs).tolist()

        # Combinamos los chunks con sus puntuaciones y ordenamos
        scored_results = sorted(zip(scores, retrieved_text), key=lambda x: x[0], reverse=True)
        
        # Devolvemos solo los textos ordenados (o podrías devolver también el score)
        return scored_results
