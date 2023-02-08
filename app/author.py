from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db


router = APIRouter()


# [...] get all authors
@router.get('/')
def get_authors(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    authors = db.query(models.Author).filter(
        models.Author.full_name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(authors), 'authors': authors}


# [...] create author
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_author(payload: schemas.AuthorCreateSchema, db: Session = Depends(get_db)):
    new_author = models.Author(**payload.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return {"status": "success", "author": new_author}


# [...] get single record
@router.get('/{authorId}')
def get_author(authorId: str, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == authorId).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No author with this id: {id} found")
    return {"status": "success", "author": author}


# [...] edit record
@router.patch('/{authorId}')
def update_author(authorId: str, payload: schemas.AuthorBaseSchema, db: Session = Depends(get_db)):
    author_query = db.query(models.Author).filter(models.Author.id == authorId)
    db_author = author_query.first()

    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No author with this id: {authorId} found')
    update_data = payload.dict(exclude_unset=True)
    author_query.filter(models.Author.id == authorId).update(update_data,
                                                             synchronize_session=False)
    db.commit()
    db.refresh(db_author)
    return {"status": "success", "author": db_author}


# [...] delete record
@router.delete('/{authorId}')
def delete_author(authorId: str, db: Session = Depends(get_db)):
    author_query = db.query(models.Author).filter(models.Author.id == authorId)
    author = author_query.first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No author with this id: {id} found')
    author_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
