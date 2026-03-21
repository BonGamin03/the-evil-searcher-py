from collections import defaultdict
from skiplist import SkipList
class InvertedIndex:
    def __init__(self):
        #Duda sobre campos private
        self._index = defaultdict(SkipList)
        self._words=0
    
    def add_document(self,doc_id:int,terms:list[str]):
        for term in terms:
            self._index[term].insert(doc_id)
            self._words += 1

    def search(self,term:str)->SkipList:
        return self._index.get(term, SkipList())
    