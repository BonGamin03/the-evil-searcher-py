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
from application.get_content_search_use_case import GetContentSearchUseCase
from application.smart_search_use_case import SmartSearchUseCase
from infrastructure.zenserp_searcher import ZenserpSearcher
from infrastructure.re_rank_chunks import ReRankCTexts
from application.run_scraper_use_case import RunFullScraperUseCase

def main():
    print("Conectando a MongoDB...")
    # Usar la URI definida en tu docker-compose o la por defecto
    client = MongoClient("mongodb://admin:admin@localhost:27017/evil_searcher?authSource=admin")
    db = client["evil_searcher"]
    
    print("Inicializando repositorios...")
    document_repo = DocumentRepository(db)
    vector_repo = ChromaVectorRepository()
    document_processor = DocumentProcessor()
    re_rank_text = ReRankCTexts()
    
    builder = BuildInvertedIndexUseCase(document_repo, document_processor)
    inverted_index = builder.execute()

    print("Cargando documentos e inicializando modelo de embeddings...")
    # Se obtienen todos los documentos en caso de que LSA necesite entrenar
    documents = document_repo.get_all_documents()
    embedding = HGEmbeddingGen()
    generator = LoadEmbeddingsUseCase(document_repo, embedding, vector_repo)
    
    # Tokens e instanciación de servicios externos
    hf_token = 'HG_TOKEN'
    rag_model = MetaLLamaRAG(hf_token)
    searcher = ZenserpSearcher('API-KEY')
     
    # Casos de uso atómicos
    show_results = ShowResultsUseCase(document_repo, inverted_index, document_processor, vector_repo, embedding,re_rank_text)
    get_content = GetContentSearchUseCase(searcher, document_repo)
    
    # Orquestador
    smart_search = SmartSearchUseCase(
        show_results_use_case=show_results,
        get_content_use_case=get_content,
        load_embeddings_use_case=generator,
        rag_model=rag_model,
        inverted_index=inverted_index,
        document_processor=document_processor,
        re_rank= re_rank_text
    )
    
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
        
        # El caso de uso se encarga de todo (RAG, juez, búsqueda web y base de conocimiento)
        documents_list, rag_response = smart_search.execute(query)

        print(f"Se encontraron {len(documents_list)} resultados:")
        for doc in documents_list: 
            print(f"{doc.id}. [{doc.league}] {doc.title}")
            print(f"   URL: {doc.url}\n")
            
        print("\n--- Respuesta del Modelo RAG ---")
        print(rag_response)
        print("--------------------------------\n")

if __name__ == "__main__":
    main()