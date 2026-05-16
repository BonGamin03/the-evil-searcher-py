from abc import ABC, abstractmethod

class IReRankLLMContext(ABC):
    @abstractmethod

    def re_rank_results(self, query : str, chunks : list[str]) -> list[tuple[float,str]]:
        pass