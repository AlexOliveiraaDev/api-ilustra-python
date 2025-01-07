import os
import json
from bson import json_util
from typing import Union
from fastapi import FastAPI
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

api_url = os.getenv("API_URL")
client = AsyncMongoClient("mongodb+srv://ilustraUserDB:Acc00102030@ilustra-db.nvueg.mongodb.net/?retryWrites=true&w=majority&appName=ilustra-db")

db = client["ilustra-db"]


class Item(BaseModel):
    name:str
    age:int
    have_car : Union[bool,None] = None


@app.get("/getDayWord")
async def get_day_word():
    try:
       return serialize(await db.dayWord.find())
    except Exception as e:
        return {"message": str(e)}

def serialize(mongoObject):
    return json.loads(json_util.dumps(mongoObject))
