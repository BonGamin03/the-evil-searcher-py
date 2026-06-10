from domain.i_user_repository import IUserRepository
from domain.user import User
import passlib.hash as hash

class LoginUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
        
        if not hash.bcrypt.verify(password, user.password):
            raise ValueError("Invalid email or password")
            
        return user
