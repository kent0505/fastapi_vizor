from pydantic import BaseModel
from typing import List
from mypy_boto3_s3 import S3Client

import boto3
import os

class Settings(BaseModel):
    swagger: dict = {"defaultModelsExpandDepth": -1}
    password: str = os.getenv("PASSWORD")
    token: str = os.getenv("TOKEN")
    jwt_key: str = os.getenv("KEY", "xyz")
    endpoint_url: str = os.getenv("S3_ENDPOINT_URL")
    aws_access_key_id: str = os.getenv("S3_ACCESS_KEY")
    aws_secret_access_key: str = os.getenv("S3_SECRET_KEY")
    bucket: str = os.getenv("S3_BUCKET")
    image_formats: List[str] = ['png', 'jpg', 'jpeg']
    day_seconds: int = 86400
    year_seconds: int = 31536000

settings = Settings()

s3: S3Client = boto3.client(
    "s3",
    endpoint_url=settings.endpoint_url,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name="ru-1",
)
