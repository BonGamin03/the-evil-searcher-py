import scrapy
from scrapy.http import Response
from futbolCrawler.date_extractor import DateFinderInHTML, DateExtractor

class AsSpider(scrapy.Spider):
    name = 'as_spider'
    allowed_domains = ['as.com']
    
    start_urls = [
        'https://as.com/futbol/primera/',
        'https://as.com/futbol/segunda/'
    ]

    def parse(self, response):
        liga = response.url.split('/')[-2].replace('_', ' ').title()
        
        enlaces_noticias = response.css('h3.s_t a::attr(href)').getall()

        for url in enlaces_noticias:
            yield response.follow(url, callback=self.parse_news, cb_kwargs={'liga': liga})

    def parse_news(self, response, liga):

        titulo = response.css('h1::text').get()
        entradilla = response.css('p.a_st::text').get()

        #Esto es para quitarnos el ultimo parrafo publicitario 
        parrafos_raw = response.xpath('//div[@class="a_c"]/p')[:-1]
        
        texto_limpio = []
        for p in parrafos_raw:

            texto_parrafo = "".join(p.xpath('.//text()').getall()).strip()
            if texto_parrafo:
                texto_limpio.append(texto_parrafo)
        
        if entradilla:
            texto_limpio.insert(0, entradilla.strip())

        # Extraer fecha
        fecha = self._extract_publication_date(response)

        if texto_limpio:
            yield {
                'liga': liga,
                'titular': titulo.strip() if titulo else None,
                'url': response.url,
                'texto_noticia': texto_limpio,
                'fecha_publicacion': fecha
            }
    
    def _extract_publication_date(self, response: Response) -> str:
        """
        Extrae la fecha de publicación de AS
        """
        # 1. Intentar con JSON-LD primero (más confiable)
        fecha = DateFinderInHTML.find_in_json_ld(response)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 2. Intentar con meta tags
        fecha = DateFinderInHTML.find_in_meta_tags(response)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 3. Selectores específicos de AS
        selectors_as = [
            'time::attr(datetime)',
            'span.a_auth_time::text',
            'span[class*="date"]::text',
            'span[class*="time"]::text',
            'div.a_a_time span::text',
            'p.a_a_time::text',
        ]
        
        fecha = DateFinderInHTML.find_in_common_selectors(response, selectors_as)
        if fecha:
            return DateExtractor.format_date(fecha)
        
        # 4. Buscar en texto de autor/metadata
        author_text = " ".join(response.css('div[class*="author"] ::text, div[class*="metadata"] ::text, div.a_a ::text').getall())
        if author_text:
            fecha = DateExtractor.extract_date(author_text)
            if fecha:
                return DateExtractor.format_date(fecha)
        
        return None