"""
Utilidades simples para extracción de fechas sin dependencias Scrapy
"""
import re
from datetime import datetime, timedelta
from typing import Optional


class SimpleeDateExtractor:
    """Extrae fechas de texto sin dependencias externas"""
    
    MESES_ES = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12,
        'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5,
        'jun': 6, 'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10,
        'nov': 11, 'dic': 12
    }
    
    @staticmethod
    def extract_date(text: str) -> Optional[str]:
        """
        Extrae fecha del texto y retorna en formato YYYY-MM-DD
        o None si no encuentra
        """
        if not text:
            return None
        
        text = str(text).strip().lower()
        
        # Patrón ISO: YYYY-MM-DD
        iso_match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', text)
        if iso_match:
            year, month, day = iso_match.groups()
            try:
                date_obj = datetime(int(year), int(month), int(day))
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                pass
        
        # Patrón: "5 de mayo de 2026" o "5 mayo 2026"
        pattern1 = r'(\d{1,2})\s+(?:de\s+)?(\w+)(?:\s+de)?\s+(\d{4})'
        match = re.search(pattern1, text)
        if match:
            day, month_str, year = match.groups()
            month = SimpleeDateExtractor.MESES_ES.get(month_str.lower())
            if month:
                try:
                    date_obj = datetime(int(year), month, int(day))
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    pass
        
        # Patrón: "05/05/2026"
        pattern2 = r'(\d{1,2})/(\d{1,2})/(\d{4})'
        match = re.search(pattern2, text)
        if match:
            day, month, year = match.groups()
            try:
                date_obj = datetime(int(year), int(month), int(day))
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                pass
        
        # Patrón: "5 de mayo" (asumir año actual)
        pattern3 = r'(\d{1,2})\s+(?:de\s+)?(\w+)(?:\s+de)?$'
        match = re.search(pattern3, text)
        if match:
            day, month_str = match.groups()
            month = SimpleeDateExtractor.MESES_ES.get(month_str.lower())
            if month:
                try:
                    date_obj = datetime(datetime.now().year, month, int(day))
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    pass
        
        return None
