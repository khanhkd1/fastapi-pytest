import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Author


def test_get_authors(client, db_session):
    db_session.add_all([
        Author(full_name='KhanhKD1'),
        Author(full_name='KhanhKD2'),
        Author(full_name='KhanhKD3'),
    ])
    db_session.commit()
    response = client.get("/api/authors/")
    assert response.json()['status'] == "success"
    assert response.json()['results'] == 3
    assert set([author['full_name'] for author in response.json()['authors']]) == {'KhanhKD1', 'KhanhKD2', 'KhanhKD3'}


def test_create_author(client):
    data = {"full_name": "KhanhKD1"}
    response = client.post("/api/authors/", content=json.dumps(data))
    assert response.json()['status'] == "success"
