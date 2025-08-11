from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

import os

load_dotenv()

class Settings(BaseModel):
    swagger: dict = {"defaultModelsExpandDepth": -1}

    image_formats: List[str] = ['png', 'jpg', 'jpeg']
    day_seconds: int = 86400
    year_seconds: int = 31536000
    
    version:               int = os.getenv("VERSION")
    # bot
    token:                 str = os.getenv("TOKEN")
    # s3
    endpoint_url:          str = os.getenv("S3_ENDPOINT_URL")
    aws_access_key_id:     str = os.getenv("S3_ACCESS_KEY")
    aws_secret_access_key: str = os.getenv("S3_SECRET_KEY")
    bucket:                str = os.getenv("S3_BUCKET")
    # twilio
    account_sid:           str = os.getenv("ACCOUNT_SID")
    auth_token:            str = os.getenv("AUTH_TOKEN")

settings = Settings()
