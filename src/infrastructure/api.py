from fastapi import FastAPI , Query , Depends
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from application.run_scraper_use_case import RunFullScraperUseCase
from application.show_results_use_case import ShowResultsUseCase
from infrastructure.document_repository import DocumentRepository
from infrastructure.lsa_embedding_generator import LSAEmbeddingGenerator
from infrastructure.meta_llama_rag import MetaLLamaRAG
from infrastructure.vector_repository import ChromaVectorRepository

app = FastAPI(title="The Evil Searcher API ")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client.evil_searcher
# lsa_model = LSAEmbeddingGenerator(documents=None)
# doc_repo = DocumentRepository(db)
# vec_repo = ChromaVectorRepository()
# rag_gen=MetaLLamaRAG()

# def get_search_use_case():
#     return ShowResultsUseCase(doc_repo, vec_repo, lsa_model,rag_gen)
def get_scraper_use_case():
     return RunFullScraperUseCase()

# @app.get("/search")
# def search(query: str = Query(...,min_length=1),use_case=Depends(get_search_use_case)):
#     results=use_case.execute(query)
#     return {"query": query, "results": results}

@app.get("/scraper")
def search(use_case=Depends(get_scraper_use_case)):
    use_case.execute()
    return {"results":"ok"}