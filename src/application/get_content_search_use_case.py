import requests
from bs4 import BeautifulSoup
from readability import Document as ReadabilityDocument
from domain.i_web_searcher import IWebSearcher
from domain.i_document_repository import IDocumentRepository
from domain.document import Document

class GetContentSearchUseCase:
    def __init__(
        self, 
        web_searcher: IWebSearcher, 
        document_repository: IDocumentRepository,
    ):
        self.web_searcher = web_searcher
        self.document_repository = document_repository

    def execute(self, query: str) -> tuple[list[Document], str]:
        search_results = self.web_searcher.search(query)
        documents = []
        context_str = ''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        for result in search_results:
            url = result.get("link")
            if not url:
                continue

            try:
                # 1. Petición para obtener el HTML de la página
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # 2. Limpieza inicial con Readability
                doc = ReadabilityDocument(response.text)
                title = doc.title()
                html_summary = doc.summary()
                
                # 3. Quitar etiquetas HTML restantes usando BeautifulSoup
                soup = BeautifulSoup(html_summary, 'html.parser')
                initial_clean_text = soup.get_text(separator='\n', strip=True)
                
                
                # Separar por saltos de línea y quitar los vacíos
                clean_content = [p.strip() for p in initial_clean_text.split('\n') if len(p.strip()) > 10]
                
                
                clean_title = title.strip() if title else "Sin título"
                
                # Acumular en la variable de contexto ANTES de guardar
                context_str += "\n...\n".join(clean_content) + "\n"
                
                league = url.split('/')[-1].replace('.html', '').title()
                
                # 5. Guardar en MongoDB usando el repositorio
                doc_id = self.document_repository.save_document(
                    title=clean_title,
                    league=league,
                    url=url,
                    content=clean_content
                )
                
                # 6. Agregar el documento instanciado a la lista a retornar
                new_doc = Document(id=doc_id, title=clean_title, league=league, url=url, content=clean_content)
                documents.append(new_doc)

            except Exception as e:
                print(f"Error procesando {url}: {e}")
                continue
            
        return documents, context_str