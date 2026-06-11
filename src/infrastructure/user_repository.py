from pymongo.database import Database
from typing import Optional
from domain.user import User
from domain.i_user_repository import IUserRepository

class UserRepository(IUserRepository):
    def __init__(self, db: Database):
        self.collection = db["users"]

    def save(self, user: User) -> None:
        user_doc = {
            "email": user.email,
            "password": user.password,
            "read_docs": user.read_docs
        }
        self.collection.insert_one(user_doc)

    def get_by_email(self, email: str) -> Optional[User]:
        doc = self.collection.find_one({"email": email})
        if doc:
            return User(email=doc["email"], password=doc["password"], read_docs=doc.get("read_docs", []))
        return None

    def update(self, user: User) -> None:
        self.collection.update_one(
            {"email": user.email},
            {"$set": {"password": user.password, "read_docs": user.read_docs}}
        )
    def update_read_docs(self, user_email: str, doc_id: int) -> None:
         
        self.collection.update_one(
            {"email": user_email},
            {"$pull": {"read_docs": doc_id}}
        )
        
         
        self.collection.update_one(
            {"email": user_email},
            {
                "$push": {
                    "read_docs": {
                        "$each": [doc_id],
                        "$slice": -20
                    }
                }
            }
        )
