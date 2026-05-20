from typing import Any
import scrapy
from scrapy.http import Response
from ..date_extractor import DateFinderInHTML, DateExtractor

class TudnSpider(scrapy.Spider):
    name = 'tudn_spider'
    allowed_domains = ['tudn.com']
    
    # Start URLs basadas en las secciones de fútbol de TUDN
    start_urls = [
        'https://www.tudn.com/futbol/liga-mx',
        'https://www.tudn.com/futbol/uefa-champions-league',
        'https://www.tudn.com/futbol/seleccion-mexico',
        'https://www.tudn.com/futbol/premier-league',
        'https://www.tudn.com/futbol/copa-america',
        'https://www.tudn.com/futbol/la-liga',
        'https://www.tudn.com/futbol/mls'
    ]

    def parse(self, response):

        if response.status in [500, 503, 504]:
            self.logger.error(f"Error {response.status} en {response.url}. Saltando...")
            return 
        
        liga = response.url.split('/')[-1].replace('-', ' ').title()
        
        enlaces_noticias = response.css('a[href*="/futbol/"]::attr(href)').getall()

        for url in enlaces_noticias:
            
            if any(substring in url for substring in ['resultados', 'posiciones', 'equipos', 'calendario']):
                continue
                
            yield response.follow(url, callback=self.parse_news, cb_kwargs={'liga': liga})

    def parse_news(self, response, liga):

        titulo = response.css('h1::text').get()
        entradilla = response.css('h2::text, .article-subheadline::text').get()
        parrafos_raw = response.css('div.articleBody p')
        
        texto_limpio = []
        for p in parrafos_raw:

            texto_parrafo = "".join(p.xpath('.//text()').getall()).strip()
            if texto_parrafo:

                if len(texto_parrafo) > 10:
                    texto_limpio.append(texto_parrafo)
        if entradilla:
            texto_limpio.insert(0, entradilla.strip())

        # Extraer fecha
        fecha = self._extract_publication_date(response)

        # Condicion para filtar noticias poco documentadas y anuncios 
        if len(texto_limpio) > 2:
            yield {
                'liga': liga,
                'titular': titulo.strip() if titulo else None,
                'url': response.url,
                'texto_noticia': texto_limpio,
                'fecha_publicacion': fecha
            }
    
    def _extract_publication_date(self, response: Response) -> str:
        """
        Extrae la fecha de publicación de TUDN
        """
        # 1. Intentar con JSON-LD primero (más confiable)
        fecha = DateFinderInHTML.find_in_json_ld(response)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 2. Intentar con meta tags
        fecha = DateFinderInHTML.find_in_meta_tags(response)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 3. Selectores específicos de TUDN
        selectors_tudn = [
            'time::attr(datetime)',
            'span.articleDate::text',
            'span[class*="published"]::text',
            'span[class*="date"]::text',
            'span[class*="time"]::text',
            'div.article-date::text',
            'p.article-date::text',
        ]
        
        fecha = DateFinderInHTML.find_in_common_selectors(response, selectors_tudn)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 4. Buscar en metadata del artículo
        article_info = " ".join(response.css('div[class*="article__info"] ::text, div[class*="article__meta"] ::text').getall())
        if article_info:
            fecha = DateExtractor.extract_date(article_info)
            if fecha:
                return DateExtractor.format_date(fecha)
        
        return None