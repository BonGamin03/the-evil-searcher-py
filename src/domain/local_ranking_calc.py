
from domain.document import Document


class LocalRankingCalculator:
     

    def __init__(self):
        
        self.league_locations = {
            'la liga': 'Spain',
            'premier league': 'England',
            'serie a': 'Italy',
            'ligue 1': 'France',
            'bundesliga': 'Germany',
            'laliga': 'Spain',
            'english': 'England',
            'italian': 'Italy',
            'french': 'France',
            'german': 'Germany',
            'primera division':'Spain',
            'liga mx':'Mexico',
            'champions league': 'Europe',
            'copa america': 'South America',
            'europa league':'Europe',
            'liga francesa':'France',
            'liga italiana':'Italy',
            'mls':'United States',
            'mundial':'world',
            'uefa champions league':'Europe'

        }

    def calculate_local_relevance(self,document: Document, user_location: str = None) -> float:
        """
        Calculate local relevance by region of user
        """
        league_lower = document.league.lower().replace('-', ' ')
        league_location = [y for x , y in self.league_locations.items() if x==league_lower]
        if not league_location:
            return 0.0  
        
        if user_location and league_location[0] == user_location:
            return 30.0  
        
        return 0.0