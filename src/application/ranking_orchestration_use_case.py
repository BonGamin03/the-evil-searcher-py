from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from datetime import datetime
import re
from enum import Enum
from domain.document import Document
from domain.i_document_processor import IDocumentProcessor
from domain.i_re_rank_llm_context import IReRankLLMContext


class ContentType(Enum):
    """Tipos de contenido para clasificación"""
    NEWS = "news"
    ANALYSIS = "analysis"
    LIVE_UPDATE = "live"
    STATISTICS = "stats"


@dataclass
class RankingScore:
    """Estructura de scoring para cada documento"""
    document: Document
    relevance_score: float  # Score del modelo probabilístico (0-100)
    authority_score: float  # Autoridad del dominio (0-100)
    freshness_score: float  # Recencia del contenido (0-100)
    final_score: float  # Score final ponderado
    ranking_type: str  # "organic", "local"
    featured_snippet: Optional[str] = None  # Fragmento destacado
    snippet_confidence: float = 0.0  # Confianza del snippet
    content_type: ContentType = ContentType.NEWS


class OrganicRankingCalculator:
    """Calcula posicionamiento orgánico (natural) basado en múltiples factores"""

    def __init__(self):
        # Pesos para la combinación de factores
        self.weights = {
            'relevance': 0.50,   # BIM score
            'authority': 0.30,   # Autoridad del dominio
            'freshness': 0.20    # Antigüedad del contenido
        }

        # Base de datos de autoridad por dominio
        self.domain_authority = {
            'espn.com': 95,
            'espndeportes.espn.com': 90,
            'marca.es': 85,
            'as.com': 85,
            'sport.es': 80,
            'tudn.com': 75,
            'fox-sports.com': 80,
            'goal.com': 75,
            'transfermarkt.es': 70,
            'wikipedia.org': 90,
        }

    def _extract_domain(self, url: str) -> str:
        """Extrae el dominio de una URL"""
        try:
            # Remover protocolo
            url = url.replace('https://', '').replace('http://', '')
            # Remover 'www.'
            url = url.replace('www.', '')
            # Tomar solo el dominio principal
            domain = url.split('/')[0]
            return domain.lower()
        except:
            return "unknown"

    def calculate_authority_score(self, url: str) -> float:
        """
        Calcula el score de autoridad del dominio.
        Utiliza una base de datos de dominios conocidos.
        """
        domain = self._extract_domain(url)
        
        # Buscar match exacto
        if domain in self.domain_authority:
            return self.domain_authority[domain]
        
        # Buscar match parcial (p.ej. subdominios)
        for known_domain, score in self.domain_authority.items():
            if known_domain in domain:
                return score * 0.9  # Penalizar subdominios levemente
        
        # Default para dominios desconocidos pero válidos
        return 50

    def extract_date_from_text(self, content: List[str]) -> Optional[datetime]:
        """
        Intenta extraer la fecha de publicación del contenido.
        Busca patrones como "3 de mayo de 2026", "hace 2 horas", etc.
        """
        text = " ".join(content[:5])  # Primeros párrafos
        
        # Patrones de fecha en español
        date_patterns = [
            r'(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+de\s+(\d{4})',
            r'hace\s+(\d+)\s+(horas|días|minutos)',
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return datetime.now()  # Simplificado: solo detectar presencia
        
        return None

    def calculate_freshness_score(self, content: List[str]) -> float:
        """
        Calcula score de frescura basado en si hay fecha en el contenido.
        Reciente: 90-100
        Antiguo: 20-40
        """
        date = self.extract_date_from_text(content)
        
        if date:
            days_old = (datetime.now() - date).days
            
            if days_old <= 1:
                return 100.0
            elif days_old <= 7:
                return 90.0
            elif days_old <= 30:
                return 75.0
            elif days_old <= 90:
                return 50.0
            else:
                return 30.0
        
        # Si no hay fecha detectada, asumir contenido medio-fresco
        return 60.0

    def calculate_organic_rank(self,
                              document: Document,
                              relevance_score: float) -> RankingScore:
        """
        Calcula el ranking orgánico final combinando todos los factores.
        """
        authority = self.calculate_authority_score(document.url)
        freshness = self.calculate_freshness_score(document.content)

        # Fórmula ponderada
        final_score = (
            self.weights['relevance'] * (relevance_score / 100 * 100) +  # Normalizar a 0-100
            self.weights['authority'] * authority +
            self.weights['freshness'] * freshness
        )

        return RankingScore(
            document=document,
            relevance_score=relevance_score,
            authority_score=authority,
            freshness_score=freshness,
            final_score=final_score,
            ranking_type="organic"
        )


class LocalRankingCalculator:
    """Calcula posicionamiento local (geo-targeting)"""

    def __init__(self):
        # Mapeo de competiciones a ubicaciones
        self.league_locations = {
            'la-liga': 'Spain',
            'premier-league': 'England',
            'serie-a': 'Italy',
            'ligue-1': 'France',
            'bundesliga': 'Germany',
            'laliga': 'Spain',
            'english': 'England',
            'italian': 'Italy',
            'french': 'France',
            'german': 'Germany',
        }

    def calculate_local_relevance(self,
                                 document: Document,
                                 user_location: str = None) -> float:
        """
        Prioriza documentos de competiciones locales si el usuario
        está en una región específica.
        """
        league_lower = document.league.lower()
        
        # Buscar ubicación de la competición
        league_location = None
        for key, location in self.league_locations.items():
            if key in league_lower:
                league_location = location
                break
        
        if not league_location:
            return 0.0  # Sin información local
        
        if user_location and league_location == user_location:
            return 30.0  # Bonus para contenido local (+30 puntos)
        
        return 0.0


class FeaturedSnippetExtractor:
    """Extrae fragmentos destacados de los documentos"""

    def __init__(self, re_rank_model: IReRankLLMContext):
        self.re_rank_model = re_rank_model

    def extract_featured_snippet(self,
                                query: str,
                                document: Document,
                                max_length: int = 160) -> Tuple[str, float]:
        """
        Identifica el párrafo más relevante como snippet destacado.
        Usa reranking para encontrar la mejor coincidencia.
        """
        if not document.content:
            return "", 0.0

        # Usar el modelo de reranking para obtener mejor match
        scored_results = self.re_rank_model.re_rank_results(
            query,
            document.content
        )

        if not scored_results:
            return "", 0.0

        # Obtener el mejor resultado
        best_score, best_snippet = scored_results[0]

        # Truncar si es muy largo
        if len(best_snippet) > max_length:
            truncated = best_snippet[:max_length]
            # Truncar en límite de palabra
            truncated = truncated.rsplit(' ', 1)[0] + "..."
        else:
            truncated = best_snippet

        # Normalizar score de -1 a 1 a 0 a 1
        confidence = (float(best_score) + 1) / 2 if best_score else 0.5

        return truncated, confidence


class RankingOrchestrationUseCase:
    """
    Orquesta todos los tipos de posicionamiento y retorna
    resultados ordenados según ranking final.
    """

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
        """
        Ejecuta la orquestación de ranking:
        1. Calcula posicionamiento orgánico
        2. Aplica bonos locales si aplica
        3. Extrae fragmentos destacados
        4. Ordena por score final
        """
        ranking_scores = []

        # Si no tenemos scores probabilísticos, usamos scores por defecto
        if probabilistic_scores is None:
            probabilistic_scores = [(doc, 70.0) for doc in documents]

        # Crear diccionario para búsqueda rápida
        prob_scores_dict = {doc.id: score for doc, score in probabilistic_scores}

        for document in documents:
            # Obtener score probabilístico
            relevance_score = prob_scores_dict.get(document.id, 70.0)

            # Calcular ranking orgánico
            ranking = self.organic_calculator.calculate_organic_rank(
                document,
                relevance_score
            )

            # Aplicar bonus local si aplica
            local_bonus = self.local_calculator.calculate_local_relevance(
                document,
                user_location
            )
            ranking.final_score += local_bonus

            # Extraer fragmento destacado
            try:
                snippet, confidence = self.snippet_extractor.extract_featured_snippet(
                    query,
                    document
                )
                ranking.featured_snippet = snippet
                ranking.snippet_confidence = confidence
            except Exception as e:
                print(f"Error extrayendo snippet: {e}")
                ranking.featured_snippet = ""
                ranking.snippet_confidence = 0.0

            # Asignar tipo de contenido basado en URL/título
            ranking.content_type = self._classify_content_type(document)

            ranking_scores.append(ranking)

        # Ordenar por score final (descendente)
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
