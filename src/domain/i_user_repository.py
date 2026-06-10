from abc import ABC, abstractmethod
from typing import Optional
from domain.user import User

class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass
    
    @abstractmethod
    def update_read_docs(self, user_email:str, doc_id: int) -> None:
        pass
