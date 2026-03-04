from dataclasses import dataclass
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
        
    """
    id:str
    title:str
    league:str
    url:str
    content:str

    def get_full_text(self) -> str:
        """
        Get the news full text include title and league
        
        Returns:
            str. full text
        """
        return f"{self.title} {self.league} {self.content}"
    
    def get_word_count(self) -> int:
        """
        Get doc lenght
        
        Returns:
            int. word count 
        """
        return len(self.get_full_text().split())