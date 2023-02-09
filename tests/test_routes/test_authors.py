import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models import Author, Book


authors = [
    {'full_name': 'KhanhKD1', 'books': [{'title': 'Book 1 of KhanhKD1'}, {'title': 'Book 2 of KhanhKD1'}]},
    {'full_name': 'KhanhKD2', 'books': [{'title': 'Book 1 of KhanhKD2'}]},
    {'full_name': 'KhanhKD3', 'books': [{'title': 'Book 1 of KhanhKD3'}, {'title': 'Book 2 of KhanhKD3'}]},
]


def test_get_authors(client, db_session):
    for author in authors:
        author_ = Author(full_name=author['full_name'])
        db_session.add(author_)
        db_session.flush()
        db_session.add_all([
            Book(title=book['title'], author_id=author_.id) for book in author['books']
        ])

    db_session.commit()
    response = client.get("/api/authors/").json()
    assert response['status'] == "success", 'status must be success'
    assert response['results'] == len(authors), 'results number must be equal authors number'
    assert set([author['full_name'] for author in response['authors']]) == \
           set([author['full_name'] for author in authors]), 'list author names must be equal'


def test_create_author(client):
    for author in authors:
        author_data = {"full_name": author['full_name']}
        author_res = client.post("/api/authors/", content=json.dumps(author_data)).json()
        assert author_res['status'] == "success"
        assert author_res['author']['full_name'] == author['full_name']
        for book in author['books']:
            book_data = {"title": book['title'], 'author_id': author_res['author']['id']}
            book_res = client.post("/api/books/", content=json.dumps(book_data)).json()
            assert book_res['status'] == "success", 'status must be success'
            assert book_res['book']['title'] == book['title']
            assert book_res['book']['author_id'] == author_res['author']['id']
