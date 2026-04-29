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
from infrastructure.meta_llama_rag import MetaLLamaRAG

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
    rag_model = MetaLLamaRAG()
    generator.execute()
    queryObj=ShowResultsUseCase(document_repo,vector_repo,embedding,rag_model)
    print("Inicializando caso de uso de búsqueda...")
    while True:
        print("\n" + "="*50)
        query = input("Introduce tu búsqueda (o escribe 'salir' para terminar): ").strip()
        
        if query.lower() in ['salir', 'exit', 'quit']:
            print("Saliendo del buscador...")
            break
            
        if not query:
            continue

        print(f"\nEjecutando búsqueda para la query: '{query}'\n")
        
        # Desempaquetamos los documentos y la respuesta de RAG
        documents, rag_response = queryObj.execute(query)
        
        if not documents:
            print("No se encontraron resultados.")
        else:
            print(f"Se encontraron {len(documents)} resultados:")
            for idx, doc in enumerate(documents, 1):
                print(f"{idx}. [{doc.league}] {doc.title}")
                print(f"   URL: {doc.url}\n")
            
            print("\n--- Respuesta del Modelo RAG ---")
            print(rag_response)
            print("--------------------------------\n")

main()
 

