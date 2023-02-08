import json
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is to include backend dir in sys.path so that we can import from db,main.py

# from app.schemas import AuthorCreateSchema


def test_create_author(client: TestClient):
    data = {"full_name": "KhanhKD1"}
    response = client.post("/api/authors", data=data)
    assert response.json()["full_name"] == "KhanhKD1"
