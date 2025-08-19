from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from config import settings

class User(BaseModel):
    id: int
    phone: str

client = AsyncIOMotorClient(settings.mongo_url)
db = client[settings.mongo_db]

users = db["users"]
