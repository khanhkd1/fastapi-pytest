from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from app.database import Base


class Author(Base):
    __tablename__ = "authors"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    full_name = Column(String, index=True)
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

    def get_info(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'books': self.get_books()
        }

    def get_books(self):
        books = []
        for book in list(self.books):
            books.append({
                'id': book.id,
                'title': book.title
            })
        return books


class Book(Base):
    __tablename__ = "books"
    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    title = Column(String, index=True)
    author_id = Column(GUID, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
