from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db


router = APIRouter()


# [...] get all books
@router.get('/')
def get_books(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    books = db.query(models.Book).filter(
        models.Book.title.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(books), 'books': books}


# [...] create book
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_book(payload: schemas.BookCreateSchema, db: Session = Depends(get_db)):
    author_id = payload.dict()['author_id']
    author_query = db.query(models.Author).filter(models.Author.id == author_id)
    author = author_query.first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No author with this id: {id} found')
    new_book = models.Book(**payload.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"status": "success", "book": new_book}


# [...] get single record
@router.get('/{bookId}')
def get_book(bookId: str, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == bookId).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No book with this id: {id} found")
    return {"status": "success", "book": book}


# [...] edit record
@router.patch('/{bookId}')
def update_book(bookId: str, payload: schemas.BookBaseSchema, db: Session = Depends(get_db)):
    book_query = db.query(models.Book).filter(models.Book.id == bookId)
    db_book = book_query.first()

    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No book with this id: {bookId} found')
    update_data = payload.dict(exclude_unset=True)
    book_query.filter(models.Book.id == bookId).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_book)
    return {"status": "success", "book": db_book}


# [...] delete record
@router.delete('/{bookId}')
def delete_book(bookId: str, db: Session = Depends(get_db)):
    note_query = db.query(models.Book).filter(models.Book.id == bookId)
    note = note_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No book with this id: {id} found')
    note_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
