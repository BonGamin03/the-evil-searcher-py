# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FutbolcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    liga = scrapy.Field()
    titular = scrapy.Field()
    url = scrapy.Field()
    texto_noticia = scrapy.Field()
    fecha_publicacion = scrapy.Field()  # Fecha en formato YYYY-MM-DD
