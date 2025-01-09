import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.fixture(scope="module")
def mock_db():
    return {
        "dayWord": [
            {
                "_id": {"$oid": "677f1aef8adee120d7892fd7"},
                "word": "Teste",
                "images": [
                    "https://example.com", "https://example.com", "https://example.com", 
                    "https://example.com", "https://example.com"
                ],
                "closeWords": ["testes", "palavra", "outros"],
                "lastDate": {"$date": {"$numberLong": "1734318000000"}}
            }
        ]
    }

def test_get_day_word(mock_db):
    response = client.get("/getDayWord")
    assert response.status_code == 200
    data = response.json()
    assert "word" in data
    assert "images" in data
    assert "closeWords" in data
    assert "lastDate" in data

def test_get_day_word_not_found(mock_db):
    mock_db["dayWord"] = []
    response = client.get("/getDayWord")
    assert response.status_code == 404
    assert response.json() == {"message": "Word of the day not found"}

def test_add_day_word(mock_db):
    word = {
        "word": "NewWord",
        "images": [
            "https://newimage1.com", "https://newimage2.com", "https://newimage3.com", 
            "https://newimage4.com", "https://newimage5.com"
        ],
        "closeWords": ["new", "word", "test"],
        "lastDate": {"$date": {"$numberLong": "1734318000000"}}
    }
    response = client.post("/addDayWord", json=word)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Word added successfully"

def test_delete_day_word(mock_db):
    word_id = "677f1aef8adee120d7892fd7"
    response = client.delete(f"/deleteDayWord/{word_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Word deleted successfully"}

def test_delete_day_word_not_found(mock_db):
    word_id = "nonexistent_id"
    response = client.delete(f"/deleteDayWord/{word_id}")
    assert response.status_code == 404
    assert response.json() == {"message": "Word not found"}

def test_update_day_word(mock_db):
    word_id = "677f1aef8adee120d7892fd7"
    updated_data = {
        "word": "UpdatedWord",
        "images": [
            "https://updatedimage1.com", "https://updatedimage2.com", "https://updatedimage3.com", 
            "https://updatedimage4.com", "https://updatedimage5.com"
        ],
        "closeWords": ["updated", "word", "example"],
        "lastDate": {"$date": {"$numberLong": "1734318000000"}}
    }
    response = client.put(f"/updateDayWord/{word_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Word updated successfully"}

def test_update_day_word_not_found(mock_db):
    word_id = "nonexistent_id"
    updated_data = {
        "word": "UpdatedWord",
        "images": [
            "https://updatedimage1.com", "https://updatedimage2.com", "https://updatedimage3.com", 
            "https://updatedimage4.com", "https://updatedimage5.com"
        ],
        "closeWords": ["updated", "word", "example"],
        "lastDate": {"$date": {"$numberLong": "1734318000000"}}
    }
    response = client.put(f"/updateDayWord/{word_id}", json=updated_data)
    assert response.status_code == 404
    assert response.json() == {"message": "Word not found"}
