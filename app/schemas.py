from typing import List
from pydantic import BaseModel


class AuthorBaseSchema(BaseModel):
    id: str
    full_name: str
    books: list

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class AuthorCreateSchema(BaseModel):
    full_name: str


class ListAuthorResponse(BaseModel):
    status: str
    results: int
    authors: List[AuthorBaseSchema]


class BookBaseSchema(BaseModel):
    id: str
    title: str
    author_id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class BookCreateSchema(BaseModel):
    title: str
    author_id: str


class ListBookResponse(BaseModel):
    status: str
    results: int
    books: List[BookBaseSchema]
