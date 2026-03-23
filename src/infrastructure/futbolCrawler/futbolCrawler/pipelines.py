# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class FutbolcrawlerPipeline:
    def process_item(self, item, spider):

        if item.get("texto_noticia"):
            item["texto_noticia"] = self.clean_text(item["texto_noticia"]) 
            item['titular'] = self.clean_text(item['texto_noticia'])

        return item 

    def clean_text(self, text):
        
        #Allow all this 
        text = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\.\,\:\;\"\'\!\?\¿\¡\-\+\(\)\@\$\#\[\]]', '', text)
        #Remove multiple spaces and odd line breaks.
        text = re.sub(r'\s+', ' ', text)

        return text.strip()