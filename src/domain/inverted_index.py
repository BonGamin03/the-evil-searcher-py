from collections import defaultdict,Counter
from skiplist import SkipList
class InvertedIndex:
    def __init__(self):
        #Duda sobre campos private
        self._index = defaultdict(SkipList)
        self._words=0
    
    def add_document(self,doc_id:int,terms:list[str]):
        terms_count=Counter(token for token in terms)
        for term,freq in terms_count.items():
            self._index[term].insert(doc_id,freq)
        self._words=len(self._index)

    def search(self,term:str)->SkipList:
        return self._index.get(term, SkipList())
    
    def and_query(self,terms:list[str])->list[int]:
        if not terms:
            return []
        result = self.search(terms[0])
        for term in terms[1:]:
            result = result.intersect(self.search(term))
        return result.to_list()
    