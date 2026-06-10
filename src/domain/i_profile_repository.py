from abc import ABC, abstractmethod
from typing import Optional


class IProfileRepository(ABC):
    """
    User Vectorial Profile Representation Repository Interface.
    
    """

    @abstractmethod
    def upsert_profile(self, email: str, embedding: list[float], metadata: dict) -> None:
        pass

    @abstractmethod
    def get_profile(self, email: str) -> Optional[dict]:
         pass
