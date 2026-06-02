import logging
import os

from pymongo import MongoClient
from application.run_scraper_use_case import RunFullScraperUseCase
from infrastructure.word2vec_query_expander import Word2VecQueryExpander
from infrastructure.document_repository import DocumentRepository
from infrastructure.document_processor import DocumentProcessor
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("pymongo.topology").setLevel(logging.WARNING)
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://admin:admin@mongodb:27017/evil_searcher?authSource=admin",
)
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["evil_searcher"]
doc_repo = DocumentRepository(db)
doc_proccesor=DocumentProcessor()
query_expander = Word2VecQueryExpander(doc_repo, doc_proccesor)
test=RunFullScraperUseCase(query_expander)
test.execute()
 