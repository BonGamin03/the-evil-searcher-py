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
        if item.get('titular'):
            item['titular'] = self.clean_text(item['titular'])

        return item 

    def clean_text(self, text):
        
        #Allow all this 
        text = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\.\,\:\;\"\'\!\?\¿\¡\-\+\(\)\@\$\#\[\]]', '', text)
        #Remove multiple spaces and odd line breaks.
        text = re.sub(r'\s+', ' ', text)

        return text.strip()
    
# dentro de futbolCrawler/pipelines.py
import os
from pymongo import MongoClient
from infrastructure.document_repository import DocumentRepository

class MongoStorePipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "evil_searcher"),
        )

    def __init__(self, mongo_uri: str, mongo_db: str):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None
        self.repo = None

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.repo = DocumentRepository(self.db)

    def close_spider(self, spider):
        if self.client:
            self.client.close()

    def process_item(self, item, spider):
        liga = item.get("liga")
        titulo = item.get("titular")
        url = item.get("url")
        content = item.get("texto_noticia")

        if liga and titulo and url and content:
            doc_id = self.repo.save_document(
                title=titulo,
                league=liga,
                url=url,
                content=content,
            )
            item["doc_id"] = doc_id

        return item