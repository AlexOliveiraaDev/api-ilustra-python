import os
import json
from bson import json_util
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.id import ID
from appwrite.input_file import InputFile


storageClient = Client()
storageClient.set_endpoint('https://cloud.appwrite.io/v1')
storageClient.set_project(os.getenv("APPWRITE_PROJECT"))
storageClient.set_key(os.getenv("APPWRITE_KEY"))

storage = Storage(storageClient)

async def upload_images(images):
    try:
        save_images(images)
        for image in images:
            temp_path = f"temp/{image}"
            result = await storage.create_file(
                bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
                file_id=ID.unique(),
                file=InputFile.from_path(temp_path)
            )
            return result
    except Exception as e:
        return {"message": str(e)}
    
async def save_images(images):
    try:
        for image in images:
            temp_path = f"temp/{image}"
            with open(temp_path, "wb") as f:
                f.write(image)
    except Exception as e:
        return {"message": str(e)}

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:4200",
    "https://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_url = os.getenv("DB_KEY_URL")
client = AsyncMongoClient(api_url)
db = client["ilustra-db"]


class Word(BaseModel):
    word:str
    images:list[str]
    closeWords:list[str]
    lastDate:dict

@app.get("/")
async def root():
    return {"message": "Yes, the api is working!"}

@app.get("/getDayWord")
async def get_day_word():
    try:
        word = await db.dayWord.find_one()
        if not word:
            raise HTTPException(status_code=404, detail="Word of the day not found")
        return serialize(word)
    except Exception as e:
        return {"message": str(e)}

@app.post("/setDayWord/{word}")
async def set_day_word(word: str):
    try:
        await db.dayWord.delete_many({})
        result = await db.words.find_one({"word": word})
        if not result:
            raise HTTPException(status_code=404, detail="Word not found")
        await db.dayWord.insert_one(result)
        return {"message": "Word: " + word + " set as word of the day"}

    except Exception as e:
        return {"message": str(e)}


@app.post("/addWord")
async def add_day_word(word: Word):
    try:
        # Extrai as imagens do objeto `Word`
        images = word.images if hasattr(word, 'images') else []
        if not isinstance(images, list):
            return {"message": "Invalid images format. Must be a list."}

        # Converte o objeto `Word` para um dicionário usando `model_dump`
        word_dict = word.model_dump()

        # Faz o upload das imagens
        try:
            uploaded_images = await upload_images(images)
        except Exception as e:
            return {"message": f"Error uploading images: {str(e)}"}

        # Insere o documento no banco de dados
        try:
            result = await db.words.insert_one(word_dict)
        except Exception as e:
            return {"message": f"Error inserting word into database: {str(e)}"}

        # Retorna o resultado com o ID do documento inserido
        return {
            "message": "Word added successfully",
            "id": str(result.inserted_id),
            "uploaded_images": uploaded_images,
        }
    except Exception as e:
        # Captura erros gerais na função
        return {"message": f"Unexpected error: {str(e)}"}

@app.delete("/deleteWord/{word}")
async def delete_word(word: str):
    try:
        result = await db.words.delete_one({"word": word})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Word not found")
        return {"message": "Word deleted successfully"}
    except Exception as e:
        return {"message": str(e)}
    
@app.get("/testStorage")
async def test_storage():
    return storage.get_bucket(os.getenv("APPWRITE_BUCKET_ID"))

def serialize(mongoObject):
    return json.loads(json_util.dumps(mongoObject))