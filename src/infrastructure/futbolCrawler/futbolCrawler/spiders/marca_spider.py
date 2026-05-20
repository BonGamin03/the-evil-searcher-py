from typing import Any
import scrapy
from scrapy.http import Response
from futbolCrawler.date_extractor import DateFinderInHTML, DateExtractor

class MarcaSpider(scrapy.Spider):
    name='marca_spider'
    allowed_domains=['marca.com']
    start_urls=['https://www.marca.com/futbol/primera-division.html',
                'https://www.marca.com/futbol/premier-league.html',
                'https://www.marca.com/futbol/bundesliga.html',
                'https://www.marca.com/futbol/champions-league.html',
                'https://www.marca.com/futbol/liga-italiana.html',
                'https://www.marca.com/futbol/liga-francesa.html',
                'https://www.marca.com/futbol/europa-league.html',
                'https://www.marca.com/futbol/mundial.html']
    

    def parse(self, response):
         
        liga = response.url.split('/')[-1].replace('.html', '').title()
        enlaces_noticias = response.css('article a.ue-c-cover-content__link::attr(href)').getall()

        for url in enlaces_noticias:
             if 'marca.com' in url:
                 yield response.follow(url, callback=self.parse_news , cb_kwargs={'liga': liga})

    def parse_news(self, response, liga):
     
        titulo = response.css('h1.ue-c-article__headline::text').get()
        entradilla = response.css('p.ue-c-article__standfirst::text').get()
        parrafos_raw = response.css('div.ue-c-article__body p')
        
        texto_limpio = []
        for p in parrafos_raw:
            # EXPLICACIÓN: 'xpath(".//text()")' extrae el texto de P y de TODOS sus hijos (strong, a, em, etc.)
            # Luego los unimos para que no queden huecos.
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
        Extrae la fecha de publicación de Marca
        """
        # 1. Intentar con JSON-LD primero (más confiable)
        fecha = DateFinderInHTML.find_in_json_ld(response)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 2. Intentar con meta tags
        fecha = DateFinderInHTML.find_in_meta_tags(response)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 3. Selectores específicos de Marca
        selectors_marca = [
            'time::attr(datetime)',
            'span.ue-c-article__publication-date::text',
            'div.ue-c-article__publication-info span::text',
            'span[class*="date"]::text',
            'span[class*="time"]::text',
            'div.article-date::text',
        ]
        
        fecha = DateFinderInHTML.find_in_common_selectors(response, selectors_marca)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 4. Buscar en metadata y atributos
        header_text = " ".join(response.css('div[class*="article__header"] ::text, div[class*="publication"] ::text').getall())
        if header_text:
            fecha = DateExtractor.extract_date(header_text)
            if fecha:
                return DateExtractor.format_date(fecha)
        
        return None