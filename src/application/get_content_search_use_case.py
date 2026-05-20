import requests
from bs4 import BeautifulSoup
from readability import Document as ReadabilityDocument
from domain.i_web_searcher import IWebSearcher
from domain.i_document_repository import IDocumentRepository
from domain.document import Document
import json
import re

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
                
                # Extraer fecha de publicación
                publication_date = self._extract_publication_date(response.text)
                
                # 5. Guardar en MongoDB usando el repositorio
                doc_id = self.document_repository.save_document(
                    title=clean_title,
                    league=league,
                    url=url,
                    content=clean_content,
                    publication_date=publication_date
                )
                
                # 6. Agregar el documento instanciado a la lista a retornar
                new_doc = Document(
                    id=doc_id, 
                    title=clean_title, 
                    league=league, 
                    url=url, 
                    content=clean_content,
                    publication_date=publication_date
                )
                documents.append(new_doc)

            except Exception as e:
                print(f"Error procesando {url}: {e}")
                continue
            
        return documents, context_str
    
    def _extract_publication_date(self, html_content: str) -> str:
        """
        Extrae la fecha de publicación del contenido HTML
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. Buscar en meta tags
        publication_date = self._get_from_meta_tags(soup)
        if publication_date:
            return publication_date
        
        # 2. Buscar en JSON-LD
        publication_date = self._get_from_json_ld(soup)
        if publication_date:
            return publication_date
        
        # 3. Buscar en elementos comunes
        publication_date = self._get_from_common_elements(soup)
        if publication_date:
            return publication_date
        
        return None
    
    def _get_from_meta_tags(self, soup: BeautifulSoup) -> str:
        """Busca fecha en meta tags"""
        meta_attrs = [
            ('property', 'article:published_time'),
            ('name', 'datePublished'),
            ('name', 'publish_date'),
            ('name', 'DC.date.created'),
        ]
        
        for attr_name, attr_value in meta_attrs:
            meta = soup.find('meta', {attr_name: attr_value})
            if meta and meta.get('content'):
                return self._clean_date_string(meta.get('content'))
        
        return None
    
    def _get_from_json_ld(self, soup: BeautifulSoup) -> str:
        """Busca fecha en JSON-LD"""
        scripts = soup.find_all('script', {'type': 'application/ld+json'})
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                
                # Buscar en estructura común
                if isinstance(data, dict):
                    for key in ['datePublished', 'publishedDate', 'dateModified']:
                        if key in data:
                            return self._clean_date_string(data[key])
                
                # Si es lista, iterar
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            for key in ['datePublished', 'publishedDate', 'dateModified']:
                                if key in item:
                                    return self._clean_date_string(item[key])
            except (json.JSONDecodeError, AttributeError, TypeError):
                pass
        
        return None
    
    def _get_from_common_elements(self, soup: BeautifulSoup) -> str:
        """Busca fecha en elementos HTML comunes"""
        selectors = [
            'time',
            '[class*="date"]',
            '[class*="time"]',
            '[class*="published"]',
        ]
        
        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    # Intentar obtener del atributo datetime primero
                    if element.get('datetime'):
                        return self._clean_date_string(element.get('datetime'))
                    
                    # Luego del texto
                    text = element.get_text(strip=True)
                    if text:
                        return self._clean_date_string(text)
            except:
                pass
        
        return None
    
    def _clean_date_string(self, date_str: str) -> str:
        """
        Limpia y normaliza string de fecha
        Retorna en formato YYYY-MM-DD o None
        """
        if not date_str:
            return None
        
        date_str = date_str.strip()
        
        # Si ya está en formato ISO (YYYY-MM-DD o YYYY-MM-DDTHH:mm:ss)
        iso_match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_str)
        if iso_match:
            return iso_match.group(0)
        
        # Intentar extraer usando DateExtractor si es posible
        try:
            # Importar el extractor aquí para evitar dependencias circulares
            from infrastructure.date_extraction import SimpleeDateExtractor
            return SimpleeDateExtractor.extract_date(date_str)
        except:
            pass
        
        return None