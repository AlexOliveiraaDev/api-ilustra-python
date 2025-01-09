import os
import json
from bson import json_util
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import AsyncMongoClient
from dotenv import load_dotenv


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


class Item(BaseModel):
    name:str
    age:int
    have_car : Union[bool,None] = None


@app.get("/getDayWord")
async def get_day_word():
    try:
        word = await db.dayWord.find_one()
        if not word:
            raise HTTPException(status_code=404, detail="Word of the day not found")
        return serialize(word)
    except Exception as e:
        return {"message": str(e)}

@app.post("/addDayWord")
async def add_day_word(word: dict):
    try:
        result = await db.dayWord.insert_one(word)
        return {"message": "Word added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        return {"message": str(e)}

@app.delete("/deleteDayWord/{word_id}")
async def delete_day_word(word_id: str):
    try:
        result = await db.dayWord.delete_one({"_id": word_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Word not found")
        return {"message": "Word deleted successfully"}
    except Exception as e:
        return {"message": str(e)}

@app.put("/updateDayWord/{word_id}")
async def update_day_word(word_id: str, updated_data: dict):
    
    try:
        result = await db.dayWord.update_one({"_id": word_id}, {"$set": updated_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Word not found")
        return {"message": "Word updated successfully"}
    except Exception as e:
        return {"message": str(e)}

def serialize(mongoObject):
    return json.loads(json_util.dumps(mongoObject))
