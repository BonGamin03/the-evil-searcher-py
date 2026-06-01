import joblib
import sys
from domain.inverted_index import InvertedIndex

class SaveInvertedIndexUseCase:
    def __init__(self, index_path: str = "inverted_index.joblib"):
        self.index_path = index_path

    def execute(self, inverted_index: InvertedIndex) -> None:
        sys.setrecursionlimit(10000000)
        joblib.dump(inverted_index._index, self.index_path)