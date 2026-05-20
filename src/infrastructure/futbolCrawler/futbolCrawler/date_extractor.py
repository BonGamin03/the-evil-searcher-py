"""
Utilidades para extracción y normalización de fechas
en noticias de fútbol
"""
import re
from datetime import datetime, timedelta
from typing import Optional

class DateExtractor:
    """Extrae y normaliza fechas de diferentes formatos"""
    
    MESES_ES = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12,
        'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5,
        'jun': 6, 'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10,
        'nov': 11, 'dic': 12
    }
    
    @staticmethod
    def parse_spanish_date(text: str) -> Optional[datetime]:
        """
        Parse fechas en español como:
        - "5 de mayo de 2026"
        - "5 mayo 2026"
        - "05/05/2026"
        """
        if not text:
            return None
        
        text = text.strip().lower()
        
        # Patrón: "5 de mayo de 2026" o "5 mayo de 2026"
        pattern1 = r'(\d{1,2})\s+(?:de\s+)?(\w+)(?:\s+de)?\s+(\d{4})'
        match = re.search(pattern1, text)
        if match:
            day, month_str, year = match.groups()
            month = DateExtractor.MESES_ES.get(month_str.lower())
            if month:
                try:
                    return datetime(int(year), month, int(day))
                except (ValueError, KeyError):
                    pass
        
        # Patrón: "05/05/2026"
        pattern2 = r'(\d{1,2})/(\d{1,2})/(\d{4})'
        match = re.search(pattern2, text)
        if match:
            day, month, year = match.groups()
            try:
                return datetime(int(year), int(month), int(day))
            except ValueError:
                pass
        
        # Patrón: "2026-05-05"
        pattern3 = r'(\d{4})-(\d{1,2})-(\d{1,2})'
        match = re.search(pattern3, text)
        if match:
            year, month, day = match.groups()
            try:
                return datetime(int(year), int(month), int(day))
            except ValueError:
                pass
        
        return None
    
    @staticmethod
    def parse_relative_date(text: str) -> Optional[datetime]:
        """
        Parse fechas relativas como:
        - "hace 2 horas"
        - "hace 1 día"
        - "ayer"
        - "hoy"
        """
        if not text:
            return None
        
        text = text.strip().lower()
        now = datetime.now()
        
        # Casos especiales
        if 'hoy' in text or 'ahora' in text:
            return now
        
        if 'ayer' in text or 'hace 1 día' in text or 'hace un día' in text:
            return now - timedelta(days=1)
        
        # Patrón: "hace X horas/días/minutos"
        pattern = r'hace\s+(\d+)\s+(hora|horas|día|días|minuto|minutos|semana|semanas)'
        match = re.search(pattern, text)
        if match:
            cantidad, unidad = match.groups()
            cantidad = int(cantidad)
            
            if 'minuto' in unidad:
                return now - timedelta(minutes=cantidad)
            elif 'hora' in unidad:
                return now - timedelta(hours=cantidad)
            elif 'día' in unidad:
                return now - timedelta(days=cantidad)
            elif 'semana' in unidad:
                return now - timedelta(weeks=cantidad)
        
        return None
    
    @staticmethod
    def extract_date(text: str) -> Optional[datetime]:
        """
        Intenta extraer fecha en cualquier formato.
        Retorna datetime o None.
        """
        if not text:
            return None
        
        # Intentar formato español absoluto primero
        date = DateExtractor.parse_spanish_date(text)
        if date:
            return date
        
        # Luego formato relativo
        date = DateExtractor.parse_relative_date(text)
        if date:
            return date
        
        # Intentar con dateutil si está disponible (fallback)
        try:
            from dateutil import parser
            return parser.parse(text, fuzzy=True)
        except:
            pass
        
        return None
    
    @staticmethod
    def format_date(date: Optional[datetime]) -> Optional[str]:
        """Formatea fecha a string 'YYYY-MM-DD'"""
        if date:
            return date.strftime('%Y-%m-%d')
        return None


class DateFinderInHTML:
    """
    Busca fechas en elementos HTML comunes
    """
    
    @staticmethod
    def find_in_common_selectors(response, selectors_list: list) -> Optional[datetime]:
        """
        Intenta encontrar fecha usando una lista de selectores CSS
        
        Args:
            response: Response de Scrapy
            selectors_list: Lista de selectores CSS a intentar
        
        Returns:
            datetime o None
        """
        for selector in selectors_list:
            text = response.css(selector).get()
            if text:
                # Limpiar HTML tags si existen
                text = re.sub(r'<[^>]+>', '', text)
                date = DateExtractor.extract_date(text)
                if date:
                    return date
        
        return None
    
    @staticmethod
    def find_in_meta_tags(response) -> Optional[datetime]:
        """
        Busca fecha en meta tags comunes
        (article:published_time, datePublished, etc.)
        """
        meta_attrs = [
            'article:published_time',
            'datePublished',
            'publish_date',
            'DC.date.created',
            'date'
        ]
        
        for attr in meta_attrs:
            value = response.css(f'meta[property="{attr}"]::attr(content)').get()
            if not value:
                value = response.css(f'meta[name="{attr}"]::attr(content)').get()
            
            if value:
                date = DateExtractor.extract_date(value)
                if date:
                    return date
        
        return None
    
    @staticmethod
    def find_in_json_ld(response) -> Optional[datetime]:
        """
        Busca fecha en JSON-LD (schema.org)
        """
        import json
        
        json_ld = response.css('script[type="application/ld+json"]::text').getall()
        
        for script in json_ld:
            try:
                data = json.loads(script)
                
                # Buscar datePublished
                if isinstance(data, dict):
                    for key in ['datePublished', 'publishedDate', 'dateModified']:
                        if key in data:
                            date = DateExtractor.extract_date(data[key])
                            if date:
                                return date
                
                # Si es un array, iterar
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            for key in ['datePublished', 'publishedDate', 'dateModified']:
                                if key in item:
                                    date = DateExtractor.extract_date(item[key])
                                    if date:
                                        return date
            except (json.JSONDecodeError, TypeError):
                pass
        
        return None
