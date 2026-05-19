from dataclasses import dataclass
from enum import Enum
from typing import Optional
from document import Document


class ContentType(Enum):
    """Types of Content (only news for now) """
    NEWS = "news"
    ANALYSIS = "analysis"
    LIVE_UPDATE = "live"
    STATISTICS = "stats"


@dataclass
class RankingScore:
    """Scoring for each doc"""
    document: Document
    relevance_score: float  # Score del modelo probabilístico (0-100)
    authority_score: float  # Autoridad del dominio (0-100)
    freshness_score: float  # Recencia del contenido (0-100)
    final_score: float  # Score final ponderado
    ranking_type: str  # "organic", "local"
    featured_snippet: Optional[str] = None  # Fragmento destacado
    snippet_confidence: float = 0.0  # Confianza del snippet
    content_type: ContentType = ContentType.NEWS