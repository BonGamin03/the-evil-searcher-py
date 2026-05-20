from typing import Any
import scrapy
from scrapy.http import Response
from futbolCrawler.date_extractor import DateFinderInHTML, DateExtractor

class EspnSpider(scrapy.Spider):
    name = 'espn_spider'
    allowed_domains = ['espndeportes.espn.com', 'espn.com']
    start_urls = [
        'https://espndeportes.espn.com/futbol/liga/_/nombre/esp.1/primera-division-de-espana',
        'https://espndeportes.espn.com/futbol/liga/_/nombre/eng.1/liga-premier',
        'https://espndeportes.espn.com/futbol/liga/_/nombre/ger.1/bundesliga',
        'https://espndeportes.espn.com/futbol/liga/_/nombre/uefa.champions/uefa-champions-league',
        'https://espndeportes.espn.com/futbol/liga/_/nombre/ita.1/serie-a-de-italia',
        'https://espndeportes.espn.com/futbol/liga/_/nombre/fra.1/ligue-1-francia',
        'https://espndeportes.espn.com/futbol/liga/_/nombre/uefa.europa/uefa-europa-league',
        'https://espndeportes.espn.com/futbol/mundial',
    ]

    ligas = {
        'Esp.1' : 'La Liga',
        'Eng.1' : 'Premier League',
        'Ger.1' : 'Bundesliga',
        'Uefa.Champions' : 'UEFA Champions League',
        'Ita.1' : 'Serie A',
        'Fra.1' : 'Ligue 1',
        'Uefa.Europa' : 'UEFA Europa League',
        'Mundial' : 'Mundial'
    }

    def parse(self, response: Response):
        url = response.url
        if '_/nombre/' in url:
            liga = self.ligas[url.split('_/nombre/')[-1].split('/')[0].replace('-', ' ').title()]
        else:
            liga = url.split('/')[-1].replace('-', ' ').title()

        enlaces_noticias = response.css('a.realStory::attr(href)').getall()

        for url_noticia in enlaces_noticias:
            
            if url_noticia.startswith('/'):
                url_noticia = 'https://espndeportes.espn.com' + url_noticia
            if 'espn.com' in url_noticia and '/nota/' in url_noticia:
                yield response.follow(
                    url_noticia,
                    callback=self.parse_news,
                    cb_kwargs={'liga': liga}
                )

    def parse_news(self, response: Response, liga: str):
        titulo = response.css('h1.article-header::text').get()
        entradilla = response.css('div.article-body h2::text').get()
        parrafos_raw = response.css('div.article-body p')

        texto_limpio = []

        for p in parrafos_raw:
            # Extraemos texto de P y todos sus hijos
            texto_parrafo = "".join(p.xpath('.//text()').getall()).strip()
            if texto_parrafo:
                texto_limpio.append(texto_parrafo)

        if entradilla:
            texto_limpio.insert(0, entradilla.strip())
        
        # Extraer fecha
        fecha = self._extract_publication_date(response)
        
        yield {
            'liga': liga,
            'titular': titulo.strip() if titulo else None,
            'url': response.url,
            'texto_noticia': texto_limpio,
            'fecha_publicacion': fecha
        }
    
    def _extract_publication_date(self, response: Response) -> str:
        """
        Extrae la fecha de publicación de ESPN
        """
        # 1. Intentar con JSON-LD primero (más confiable)
        fecha = DateFinderInHTML.find_in_json_ld(response)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 2. Intentar con meta tags
        fecha = DateFinderInHTML.find_in_meta_tags(response)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 3. Selectores específicos de ESPN
        selectors_espn = [
            'span.article-timestamp::text',
            'div.article-header span::text',
            'time::attr(datetime)',
            'span[data-date]::text',
            'span[class*="time"]::text',
        ]
        
        fecha = DateFinderInHTML.find_in_common_selectors(response, selectors_espn)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 4. Buscar en texto visible como último recurso
        header_text = " ".join(response.css('div.article-header ::text').getall())
        fecha = DateExtractor.extract_date(header_text)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        return None