'''from application.run_scraper_use_case import RunFullScraperUseCase
test=RunFullScraperUseCase()
test.execute()'''
from pymongo import MongoClient

from infrastructure.document_repository import DocumentRepository
from infrastructure.vector_repository import ChromaVectorRepository
from infrastructure.hg_embedding_gen import HGEmbeddingGen
from application.show_results_use_case import ShowResultsUseCase
from application.load_embedings_use_case import LoadEmbeddingsUseCase
from infrastructure.meta_llama_rag import MetaLLamaRAG
from domain.inverted_index import InvertedIndex
from infrastructure.document_processor import DocumentProcessor
from application.build_inverted_index import BuildInvertedIndexUseCase

def main():
    print("Conectando a MongoDB...")
    # Usar la URI definida en tu docker-compose o la por defecto
    client = MongoClient("mongodb://admin:admin@localhost:27017/evil_searcher?authSource=admin")
    db = client["evil_searcher"]
    
    print("Inicializando repositorios...")
    document_repo = DocumentRepository(db)
    vector_repo = ChromaVectorRepository()
    document_procesor = DocumentProcessor()
    builder = BuildInvertedIndexUseCase(document_repo,document_procesor)
    inverted_index = builder.execute()


    
    print("Cargando documentos e inicializando modelo de embeddings...")
    # Se obtienen todos los documentos en caso de que LSA necesite entrenar
    documents=document_repo.get_all_documents()
    embedding=HGEmbeddingGen()
    generator=LoadEmbeddingsUseCase(document_repo,embedding,vector_repo)
    rag_model = MetaLLamaRAG()
    generator.execute()
    queryObj=ShowResultsUseCase(document_repo,inverted_index,document_procesor,
    vector_repo,embedding,rag_model)
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
            for doc,score in documents:
                print(f"{doc.id}. [{doc.league}] {doc.title}")
                print(f"   URL: {doc.url}\n")
                print(f"Score : {score}")
            
            print("\n--- Respuesta del Modelo RAG ---")
            print(rag_response)
            print("--------------------------------\n")

main()
 

