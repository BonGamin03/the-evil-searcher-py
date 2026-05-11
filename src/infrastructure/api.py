from fastapi import FastAPI , Query , Depends
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from application.run_scraper_use_case import RunFullScraperUseCase
from application.show_results_use_case import ShowResultsUseCase
from infrastructure.document_repository import DocumentRepository
from infrastructure.lsa_embedding_generator import LSAEmbeddingGenerator
from infrastructure.meta_llama_rag import MetaLLamaRAG
from infrastructure.vector_repository import ChromaVectorRepository
from application.build_inverted_index import BuildInvertedIndexUseCase
from application.load_embedings_use_case import LoadEmbeddingsUseCase
from infrastructure.document_processor import DocumentProcessor
from infrastructure.hg_embedding_gen import HGEmbeddingGen

app = FastAPI(title="The Evil Searcher API ")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
mongo_client = MongoClient("mongodb://admin:admin@localhost:27017/evil_searcher?authSource=admin")
db = mongo_client["evil_searcher"]
doc_repo = DocumentRepository(db)
doc_proccesor=DocumentProcessor()
vec_repo = ChromaVectorRepository()
embedding_gen=HGEmbeddingGen()
rag_gen=MetaLLamaRAG()
builder_index=BuildInvertedIndexUseCase(doc_repo,doc_proccesor)
inverted_index=builder_index.execute()

def get_search_use_case():
     return ShowResultsUseCase(doc_repo,inverted_index,doc_proccesor,vec_repo,embedding_gen,rag_gen)
def get_scraper_use_case():
     return RunFullScraperUseCase()

@app.get("/search")
def search(query: str = Query(...,min_length=1),use_case: ShowResultsUseCase = Depends(get_search_use_case)):
    docs,rag = use_case.execute(query)
    return {"query": query, "results": docs, "rag": rag}

@app.get("/scraper")
def search(use_case=Depends(get_scraper_use_case)):
    use_case.execute()
    return {"results":"ok"}