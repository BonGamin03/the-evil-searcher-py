'''from application.run_scraper_use_case import RunFullScraperUseCase
test=RunFullScraperUseCase()
test.execute()'''
import asyncio
from pymongo import MongoClient

from infrastructure.document_repository import DocumentRepository
from infrastructure.vector_repository import ChromaVectorRepository
from infrastructure.lsa_embedding_generator import LSAEmbeddingGenerator
from application.show_results_use_case import ShowResultsUseCase
from application.load_embedings_use_case import LoadEmbeddingsUseCase

def main():
    print("Conectando a MongoDB...")
    # Usar la URI definida en tu docker-compose o la por defecto
    client = MongoClient("mongodb://admin:admin@localhost:27017/evil_searcher?authSource=admin")
    db = client["evil_searcher"]
    
    print("Inicializando repositorios...")
    document_repo = DocumentRepository(db)
    vector_repo = ChromaVectorRepository()
    
    print("Cargando documentos e inicializando modelo de embeddings...")
    # Se obtienen todos los documentos en caso de que LSA necesite entrenar
    documents=document_repo.get_all_documents()
    embedding=LSAEmbeddingGenerator(documents)
    generator=LoadEmbeddingsUseCase(document_repo,embedding,vector_repo)
    generator.execute()
    queryObj=ShowResultsUseCase(document_repo,vector_repo,embedding)
    print("Inicializando caso de uso de búsqueda...")
     
    
    query = "CR7"
    print(f"\nEjecutando búsqueda para la query: '{query}'\n")
    # Al estar definido como 'async def execute', usamos await
    results = queryObj.execute(query)
    
    if not results:
        print("No se encontraron resultados.")
    else:
        print(f"Se encontraron {len(results)} resultados:")
        for idx, doc in enumerate(results, 1):
            print(f"{idx}. [{doc.league}] {doc.title}")
            print(f"   URL: {doc.url}\n")

main()
 

