from typing import Any
import scrapy
from scrapy.http import Response
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
                 yield response.follow(url, callback=self.parse_news, cb_kwargs={'liga': liga})

    def parse_news(self, response,liga):
     
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
        
         
        cuerpo_completo = " ".join(texto_limpio)
        noticia_final = f"{entradilla} {cuerpo_completo}" if entradilla else cuerpo_completo
        equipo = response.css('.ue-c-article__kicker::text').get()

        yield {
            'liga': liga,
            'equipo': equipo.strip() if equipo else 'Genérico',
            'titular': titulo.strip() if titulo else None,
            'url': response.url,
            'texto_noticia': noticia_final.strip()
        }