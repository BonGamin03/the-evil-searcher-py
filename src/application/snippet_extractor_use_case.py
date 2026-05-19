
from typing import Tuple
from document import Document
from i_re_rank_llm_context import IReRankLLMContext


class FeaturedSnippetExtractor:
   

    def __init__(self, re_rank_model: IReRankLLMContext):
        self.re_rank_model = re_rank_model

    #Observar latencia OOJO
    def extract_featured_snippet(self,query: str,document: Document,max_length: int = 160) -> Tuple[str, float]:
        """
         Extract the most relevant snippet on doc
        """
        
        scored_results = self.re_rank_model.re_rank_results(query,document.content )
         
        best_score, best_snippet = scored_results[0]

        if len(best_snippet) > max_length:
            truncated = best_snippet[:max_length]
             
            truncated = truncated.rsplit(' ', 1)[0] + "..."
        else:
            truncated = best_snippet

        # Normalizar score de -1 a 1 a 0 a 1
        confidence = (float(best_score) + 1) / 2 if best_score else 0.5

        return truncated, confidence
