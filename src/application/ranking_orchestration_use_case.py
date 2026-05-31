from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from datetime import datetime
import re
from enum import Enum
from domain.document import Document
from domain.i_document_processor import IDocumentProcessor
from domain.i_re_rank_llm_context import IReRankLLMContext
from domain.local_ranking_calc import LocalRankingCalculator
from domain.organic_ranking_calc import OrganicRankingCalculator
from domain.ranking_score import ContentType, RankingScore
from application.snippet_extractor_use_case import FeaturedSnippetExtractor
 
class RankingOrchestrationUseCase:
     
    def __init__(self,
                 document_processor: IDocumentProcessor,
                 re_rank_model: IReRankLLMContext):
        self.organic_calculator = OrganicRankingCalculator()
        self.local_calculator = LocalRankingCalculator()
        self.snippet_extractor = FeaturedSnippetExtractor(re_rank_model)
        self.document_processor = document_processor

    def execute(self,
                documents: List[Document],
                query: str,
                probabilistic_scores: List[Tuple[Document, float]] = None,
                user_location: str = None) -> List[RankingScore]:
        
        ranking_scores = []
        prob_scores_dict = {doc.id: score for doc, score in probabilistic_scores} if probabilistic_scores else {}

        for document in documents:
            
            relevance_score = prob_scores_dict.get(document.id,0)
            ranking = self.organic_calculator.calculate_organic_rank(document,relevance_score)
            local_bonus = self.local_calculator.calculate_local_relevance(document,user_location)
            ranking.final_score += local_bonus
            #snippet, confidence = self.snippet_extractor.extract_featured_snippet(query,document)
            #ranking.featured_snippet = snippet
            #ranking.snippet_confidence = confidence
            ranking.content_type = self._classify_content_type(document)
            ranking_scores.append(ranking)

         
        ranking_scores.sort(key=lambda x: x.final_score, reverse=True)

        return ranking_scores

    def _classify_content_type(self, document: Document) -> ContentType:
        """Clasifica el tipo de contenido basado en URL y título"""
        url_lower = document.url.lower()
        title_lower = document.title.lower()
        content_lower = " ".join(document.content).lower() if document.content else ""

        if 'directo' in url_lower or 'live' in url_lower or 'en vivo' in title_lower:
            return ContentType.LIVE_UPDATE
        elif 'análisis' in title_lower or 'análisis' in content_lower or 'opinión' in content_lower:
            return ContentType.ANALYSIS
        elif 'estadísticas' in title_lower or 'estadísticas' in content_lower or 'stats' in url_lower:
            return ContentType.STATISTICS
        else:
            return ContentType.NEWS
