from datetime import datetime
import re
from typing import List, Optional

from domain.document import Document
from domain.ranking_score import RankingScore


class OrganicRankingCalculator:
    """Calculate organic ranking based on many factors"""

    def __init__(self):
       
        self.weights = {
            'relevance': 0.50,
            'authority': 0.30,   
            'freshness': 0.20    # Activado el factor de frescura
        }

        # Base de datos de autoridad por dominio
        self.domain_authority = {
            'espn': 95,
            'espndeportes': 95,
            'marca': 95,
            'as': 95,
            'sport': 95,
            'tudn': 95,
            
        }

    def calculate_organic_rank(self, document: Document, relevance_score: float) -> RankingScore:
        """
        Calculate organic rank combining all factors.
        """
        authority = self.calculate_authority_score(document.url)
        freshness = self.calculate_freshness_score(document)

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
    
    def _extract_domain(self, url: str) -> str:
        """Domain from an url"""
        try:
            url = url.replace('https://', '').replace('http://', '')
            url = url.replace('www.', '')
            domain = url.split('/')[0]
            domain = url.split('.')[0]  
            return domain.lower()
        except:
            return "unknown"

    def calculate_authority_score(self, url: str) -> float:
        """
        Calculate authority score
        """
        domain = self._extract_domain(url)
        if domain in self.domain_authority:
            return self.domain_authority[domain]
        
        
        for known_domain, score in self.domain_authority.items():
            if known_domain in domain:
                return score * 0.9  # Subdomains 
        
        # Default
        return 50

    def parse_publication_date(self, date_str: str) -> Optional[datetime]:
        """
        Parsea una fecha en formato YYYY-MM-DD a datetime
        """
        if not date_str:
            return None
        
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            return None

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

    def calculate_freshness_score(self, document: Document) -> float:
        """
        Calculate freshness score using publication_date from document.
        Recently: 90-100
        Old: 20-40
        """
        date = None
        
        # Primero intenta usar la fecha de publicación del documento (más confiable)
        if document.publication_date:
            date = self.parse_publication_date(document.publication_date)
        
        # Si no hay fecha en metadata, intenta extraerla del contenido
        if not date:
            date = self.extract_date_from_text(document.content)
        
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

