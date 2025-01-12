import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
def test_get_day_word():
    response = client.get("/getDayWord")
    assert response.status_code == 200
    return response.json()

def test_add_day_word():
    word = "teste5"
    response = client.post("/addWord", json={"word": word, "images": ["https://example.com", "https://example.com", "https://example.com", "https://example.com", "https://example.com"], "closeWords": ["word1", "word2", "word3", "word4", "word5"], "lastDate": {"$date": {"$numberLong": "1734318000000"}}})
    assert response.status_code == 200

def test_set_day_word():
    word = "teste5"
    response = client.post("/setDayWord/" + word)
    assert response.status_code == 200
    assert test_get_day_word() == {"word": word}
