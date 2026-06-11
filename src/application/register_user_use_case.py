from domain.i_user_repository import IUserRepository
from domain.user import User
import bcrypt

class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, email: str, password: str) -> User:
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already in use")
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(email=email, password=hashed_password, read_docs=[])
        self.user_repo.save(user)
        return user
