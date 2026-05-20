from dataclasses import dataclass
from typing import Optional

@dataclass
class Document:
    """
    Document structure represents news
    
    Args:
        id: str. Unique Doc id
        title: str. Doc Title
        league:str. Represents the soccer league
        url: str. News url
        content: str. Full News content
        publication_date: Optional[str]. Publication date in YYYY-MM-DD format
        
    """
    id:int
    title:str
    league:str
    url:str
    content: list
    publication_date: Optional[str] = None

    def get_full_text(self) -> str:
        """
        Get the news full text include title and league
        
        Returns:
            str. full text
        """
        content_text = "\n".join(self.content) 
        
        return f"{self.title} {self.league}\n{content_text}"
    
    def get_word_count(self) -> int:
        """
        Get doc lenght
        
        Returns:
            int. word count 
        """
        return len(self.get_full_text().split())
