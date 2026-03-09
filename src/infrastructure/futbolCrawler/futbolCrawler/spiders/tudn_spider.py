from typing import Any
import scrapy
from scrapy.http import Response

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
        
        cuerpo_completo = " ".join(texto_limpio)
        noticia_final = f"{entradilla} {cuerpo_completo}" if entradilla else cuerpo_completo
        
        # Condicion para filtar noticias poco documentadas y anuncios 
        if len(cuerpo_completo) > 100:
            yield {
                'liga': liga,
                'titular': titulo.strip() if titulo else None,
                'url': response.url,
                'texto_noticia': noticia_final.strip()
            }