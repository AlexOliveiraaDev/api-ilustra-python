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

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Here =>", self.path)
        if self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, world!').encode('utf-8')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found').encode('utf-8')

def main(args):
    print("Success!")
    
storageClient = Client()
storageClient.set_endpoint('https://cloud.appwrite.io/v1')
storageClient.set_project(os.getenv("APPWRITE_PROJECT"))
storageClient.set_key(os.getenv("APPWRITE_KEY"))

storage = Storage(storageClient)

async def upload_images(image_urls: list[str]):
    try:
        for image_url in image_urls:
            result = await storage.create_file(
                bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
                file_id=ID.unique(),
                file=InputFile.from_path(image_url)
            )
            return result
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
        images = word.images
        print(images)
        word = word.model_dump()
        await upload_images(images)
        result = await db.words.insert_one(word)
        return {"message": "Word added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        return {"message": str(e)}

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