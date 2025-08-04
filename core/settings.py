from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import os

load_dotenv()

class Settings(BaseModel):
    swagger: dict = {"defaultModelsExpandDepth": -1}
    password: str = os.getenv("PASSWORD", "123")
    token: str = os.getenv("TOKEN")
    endpoint_url: str = os.getenv("S3_ENDPOINT_URL")
    aws_access_key_id: str = os.getenv("S3_ACCESS_KEY")
    aws_secret_access_key: str = os.getenv("S3_SECRET_KEY")
    bucket: str = os.getenv("S3_BUCKET")
    image_formats: List[str] = ['png', 'jpg', 'jpeg']
    day_seconds: int = 86400
    year_seconds: int = 31536000

settings = Settings()
