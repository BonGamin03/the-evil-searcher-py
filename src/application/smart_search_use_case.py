from typing import Tuple
from threading import Thread
from domain.document import Document
from domain.inverted_index import InvertedIndex
from domain.i_document_processor import IDocumentProcessor
from domain.i_rag import IRAG
from application.show_results_use_case import ShowResultsUseCase
from application.get_content_search_use_case import GetContentSearchUseCase
from application.load_embedings_use_case import LoadEmbeddingsUseCase
from application.save_inverted_index import SaveInvertedIndexUseCase
from domain.probabilistic_model import ProbabilisticModel
from domain.i_re_rank_llm_context import IReRankLLMContext
from application.ranking_orchestration_use_case import RankingOrchestrationUseCase
from domain.ranking_score import RankingScore

class SmartSearchUseCase:
    def __init__(
        self,
        show_results_use_case: ShowResultsUseCase,
        get_content_use_case: GetContentSearchUseCase,
        load_embeddings_use_case: LoadEmbeddingsUseCase,
        rag_model: IRAG,
        inverted_index: InvertedIndex,
        document_processor: IDocumentProcessor,
        re_rank : IReRankLLMContext,
        doc_ranking : RankingOrchestrationUseCase
    ):
        self.show_results_use_case = show_results_use_case
        self.get_content_use_case = get_content_use_case
        self.load_embeddings_use_case = load_embeddings_use_case
        self.rag_model = rag_model
        self.inverted_index = inverted_index
        self.document_processor = document_processor
        self.re_rank = re_rank
        self.doc_ranking=doc_ranking

    def execute(self, query: str) -> Tuple[list[RankingScore], str]:

        documents, context = self.show_results_use_case.execute(query)
        
        model = ProbabilisticModel(self.inverted_index,self.document_processor)

        documents = model.calculate_similarity(query, documents)
        
        score = [sc for sc, doc in  self.re_rank.re_rank_results(query, [x.get_full_text() for x , y in documents])]

        print(f"Score de documentos : {score}")  # Para depuración y seguimiento de resultados
        # if abs(score[0]) < 6.0:  # Si el documento más relevante tiene una puntuación baja, consideramos el contexto no relevante
        #     print("El contexto recuperado no es relevante. Realizando búsqueda web...")
        #     documents, context = self.get_content_use_case.execute(query)
            
    
        #     vec_db_thread = Thread(target=self.load_embeddings_use_case.execute, args=(documents,))
        #     vec_db_thread.start()
            
        #     inverted_index_thread = Thread(target=self.async_updates_inverted_index, args=(documents,))
        #     inverted_index_thread.start()

        document_results = []
        for item in documents:
            if isinstance(item, tuple):
                document_results.append(item[0])
            else:
                document_results.append(item)
                
        documents=[(x,abs(y)) for x,y in documents]
        rag_response = self.rag_model.generate_response(query, context)
        last_ranking=self.doc_ranking.execute(document_results,query,documents)

        return last_ranking, rag_response
    
    def async_updates_inverted_index(self,documents : list[Document]):

        for doc in documents:
            terms = self.document_processor.process_document(doc)
            self.inverted_index.add_document(doc.id, terms)

        save_inverted_index = SaveInvertedIndexUseCase()
        save_inverted_index.execute(self.inverted_index)
        print("Índice invertido actualizado con nuevos documentos.")



        
        

        