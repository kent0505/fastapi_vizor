from fastapi import UploadFile, HTTPException
from mypy_boto3_s3 import S3Client
from core.config import settings
from core.utils import get_timestamp

import boto3
import logging

class S3Service:
    def __init__(self):
        self.s3: S3Client = boto3.client(
            "s3",
            endpoint_url=settings.s3.endpoint_url,
            aws_access_key_id=settings.s3.access_key,
            aws_secret_access_key=settings.s3.secret_key,
            region_name=settings.s3.region_name,
        )
        self.bucket = settings.s3.bucket
        self.allowed_formats = ['png', 'jpg', 'jpeg']

    async def put_object(
        self, 
        id: int,
        folder: str,
        file: UploadFile,
    ) -> str | None:
        try:
            ext = file.filename.split(".")[-1].lower()
            if ext not in self.allowed_formats:
                raise HTTPException(400, "unsupported file format")

            key = f"{folder}/{id}_{get_timestamp()}.{ext}"

            body = await file.read()

            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=body,
                ContentType=file.content_type,
            )
            return key
        except Exception as e:
            logging.error(e)
            return None

    async def delete_object(
        self, 
        key: str,
    ):
        try:
            self.s3.delete_object(
                Bucket=self.bucket,
                Key=key,
            )
        except Exception as e:
            logging.error(e)

s3_service = S3Service()
