from typing import Optional
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from domain.document import Document
from domain.i_document_repository import IDocumentRepository

class DocumentRepository(IDocumentRepository):
    def __init__(self, db) -> None:
        self.db = db

    def _get_next_doc_id(self) -> int:
        counter = self.db.counters.find_one_and_update(
            {"_id": "documents"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return int(counter["seq"])
    
    def _get_doc_id_by_url(self, url: str) -> int | None:
        doc = self.db.documents.find_one({"url": url}, {"doc_id": 1})
        return int(doc["doc_id"]) if doc and "doc_id" in doc else None

    def save_document(self, title: str, league: str, url: str, content: str) -> int:
        existing = self._get_doc_id_by_url(url)
        if existing:
            return existing

        doc_id = self._get_next_doc_id()
        try:
            self.db.documents.insert_one(
                {
                    "doc_id": doc_id,
                    "title": title,
                    "league": league,
                    "url": url,
                    "content": content,
                }
            )
            return doc_id
        except DuplicateKeyError:
            existing = self._get_doc_id_by_url(url)
            if existing:
                return existing
            raise

    def get_all_documents(self) -> list[Document]:
        documents = []
        for doc in self.db.documents.find({}, {"_id": 0}):
            documents.append(
                Document(
                    int(doc["doc_id"]),
                    doc["title"],
                    doc["league"],
                    doc["url"],
                    doc["content"],
                )
            )
        return documents

    def get_document(self, id: int) -> Optional[Document]:
        doc = self.db.documents.find_one({"doc_id": int(id)}, {"_id": 0})
        if not doc:
            return None
        return Document(
            int(doc["doc_id"]),
            doc["title"],
            doc["league"],
            doc["url"],
            doc["content"],
        )

 