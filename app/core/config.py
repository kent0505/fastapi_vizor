from dotenv import load_dotenv
from pydantic import BaseModel

import os

load_dotenv()

class Settings(BaseModel):
    swagger: dict = {"defaultModelsExpandDepth": -1}

    image_formats: list[str] = ['png', 'jpg', 'jpeg']
    day_seconds: int = 86400
    year_seconds: int = 31536000

    # jwt
    version: int = 1
    key: str = os.getenv("KEY")
    admin: str = os.getenv("ADMIN")
    # s3
    s3_endpoint_url: str = "https://s3.twcstorage.ru"
    s3_region_name: str = "ru-1"
    s3_access_key: str = os.getenv("S3_ACCESS_KEY")
    s3_secret_key: str = os.getenv("S3_SECRET_KEY")
    s3_bucket: str = os.getenv("S3_BUCKET")
    # db
    db_url: str = os.getenv("POSTGRES_URL")
    # twilio
    account_sid: str = os.getenv("ACCOUNT_SID")
    auth_token: str = os.getenv("AUTH_TOKEN")
    # broker
    rabbit_url: str = os.getenv("RABBIT_URL")

settings = Settings()
