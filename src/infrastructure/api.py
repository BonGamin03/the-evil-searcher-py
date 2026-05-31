from fastapi import FastAPI , Query , Depends, Path
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
from application.smart_search_use_case import SmartSearchUseCase
from application.get_content_search_use_case import GetContentSearchUseCase
from infrastructure.zenserp_searcher import ZenserpSearcher
from infrastructure.re_rank_chunks import ReRankCTexts
from application.ranking_orchestration_use_case import RankingOrchestrationUseCase
from infrastructure.word2vec_query_expander import Word2VecQueryExpander

app = FastAPI(title="The Evil Searcher API ")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
mongo_client = MongoClient("mongodb://admin:admin@localhost:27017/evil_searcher?authSource=admin")
db = mongo_client["evil_searcher"]
doc_repo = DocumentRepository(db)
doc_proccesor=DocumentProcessor()
vec_repo = ChromaVectorRepository()
embedding_gen=HGEmbeddingGen()
rag_gen=MetaLLamaRAG("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")
builder_index=BuildInvertedIndexUseCase(doc_repo,doc_proccesor)
embeddings=LoadEmbeddingsUseCase(doc_repo,embedding_gen,vec_repo)
inverted_index=builder_index.execute()
web_searcher=ZenserpSearcher('15b69a40-4b14-11f1-8fd9-734ce4fa9350')
get_content=GetContentSearchUseCase(web_searcher,doc_repo)
query_expander=Word2VecQueryExpander(doc_repo,doc_proccesor)
re_rank=ReRankCTexts()
final_ranking=RankingOrchestrationUseCase(doc_proccesor,re_rank)
#embeddings.execute()

def get_search_use_case():
     show_result= ShowResultsUseCase(doc_repo,inverted_index,doc_proccesor,vec_repo,embedding_gen,re_rank)
     return SmartSearchUseCase(show_result,get_content,embeddings,rag_gen,inverted_index,doc_proccesor,re_rank,final_ranking, query_expander)
def get_scraper_use_case():
     return RunFullScraperUseCase()

@app.get("/search")
def search(query: str = Query(..., min_length=1),location: str = Query(None),use_case: SmartSearchUseCase = Depends(get_search_use_case)
):
    ranked_results, rag = use_case.execute(query, user_location=location)
    
    # Convertir RankingScore a diccionario
    results_dict = []
    for ranked in ranked_results:
        result_item = {
            "id": ranked.document.id,
            "title": ranked.document.title,
            "url": ranked.document.url,
            "league": ranked.document.league,
            "content": ranked.document.content,
            # Metadatos de ranking
            "relevance_score": round(ranked.relevance_score, 2),
            "authority_score": round(ranked.authority_score, 2),
            "freshness_score": round(ranked.freshness_score, 2),
            "final_score": round(ranked.final_score, 2),
            "ranking_type": ranked.ranking_type,
            "content_type": ranked.content_type.value,
            "featured_snippet": ranked.featured_snippet,
            "snippet_confidence": round(ranked.snippet_confidence, 2),
        }
        results_dict.append(result_item)
    
    return {
        "query": query,
        "results": results_dict,
        "rag": rag
    }

@app.get("/article/{doc_id}")
def get_article(doc_id: int = Path(..., description="ID del documento")):
    """Retorna el contenido completo de un artículo"""
    
    doc = doc_repo.get_document(doc_id)
    
    if not doc:
        return {"error": "Documento no encontrado"}
    
    return {
        "id": doc.id,
        "title": doc.title,
        "url": doc.url,
        "league": doc.league,
        "content": doc.content,
        "full_text": doc.get_full_text()
    }

@app.get("/scraper")
def search(use_case=Depends(get_scraper_use_case)):
    use_case.execute()
    return {"results":"ok"}