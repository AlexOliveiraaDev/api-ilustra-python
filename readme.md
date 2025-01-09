# Ilustra API

![Ilustra](https://img.shields.io/badge/Ilustra-7A4B2D?style=flat-square&logo=visualstudiocode)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb)
![Pytest](https://img.shields.io/badge/Pytest-0A9B8B?style=flat-square&logo=pytest)


🚀 **Ilustra API for managing the word of the day** using `fastapi` and `pymongo`. The app provides endpoints for retrieving, adding, updating, and deleting words.

<img src="https://img.shields.io/badge/In%20Development-orange?style=for-the-badge" alt="In Development Badge">

## Features

- **GET `/getDayWord`**: Retrieve the current word of the day 📝
- **POST `/addDayWord`**: Add a new word of the day ➕
- **PUT `/updateDayWord/{word_id}`**: Update an existing word of the day 🔄
- **DELETE `/deleteDayWord/{word_id}`**: Delete a word of the day 🗑️

## Setup 🛠️

### Prerequisites

- Python 3.8+
- MongoDB (or a running instance of MongoDB Atlas)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/AlexOliveiraaDev/api-ilustra-python.git
   cd api-ilustra-python
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add the following line to the `.env` file:
     ```env
     API_URL=mongodb://your-mongo-url
     ```

4. Run the application:
   ```bash
   fastapi dev app.py
   ```

## API Endpoints 📚

### `GET /getDayWord`

Fetch the current word of the day.

**Response:**
```json
{
  "_id": "677f1aef8adee120d7892fd7",
  "word": "Teste",
  "images": [
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com"
  ],
  "closeWords": [
    "testes",
    "palavra",
    "outros"
  ],
  "lastDate": {
    "$date": {
      "$numberLong": "1734318000000"
    }
  }
}
```

### `POST /addDayWord`

Add a new word of the day. The request body should be in the following format:

**Request Body:**
```json
{
  "word": "NewWord",
  "images": [
    "https://newimage1.com",
    "https://newimage2.com",
    "https://newimage3.com",
    "https://newimage4.com",
    "https://newimage5.com"
  ],
  "closeWords": [
    "new",
    "word",
    "test"
  ],
  "lastDate": {
    "$date": {
      "$numberLong": "1734318000000"
    }
  }
}
```

**Response:**
```json
{
  "message": "Word added successfully",
  "id": "your-inserted-id"
}
```

### `PUT /updateDayWord/{word_id}`

Update an existing word of the day. Provide the word ID and updated data.

**Request Body:**
```json
{
  "word": "UpdatedWord",
  "images": [
    "https://updatedimage1.com",
    "https://updatedimage2.com",
    "https://updatedimage3.com",
    "https://updatedimage4.com",
    "https://updatedimage5.com"
  ],
  "closeWords": [
    "updated",
    "word",
    "example"
  ],
  "lastDate": {
    "$date": {
      "$numberLong": "1734318000000"
    }
  }
}
```

**Response:**
```json
{
  "message": "Word updated successfully"
}
```

### `DELETE /deleteDayWord/{word_id}`

Delete the word of the day by its ID.

**Response:**
```json
{
  "message": "Word deleted successfully"
}
```

Esse formato mantém o conteúdo organizado e pronto para ser compartilhado em Markdown.

## Testing 🧪

### Running Tests

To run the tests, use `pytest`:
```bash
pytest
```

The tests are defined in `tests.py` and test the following functionalities:

- Fetching the day word.
- Adding a new day word.
- Updating an existing day word.
- Deleting a day word.

### Example Test for GET `/getDayWord`
```python
def test_get_day_word(mock_db):
    response = client.get("/getDayWord")
    assert response.status_code == 200
    data = response.json()
    assert "word" in data
    assert "images" in data
    assert "closeWords" in data
    assert "lastDate" in data
```

## Acknowledgments 🙏

- **FastAPI**: Web framework used for building the API.
- **PyMongo**: MongoDB driver for Python.
- **pytest**: Framework used for testing.

<p align="center">
    Made with ❤️ by <a href="https://github.com/AlexOliveiraaDev/">Alex Oliveira</a>
</p>
