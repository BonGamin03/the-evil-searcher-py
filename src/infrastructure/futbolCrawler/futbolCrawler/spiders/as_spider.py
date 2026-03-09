import scrapy

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
        
        cuerpo_completo = " ".join(texto_limpio)
        noticia_final = f"{entradilla} {cuerpo_completo}" if entradilla else cuerpo_completo

        if len(cuerpo_completo) > 100:
            yield {
                'liga': liga,
                'titular': titulo.strip() if titulo else None,
                'url': response.url,
                'texto_noticia': noticia_final.strip()
            }