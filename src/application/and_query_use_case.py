from typing import Any, List
from domain.inverted_index import InvertedIndex


class AndQueryUseCase:
    def __init__(self, inverted_index: InvertedIndex) -> None:
        self._inverted_index = inverted_index

    
    def execute(self, terms: List[str]) -> List[Any]:
        return self._inverted_index.and_query(terms)
